# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite
from common import load_image

class Button(Sprite):

    def __init__(self, label, x, y):
        Sprite.__init__(self)
        self._create_images(label)
        self.image = self.glass_image
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.can_click = True
        self.can_drag = False

    def on_mouse_move(self):
        self.image = self.normal_image

    def on_mouse_leave(self):
        self.image = self.glass_image

    def on_mouse_click(self):
        print "Ha pulsado este boton: %s" %str(self)

    def _create_images(self, label):
        self.normal_image = load_image("%s.png" %label, "buttons")
        self.glass_image = load_image("%s.png" %label, "buttons").convert()
        self.glass_image.set_alpha(128)
