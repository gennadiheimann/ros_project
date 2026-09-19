#!/usr/bin/env python3
import rclpy
import time
import threading
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from interfaces.action import RobotMovement
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

class RobotMovementServer(Node): 
  def __init__(self):
    super().__init__("robot_movement_server") 
    self.goal_handle_: ServerGoalHandle = None
    self.goal_lock_ = threading.Lock()
    self.current_position = 50
    self.robot_movement_server_ = ActionServer(
      self,
      RobotMovement,
      "robot_movement",
      # handle_accepted_callback=self.handle_accepted_callback,
      goal_callback = self.goal_callback,
      cancel_callback = self.cancel_callback,
      execute_callback = self.execute_callback,
      callback_group = ReentrantCallbackGroup()
    )
    self.get_logger().info("Action server has been started")
    
  # def handle_accepted_callback(self, goal_handle: ServerGoalHandle):
    # with self.goal_lock_:
    #   if self.goal_handle_ is not None:
    #     self.goal_queue_.append(goal_handle)
    #   else:
    #     goal_handle.execute()
    
  def cancel_callback(self, goal_handle: ServerGoalHandle):
    self.get_logger().warn("Received a cancel request")
    return CancelResponse.ACCEPT # or REJECT
    
  def goal_callback(self, goal_request: RobotMovement.Goal):
    self.get_logger().info("Received goal")
    
    # Policy: refuse new goal if current goal still active
    # with self.goal_lock_:
    #   if self.goal_handle_ is not None and self.goal_handle_.is_active:
    #     self.get_logger().info("A goal is already active, rejecting new goal")
    #     return GoalResponse.REJECT
    
    # Validate goal request
    if goal_request.position < 0 or goal_request.position > 100:
      self.get_logger().info("Rejecting the goal")
      return GoalResponse.REJECT
  
    # Policy: preempt existing goal when receiving new goal
    with self.goal_lock_:
      if self.goal_handle_ is not None and self.goal_handle_.is_active:
        self.get_logger().info("Abort current goal and accept new goal")
        self.goal_handle_.abort()
        
    self.get_logger().info("Accepting the goal")
    return GoalResponse.ACCEPT
    
  def execute_callback(self, goal_handle: ServerGoalHandle):
    with self.goal_lock_: 
      self.goal_handle_ = goal_handle
    
    # Ger request frm goal
    position = goal_handle.request.position
    velocity = goal_handle.request.velocity
    
    # Excute the action
    self.get_logger().info("Excuting the goal")
    feedback = RobotMovement.Feedback()
    result = RobotMovement.Result()

    while rclpy.ok():
      if not goal_handle.is_active:
        self.get_logger().warn("Goal is not active")
        result.position = self.current_position
        return result
        
      if goal_handle.is_cancel_requested:
        self.get_logger().warn("Canceling the goal")
        result.position = self.current_position
        if position == self.current_position:
          result.message = "Robot reach the position"
          goal_handle.succeed()
        else: 
          result.message = "Canceled"
          goal_handle.canceled()
        return result
        
      diff = position - self.current_position
              
      if diff < 0 :
        # Backwards
        if abs(diff) < velocity:
          self.current_position -= abs(diff)
          break
        self.current_position -= velocity
      else:
        # forwards
        if abs(diff) < velocity:
          self.current_position += diff
          break
        self.current_position += velocity
        
      self.get_logger().info("Current Position: " + str(self.current_position))
      feedback.current_position = self.current_position
      goal_handle.publish_feedback(feedback)
        
      time.sleep(1.0)
    # Once done, set goal final state
    if goal_handle.is_active:
      goal_handle.succeed()
    else:
      self.get_logger().warn("Goal was aborted, not calling succeed()")
          
    # and send the result
    self.get_logger().info("Robot reach tehe position: " + str(self.current_position))
    result.position = self.current_position
    result.message = "Robot reachs the position"
    return result
  
def main(args=None):
  rclpy.init(args=args)
  node = RobotMovementServer()
  rclpy.spin(node, MultiThreadedExecutor())
  rclpy.shutdown()


if __name__ == "__main__":
  main()