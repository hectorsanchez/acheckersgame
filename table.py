# -*- encoding: utf-8 -*-
import pygame
import config
import common
from checker import Checker

class Table:

    def __init__(self, group, theme):
        self.group = group
        self.image = common.load_image('table.png', theme)
        self._create_collision_rects()
        self._create_checkers()

        # setea las posiciones iniciales de las
        # pieces a ocupado
        self.positions = {}
        pos_player1 = range(1, 13)
        pos_player2 = range(21, 33)
        for x, y in zip(pos_player1, pos_player2):
            self.positions[x] = True
            self.positions[y] = True
        #print self.positions


    def square_occupied(self, position):
        """Devuelve si la posicion esta ocupada o no"""
        return self.positions.get(position, False)


    def squares_possible(self, checker, player):
        """Devuelve los casilleros posibles para el jugador player y
        la pieza checker"""
        increment_pos = self.increment_pos(checker, player)
        result = []
        for pos in increment_pos:
            adjacent_position = checker.position + pos
            if not self.square_occupied(adjacent_position):
                result.append(adjacent_position)
        print "Posicion de la pieza:", checker.position
        print "Posibles movimientos:", result
        return result


    def wall_left(self, checker):
        return checker.position in self.wall_left_positions

    def wall_right(self, checker):
        return checker.position in self.wall_right_positions

    def forced_jump(self, player, pieces):
        """Indica si ese jugador esta obligado a comer"""
        increment_pos = self.increment_pos(player)
        for piece in pieces:
            if piece.player == player:
                for pos in self.increment_pos:
                    adjacent_position = checker.position + pos
                    if square_occupied(adjacent_position):
                        pass


    def increment_pos(self, checker, player):
        """Devuelve la lista a sumar a la posicion actual de la ficha
        del jugador para obtener las posiciones adyacentes"""
        wall_left_positions = {29:True, 21:True, 13:True, 5:True}
        wall_right_positions = {28:True, 20:True, 12:True, 4:True}
        if player == 1:
            if wall_left_positions.get(checker.position, False) \
            or wall_right_positions.get(checker.position, False):
                print "esta a la izquierda o derecha"
                return [4]
            if not self.even_column(checker):
                return [3, 4]
            return [4, 5]
        else:
            if wall_left_positions.get(checker.position, False) \
            or wall_right_positions.get(checker.position, False):
                print "esta a la izquierda o derecha"
                return [-4]
            elif self.even_column(checker):
                return [-3, -4]
            else:
                return [-4, -5]

    def even_column(self, checker):
        return checker.position in [1,2,3,4,9,10,11,12,17,18,19,20,25,26,27,28]

    def change_theme(self, theme):
        self.image = common.load_image('table.png', theme)

        for checker in self.checkers:
            checker.change_theme(theme)

    def draw(self, destination):
        destination.blit(self.image, (0, 0))

    def get_checker_at(self, (x, y)):
        """Devuelve el sprite que se encuentra en la posicion en la que se
        hizo click con el mouse"""
        for sprite in self.group.sprites():
            if sprite.rect.x < x < (sprite.rect.x + sprite.rect.w):
                if sprite.rect.y < y < (sprite.rect.y + sprite.rect.h):
                    return sprite

    def get_index_at(self, (x, y)):
        """Devuelve el indice de tablero mas cercano a la posición (x,y). 

        Puede devolver None si no está cerca de ningún elemento."""
        i = 1

        for rect in self.rects:
            if rect.collidepoint(x, y):
                return i
            else:
                i += 1
        else:
            return None

    def _create_collision_rects(self):
        """Genera rectángulos que representan las zonas de tablero."""

        #TODO: tal vez esta estructura pueda reemplazar a PIECE_POSITIONS
        #      en un futuro.

        self.rects = [pygame.Rect(x, y, 50, 50)
                    for x, y in config.PIECE_POSITIONS.values()]

    def _create_checkers(self):
        self.checkers = []

        for position in xrange(1, 13):
            c = Checker(1, position, self)
            self.checkers.append(c)

        for position in xrange(21, 33):
            c = Checker(2, position, self)
            self.checkers.append(c)

        self.group.add(self.checkers)
