import RPi.GPIO as GPIO
import configparser
import time

class Motor():
    def __init__(self, config):
        self.config = config

        self.pinMotor1 = int(config["MOTOR"]["pinMotor1"])
        self.pinMotor1Invert = int(config["MOTOR"]["pinInvertMotor1"])
        self.pinMotor2 = int(config["MOTOR"]["pinMotor2"])
        self.pinMotor2Invert = int(config["MOTOR"]["pinInvertMotor2"])

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.pinMotor1, GPIO.OUT)
        GPIO.setup(self.pinMotor1Invert, GPIO.OUT)
        GPIO.setup(self.pinMotor2, GPIO.OUT)
        GPIO.setup(self.pinMotor2Invert, GPIO.OUT)

        GPIO.output(self.pinMotor1, GPIO.LOW)
        GPIO.output(self.pinMotor1Invert, GPIO.LOW)
        GPIO.output(self.pinMotor2, GPIO.LOW)
        GPIO.output(self.pinMotor2Invert, GPIO.LOW)

        self.running = "(2)"
        self.direction = "(1)"

    def changeStatus(self, status):
        self.running = status
        self.changeDirection(self.direction)

    def changeDirection(self, direction):
        self.direction = direction
        if self.running == "(1)":
            if self.direction == "(1)":
                GPIO.output(self.pinMotor1Invert, GPIO.LOW)
                GPIO.output(self.pinMotor2Invert, GPIO.LOW)
                GPIO.output(self.pinMotor1, GPIO.HIGH)
                GPIO.output(self.pinMotor2, GPIO.HIGH)
            elif self.direction == "(2)":
                GPIO.output(self.pinMotor1, GPIO.LOW)
                GPIO.output(self.pinMotor2, GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(self.pinMotor1Invert, GPIO.HIGH)
                GPIO.output(self.pinMotor2Invert, GPIO.HIGH)
            elif self.direction == "(4)":
                GPIO.output(self.pinMotor1, GPIO.LOW)
                GPIO.output(self.pinMotor2Invert, GPIO.LOW)
                GPIO.output(self.pinMotor2, GPIO.HIGH)
                GPIO.output(self.pinMotor1Invert, GPIO.HIGH)
            elif self.direction == "(3)":
                GPIO.output(self.pinMotor2, GPIO.LOW)
                GPIO.output(self.pinMotor1Invert, GPIO.LOW)
                GPIO.output(self.pinMotor1, GPIO.HIGH)
                GPIO.output(self.pinMotor2Invert, GPIO.HIGH)
        else:
            GPIO.output(self.pinMotor1, GPIO.LOW)
            GPIO.output(self.pinMotor1Invert, GPIO.LOW)
            GPIO.output(self.pinMotor2, GPIO.LOW)
            GPIO.output(self.pinMotor2Invert, GPIO.LOW)
