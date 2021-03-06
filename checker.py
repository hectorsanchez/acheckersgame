# -*- encoding: utf-8 -*-
"""Modulo para manejo de fichas"""
import pygame
from pygame.sprite import Sprite
import config
from common import load_image
import states

NORMAL, OVER, DRAG = 0, 1, 2

class Checker(Sprite):
    """Representa una pieza del juego.

    Interactúa con el objeto Mouse para realizar cambios de posición, e
    interactúa con el objeto Table para conocer donde puede ocupar
    posiciones dentro del tablero."""

    def __init__(self, player, initial_position, table):
        Sprite.__init__(self)
        self.player = player
        self._load_images(player)
        self.show_image(NORMAL)
        self.rect = self.image.get_rect()
        self._move(initial_position)
        self.can_drag = True
        self.can_click = False
        self.table = table
        self.change_state(states.Starting(self, initial_position, player))
        self.quality = 5
        self.king = False

    def update(self):
        """Actualiza el estado de la ficha"""
        self.state.update()

    def change_state(self, new_state):
        """Cambia el estado de la ficha"""
        self.state = new_state

    def _move(self, position):
        """Mueve la ficha a la posicion indicada por position.
        Las posiciones corresponden a la fila y columna de la matriz"""
        self.position = position
        self.rect.x, self.rect.y = config.PIECE_POSITIONS[position]

    def _load_images(self, player):
        """Carga todas las imagenes del tema"""
        prefix = "p%d_"% player
        names =  ['normal', 'over', 'drag']
        filenames = [prefix + name + '.png' for name in names]
        self.images = [load_image(name) for name in filenames]

    def show_image(self, index):
        """Asigna la nueva imagen a la ficha"""
        self.image = self.images[index]

    def on_mouse_move(self):
        """Se esta moviendo el mouse"""
        self.show_image(OVER)

    def on_mouse_leave(self):
        """Se suelta el mouse"""
        self.show_image(NORMAL)

    def on_mouse_drag_start(self):
        """Comienza a realizar el drag con el mouse"""
        self.last_rect = pygame.Rect(self.rect)
        self.show_image(DRAG)
        if self.table.are_checker_in_path(self):
            self.table.filter_only_path_checker(self)

    def on_mouse_drag(self, pos_dx, pos_dy):
        """Realizando el drag con el mouse"""
        self.rect.move_ip(pos_dx, pos_dy)

    def on_mouse_drag_end(self):
        """Finaliza el drag con el mouse."""
        from_x, from_y = self.last_rect.x, self.last_rect.y
        destination_index = self.table.get_index_at(self.rect.center)

        if self.table.can_move_to_this_position(self, destination_index):
            self.table.move_this_checker_to(self, destination_index)
        else:
            self.change_state(states.Moving(self, from_x, from_y))

    def set_position(self, position, interpolate=False):
        to_x, to_y = config.PIECE_POSITIONS[position]

        if interpolate:
            self.change_state(states.Moving(self, to_x, to_y))
            pass
        else:
            self.rect.topleft = to_x, to_y

        # TODO: Contemplar el caso de 'inmediate' == False.
        self.position = position

    def can_drag_me_actual_player(self):
        """ Chequea si el usuario de turno puede hacer drag en la ficha"""
        return self.table.my_turn(self.player)

    def __repr__(self):
        return "<Checker at %s>" %str(self.position)

    def are_in_path_dictionary(self):
        """Consulta si esta ficha esta en el diccionario
        de los movimientos posibles."""
        return self.table.are_checker_in_path(self)

    def kill(self):
        self.change_state(states.WhenDie(self))

    def remove_from_groups(self):
        Sprite.kill(self)

    def do_blink(self):
        self.change_state(states.Blinking(self))

    def must_crown(self):
        if self.player == 1:
            return self.position[0] == 7
        else:
            return self.position[0] == 0
