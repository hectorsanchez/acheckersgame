import pygame
from pygame.locals import *

MOUSE_EVENTS = [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, ACTIVEEVENT]

def load_image(file, theme):
    image = pygame.image.load('ima/%s/%s' %(theme, file))
    return image
