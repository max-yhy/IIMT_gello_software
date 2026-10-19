"""Read raw joint positions from a GELLO Dynamixel bus.

This utility only reads the present-position registers. It does not enable
torque or send goal positions. The output is in raw Dynamixel coordinates,
converted to radians; GELLO assembly offsets and joint signs are not applied.
"""

import argparse
import math
import time
from typing import Sequence

from dynamixel_sdk import COMM_SUCCESS, GroupSyncRead, PacketHandler, PortHandler


PRESENT_POSITION_ADDRESS = 132
PRESENT_POSITION_LENGTH = 4
DEFAULT_BAUDRATE = 57600
DEFAULT_IDS = tuple(range(1, 8))


def read_raw_positions(
    port: PortHandler,
    packet: PacketHandler,
    reader: GroupSyncRead,
    ids: Sequence[int],
) -> list[float]:
    result = reader.txRxPacket()
    if result != COMM_SUCCESS:
        raise RuntimeError(f"Dynamixel read failed: {result}")

    positions = []
    for motor_id in ids:
        if not reader.isAvailable(
            motor_id, PRESENT_POSITION_ADDRESS, PRESENT_POSITION_LENGTH
        ):
            raise RuntimeError(f"Position unavailable for Dynamixel ID {motor_id}")

        ticks = reader.getData(
            motor_id, PRESENT_POSITION_ADDRESS, PRESENT_POSITION_LENGTH
        )
        if ticks > 0x7FFFFFFF:
            ticks -= 0x100000000
        positions.append(ticks / 2048.0 * math.pi)

    return positions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="/dev/ttyUSB0")
    parser.add_argument("--baudrate", type=int, default=DEFAULT_BAUDRATE)
    parser.add_argument("--interval", type=float, default=0.05)
    parser.add_argument(
        "--ids",
        type=int,
        nargs="+",
        default=list(DEFAULT_IDS),
        help="Dynamixel IDs to read, default: 1 2 3 4 5 6 7",
    )
    parser.add_argument(
        "--once", action="store_true", help="Read one sample and exit"
    )
    args = parser.parse_args()

    port = PortHandler(args.port)
    packet = PacketHandler(2.0)
    reader = GroupSyncRead(
        port,
        packet,
        PRESENT_POSITION_ADDRESS,
        PRESENT_POSITION_LENGTH,
    )

    if not port.openPort():
        raise RuntimeError(f"Could not open serial port: {args.port}")
    if not port.setBaudRate(args.baudrate):
        port.closePort()
        raise RuntimeError(f"Could not set baudrate: {args.baudrate}")

    try:
        for motor_id in args.ids:
            if not reader.addParam(motor_id):
                raise RuntimeError(f"Could not add Dynamixel ID {motor_id}")

        while True:
            positions = read_raw_positions(port, packet, reader, args.ids)
            timestamp = time.strftime("%H:%M:%S")
            values = ", ".join(
                f"id{motor_id}={position:.6f}"
                for motor_id, position in zip(args.ids, positions)
            )
            print(f"[{timestamp}] {values}", flush=True)

            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        reader.clearParam()
        port.closePort()


if __name__ == "__main__":
    main()
