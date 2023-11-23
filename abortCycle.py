import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class Abort_cycle(Node):

    def __init__(self):
        super().__init__('abort_cycle')
        self.server = self.create_service(Trigger, 'abort_cycle', self.callback)

    def callback(self, request, response):
        self.get_logger().info("El servicio abort_cycle fue activado.")
        response.success = True
        response.message = "El servicio abort_cycle ha fracasado"
        return response

def main(args=None):
    rclpy.init(args=args)
    server_node = Abort_cycle()
    rclpy.spin(server_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()