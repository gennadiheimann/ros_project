#!/usr/bin/env python3
import rclpy
import time
import threading
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from interfaces.action import CountUntil
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

class CountUntilServer(Node): 
  def __init__(self):
    super().__init__("count_until_server") 
    self.goal_handle_: ServerGoalHandle = None
    self.goal_lock_ = threading.Lock()
    self.goal_queue_ = []
    self.count_until_server_ = ActionServer(
      self,
      CountUntil,
      "count_until",
      handle_accepted_callback=self.handle_accepted_callback,
      goal_callback = self.goal_callback,
      cancel_callback = self.cancel_callback,
      execute_callback = self.execute_callback,
      callback_group = ReentrantCallbackGroup()
    )
    self.get_logger().info("Action server has been started")
    
  def handle_accepted_callback(self, goal_handle: ServerGoalHandle):
    with self.goal_lock_:
      if self.goal_handle_ is not None:
        self.goal_queue_.append(goal_handle)
      else:
        goal_handle.execute()
    
  def cancel_callback(self, goal_handle: ServerGoalHandle):
    self.get_logger().warn("Received a cancel request")
    return CancelResponse.ACCEPT # or REJECT
    
  def goal_callback(self, goal_request: CountUntil.Goal):
    self.get_logger().info("Received goal")
    
    # Policy: refuse new goal if current goal still active
    # with self.goal_lock_:
    #   if self.goal_handle_ is not None and self.goal_handle_.is_active:
    #     self.get_logger().info("A goal is already active, rejecting new goal")
    #     return GoalResponse.REJECT
    
    # Validate goal request
    if goal_request.target_number <= 0:
      self.get_logger().info("Rejecting the goal")
      return GoalResponse.REJECT
    self.get_logger().info("Accepting the goal")
    return GoalResponse.ACCEPT
  
    # Policy: preempt existing goal when receiving new goal
    # with self.goal_lock_:
    #   if self.goal_handle_ is not None and self.goal_handle_.is_active:
    #     self.get_logger().info("Abort current goal and accept new goal")
    #     self.goal_handle_.abort()
        
    
  def execute_callback(self, goal_handle: ServerGoalHandle):
    with self.goal_lock_: 
      self.goal_handle_ = goal_handle
    
    # Ger request frm goal
    target_number = goal_handle.request.target_number
    period = goal_handle.request.period
    
    # Excute the action
    self.get_logger().info("Excuting the goal")
    feedback = CountUntil.Feedback()
    counter = 0
    result = CountUntil.Result()
    for i in range(target_number):
      if not self.goal_handle_.is_active:
        self.get_logger().warn("Goal is not active")
        result.reached_number = counter
        self.process_next_goal_in_queue()
        return result
      if goal_handle.is_cancel_requested:
        self.get_logger().warn("Canceling the goal")
        goal_handle.canceled()
        result.reached_number = counter
        self.process_next_goal_in_queue()
        return result
      counter += 1
      self.get_logger().info(str(counter))
      feedback.current_number = counter
      goal_handle.publish_feedback(feedback)
      time.sleep(period)
    
    # Once done, set goal final state
    goal_handle.succeed()
    # goal_handle.abort()
    
    # and send the result
    result.reached_number = counter
    self.process_next_goal_in_queue()
    return result
  
  def process_next_goal_in_queue(self):
    with self.goal_lock_:
      if len(self.goal_queue_) > 0:
        self.goal_queue_.pop(0).execute()
      else:
        self.goal_handle_ = None

      
def main(args=None):
  rclpy.init(args=args)
  node = CountUntilServer()
  rclpy.spin(node, MultiThreadedExecutor())
  rclpy.shutdown()


if __name__ == "__main__":
  main()