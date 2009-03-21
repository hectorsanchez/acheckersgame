# -*- encoding: utf-8 -*-
"""Modulo para manejo de fichas"""
import pygame
from pygame.sprite import Sprite
from config import PIECE_POSITIONS, THEME
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
        self._load_images(player, THEME)
        self.show_image(NORMAL)
        self.rect = self.image.get_rect()
        self._move(initial_position)
        self.can_drag = True
        self.can_click = False
        self.table = table
        self.change_state(states.Starting(self, initial_position, player))


    def update(self):
        """Actualiza el estado de la ficha"""
        self.state.update()

    def change_state(self, new_state):
        """Cambia el estado de la ficha"""
        self.state = new_state

    def _move(self, position):
        """Mueve la ficha a la posicion indicada por position. Las posiciones
        corresponden a la fila y columna de la matriz"""
        self.position = position
        self.rect.x, self.rect.y = PIECE_POSITIONS[position]

    def change_theme(self, theme):
        """Cambia el tema de la ficha"""
        self._load_images(self.player, theme)
        self.show_image(NORMAL)

    def _load_images(self, player, theme):
        """Carga todas las imagenes del tema"""
        prefix = "p%d_"% player
        names =  ['normal', 'over', 'drag']
        filenames = [prefix + name + '.png' for name in names]
        self.images = [load_image(name, theme) for name in filenames]

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

        next_squares = self.table.squares_adyacent(self)
        paths = self.table.get_path(self.position, self.player, next_squares)
        print list(paths)

        # paths es el generador con todos los movimentos que
        # se pueden realizar.

        print "Caminos posibles para esta pieza:"
        for index, path in enumerate(paths):
            print " -> camino", index, ":", path
        print ""

    def on_mouse_drag(self, pos_dx, pos_dy):
        """Realizando el drag con el mouse"""
        self.rect.move_ip(pos_dx, pos_dy)

    def on_mouse_drag_end(self):
        """Finaliza el drag con el mouse"""
        from_x, from_y = self.last_rect.x, self.last_rect.y
        destination_index = self.table.get_index_at(self.rect.center)

        if (destination_index and \
           self.table.my_turn(self.player) and \
           destination_index in self.table.squares_adyacent_possibles(self)):
            self.table.change_turn()
            self.rect.topleft = PIECE_POSITIONS[destination_index]
            self.table.move(self.position, destination_index)
            self.position = destination_index
        else:
            # regresa a su posicion inicial
            self.change_state(states.Moving(self, from_x, from_y))

    def can_drag_me_actual_player(self):
        """ Chequea si el usuario de turno puede hacer drag en la ficha"""
        return self.table.my_turn(self.player)
