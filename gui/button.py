# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite
import common

class Button(Sprite):

    def __init__(self, label, font, x, y, callback):
        Sprite.__init__(self)
        self._create_images(label, font)
        self.image = self.glass_image
        self.rect = self.image.get_rect()
        self.can_click = True
        self.can_drag = False
        self.x = 640
        self.y = y
        self.to_x = x
        self.to_y = y
        self.callback = callback

    def update(self):
        self.x += (self.to_x - self.x) / common.MOTION_SPEED
        self.y += (self.to_y - self.y) / common.MOTION_SPEED
        self.rect.topleft = int(self.x), int(self.y)

    def on_mouse_move(self):
        self.image = self.normal_image

    def on_mouse_leave(self):
        self.image = self.glass_image

    def on_mouse_click(self):
        self.x = self.to_x + 10
        self.y = self.to_y + 10
        self.callback()

    def _create_images(self, label, font):
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
