#! /usr/bin/env python3
import pygame
from pygame.locals import *
import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

print("A partir de quelle image voulez commencez l'affichage ?")
x = int(input("--> "))
try:
    img = pygame.image.load("img/img"+str(x)+".jpg")

    windowSize = img.get_rect().size

    timeBetweenImg = int(config["CAMERA"]["timeBetweenImg"])/1000

    window = pygame.display.set_mode((windowSize[0],windowSize[1]))
    pygame.init()
    pygame.display.set_caption("Afficheur")

    running = True
except:
    print("Image de base introuvable")
    running = False

while running == True:
    window.blit(img, (0,0))
    pygame.display.flip()
    x+=1
    try:
        img = pygame.image.load("img/img"+str(x)+".jpg")
    except:
        print("Plus d'image !")
        running = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    time.sleep(timeBetweenImg)
