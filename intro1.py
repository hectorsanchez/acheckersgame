import pygame
import intro
import intro2

class Intro1(intro.Intro):

    def load_image(self):
        self.fondo = pygame.image.load('ima/intro1.png').convert()

    def go_to_next(self):
        new_scene = intro2.Intro2(self.world)
        self.world.change_scene(new_scene)

