# -*- encoding: utf-8 -*-
import group
import gui
from table import Table
from config import *
import scene
import pygame
import common

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


    def on_event(self, event):
        if event.type in common.MOUSE_EVENTS:
            self.mouse.send_event(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.table.blink_checkers_that_can_move()
            elif event.key == pygame.K_u:
                #for DEBUG
                mov = ask(self.screen, "Convertir a Dama")
                regular = re.compile(r'^([0-7]),([0-7])$')
                if not regular.match(mov):
                    message = 'Fichas ' + mov + ' invalida'
                    self.update_view(self.theme)
                else:
                    r, _, c = tuple(mov)
                    try:
                        if self.table.square_occupied((int(r),int(c))):
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
                regular = re.compile(r'^([0-7]),([0-7])$')
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

                regular = re.compile(r'(1|2)?(\d|3[0-2]),(\d|3[0-2])')
                if regular.match(mov):
                    origen, destino = mov.split(",")
                    position_ori = self.table.bind_position(int(origen))
                    position_dest = self.table.bind_position(int(destino))

                    checker_ori = self.table.get_checker_at_position(position_ori)

                    # verificar que este dentro del diccionario

                    if self.table.can_move_to_this_position(checker_ori, position_dest):
                        # realizar el movimiento de la ficha
                        self.table.move_this_checker_to(checker_ori, position_dest, True)

                self.update_view(self.theme)
