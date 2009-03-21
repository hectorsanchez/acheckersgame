# -*- coding: utf-8 -*-
"""Modulo para manejor de turnos"""
import pygame
from pygame.sprite import Sprite
import common
from config import THEME

class Turn(Sprite):
    """Representa un visor de turnos, indicando que jugador debe mover la
    siguiente pieza del juego."""

    def __init__(self):
        Sprite.__init__(self)
        self.base_image = common.load_image('turn.png', THEME)
        self.can_drag = False
        self.can_click = False

        self.font = pygame.font.Font("font/DejaVuSans.ttf", 17)
        self.update = self.update_starting
        self.movement = common.interpolate((640, 200), (445, 200))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

    def change(self, player):
        "Altera el mensaje de texto indicado el jugador con turno."
        self.image = self.base_image.copy()
        text = "Turno del jugador: %d" % (player)
        text_image = self.font.render(text, 1, (0, 0, 0))
        self.image.blit(text_image, (5, 5))

    def on_mouse_move(self):
        """ Cuando se muevoe el mouse"""
        pass

    def on_mouse_leave(self):
        """ Al dejar al mouse"""
        pass

    def update_normal(self):
        """ Estado normal"""
        pass

    def update_starting(self):
        "Actualiza el movimiento del cuadro mientras inicia la escena."
        try:
            self.rect.topleft = self.movement.next()
        except StopIteration:
            self.update = self.update_normal
