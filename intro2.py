import pygame
import intro
import game

class Intro2(intro.Intro):

    def load_image(self):
        self.fondo = pygame.image.load('ima/intro2.png').convert()

    def go_to_next(self):
        new_scene = game.Game(self.world)
        self.world.change_scene(new_scene)

