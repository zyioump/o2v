from threading import Thread
import time
import picamera
from PIL import Image

class Camera(Thread):
    def __init__(self, config):
        Thread.__init__(self)

        self.running = True
        self.doPhoto = "(2)"
        self.camera = picamera.PiCamera()
        self.photoNb = 0
        self.delay = int(config["CAMERA"]["timeBetweenImg"])/1000
        self.rotate = int(config["CAMERA"]["rotate"])

    def setStatus(self, status):
        self.doPhoto = status

    def getPhotoNb(self):
        return self.photoNb

    def stop(self):
        self.running = False

    def run(self):
        while self.running == True:
            if self.doPhoto == "(1)":
                self.camera.capture("img/img"+str(self.photoNb)+".jpg")
                self.turnImage(self.photoNb)
                self.photoNb += 1
                time.sleep(self.delay)

    def turnImage(self, x):
        img = Image.open("img/img"+str(x)+".jpg")
        img = img.rotate(self.rotate)
        img.save("img/img"+str(x)+".jpg")
