# This Python file uses the following encoding: utf-8

# if__name__ == "__main__":
#     pass
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class TurtlebotController(Node):
    def __init__(self):
        super().__init__('turtlebot_controller_node')

        # Twist üzenet kiadása a Turtlebot mozgatásához
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Akadályt észlelve való megállításhoz szükséges távolság
        self.stop_distance = 0.5  # Méter

        self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )

    def laser_callback(self, msg):
        laser_ranges = msg.ranges

        for i, range in enumerate(laser_ranges):
            # Ha az akadály távolsága kisebb vagy egyenlő a megállási távolsággal
            if range <= self.stop_distance:
                self.stop_robot()
                return  # Kilépünk a függvényből, ha találtunk akadályt

        self.move_forward()

    def stop_robot(self):
        stop_cmd = Twist()
        stop_cmd.linear.x = 0.0
        stop_cmd.angular.z = 0.0
        self.cmd_pub.publish(stop_cmd)

    def move_forward(self):
        move_cmd = Twist()
        move_cmd.linear.x = 0.2  # Lineáris sebesség előre (m/s)
        move_cmd.angular.z = 0.0  # Szögsebesség (rad/s)
        self.cmd_pub.publish(move_cmd)


def main(args=None):
    rclpy.init(args=args)

    controller = TurtlebotController()
    rclpy.spin(controller)

    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
