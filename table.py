# -*- encoding: utf-8 -*-
import pygame
import config
import common
from checker import Checker
from common import debug

match_position = {
     1:(0,1),  2:(0,3),  3:(0,5),  4:(0,7),
     5:(1,0),  6:(1,2),  7:(1,4),  8:(1,6),
     9:(2,1), 10:(2,3), 11:(2,5), 12:(2,7),
    13:(3,0), 14:(3,2), 15:(3,4), 16:(3,6),
    17:(4,1), 18:(4,3), 19:(4,5), 20:(4,7),
    21:(5,0), 22:(5,2), 23:(5,4), 24:(5,6),
    25:(6,1), 26:(6,3), 27:(6,5), 28:(6,7),
    29:(7,0), 30:(7,2), 31:(7,4), 32:(7,6),
}

class Table:
    """ Utilizada para el manejo de las piezas en el tablero y
    consultas sobre su estado"""

    def __init__(self, group, theme, turn):
        """Inicializador de la clase"""
        self.group = group
        self.image = common.load_image('table.png', theme)
        self._create_collision_rects()
        self._create_checkers()

        # boton que muestra el jugador en turno
        self.turn = turn

        # jugador al que le corresponde mover
        self.player_move = 2
        self.change_turn()

    def squares_adyacent(self, checker):
        """Devuelve los casilleros adyacentes a la pieza"""
        r, c = checker.position
        if checker.player == 1:
            # son blancas
            return [(r+1,c+1), (r+1,c-1)]
        else:
            # son negras
            return [(r-1,c+1), (r-1,c-1)]

    def square_occupied(self, position):
        """Devuelve si la posicion esta ocupada o no"""
        checker = self.get_checker_at_position(position)

        if checker:
            return True
        else:
            return False

    def square_occupied_by_oponent(self, position):
        """Devuelve si la posicion esta ocupada por el otro jugador.

        Tener en cuenta que la celda podría estar ocupada por el mismo
        jugador, en cuyo caso devuelve false."""
        checker = self.get_checker_at_position(position)

        if checker and checker.player != self.player_move:
            return True
        else:
            return False

    def squares_adyacent_possibles(self, checker):
        """Devuelve los casilleros posibles para el jugador de la pieza checker"""
        result = []
        for adjacent_position in self.squares_adyacent(checker):
            if not self.square_occupied(adjacent_position):
                result.append(adjacent_position)

        #debug("Posicion de la pieza:", checker.position)
        #debug("casillas adyacentes libres", result)
        return result

    def get_squares_path(self, checker):
        """Arma los caminos posibles para una ficha
        Lo hace en dos partes, caminos simples que serian los adyacentes libres y
        caminos complejos, los formados por comer fichas.
        """
        path = []

        fist_path = self.squares_adyacent(checker)

        # caminos simples, adyacentes libres
        for square in fist_path:
            if not self.square_occupied(square):
                path.append(square)  # primer nivel

        print "por camino simple queda:", path

        # caminos complejos, comiendo fichas
        second_path = set(fist_path) - set(path)
        second_path = list(second_path)
        print "falta evaluar:", second_path

        for square in second_path:
            # se analiza si la pieza a saltar es del otro
            # jugador.
            if self.square_occupied_by_oponent(square):
                print "en ese cuadrado hay un oponente"
                # se obtiene el cuadrado de tablero a donde
                # tendría que ir si como la pieza.
                next_square = self.get_next_square(checker, square)

                print "el siguiente cuadrado que podría pisar es:", next_square

                # se consulta si está libre ese casillero.
                if not self.square_occupied(next_square):
                    path.append([square, next_square])

                else:
                    # no esta libre el casillero, así que no
                    # puede comer la ficha que intentaba.
                    pass
        return path

    def get_next_square(self, checker, square):
        """Devuelve el siguiente casillero a una pieza si come
        a otra en square."""
        r, c = checker.position
        square_column = square[1]

        # determina el movimiento horizontal
        if square_column > c:
            dt = +2
        else:
            dt = -2

        if checker.player == 1:
            # son blancas
            return (r+2,c+dt)
        else:
            # son negras
            return (r-2,c+dt)


    def _jump_one_checker(self, checker):
        """Indica si la pieza puede comer al menos a una ficha"""
        row = 1 if checker.player == 1 else -1
        # self.squares_adyacent, devuelve primero para la derecha
        for adjacent, column in zip(self.squares_adyacent(checker), [1,-1]):
            #debug("esta pieza cae en", (adjacent[0]+row, adjacent[1]+column))
            if self.square_occupied(adjacent) \
                and not self.checker_of_player(adjacent, checker.player) \
                and not self.square_occupied((adjacent[0]+row, adjacent[1]+column)):
                    # se puede buscar el camino aca, que ya se sabe
                    #que esta pieza come
                    #self.search_jump_way(checker.position)
                    return True

    def forced_jump_all_checkers(self, player):
        """Devuelve una lista de piezas que pueden comer"""
        # lista de piezas que pueden comer
        jump_checkers = []
        # para cada una de las piezas del jugador en
        # en el turno
        for checker in self.checkers:
            if checker.player == player:
                if self._jump_one_checker(checker):
                    jump_checkers.append(checker)

        #debug("piezas que comen", jump_checkers)

        return jump_checkers

    def checker_forced_jump(self):
        """Devuelve la pieza que esta obligada a comer. El jugador
        debe mover esta pieza. Es la que tiene el camino con cantidad
        y calidad"""
        pass

    def checker_of_player(self, position, player):
        """Chequea si la ficha de la posicion es del jugador"""
        checker = self.get_checker_at_position(position)
        if checker.player == player:
            return True
        else:
            return False

    def crown(self, checker):
        """Devuelve verdadero si corono o falso en otro caso"""
        if checker.player == 1:
            # pregunta si la fila de la posicion es igual a 0
            return checker.position[0] == 0
        else:
            # pregunta si la fila de la posicion es igual a 7
            return checker.position[0] == 7

    def my_turn(self, player):
        """Indica si es el turno del jugador"""
        if player == self.player_move:
            return True
        else:
            return False

    def change_turn(self):
        """Cambia el jugador actual"""

        self.player_move = ((self.player_move + 2) % 2) + 1
        self.turn.change(self.player_move)

    def change_theme(self, theme):
        """Cambia el tema del juego completo"""
        self.image = common.load_image('table.png', theme)

        for checker in self.checkers:
            checker.change_theme(theme)

    def draw(self, destination):
        """Dibuja el tablero"""
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
        for rect in self.rects:
            if rect.collidepoint(x, y):
                for k, v in config.PIECE_POSITIONS.iteritems():
                    if v == (rect.x, rect.y):
                        return k

    def _create_collision_rects(self):
        """Genera rectángulos que representan las zonas de tablero."""
        #TODO: tal vez esta estructura pueda reemplazar a PIECE_POSITIONS
        #      en un futuro.
        self.rects = [pygame.Rect(x, y, 50, 50)
                    for x, y in config.PIECE_POSITIONS.values()]

    def bind_position(self, position):
        """Devuelve la fila y columna de la posicion position del tablero"""
        r, c = match_position[position]
        return r, c

    def _create_checkers(self):
        """Genera todas las fichas de ambos jugadores"""
        # lista de fichas
        self.checkers = []

        # creo la matriz de 8 x 8 inicializado a None
        # TODO: verificar si se puede mejorar esto
        self.positions = []
        for x in xrange(8):
            self.positions.append([None,None,None,None,None,None,None,None])

        for position in xrange(1, 13):
            r, c = self.bind_position(position)
            checker = Checker(1, (r,c), self)

            self.positions[r][c] = checker
            self.checkers.append(checker)

        for position in xrange(21, 33):
            r, c = self.bind_position(position)
            checker = Checker(2, (r,c), self)
            self.positions[r][c] = checker
            self.checkers.append(checker)

        self.group.add(self.checkers)

    def get_checker_at_position(self, (r, c)):
        """Retorna la ficha que se encuentra en la
        posicion de index"""
        try:
            return self.positions[r][c]
        except IndexError:
            return None

    def move(self, (rf, cf), (rt, ct)):
        """Hace un swap entre las dos posiciones en la matriz"""
        #debug("cambiando pieza")
        self.positions[rf][cf], self.positions[rt][ct] = \
            self.positions[rt][ct], self.positions[rf][cf]
