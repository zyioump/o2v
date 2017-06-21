#! /usr/bin/env python3
import pygame
from pygame.locals import *
import time
import socket

pygame.init()

xMax = 800
yMax = 480

window = pygame.display.set_mode((xMax, yMax))

back = pygame.image.load("back.jpg")
back = pygame.transform.scale(back, (xMax, yMax))

volant = pygame.image.load("volant.png")
volant = pygame.transform.scale(volant, (100, 100))

running = True

class Menu():
    def __init__(self, back, volant, window, joystick, xMax, yMax, sock):
        self.delay = 50
        self.timeBetweenImg = 500
        self.totalStep = int(self.timeBetweenImg/self.delay)
        self.currentStep = self.totalStep
        self.currentImg = 0
        self.back = back
        self.volant = volant
        self.volantBis = self.volant
        self.window = window
        self.xMax = xMax
        self.yMax = yMax
        self.running = True
        self.currentMenu = "Principal"
        self.currentSelection = 0
        self.mainMenu = ["Caméra", "Ventilateur", "Lampe"]
        self.cameraMenu = ["Allumer", "Eteindre", "Nombre d'image", "Voir les images"]
        self.imageMenu = ["Depuis le début", "Semis Direct"]
        self.ventilateurMenu = ["Allumer", "Eteindre"]
        self.lampMenu = ["Allumer", "Eteindre"]
        self.boxSize = [self.xMax/2, self.yMax/2]
        self.imageBoxSize = [self.xMax - 20*2, self.yMax - 20*2]
        self.mainFont = pygame.font.SysFont("broadway",75,bold=False,italic=False)
        self.secondaryFont = pygame.font.SysFont("broadway",40,bold=False,italic=False)
        self.joystick = joystick
        self.downButton = 14
        self.rightButton = 13
        self.leftButton = 15
        self.upButton = 12
        self.backButton = 6
        self.nextButton = 7
        self.quitButton = 8
        self.pedale = 0
        self.sock = sock
        self.lastMotorState = "off"
        self.lastDirectionState = "font"

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def run(self):
        while self.running == True:
            self.window.blit(self.back, (0,0))

            if self.currentMenu == "Depuis le début" or self.currentMenu == "Semis Direct":
                pygame.draw.rect(self.window, (255, 255, 255), (self.xMax/2-self.imageBoxSize[0]/2,self.yMax/2-self.imageBoxSize[1]/2,self.imageBoxSize[0],self.imageBoxSize[1]))
            else:
                pygame.draw.rect(self.window, (255, 255, 255), (self.xMax/2-self.boxSize[0]/2,self.yMax/2-self.boxSize[1]/2,self.boxSize[0],self.boxSize[1]))
                self.window.blit(self.mainFont.render(self.currentMenu,1,(0,0,0)), (self.xMax/2-self.boxSize[0]/2,self.yMax/2-self.boxSize[1]/2))
                y = self.yMax/2-self.boxSize[1]/2 + 75
                self.window.blit(self.volantBis, (self.xMax/2, y-75+self.boxSize[1]+10))
                pygame.draw.rect(self.window, (0,0,0), (self.xMax/2-100, y-75+self.boxSize[1]+10, 60, 100))
                pygame.draw.rect(self.window, (255,255,255), (self.xMax/2-95, y-75+self.boxSize[1]+10+5, 50, 90))
                pygame.draw.rect(self.window, (0,0,0), (self.xMax/2-100, y-75+self.boxSize[1]+10+50-5/2+self.pedale*85/2, 60, 5))



            if self.currentMenu == "Principal":
                for i in range(len(self.mainMenu)):
                    if self.currentSelection == i:
                        self.window.blit(self.secondaryFont.render("  > "+self.mainMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    else:
                        self.window.blit(self.secondaryFont.render("     "+self.mainMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    y += 40
            elif self.currentMenu == "Caméra":
                for i in range(len(self.cameraMenu)):
                    if self.currentSelection == i:
                        self.window.blit(self.secondaryFont.render("  > "+self.cameraMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    else:
                        self.window.blit(self.secondaryFont.render("     "+self.cameraMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    y += 40
            elif self.currentMenu == "Ventilateur":
                for i in range(len(self.ventilateurMenu)):
                    if self.currentSelection == i:
                        self.window.blit(self.secondaryFont.render("  > "+self.ventilateurMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    else:
                        self.window.blit(self.secondaryFont.render("     "+self.ventilateurMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    y += 40
            elif self.currentMenu == "Lampe":
                for i in range(len(self.lampMenu)):
                    if self.currentSelection == i:
                        self.window.blit(self.secondaryFont.render("  > "+self.lampMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    else:
                        self.window.blit(self.secondaryFont.render("     "+self.lampMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    y += 40
            elif self.currentMenu == "Nombre d'image":
                self.window.blit(self.secondaryFont.render("     x image(s)",1,(0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
            elif self.currentMenu == "Voir les images":
                for i in range(len(self.imageMenu)):
                    if self.currentSelection == i:
                        self.window.blit(self.secondaryFont.render("  > "+self.imageMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    else:
                        self.window.blit(self.secondaryFont.render("     "+self.imageMenu[i], 1, (0,0,0)), (self.xMax/2-self.boxSize[0]/2, y))
                    y += 40
            elif self.currentMenu == "Depuis le début":
                if self.currentStep >= self.totalStep:
                    self.currentStep = 0
                    self.currentImg += 1
                try:
                    img = pygame.image.load("img/img"+str(self.currentImg+".jpg"))
                    img = pygame.transform.scale(img, (self.imageBoxSize[0]-20, self.imageBoxSize[1]-20))
                    self.window.blit(img, (self.xMax/2-self.imageBoxSize[0]/2+10,self.yMax/2-self.imageBoxSize[1]/2+10))
                except:
                    self.currentMenu = "Principal"
                    self.currentSelection = 0
                self.currentStep += 1

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == JOYBUTTONUP:
                    if event.button == self.quitButton:
                        self.running = False
                    elif event.button == self.downButton:
                        self.currentSelection += 1
                        if self.currentMenu == "Principal":
                            if self.currentSelection >= len(self.mainMenu):
                                self.currentSelection = 0
                        if self.currentMenu == "Caméra":
                            if self.currentSelection >= len(self.cameraMenu):
                                self.currentSelection = 0
                        if self.currentMenu == "Ventilateur":
                            if self.currentSelection >= len(self.ventilateurMenu):
                                self.currentSelection = 0
                        if self.currentMenu == "Lampe":
                            if self.currentSelection >= len(self.lampMenu):
                                self.currentSelection = 0
                        if self.currentMenu == "Voir les images":
                            if self.currentSelection >= len(self.imageMenu):
                                self.currentSelection = 0
                    elif event.button == self.upButton:
                        self.currentSelection -= 1
                        if self.currentSelection < 0:
                            if self.currentMenu == "Principal":
                                self.currentSelection = len(self.mainMenu)-1
                            if self.currentMenu == "Caméra":
                                self.currentSelection = len(self.cameraMenu)-1
                            if self.currentMenu == "Ventilateur":
                                self.currentSelection = len(self.ventilateurMenu)-1
                            if self.currentMenu == "Lampe":
                                self.currentSelection = len(self.lampMenu)-1
                            if self.currentMenu == "Voir les images":
                                self.currentSelection = len(self.imageMenu)-1

                    elif event.button == self.nextButton:
                        if self.currentMenu == "Principal":
                            self.currentMenu = self.mainMenu[self.currentSelection]
                            self.currentSelection = 0
                        elif self.currentMenu == "Caméra":
                            if self.currentSelection == 2 or self.currentSelection == 3:
                                self.currentMenu = self.cameraMenu[self.currentSelection]
                                self.currentSelection = 0
                        elif self.currentMenu == "Voir les images":
                            self.currentMenu = self.imageMenu[self.currentSelection]
                            self.currentSelection = 0
                            self.currentStep = self.totalStep
                            self.currentImg = 0

                    elif event.button == self.backButton:
                        self.currentMenu = "Principal"
                        self.currentSelection = 0
                elif event.type == JOYAXISMOTION:
                    if event.axis == 0:
                         self.volantBis = self.rot_center(self.volant, -event.value*90)
                         if event.value >= 1:
                             if self.lastMotorState != "right":
                                self.sock.send("direction:right".encode('utf-8'))
                                self.lastMotorState = "right"
                         elif event.value <= -1:
                             if self.lastMotorState != "left":
                                self.sock.send("direction:left".encode('utf-8'))
                                self.lastMotorState = "left"
                         else:
                             if self.lastMotorState != "front":
                                self.sock.send("direction:front".encode('utf-8'))
                                self.lastMotorState = "front"

                    elif event.axis == 3:
                        self.pedale = event.value
                        if event.value <= -1:
                            if self.lastMotorState != "on":
                                self.sock.send("motor:on".encode('utf-8'))
                                self.lastMotorState = "on"
                                self.sock.send("direction:front".encode('utf-8'))
                                self.lastDirectionState = "front"
                        elif event.value >= 1:
                            if self.lastDirectionState != "back":
                                self.sock.send("direction:back".encode('utf-8'))
                                self.lastDirectionState = "back"
                                if self.lastMotorState != "on":
                                    time.sleep(0.1)
                                    self.sock.send("motor:on".encode('utf-8'))
                                    self.lastMotorState = "on"
                        else:
                            if self.lastMotorState != "off":
                                self.sock.send("motor:off".encode('utf-8'))
                                self.lastMotorState = "off"

            time.sleep(self.delay/1000)

js = pygame.joystick.Joystick(0)
js.init()
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(("169.254.232.39", 1906))
menu = Menu(back, volant, window, js, xMax, yMax, sock)
menu.run()
print("Impossible de se connecter à la voiture")
print("Vérifier que vous êtes bien connecté à la voiture")
print("Êtes vous sur d'avoir lancé le serveur ?")
print("Est-il bien réglé sur le port "+port+" ?")
print("N'y a t'il pas de firewall activé ?")
print("Impossible d'utiliser la manette")
