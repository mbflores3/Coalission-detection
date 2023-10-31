#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import numpy as np
import pandas as pd
from std_msgs.msg import Float32MultiArray, Bool
from std_srvs.srv import Trigger
from functools import partial
from joblib import load


class Subscriber(Node):

    def __init__(self):
        super().__init__('subscriber')
        self.modelo = load('src/desafio_tecnico/desafio_tecnico/modeloCaracteristicas.pkl')
        self.corriente = []  #Lista que tendrá ventanas de corriente
        self.wind = 10  #Largo de la ventana
        self.amp=15
        self.sigma = 2
        self.subscription = self.create_subscription(Float32MultiArray,'topic',self.listener_callback,10)
        self.alarm_to_publisher = self.create_publisher(Bool, 'alarma', 10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        i = int(msg.data[1])
        self.get_logger().info('corriente: "%f"' % msg.data[0])
        self.corriente.append(msg.data[0])
        if len(self.corriente) == self.wind:
            x = self.corriente
            #Características que se extraen por cada serie temporal
            x=x/np.max(x)
            lista=list()
            lista.append(x[-1])
            derivada_9 = (x[-1]-x[0])/(len(x)-1)
            lista.append(derivada_9)
            derivada_3 = (x[-1]-x[-5])/3
            lista.append(derivada_3)
            lista.append(np.min(x))
            lista.append(np.std(x))
            lista.append(np.mean(x))

            prediccion = self.modelo.predict([lista])[0]
            #self.get_logger().info(prediccion)
            if prediccion == 1:
                message = 'abort_cylce'
                self.get_logger().info('Activando servicio')
                self.call_trigger_service(message)
                msg = Bool()
                msg.data = True
                self.alarm_to_publisher.publish(msg)

            self.corriente = []

    def call_trigger_service(self, message):
        client_ = self.create_client(Trigger, 'abort_cycle')
        while not client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('waiting for service')
        request_message = Trigger.Request()
        future = client_.call_async(request_message)
        future.add_done_callback(partial(self.callback_trigger))
                #msg = Trigger()
                #msg = '¡llamando al servicio abort_cycle!'
                #self.abo.publish()
            
        #wind = self.ventana
        #sigma = 1.9
        #if i > wind:
        #    currentData = pd.DataFrame(self.current, columns=['current'])
        #    currentData["bottom"] = currentData['current'].rolling(window=wind).mean() - (1.7 * sigma * currentData['current'].rolling(window=wind).std())
        #    currentData["top"] = currentData['current'].rolling(window=wind).mean() + (1.7 * sigma * currentData['current'].rolling(window=wind).std())
        #    rpmData = pd.DataFrame(self.rpm, columns=['rpm'])
        #    rpmData["bottom"] = rpmData['rpm'].rolling(window=wind).mean() - (1.7 * sigma * rpmData['rpm'].rolling(window=wind).std())
        #    rpmData["top"] = rpmData['rpm'].rolling(window=wind).mean() + (1.7* sigma * rpmData['rpm'].rolling(window=wind).std())
        #
        #    if (rpmData["bottom"][i] > self.rpm[i] or rpmData["top"][i] < self.rpm[i]) and (currentData["bottom"][i] > self.current[i] or currentData["top"][i] < self.current[i]):
        #        self.get_logger().info('Anomaly found in second: "%d"' % i)
        #
        #self.get_logger().info('Current value: "%f"' % msg.data[0])
    
    def callback_trigger(self, future):
        try:
            response = future.result()
            if response:
                self.get_logger().info("Servicio abort_cycle exitoso")
        except Exception as e:
            self.get_logger().error("Llamada al servicio falló: %r"% (e,))


def main(args=None):
    rclpy.init(args=args)

    subscriber = Subscriber()

    rclpy.spin(subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()