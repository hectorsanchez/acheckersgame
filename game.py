# -*- encoding: utf-8 -*-
import group
import gui
from table import Table
from config import *
import scene
import pygame

class Game(scene.Scene):

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.group = group.Group()
        self.theme = THEME
        self._create_ui()

        self.gui = gui.Gui()
        self.table = Table(self.gui, self.group, self.theme, self.turn)
        self.gui.add_widgets(self.group.sprites())

        self.mouse = gui.Mouse(self.gui)
        self.group.add_mouse(self.mouse)

        self.background = world.screen.convert()
        self.change_theme(self.theme)

    def _create_ui(self):
        """Crea la interfaz del juego """
        label = "Theme: classic"
        #but1 = gui.Button(label, self.font, 500, 45, self.on_classic__clicked)
        label = "Theme: beach"
        #but2 = gui.Button(label, self.font, 500, 100, self.on_beach__clicked)
        #self.group.add(but1, but2)

        # genera el visor de turnos
        self.turn = gui.Turn()
        self.group.add(self.turn)

    def update(self):
        self.group.update()
        self._update_view()

    def draw(self, screen):
        pass

    def change_theme(self, theme):
        """ Cambio de thema """
        self.theme = theme
        self.update_view(self.theme)


    def update_view(self, theme):
        """ Actualiza la vista"""
        self.table.change_theme(theme)
        self.table.draw(self.background)
        self.world.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def _update_view(self):
        """ Actualiza la vista"""
        self.group.clear(self.world.screen, self.background)
        pygame.display.update(self.group.draw(self.world.screen))

