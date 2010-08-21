# -*- encoding: utf-8 -*-
import config
from pygame.locals import *
import pygame
import scene
import common
import menu
import menu_base
import game

class Options(scene.Scene):

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.background = pygame.image.load("ima/options.png")
        opciones = [
            ("Pantalla completa / Ventana", self.toggle_fullscreen),
            ("Mostrar consejos:", self.toggle_tips),
            ("Seleccionar Tema:" + config.THEME, self.change_theme),
            ("Regresar", self.return_to_main_menu),
            ]
        self.menu = menu_base.MenuBase(opciones, 0)
        self.update_show_tips_label()

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

    def change_theme(self):
        self.update_theme_label()

    def update_theme_label(self):
        if config.THEMES.index(config.THEME)+1 == len(config.THEMES):
            next_index = 0
        else:
            next_index = config.THEMES.index(config.THEME)+1

        theme = config.THEMES[next_index]
        config.THEME = theme
        new_label = 'Seleccionar Tema: ' + theme
        self.menu.change_text(2, new_label)

    def toggle_tips(self):
        config.show_tips = not config.show_tips
        self.update_show_tips_label()

    def update_show_tips_label(self):
        if config.show_tips:
            new_label = "Mostrar consejos: SI"
        else:
            new_label = "Mostrar consejos: NO"

        self.menu.change_text(1, new_label)
