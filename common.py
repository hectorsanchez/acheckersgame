# -*- encoding: utf-8 --
""" Funciones comunes"""

import pygame, pygame.font, pygame.event, pygame.draw, string

from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.locals import MOUSEMOTION, ACTIVEEVENT
from pygame.locals import K_MINUS , K_RETURN, K_BACKSPACE, KEYDOWN, K_ESCAPE

show_tips = True

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

def get_key():
    """Obtiene una tecla """
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass

def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()

def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + string.join(current_string,""))
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey in [K_RETURN, K_ESCAPE]:
            break
        elif inkey == K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            if len(current_string) < 5:
                current_string.append(chr(inkey))

        display_box(screen, question + ": " + string.join(current_string,""))

    return string.join(current_string,"")

