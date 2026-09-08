#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from interfaces.action import CountUntil

class CountUntilServer(Node): 
    def __init__(self):
        super().__init__("count_until_server") 

def main(args=None):
    rclpy.init(args=args)
    node = CountUntilServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()