#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from rclpy.action.server import ServerGoalHandle
from interfaces.action import CountUntil

class CountUntilServer(Node): 
  def __init__(self):
    super().__init__("count_until_server") 
    self.count_until_server_ = ActionServer(
      self,
      CountUntil,
      "count_until",
      goal_callback = self.goal_callback,
      execute_callback=self.excute_callback
    )
    self.get_logger().info("Action server has been started")
    
  def goal_callback(self, goal_request: CountUntil.Goal):
    self.get_logger().info("Recaeived goal")
    # Validate goal request
    if goal_request.target_number <= 0:
      self.get_logger().info("Rejecting the goal")
      return GoalResponse.REJECT
    self.get_logger().info("Accepting the goal")
    return GoalResponse.ACCEPT
    
  def excute_callback(self, goal_handle: ServerGoalHandle):
    # Ger request frm goal
    target_number = goal_handle.request.target_number
    period = goal_handle.request.period
    
    # Excute the action
    self.get_logger().info("Excuting the goal")
    feedback = CountUntil.Feedback()
    counter = 0
    for i in range(target_number):
      counter += 1
      # self.get_logger().info(str(counter))
      feedback.current_number = counter
      goal_handle.publish_feedback(feedback)
      time.sleep(period)
    
    # Once done, set goal final state
    goal_handle.succeed()
    # goal_handle.abort()
    
    # and send the result
    result = CountUntil.Result()
    result.reached_number = counter
    return result
      
def main(args=None):
  rclpy.init(args=args)
  node = CountUntilServer()
  rclpy.spin(node)
  rclpy.shutdown()


if __name__ == "__main__":
  main()