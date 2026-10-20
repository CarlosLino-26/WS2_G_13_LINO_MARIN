import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MovimientoRecto(Node):
    def __init__(self):
        super().__init__('movimiento_recto_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.contador = 0

    def timer_callback(self):
        msg = Twist()
        
        if self.contador < 10:
            msg.linear.x = 0.5  # Velocidad hacia adelante
            msg.angular.z = 0.0
            self.get_logger().info('Avanzando en línea recta...')
        else:
            msg.linear.x = 0.0  # Velocidad cero para detenerse
            msg.angular.z = 0.0
            self.get_logger().info('Trayectoria terminada. Deteniendo robot.')
        
        # 1. Siempre publicar el mensaje de velocidad primero
        self.publisher_.publish(msg)
        
        # 2. Luego verificar si ya se cumplió el tiempo para apagar el nodo
        if self.contador >= 10:
            rclpy.shutdown()
            
        self.contador += 1

def main(args=None):
    rclpy.init(args=args)
    nodo = MovimientoRecto()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()

if __name__ == '__main__':
    main()
