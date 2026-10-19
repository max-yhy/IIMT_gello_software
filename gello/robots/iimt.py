"""IIMT robot adapter.

The IIMT Python SDK exposes a six-joint, radians-based API over TCP. This
adapter translates the GELLO ``Robot`` protocol to that API.

This module deliberately does not power on the robot, release the brakes, or
change the operating mode. ``command_joint_state`` does send ``API_Servoj``
commands, so it should only be used after the robot and safety state have been
checked by the operator.
"""

from pathlib import Path
import sys
import time
from typing import Dict

import numpy as np

from gello.robots.robot import Robot


_NUM_DOFS = 6


def _load_iimt_sdk(robot_ip: str, robot_port: int):
    """Load the bundled IIMT SDK and configure its connection target."""

    repo_root = Path(__file__).resolve().parents[2]
    sdk_demo_dir = repo_root / "third_party" / "IIMT-SDK" / "python" / "sdk_demo_py"
    sdk_library = (
        repo_root
        / "third_party"
        / "IIMT-SDK"
        / "python"
        / "linux"
        / "x64"
        / "lib"
        / "libiimtcl.so"
    )

    if not sdk_demo_dir.is_dir():
        raise FileNotFoundError(f"IIMT SDK Python directory not found: {sdk_demo_dir}")
    if not sdk_library.is_file():
        raise FileNotFoundError(f"IIMT SDK library not found: {sdk_library}")

    sdk_demo_path = str(sdk_demo_dir)
    if sdk_demo_path not in sys.path:
        sys.path.insert(0, sdk_demo_path)

    # Import this module first so its global connection settings are changed
    # before iimt_api loads libiimtcl.so and calls API_Login().
    import iimt_common

    iimt_common.common.address = robot_ip.encode("ascii")
    iimt_common.common.port = int(robot_port)
    iimt_common.common.path = str(sdk_library)

    import iimt_api

    return iimt_api


class IIMTRobot(Robot):
    """Six-axis IIMT robot controlled through the bundled Python SDK."""

    def __init__(
        self,
        robot_ip: str = "192.168.8.87",
        robot_port: int = 29999,
        servoj_acceleration: float = 7.0,
        servoj_velocity: float = 5.0,
        servoj_period: float = 0.008,
        servoj_lookahead_time: float = 0.0,
        servoj_gain: float = 0.0,
        print_target: bool = False,
        print_target_interval: float = 0.5,
    ):
        self._api = _load_iimt_sdk(robot_ip, robot_port)
        self._handle = None
        self._servo_handle = None
        self._closed = False

        login_result, handle = self._api.API_Login()
        if not bool(login_result):
            raise ConnectionError(
                f"IIMT API_Login failed for {robot_ip}:{robot_port}. "
                "Check that RobotMain is running, the IP is reachable, and "
                "the controller accepts SDK connections."
            )
        self._handle = handle

        # The IIMT SDK documentation recommends a separate connection for
        # API_Servoj to reduce latency. Keep state reads and servo commands on
        # different handles, which is especially important at 250 Hz.
        servo_login_result, servo_handle = self._api.API_Login()
        if not bool(servo_login_result):
            self._api.API_Logout(self._handle)
            self._handle = None
            raise ConnectionError(
                f"IIMT servo connection failed for {robot_ip}:{robot_port}"
            )
        self._servo_handle = servo_handle

        self._servoj_acceleration = float(servoj_acceleration)
        self._servoj_velocity = float(servoj_velocity)
        self._servoj_period = float(servoj_period)
        self._servoj_lookahead_time = float(servoj_lookahead_time)
        self._servoj_gain = float(servoj_gain)
        self._print_target = bool(print_target)
        self._print_target_interval = float(print_target_interval)
        self._last_target_print_time = 0.0

    def num_dofs(self) -> int:
        return _NUM_DOFS

    def get_joint_state(self) -> np.ndarray:
        """Read the current six joint positions in radians."""

        if self._closed or self._handle is None:
            raise RuntimeError("IIMT robot connection is closed")

        result, joint_rad = self._api.API_GetRobotJointRad(self._handle)
        if not bool(result):
            raise RuntimeError("IIMT API_GetRobotJointRad failed")

        return np.asarray(
            [joint_rad.robotRad[index] for index in range(_NUM_DOFS)],
            dtype=np.float64,
        )

    def command_joint_state(self, joint_state: np.ndarray) -> None:
        """Send a six-joint position command in radians through API_Servoj."""

        if self._closed or self._servo_handle is None:
            raise RuntimeError("IIMT robot connection is closed")

        joint_state = np.asarray(joint_state, dtype=np.float64)
        if joint_state.shape != (_NUM_DOFS,):
            raise ValueError(
                f"IIMT expects {_NUM_DOFS} joint values, got shape {joint_state.shape}"
            )
        if not np.all(np.isfinite(joint_state)):
            raise ValueError("IIMT joint command contains NaN or infinity")

        now = time.monotonic()
        if (
            self._print_target
            and now - self._last_target_print_time >= self._print_target_interval
        ):
            self._last_target_print_time = now
            print(
                "[IIMT target rad] "
                + np.array2string(
                    joint_state, precision=6, suppress_small=False
                ),
                flush=True,
            )
            print(
                "[IIMT target deg] "
                + np.array2string(
                    np.rad2deg(joint_state),
                    precision=3,
                    suppress_small=False,
                ),
                flush=True,
            )

        servoj = self._api.ServojParam()
        for index, value in enumerate(joint_state):
            servoj.q[index] = float(value)
        servoj.a = self._servoj_acceleration
        servoj.v = self._servoj_velocity
        servoj.t = self._servoj_period
        servoj.lookahead_time = self._servoj_lookahead_time
        servoj.gain = self._servoj_gain

        result = self._api.API_Servoj(self._servo_handle, servoj)
        if not bool(result):
            print(
                "[IIMT] API_Servoj failed for target: "
                + np.array2string(joint_state, precision=6),
                flush=True,
            )
            raise RuntimeError("IIMT API_Servoj failed")

    def get_observations(self) -> Dict[str, np.ndarray]:
        """Return the observation fields required by ``RobotEnv``."""

        joints = self.get_joint_state()
        return {
            "joint_positions": joints,
            "joint_velocities": np.zeros_like(joints),
            "ee_pos_quat": np.zeros(7, dtype=np.float64),
            "gripper_position": np.array([0.0], dtype=np.float64),
        }

    def close(self) -> None:
        """Close the SDK session without changing robot power or mode."""

        if self._closed:
            return
        self._closed = True
        if self._servo_handle is not None:
            self._api.API_Logout(self._servo_handle)
            self._servo_handle = None
        if self._handle is not None:
            self._api.API_Logout(self._handle)
            self._handle = None

    def __enter__(self) -> "IIMTRobot":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
