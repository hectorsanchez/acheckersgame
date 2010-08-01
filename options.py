# -*- encoding: utf-8 -*-
import pygame
import scene
from config import *
from pygame.locals import *
import common
import menu
import menu_base

class Options(scene.Scene):

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.background = pygame.image.load("ima/options.png")
        opciones = [
            ("Pantalla completa / Ventana", self.toggle_fullscreen),
            ("Regresar", self.return_to_main_menu),
            ]
        self.menu = menu_base.MenuBase(opciones, 0)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0,0))
        self.menu.draw(screen, self.background)
        pygame.display.flip()

    def on_event(self, e):
        if e.type == KEYDOWN:
            self.menu.on_key_down(e)
            if e.key == K_ESCAPE:
                self.return_to_main_menu()

    def toggle_fullscreen(self):
        pygame.display.toggle_fullscreen()
    def return_to_main_menu(self):
        self.world.change_scene(menu.Menu(self.world, 1))
