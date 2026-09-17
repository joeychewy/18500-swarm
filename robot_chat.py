#!/usr/bin/env python3
"""Two-way ROS 2 text chat. Run once for each robot, swapping the names."""

import argparse
import select
import sys

import rclpy
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="This robot's name, e.g. robot1")
    parser.add_argument("peer", help="The other robot's name, e.g. robot2")
    args = parser.parse_args()

    rclpy.init(args=[])
    node = rclpy.create_node(f"{args.name}_chat")

    # Publish on our topic; listen on the other robot's topic.
    publisher = node.create_publisher(String, f"/{args.name}/chat", 10)
    node.create_subscription(
        String,
        f"/{args.peer}/chat",
        lambda message: print(f"{args.peer}: {message.data}", flush=True),
        10,
    )

    print(f"{args.name} ready. Start {args.peer}, then type a message and press Enter.")
    print("Press Ctrl+C to quit.")

    try:
        while rclpy.ok():
            # Receive messages while checking the terminal for new input.
            rclpy.spin_once(node, timeout_sec=0.05)
            if select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if not line:  # Terminal input closed.
                    break
                if line.strip():
                    publisher.publish(String(data=line.rstrip("\r\n")))
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
