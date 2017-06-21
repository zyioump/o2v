from threading import Thread
import socket
import time
import json

class Volant(Thread):
    def __init__(self, config, motor):
        Thread.__init__(self)
        self.config = config
        self.motor = motor
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(("",int(self.config["VOLANT"]["serverPort"])))
        self.running = True
        self.connectionRunning = False
        self.json = {}

    def run(self):
        while self.running:
            self.sock.listen(1)
            self.volant, addr = self.sock.accept()
            self.connectionRunning = True
            while self.connectionRunning:
                msg = self.volant.recv(255).decode("utf-8")

                if not msg:
                    self.connectionRunning = False
                    return 0

                try:
                    self.json = json.loads(msg)
                except:
                    pass

                self.motor.changeStatus(self.json["motor"])
                self.motor.changeDirection(self.json["direction"])

                time.sleep(50/1000)


    def stop(self):
        self.connectionRunning = False
        self.running = False
        self.sock.close()
