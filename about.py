# -*- encoding: utf-8 -*-
import pygame
import scene
from  config import *
from pygame.locals import *
import menu

class About(scene.Scene):

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.background = pygame.image.load("ima/about.png")

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def on_event(self, e):
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                self.world.change_scene(menu.Menu(self.world, 2))
