import pygame
from pygame.sprite import Sprite
from config import PIECE_POSITIONS, THEME
from common import load_image
from states import *

NORMAL, OVER, DRAG = 0, 1, 2

class Checker(Sprite):
    "Representa un pieza del juego."
    
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
        self.change_state(Starting(self, initial_position, player))

    def update(self):
        self.state.update()

    def change_state(self, new_state):
        self.state = new_state

    def _move(self, position):
        """Mueve la ficha a la posicion indicada por position. Las posiciones
        corresponden al numero en el tablero"""
        self.position = position
        self.rect.x, self.rect.y = PIECE_POSITIONS[position]

    def change_theme(self, theme):
        self._load_images(self.player, theme)
        self.show_image(NORMAL)

    def _load_images(self, player, theme):
        prefix = "p%d_" %player
        names =  ['normal', 'over', 'drag']
        filenames = [prefix + name + '.png' for name in names]
        self.images = [load_image(name, theme) for name in filenames]

    def show_image(self, index):
        self.image = self.images[index]

    def on_mouse_move(self):
        self.show_image(OVER)

    def on_mouse_leave(self):
        self.show_image(NORMAL)

    def on_mouse_drag_start(self):
        self.last_rect = pygame.Rect(self.rect)
        self.show_image(DRAG)
    
    def on_mouse_drag(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def on_mouse_drag_end(self):
        to_x, to_y = self.rect.x, self.rect.y
        from_x, from_y = self.last_rect.x, self.last_rect.y

        destination_index = self.table.get_index_at(self.rect.center)

        if destination_index and \
           self.table.my_turn(self.player) and \
           destination_index in self.table.squares_possible(self, self.player):
            self.table.change_turn()
            self.rect.topleft = PIECE_POSITIONS[destination_index]
            self.table.positions[self.position] = False
            self.table.positions[destination_index] = True
            self.position = destination_index
            #self.table.forced_jump(self.player)
            if self.table.crown(self, self.player):
                # llamar a la funcion de coronar
                print "Coronaste!"
        else:
            # regresa a su posicion inicial
            self.change_state(Moving(self, from_x, from_y))

    def can_drag_me_actual_player(self):
        return self.table.my_turn(self.player)
