""" Modulo para manejo del tablero """
import pygame
import gui
from table import Table
import common
from config import *
import os, re
import group

class World(object):
    """Representa el objeto principal del juego.

    Su responsabilidad es asegurar la velocidad constante del
    juego y propagar eventos."""

    def __init__(self, do_center_window):
        pygame.display.init()
        self._create_font_system()

        if do_center_window:
            os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(WINDOW_TITLE)

    def _create_font_system(self):
        """ Inicializa las fonts"""
        pygame.font.init()
        self.font = pygame.font.Font(None, 25)

    def loop(self):

        end_game = False

        while not end_game:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_game = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        end_game = True
                    elif event.key == pygame.K_F3:
                        pygame.display.toggle_fullscreen()
                        #self.mouse.visible = True
                        pass

                self.scene.on_event(event)

            self.clock.tick(60)
            self.scene.update()
            self.scene.draw(self.screen)

    def on_classic__clicked(self):
        """ Click en el boton estilo classic """
        self.theme = "classic"
        self.change_theme(self.theme)

    def on_beach__clicked(self):
        """ Click en el boton estilo beach """
        self.theme = "beach"
        self.change_theme(self.theme)

    def change_scene(self, scene):
        self.scene = scene
