#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from interfaces.action import RobotMovement


class RobotMovementClient(Node):
  def __init__(self):
    super().__init__("robot_movement_client")
    self.robot_movement_client_ = ActionClient(self, RobotMovement, "robot_movement")
        
  def send_goal(self, position, velocity):
    # Wait for the server
    self.robot_movement_client_.wait_for_server()
    
    # Create a goal
    goal = RobotMovement.Goal()
    goal.position = position
    goal.velocity = velocity
    
    #Send the goal
    self.get_logger().info("Sending goal")
    self.robot_movement_client_. \
      send_goal_async(goal, feedback_callback=self.goal_feedback_callback). \
        add_done_callback(self.goal_response_callback)
    
    # Send a cancel request 2 seconds later
    # self.timer_ = self.create_timer(1.0, self.cancel_goal)
    
  def cancel_goal(self):
    self.get_logger().info("Send a cancel request")
    self.goal_handle_.cancel_goal_async()
    self.timer_.cancel()

  def goal_feedback_callback(self, feedback_msg):
    number = feedback_msg.feedback.current_position
    self.get_logger().info("Get feedback: " + str(number))
    
  
  def goal_response_callback(self, future):
    self.goal_handle_: ClientGoalHandle = future.result()
    if self.goal_handle_.accepted: 
      self.get_logger().info("Goal got accepted")
      self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)
    else:
      self.get_logger().info("Goal got rejected")

  def goal_result_callback(self, future): 
    status = future.result().status
    result = future.result().result
    if status == GoalStatus.STATUS_SUCCEEDED:
      self.get_logger().info("Success")
    elif status == GoalStatus.STATUS_ABORTED:
      self.get_logger().error("Aborted")
    elif status == GoalStatus.STATUS_CANCELED:
      self.get_logger().warn("Canceld")
    self.get_logger().info("Result : " + str(result.position))
    self.get_logger().info("Result : " + str(result.message))

def main(args=None):
  rclpy.init(args=args)
  node = RobotMovementClient()
  node.send_goal(76, 7)
  rclpy.spin(node)
  rclpy.shutdown()


if __name__ == "__main__":
  main()