import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist 
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle
from functools import partial

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.declare_parameter("catch_closest_turtle_first", True)
        self.pose_ = None
        self.turtle_to_catch_ = None
        self.catch_closest_turtle_first_ = self.get_parameter("catch_closest_turtle_first").value
        
        self.cmd_vel_publisher = self.create_publisher(
            Twist, "/turtle1/cmd_vel", 10)
        
        self.pose_subscriber = self.create_subscription(
            Pose, "/turtle1/pose", self.callback_pose, 10)
        
        self.alive_turtles_subscriber_ = self.create_subscription(
            TurtleArray, "alive_turtles", self.callback_alive_turtles, 10)
        
        self.control_loop_timer = self.create_timer(0.01, self.control_loop)
        
        self.catch_turtle_client_ = self.create_client(CatchTurtle, "catch_turtle")

    def callback_pose(self, pose: Pose):
        self.pose_ = pose
        self.get_logger().info(f"Received pose: x={pose.x}, y={pose.y}, theta={pose.theta}")
        
    def control_loop(self):
        if self.pose_ == None or self.turtle_to_catch_ == None:
            return
        
        dist_x = self.turtle_to_catch_.x - self.pose_.x
        dist_y = self.turtle_to_catch_.y - self.pose_.y
        distance = math.sqrt(dist_x**2 + dist_y**2)
        cmd = Twist()
        
        if distance > 0.5:
            # move towards the target
            cmd.linear.x = distance
            diff_angle = math.atan2(dist_y, dist_x) - self.pose_.theta
            
            if diff_angle > math.pi:
                diff_angle -= 2 * math.pi
            elif diff_angle < -math.pi:
                diff_angle += 2 * math.pi   
            
            cmd.angular.z = diff_angle
        else:
            # reached the target, stop the turtle
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            # next target
            self.call_catch_turtle_service(self.turtle_to_catch_.name)
            self.turtle_to_catch_ = None
            
        
        self.cmd_vel_publisher.publish(cmd)
        
    def callback_alive_turtles(self, turtle_list: TurtleArray):
        if(len(turtle_list.turtles) > 0):
            if(self.catch_closest_turtle_first_):
                closest_turtle = None
                closest_distance = None
                for turtle in turtle_list.turtles:
                    dist_x = turtle.x - self.pose_.x
                    dist_y = turtle.y - self.pose_.y
                    distance = math.sqrt(dist_x**2 + dist_y**2)
                    if closest_distance == None or distance < closest_distance:
                        closest_distance = distance
                        closest_turtle = turtle
                self.turtle_to_catch_ = closest_turtle
            else:
                self.turtle_to_catch_ = turtle_list.turtles[0]
            
    def call_catch_turtle_service(self, turtle_name):
        while not self.catch_turtle_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for catch_turtle service...")
            
        request = CatchTurtle.Request()   
        request.name = turtle_name
        future = self.catch_turtle_client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_catch_turtle_service, turtle_name=turtle_name))
        
    def callback_call_catch_turtle_service(self, future, turtle_name):
        response = future.result()
        if response.success:
            self.get_logger().info(f"Successfully caught the turtle: {turtle_name}")
        else:
            self.get_logger().info(f"Failed to catch the turtle: {turtle_name}")
    
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()