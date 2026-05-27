import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist 

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.target_x_ = 8.0
        self.target_y_ = 4.0
        self.pose_ = None
        
        self.cmd_vel_publisher = self.create_publisher(
            Twist, "/turtle1/cmd_vel", 10)
        
        self.pose_subscriber = self.create_subscription(
            Pose, "/turtle1/pose", self.callback_pose, 10)
        
        self.control_loop_timer = self.create_timer(0.01, self.control_loop)

    def callback_pose(self, pose: Pose):
        self.pose_ = pose
        self.get_logger().info(f"Received pose: x={pose.x}, y={pose.y}, theta={pose.theta}")
        
    def control_loop(self):
        if self.pose_ == None:
            return
        
        dist_x = self.target_x_ - self.pose_.x
        dist_y = self.target_y_ - self.pose_.y
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
        
        self.cmd_vel_publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()