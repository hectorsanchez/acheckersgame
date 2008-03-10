# -*- encoding: utf-8 -*-
import pygame
from pygame.locals import *
from config import DEBUG

MOUSE_EVENTS = [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, ACTIVEEVENT]
MOTION_SPEED = 5.0


def load_image(file, theme):
    "Carga una imagen dentro del tema indicado."
    image = pygame.image.load('ima/%s/%s' %(theme, file))
    return image.convert_alpha()

def bring_to_front(sprite):
    "Trae un sprite al frente del grupo."
    for g in sprite.groups():
        g.remove(sprite)
        g.add(sprite)


def interpolate((x, y), (to_x, to_y)):
    "Retorna un generador que aproxima gradualmente un punto a otro."

    while True:
        dist_x = to_x - x
        dist_y = to_y - y
        dx = dist_x / MOTION_SPEED
        dy = dist_y / MOTION_SPEED

        if abs(dist_x) >= 1 or abs(dist_y) >= 1:
            x += dx
            y += dy
            yield int(x), int(y)
        else:
            yield to_x, to_y
            break

def debug(*args):
    if DEBUG:
        for arg in args:
            print arg,
        print