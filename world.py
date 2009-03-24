""" Modulo para manejo del tablero """
import pygame
import gui
from table import Table
import common
from config import *
from common import ask
import os, re

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
        self.theme = THEME
        self._create_ui()


        self.gui = gui.Gui()
        self.table = Table(self.gui, self.group, self.theme, self.turn)
        self.gui.add_widgets(self.group.sprites())


        self.mouse = gui.Mouse(self.gui)
        self.group.add(self.mouse)

        self.background = self.screen.convert()
        self.change_theme(self.theme)

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
                elif event.type in common.MOUSE_EVENTS:
                    self.mouse.send_event(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        end_game = True
                    elif event.key == pygame.K_F3:
                        pygame.display.toggle_fullscreen()
                        self.mouse.visible = True
                    elif event.key == pygame.K_b:
                        self.table.blink_checkers_that_can_move()
                    elif event.key == pygame.K_u:
                        #for DEBUG
                        mov = ask(self.screen, "Convertir a Dama")
                        regular = re.compile(r'^(0|1|2|3|4|5|6|7),(0|1|2|3|4|5|6|7)$')
                        if not regular.match(mov):
                            message = 'Fichas ' + mov + ' invalida'
                            self.update_view(self.theme)
                        else:
                            r, _, c = tuple(mov)
                            try:
                                self.table.convert_to_king((int(r),int(c)))
                            except ValueError, mesg:
                                print mesg

                            finally:
                                self.update_view(self.theme)


                        #TODO: esto no esta bien, solo lo hago porque este metodo
                        #es para debug
                        self.table._create_path_dictionary()
                    elif event.key == pygame.K_d:
                        #for DEBUG
                        mov = ask(self.screen, "Borrar")
                        regular = re.compile(r'^(0|1|2|3|4|5|6|7),(0|1|2|3|4|5|6|7)$')
                        if not regular.match(mov):
                            message = 'Fichas ' + mov + ' invalida'
                            self.update_view(self.theme)
                        else:
                            r, _, c = tuple(mov)
                            try:
                                self.table.remove_checker_at((int(r),int(c)))
                            except ValueError, mesg:
                                print mesg

                            finally:
                                self.update_view(self.theme)

                        #TODO: esto no esta bien, solo lo hago porque este metodo
                        #es para debug
                        self.table._create_path_dictionary()

                    elif event.key == pygame.K_m:
                        mov = ask(self.screen, "Movimiento")
                        # validar el movimiento ingresado, el formato: 32,32
                        regular = re.compile(r'^((1|2)?[\d]|3(0|1|2)),((1|2)?[\d]|3(0|1|2))$')
                        if regular.match(mov):
                            origen, destino = mov.split(",")
                            position_ori = self.table.bind_position(int(origen))
                            position_dest = self.table.bind_position(int(destino))

                            checker_ori = self.table.get_checker_at_position(position_ori)

                            # verificar que este dentro del diccionario
                            if self.table.are_checker_in_path(checker_ori):
                                # realizar el movimiento de la ficha
                                self.table.move_this_checker_to(checker_ori, position_dest, True)

                        self.update_view(self.theme)

            self.clock.tick(60)
            self.group.update()
            self._update_view()

    def _update_view(self):
        """ Actualiza la vista"""
        self.group.clear(self.screen, self.background)
        pygame.display.update(self.group.draw(self.screen))

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

    def on_classic__clicked(self):
        """ Click en el boton estilo classic """
        self.theme = "classic"
        self.change_theme(self.theme)

    def on_beach__clicked(self):
        """ Click en el boton estilo beach """
        self.theme = "beach"
        self.change_theme(self.theme)

    def change_theme(self, theme):
        """ Cambio de thema """
        self.theme = theme
        self.update_view(self.theme)

    def update_view(self, theme):
        """ Actualiza la vista"""
        self.table.change_theme(theme)
        self.table.draw(self.background)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
