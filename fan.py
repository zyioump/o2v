import RPi.GPIO as GPIO
import configparser

class Fan():
    def __init__(self, config):
        self.config = config

        self.pinFan = int(config["FAN"]["fanPin"])

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.pinFan, GPIO.OUT)

        GPIO.output(self.pinFan, GPIO.LOW)

        self.running = "(2)"

    def changeStatus(self, status):
        self.running = status
        print(self.running)
        if self.running == "(1)":
            GPIO.output(self.pinFan, GPIO.HIGH)
        else:
            GPIO.output(self.pinFan, GPIO.LOW)
