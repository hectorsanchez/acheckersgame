# -*- coding: utf-8 -*-
"""Modulo para manejor de turnos"""
import pygame
from pygame.sprite import Sprite
import common
import config

class Turn(Sprite):
    """Representa un visor de turnos, indicando que jugador debe mover la
    siguiente pieza del juego."""

    def __init__(self):
        Sprite.__init__(self)
        self.base_image = common.load_image('turn.png')
        self.can_drag = False
        self.can_click = False

        self.font = pygame.font.Font("font/DejaVuSans.ttf", 17)
        self.update = self.update_starting
        self.movement = common.interpolate((445, 600), (445, 45))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

    def change(self, player):
        "Altera el mensaje de texto indicado el jugador con turno."
        self.image = self.base_image.copy()
        self.common_image = common.load_image('p%s_normal.png' % (player))
        self.image.blit(self.common_image, (64, 25))

    def on_mouse_move(self):
        """ Cuando se mueve el mouse"""
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
