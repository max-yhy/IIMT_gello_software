"""Joint-space command smoothing for hardware teleoperation.

The smoothers in this module operate on six joint positions in radians.  They
are deliberately stateful: the first command should be seeded with the
robot's actual joint state, then each subsequent Gello target is filtered
before it is sent to ``API_Servoj``.

The modes are intentionally mutually exclusive:

* ``raw``: send the converted Gello target unchanged;
* ``linear``: move from the previous command to a new target over a fixed
  duration;
* ``second_order``: critically damped position tracking with velocity and
  acceleration limits;
* ``ruckig``: jerk-limited online trajectory generation.  If the optional
  package is unavailable, it falls back to the second-order smoother.
"""

from __future__ import annotations

import time
from typing import Iterable

import numpy as np


SMOOTH_MODES = ("raw", "linear", "second_order", "ruckig")

try:  # Ruckig is optional so read-only monitoring still works without it.
    from ruckig import InputParameter, OutputParameter, Result, Ruckig

    RUCKIG_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised on machines before install
    InputParameter = OutputParameter = Result = Ruckig = None
    RUCKIG_AVAILABLE = False


def normalize_smooth_mode(mode: str | None) -> str:
    """Return a supported mode, defaulting safely to ``raw``."""

    value = str(mode or "raw").strip().lower()
    aliases = {
        "none": "raw",
        "direct": "raw",
        "linear_time": "linear",
        "time": "linear",
        "second-order": "second_order",
        "secondorder": "second_order",
    }
    value = aliases.get(value, value)
    if value not in SMOOTH_MODES:
        raise ValueError(
            f"smooth_mode must be one of {SMOOTH_MODES}, got {mode!r}"
        )
    return value


def _joint_vector(values: Iterable[float], name: str = "joint state") -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.shape != (6,):
        raise ValueError(f"{name} must contain 6 values, got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} contains NaN or infinity")
    return array


class JointLinearSmoother:
    """Piecewise linear interpolation in joint position space."""

    def __init__(self, duration: float = 0.02) -> None:
        self.duration = max(float(duration), 1e-4)
        self.command: np.ndarray | None = None
        self._start: np.ndarray | None = None
        self._target: np.ndarray | None = None
        self._start_time = 0.0

    def reset(self, current: Iterable[float]) -> None:
        current = _joint_vector(current, "current joint state")
        self.command = current.copy()
        self._start = current.copy()
        self._target = current.copy()
        self._start_time = time.monotonic()

    def update(
        self,
        target: Iterable[float],
        now: float | None = None,
        duration: float | None = None,
    ) -> np.ndarray:
        target = _joint_vector(target, "joint target")
        if self.command is None:
            self.reset(target)

        now = time.monotonic() if now is None else float(now)
        duration = self.duration if duration is None else max(float(duration), 1e-4)
        if self._target is None or not np.array_equal(target, self._target):
            self._start = self.command.copy()
            self._target = target.copy()
            self._start_time = now
            self.duration = duration

        assert self._start is not None
        assert self._target is not None
        alpha = np.clip((now - self._start_time) / self.duration, 0.0, 1.0)
        self.command = self._start + (self._target - self._start) * alpha
        return self.command.copy()


class JointSecondOrderSmoother:
    """Second-order damped position tracker with velocity/acceleration limits."""

    def __init__(
        self,
        omega: float = 18.0,
        zeta: float = 1.0,
        max_vel: float = 2.5,
        max_acc: float = 30.0,
    ) -> None:
        self.omega = max(float(omega), 1e-4)
        self.zeta = max(float(zeta), 0.0)
        self.max_vel = max(float(max_vel), 1e-4)
        self.max_acc = max(float(max_acc), 1e-4)
        self.command: np.ndarray | None = None
        self.velocity = np.zeros(6, dtype=np.float64)
        self._last_time: float | None = None

    def reset(self, current: Iterable[float]) -> None:
        self.command = _joint_vector(current, "current joint state").copy()
        self.velocity.fill(0.0)
        self._last_time = time.monotonic()

    def update(
        self,
        target: Iterable[float],
        now: float | None = None,
        dt: float = 0.004,
    ) -> np.ndarray:
        target = _joint_vector(target, "joint target")
        if self.command is None:
            self.reset(target)

        now = time.monotonic() if now is None else float(now)
        if self._last_time is None:
            actual_dt = float(dt)
        else:
            actual_dt = now - self._last_time
        self._last_time = now
        actual_dt = max(1e-4, min(0.05, actual_dt))

        assert self.command is not None
        acceleration = self.omega**2 * (target - self.command)
        acceleration -= 2.0 * self.zeta * self.omega * self.velocity
        acceleration = np.clip(acceleration, -self.max_acc, self.max_acc)
        self.velocity = np.clip(
            self.velocity + acceleration * actual_dt,
            -self.max_vel,
            self.max_vel,
        )
        self.command = self.command + self.velocity * actual_dt
        return self.command.copy()


