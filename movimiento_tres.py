import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MovimientoTres(Node):
    def __init__(self):
        super().__init__('movimiento_tres_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        # Temporizador configurado a 0.5 segundos por iteración
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.contador = 0

    def timer_callback(self):
        msg = Twist()
        
        if self.contador < 8:
            # Fase 1: Arco superior (4 segundos)
            # Avanza mientras gira a la derecha formando un semicírculo
            msg.linear.x = 0.4
            msg.angular.z = -0.8
            self.get_logger().info('Trazando arco superior...')
            
        elif self.contador < 12:
            # Fase 2: Giro sobre su propio eje (2 segundos)
            # Se detiene linealmente y gira a la izquierda para acomodarse
            msg.linear.x = 0.0
            msg.angular.z = 1.57  
            self.get_logger().info('Girando en el centro del 3...')
            
        elif self.contador < 20:
            # Fase 3: Arco inferior (4 segundos)
            # Vuelve a avanzar girando a la derecha para cerrar el 3
            msg.linear.x = 0.4
            msg.angular.z = -0.8
            self.get_logger().info('Trazando arco inferior...')
            
        else:
            # Fase 4: Detenerse
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('Trayectoria terminada. Deteniendo robot.')
        
        # Publicar el comando de velocidad actual
        self.publisher_.publish(msg)
        
        # Apagar el nodo si ya pasó la última fase
        if self.contador >= 20:
            rclpy.shutdown()
            
        self.contador += 1

def main(args=None):
    rclpy.init(args=args)
    nodo = MovimientoTres()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()

if __name__ == '__main__':
    main()
