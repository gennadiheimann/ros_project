#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "interfaces/action/count_until.hpp"

using CountUntil = interfaces::action::CountUntil;
using CountUntilGoalHandle =  rclcpp_action::ServerGoalHandle<CountUntil>;
using namespace std::placeholders;

class CountUntilServer : public rclcpp::Node // MODIFY NAME
{
public:
  CountUntilServer() : Node("count_until_server") // MODIFY NAME
  {
    count_until_server_ = rclcpp_action::create_server<CountUntil>(
      this,
      "count_until",
      std::bind(&CountUntilServer::goal_callback, this, _1, _2),
      std::bind(&CountUntilServer::cancel_callback, this, _1),
      std::bind(&CountUntilServer::handle_sccepted_callback, this, _1)
    );
    RCLCPP_INFO(this->get_logger(), "Action server has been started");
  }

private:
  rclcpp_action::GoalResponse goal_callback(
    const rclcpp_action::GoalUUID &uuid, std::shared_ptr<const CountUntil::Goal> goal){
      return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse cancel_callback(
    const std::shared_ptr<CountUntilGoalHandle> goal_handle){
      return rclcpp_action::CancelResponse::ACCEPT;
  }

  void handle_sccepted_callback(const std::shared_ptr<CountUntilGoalHandle> goal_handle){
    execute_goal(goal_handle);
  }

  void execute_goal(const std::shared_ptr<CountUntilGoalHandle> goal_handle){
    
  }

  rclcpp_action::Server<CountUntil>::SharedPtr count_until_server_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<CountUntilServer>(); // MODIFY NAME
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
