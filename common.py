# -*- encoding: utf-8 --
""" Funciones comunes"""
import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.locals import MOUSEMOTION, ACTIVEEVENT

MOUSE_EVENTS = [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, ACTIVEEVENT]
MOTION_SPEED = 5.0


def load_image(imagefile, theme):
    """Carga una imagen dentro del tema indicado."""
    image = pygame.image.load('ima/%s/%s' %(theme, imagefile))
    return image.convert_alpha()

def bring_to_front(sprite):
    """Trae un sprite al frente del grupo."""
    for group in sprite.groups():
        group.remove(sprite)
        group.add(sprite)

def interpolate((pos_x, pos_y), (to_x, to_y)):
    """Retorna un generador que aproxima gradualmente un punto a otro."""

    while True:
        dist_x = to_x - pos_x
        dist_y = to_y - pos_y
        dta_x = dist_x / MOTION_SPEED
        dta_y = dist_y / MOTION_SPEED

        if abs(dist_x) >= 1 or abs(dist_y) >= 1:
            pos_x += dta_x
            pos_y += dta_y
            yield int(pos_x), int(pos_y)
        else:
            yield to_x, to_y
            break
