# -*- encoding: utf-8 -*-

import pygame
import scene
import sys
from  config import *
from pygame.locals import *
import game
import options
import about
import help
import menu_base

class Menu(scene.Scene):

    def __init__(self, world, initial_position=0):
        opciones = [
            ("Jugar", self.jugar),
            ("Opciones", self.mostrar_opciones),
            ("Creditos", self.mostrar_creditos),
            ("Ayuda", self.mostrar_ayuda),
            ("Salir", self.salir_menu)
        ]
        self.menu = menu_base.MenuBase(opciones, initial_position)
        self.world = world
        # self.sonido_menu = pygame.mixer.Sound(KEY_SOUND)
        self.fondo = pygame.image.load(MENU_IMAGE).convert()
        self.title = pygame.image.load("ima/title.png")
        self.screen = None

    def update(self):
        pass

    def draw(self, screen):
        self.screen = screen
        self.screen.blit(self.fondo, (0,0))
        self.menu.draw(self.screen, self.fondo)
        self.screen.blit(self.title, (150, 80))
        pygame.display.flip()

    def on_event(self, e):
        if e.type == KEYDOWN:
            self.menu.on_key_down(e)
            
    def jugar(self):
        new_scene = game.Game(self.world)
        self.world.change_scene(new_scene)

    def mostrar_opciones(self):
        new_scene = options.Options(self.world)
        self.world.change_scene(new_scene)

    def mostrar_creditos(self):
        new_scene = about.About(self.world)
        self.world.change_scene(new_scene)

    def mostrar_ayuda(self):
        new_scene = help.Help(self.world)
        self.world.change_scene(new_scene)

    def salir_menu(self):
        sys.exit(0)
