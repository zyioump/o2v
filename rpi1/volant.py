from threading import Thread
import socket
import time

class Volant(Thread):
    def __init__(self, config, motor):
        Thread.__init__(self)
        self.config = config
        self.motor = motor
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(("",int(self.config["VOLANT"]["serverPort"])))
        self.running = True
        self.connectionRunning = False
        print(self.config["VOLANT"]["serverPort"])

    def run(self):
        while self.running:
            self.sock.listen(1)
            volant, addr = self.sock.accept()
            self.connectionRunning = True
            while self.connectionRunning:
                msg = volant.recv(255).decode("utf-8")
                if not msg:
                    self.connectionRunning = False
                elif msg == "motor:on":
                    self.motor.changeStatus("(1)")
                elif msg == "motor:off":
                    self.motor.changeStatus("(2)")
                elif msg == "direction:front":
                    self.motor.changeDirection("(1)")
                elif msg == "direction:back":
                    self.motor.changeDirection("(2)")
                elif msg == "direction:right":
                    self.motor.changeDirection("(3)")
                elif msg == "direction:left":
                    self.motor.changeDirection("(4)")

                time.sleep(0.250)


    def stop(self):
        self.connectionRunning = False
        self.running = False