class JointRuckigSmoother:
    """Jerk-limited online joint trajectory generator."""

    def __init__(
        self,
        dt: float = 0.004,
        max_vel: float = 2.5,
        max_acc: float = 30.0,
        max_jerk: float = 200.0,
        fallback: JointSecondOrderSmoother | None = None,
    ) -> None:
        self.dt = max(float(dt), 1e-4)
        self.max_vel = max(float(max_vel), 1e-4)
        self.max_acc = max(float(max_acc), 1e-4)
        self.max_jerk = max(float(max_jerk), 1e-4)
        self.fallback = fallback or JointSecondOrderSmoother(
            max_vel=self.max_vel,
            max_acc=self.max_acc,
        )
        self.command: np.ndarray | None = None
        self._otg = None
        self._input = None
        self._output = None
        if RUCKIG_AVAILABLE:
            self._otg = Ruckig(6, self.dt)
            self._input = InputParameter(6)
            self._output = OutputParameter(6)

    @property
    def available(self) -> bool:
        return RUCKIG_AVAILABLE

    def reset(self, current: Iterable[float]) -> None:
        current = _joint_vector(current, "current joint state")
        self.command = current.copy()
        self.fallback.reset(current)
        if not self.available:
            return

        assert self._input is not None
        self._input.current_position = current.tolist()
        self._input.current_velocity = [0.0] * 6
        self._input.current_acceleration = [0.0] * 6
        self._input.target_position = current.tolist()
        self._input.target_velocity = [0.0] * 6
        self._input.target_acceleration = [0.0] * 6
        self._input.max_velocity = [self.max_vel] * 6
        self._input.max_acceleration = [self.max_acc] * 6
        self._input.max_jerk = [self.max_jerk] * 6

    def _fallback_update(
        self, target: np.ndarray, now: float | None, dt: float
    ) -> np.ndarray:
        if self.command is None:
            self.reset(target)
        command = self.fallback.update(target, now=now, dt=dt)
        self.command = command.copy()
        return command

    def update(
        self,
        target: Iterable[float],
        now: float | None = None,
        dt: float | None = None,
    ) -> np.ndarray:
        target = _joint_vector(target, "joint target")
        actual_dt = self.dt if dt is None else max(float(dt), 1e-4)
        if not self.available:
            return self._fallback_update(target, now, actual_dt)

        if self.command is None:
            self.reset(target)
        assert self._otg is not None
        assert self._input is not None
        assert self._output is not None

        self._input.target_position = target.tolist()
        self._input.target_velocity = [0.0] * 6
        self._input.target_acceleration = [0.0] * 6
        result = self._otg.update(self._input, self._output)
        if result in (Result.Working, Result.Finished):
            self.command = np.asarray(
                self._output.new_position, dtype=np.float64
            )
            self._output.pass_to_input(self._input)
            return self.command.copy()

        # A transient invalid trajectory should not disable teleoperation.
        # Continue with the bounded second-order controller instead.
        return self._fallback_update(target, now, actual_dt)


class JointCommandSmoother:
    """Select and run one of the joint smoothers above."""

    def __init__(
        self,
        mode: str = "raw",
        dt: float = 0.004,
        interpolation_duration: float = 0.02,
        second_order_omega: float = 18.0,
        second_order_zeta: float = 1.0,
        joint_max_vel: float = 2.5,
        joint_max_acc: float = 30.0,
        joint_max_jerk: float = 200.0,
    ) -> None:
        self.mode = normalize_smooth_mode(mode)
        self.dt = max(float(dt), 1e-4)
        self.linear = JointLinearSmoother(interpolation_duration)
        self.second_order = JointSecondOrderSmoother(
            omega=second_order_omega,
            zeta=second_order_zeta,
            max_vel=joint_max_vel,
            max_acc=joint_max_acc,
        )
        self.ruckig = JointRuckigSmoother(
            dt=self.dt,
            max_vel=joint_max_vel,
            max_acc=joint_max_acc,
            max_jerk=joint_max_jerk,
            fallback=self.second_order,
        )
        self.command: np.ndarray | None = None

    @property
    def ruckig_available(self) -> bool:
        return self.ruckig.available

    def reset(self, current: Iterable[float]) -> None:
        current = _joint_vector(current, "current joint state")
        self.command = current.copy()
        self.linear.reset(current)
        self.second_order.reset(current)
        self.ruckig.reset(current)

    def set_mode(self, mode: str, current: Iterable[float] | None = None) -> None:
        self.mode = normalize_smooth_mode(mode)
        if current is not None:
            self.reset(current)

    def update(
        self,
        target: Iterable[float],
        now: float | None = None,
    ) -> np.ndarray:
        target = _joint_vector(target, "joint target")
        if self.mode == "raw":
            self.command = target.copy()
        elif self.mode == "linear":
            self.command = self.linear.update(target, now=now)
        elif self.mode == "second_order":
            self.command = self.second_order.update(
                target, now=now, dt=self.dt
            )
        elif self.mode == "ruckig":
            self.command = self.ruckig.update(target, now=now, dt=self.dt)
        else:  # normalize_smooth_mode prevents this branch.
            raise RuntimeError(f"Unsupported smoothing mode: {self.mode}")
        return self.command.copy()
