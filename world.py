import pygame
import gui
from table import Table
import common
from config import *
import os

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
        self.group = pygame.sprite.OrderedUpdates()
        pygame.display.set_caption(WINDOW_TITLE)

        self._create_ui()

        self.table = Table(self.group, THEME, self.turn)

        self.gui = gui.Gui(self.group.sprites())
        self.mouse = gui.Mouse(self.gui)
        self.group.add(self.mouse)

        self.background = self.screen.convert()
        self.change_theme(THEME)

    def _create_font_system(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 25)

    def loop(self):

        quit = False

        while not quit:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit = True
                elif e.type in common.MOUSE_EVENTS:
                    self.mouse.send_event(e)
                elif e.type == pygame.KEYDOWN:
                    if e.key in [pygame.K_ESCAPE, pygame.K_q]:
                        quit = True
                    elif e.key == pygame.K_F3:
                        pygame.display.toggle_fullscreen()
                        self.mouse.visible = True

            self.clock.tick(60)
            self.group.update()
            self._update_view()

    def _update_view(self):
        self.group.clear(self.screen, self.background)
        pygame.display.update(self.group.draw(self.screen))

    def _create_ui(self):
        b1 = gui.Button("Theme: classic", self.font, 500, 45, self.on_classic__clicked)
        b2 = gui.Button("Theme: beach", self.font, 500, 100, self.on_beach__clicked)
        self.group.add(b1, b2)

        # genera el visor de turnos
        self.turn = gui.Turn()
        self.group.add(self.turn)

    def on_classic__clicked(self):
        self.change_theme("classic")

    def on_beach__clicked(self):
        self.change_theme("beach")

    def change_theme(self, theme):
        THEME = theme
        self.update_view(THEME)

    def update_view(self, THEME):
        self.table.change_theme(THEME)
        self.table.draw(self.background)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
