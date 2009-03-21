# -*- coding: utf-8 -*-
""" Manejo de los botones del juego"""
import pygame
from pygame.sprite import Sprite
import common

class Button(Sprite):
    """Clase para manejo de botones """
    def __init__(self, label, font, pos_x, pos_y, callback):
        Sprite.__init__(self)
        self.glass_image = None
        self.normal_image = None
        self._create_images(label, font)
        self.image = self.glass_image
        self.rect = self.image.get_rect()
        self.can_click = True
        self.can_drag = False
        self.pos_x = 640
        self.pos_y = pos_y
        self.to_x = pos_x
        self.to_y = pos_y
        self.callback = callback


    def update(self):
        """ Actualiza el estado del boton"""
        self.pos_x += (self.to_x - self.pos_x) / common.MOTION_SPEED
        self.pos_y += (self.to_y - self.pos_y) / common.MOTION_SPEED
        self.rect.topleft = int(self.pos_x), int(self.pos_y)

    def on_mouse_move(self):
        """Cambia la imagen al mover el mouse sobre el boton"""
        self.image = self.normal_image

    def on_mouse_leave(self):
        """Cambia la imagen al mover el mouse fuera del boton"""
        self.image = self.glass_image

    def on_mouse_click(self):
        """Mueve el boton, y recarla la pantalla """
        self.pos_x = self.to_x + 10
        self.pos_y = self.to_y + 10
        self.callback()

    def _create_images(self, label, font):
        """ Carga las imagenes del juego"""
        white = (255, 255, 255)
        black = (0, 0, 0)
        gray = (200, 200, 200)

        text_surface = font.render(label, 1, black)
        button_size = text_surface.get_rect().inflate(10, 10).size

        button_surface = pygame.Surface(button_size).convert()

        button_surface.fill(white)
        button_surface.blit(text_surface, (5, 5))

        border_rect = button_surface.get_rect()
        border_rect.width -= 1
        border_rect.height -= 1

        pygame.draw.rect(button_surface, black, border_rect, 2)
        self.normal_image = button_surface

        button_surface = button_surface.convert()
        button_surface.fill(gray)
        button_surface.blit(text_surface, (5, 5))
        pygame.draw.rect(button_surface, black, border_rect, 2)

        self.glass_image = button_surface
