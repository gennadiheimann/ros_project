#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "interfaces/action/count_until.hpp"

class CountUntilServer : public rclcpp::Node // MODIFY NAME
{
public:
  CountUntilServer() : Node("count_until_server") // MODIFY NAME
  {

  }

private:

};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<CountUntilServer>(); // MODIFY NAME
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
