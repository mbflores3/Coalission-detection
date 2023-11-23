#!/usr/bin/env python3
import rclpy
import json
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, Bool

class Publisher(Node):

    def __init__(self):
        super().__init__('publisher')
        self.current = []
        self.rpm = []
        #### Ejemplo archivo no_choque ####

        #file_path = 'src/desafio_tecnico/desafio_tecnico/Extractions/1697554334557491312.json'

        #### Ejemplo archivo choque ####

        file_path = 'Extractions/1695718216618806613.json'
        self.reading(file_path)
        self.alarma = False
        self.publisher_ = self.create_publisher(Float32MultiArray, 'topic', 10)
        self.subscription_alarm = self.create_subscription(Bool,'alarma',self.cambio_estado,10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def reading(self, json_file):
        f = open(json_file)
        data = json.load(f)
        for i in data["current"]:
            self.current.append(i)
        f.close()
    
    def cambio_estado(self, msg):
        if msg.data != self.alarma:
            self.get_logger().info('Se activó la alarma')
            self.alarma = True

    def timer_callback(self):
        if not self.alarma:
            msg = Float32MultiArray()
            msg.data = [self.current[self.i], float(self.i)]
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)
            self.i += 1



def main(args=None):
    rclpy.init(args=args)

    publisher = Publisher()

    rclpy.spin(publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
