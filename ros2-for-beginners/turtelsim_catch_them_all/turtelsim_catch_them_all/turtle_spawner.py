#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from functools import partial
import random
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle

class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.declare_parameter("turtle_name_prefix", "turtle")
        self.turtle_name_prefix_ = self.get_parameter("turtle_name_prefix").value
        self.declare_parameter("spawn_frequency", 2.0)
        self.spawn_frequency_ = self.get_parameter("spawn_frequency").value
        self.counter = 1
        self.alive_turtles_ = []
        self.alive_turtles_publisher_ = self.create_publisher(TurtleArray, "alive_turtles", 10)
        self.spawn_client_ = self.create_client(Spawn, "/spawn")
        self.kill_client_ = self.create_client(Kill, "/kill")
        self.spawn_turtle_timer = self.create_timer(1.0 / self.spawn_frequency_, self.callback_spawn_turtle_timer)
        self.catch_turtle_service_ = self.create_service(CatchTurtle, "catch_turtle", self.callback_catch_turtle)
        
    def callback_catch_turtle(self, request: CatchTurtle.Request, response: CatchTurtle.Response):
        self.call_kill_service(request.name)
        response.success = True
        return response
    
    def publish_alive_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles_
        self.alive_turtles_publisher_.publish(msg)
        
    def call_spawn_service(self, turtle_name, x, y, theta):
        while not self.spawn_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for spawn service...")
            
        request = Spawn.Request()   
        request.name = turtle_name
        request.x = x               
        request.y = y
        request.theta = theta
        future = self.spawn_client_.call_async(request)
        future.add_done_callback(partial(self.calback_call_spawn_service, request=request))
        
    def calback_call_spawn_service(self, future, request):
        response = future.result()
        if response.name != "":
            self.get_logger().info(f"Spawned turtle: {response.name}")
            new_turtle = Turtle()
            new_turtle.name = response.name
            new_turtle.x = request.x
            new_turtle.y = request.y
            new_turtle.theta = request.theta
            self.alive_turtles_.append(new_turtle)
            self.publish_alive_turtles()
            
    def callback_spawn_turtle_timer(self):
        self.counter += 1
        name = self.turtle_name_prefix_ + str(self.counter)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2 * 3.14)
        self.call_spawn_service(name, x, y, theta )
        
    def call_kill_service(self, turtle_name):
        while not self.kill_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for kill service...")
            
        request = Kill.Request()   
        request.name = turtle_name
        future = self.kill_client_.call_async(request)
        future.add_done_callback(partial(self.calback_call_kill_service, request=request))
        
    def calback_call_kill_service(self, future, request):
        for (i, turtle) in enumerate(self.alive_turtles_):
            self.get_logger().info(f"Request: {request.name}")
            if turtle.name == request.name:
                del self.alive_turtles_[i]
                self.publish_alive_turtles()
                break
    
def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()