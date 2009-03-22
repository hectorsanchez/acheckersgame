# -*- encoding: utf-8 -*-
""" Modulo para manejar la tabla """
import pygame
import config
import common

from checker import Checker

from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()
#ipshell() # this call anywhere in your program will start IPython

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

class Table(object):
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
        adyacentes = []
        if checker.player == 1:
            # son blancas
            if (r+1,c-1) in match_position.values():
                adyacentes.append((r+1,c-1))
            if (r+1,c+1) in match_position.values():
                adyacentes.append((r+1,c+1))

        else:
            # son negras
            if (r-1,c-1) in match_position.values():
                adyacentes.append((r-1,c-1))
            if (r-1,c+1) in match_position.values():
                adyacentes.append((r-1,c+1))

        return adyacentes

    def squares_adyacent_by_position(self, position, player):
        """Devuelve los casilleros adyacentes a la pieza.

        Este método es similar a 'squares_adyacent', pero en
        lugar de recibir una ficha, recibe una posicion y
        un jugador. Se construye este metodo porque se quieren
        los cuadros adyacentes de una pieza no existente, una
        pieza que 'podría estar' ahí, en la celda indicada
        por 'position'."""

        r, c = position
        if player == 1:
            # son blancas
            return [(r+1,c-1), (r+1,c+1)]
        else:
            # son negras
            return [(r-1,c-1), (r-1,c+1)]

    def square_occupied(self, position):
        """Devuelve si la posicion esta ocupada o no"""
        checker = self.get_checker_at_position(position)

        if checker:
            return True
        else:
            return False

    def square_occupied_by_oponent(self, position, player=None):
        """Devuelve si la posicion esta ocupada por el otro jugador.

        Tener en cuenta que la celda podría estar ocupada por el mismo
        jugador, en cuyo caso devuelve false."""
        checker = self.get_checker_at_position(position)

        if player is None:
            player = self.player_move

        if checker and checker.player != player:
            return True
        else:
            return False

    def squares_adyacent_possibles(self, checker):
        """Devuelve los casilleros posibles para
        el jugador de la pieza checker"""
        result = []
        for adjacent_position in self.squares_adyacent(checker):
            if (not self.square_occupied(adjacent_position) and \
                    adjacent_position in match_position.values()):
                result.append(adjacent_position)

        return result

    def get_possible_next_square_by_position(self, square, player, position):
        """Devuelve el siguente casillero para una ficha que come.

        El argumento 'square' es la celda donde se comerá, player
        es el identificador del jugador que quiere comer y position
        es la posicion actual de la ficha que come.

        La necesidad de esta rutina surge porque se quiere calcular
        el movimiento imaginario de varias piezas, y los estados
        de posición futuros no se almacenan en objetos Checker."""

        r, c = position
        square_column = square[1]

        # determina el movimiento horizontal
        if square_column > c:
            dt = +2
        else:
            dt = -2

        if player == 1:
            # son blancas
            return (r+2, c+dt)
        else:
            # son negras
            return (r-2, c+dt)

    def checker_of_player(self, position, player):
        """Chequea si la ficha de la posicion es del jugador"""
        checker = self.get_checker_at_position(position)
        if checker.player == player:
            return True
        else:
            return False

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
            self.positions.append([None, None, None, None, None, None, None, None])

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

    def get_all_checkers_from_player(self, player):
        """Retorna una lista con todas las fichas de un player"""
        return [checker for checker in self.checkers if checker.player == player]

    def get_checker_at_position(self, (r, c)):
        """Retorna la ficha que se encuentra en la
        posicion de index"""
        try:
            return self.positions[r][c]
        except IndexError:
            return None

    def move(self, (rf, cf), (rt, ct)):
        """Hace un swap entre las dos posiciones en la matriz"""
        self.positions[rf][cf], self.positions[rt][ct] = \
            self.positions[rt][ct], self.positions[rf][cf]


    def get_path(self, position, player, next_squares, must_jump_to_continue=False, last=[]):
        """ Retorna todos los caminos posibles para una ficha """
        # evalua cada uno de los posibles cuadrados a pisar.
        print "Proximos casilleros:", next_squares

        for s in next_squares:
            # hace la primer busqueda sin comer
            if not must_jump_to_continue and not self.square_occupied(s):
                print "\ten un primer movimiento se puede pisar en", s
                yield last + [s]
            elif self.square_occupied_by_oponent(s, player):
                print "\tcomo", s, "esta ocupada por un rival, se busca saltarla"

                possible_destiny_square = self.get_possible_next_square_by_position(s, player, position)
                print "\t si la salto tendría que pisar en", possible_destiny_square

                if not self.square_occupied(possible_destiny_square) and possible_destiny_square in match_position.values():
                    print "\t  y esta libre, osea que puedo comer."
                    yield last + [s, possible_destiny_square]

                    print "\t   pero luego de comer intento seguir desde la", possible_destiny_square

                    new_pos = possible_destiny_square
                    possible_next_squares = self.squares_adyacent_by_position(new_pos, player)

                    # Obtiene los siguientes movimientos, pero solo buscando
                    # aquellos que comerán una ficha.
                    new_paths = self.get_path(new_pos, player, possible_next_squares, True, [s, possible_destiny_square])

                    for p in new_paths:
                        yield p
                else:
                    print "\tpero como está ocupada se descarta el camino."

