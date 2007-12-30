# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite
from common import load_image
import common

class Button(Sprite):

    def __init__(self, label, x, y, callback):
        Sprite.__init__(self)
        self._create_images(label)
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

    def _create_images(self, label):
        self.normal_image = load_image("%s.png" %label, "buttons")
        self.glass_image = load_image("%s.png" %label, "buttons").convert()
        self.glass_image.set_alpha(128)


