# -*- encoding: utf-8 -*-
""" Modulo para manejar la tabla """
import pygame
import config
import common

from checker import Checker
from king import King

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

    def __init__(self, gui, group, theme, turn):
        """Inicializador de la clase"""
        self.gui = gui
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

    def squares_adyacent_for_king(self, checker):
        """Devuelve los casilleros adyacentes para una dama"""
        r, c = checker.position
        adyacentes = []

        # intenta obtener las 4 diagonales completas.
        for x in range(1, 20):
            if (r+x,c-x) in match_position.values():
                adyacentes.append((r+x,c-x))
            if (r+x,c+x) in match_position.values():
                adyacentes.append((r+x,c+x))
            if (r-x,c-x) in match_position.values():
                adyacentes.append((r-x,c-x))
            if (r-x,c+x) in match_position.values():
                adyacentes.append((r-x,c+x))

        return adyacentes

    def _get_path_for_king(self, position, player, next_squares, 
            must_jump_to_continue=False, last=[]):
        """ Retorna todos los caminos posibles para una ficha """

        # El formato de la lista next_squares es de la forma
        #
        #   [(6, 1), (6, 3), (5, 0), (5, 4), (4, 5), (3, 6), (2, 7)]
        #
        # donde cada tupla indica casilleros donde puede pisar
        # la dama.

        if player == 1:
            opponent_player = 2
        else:
            opponent_player = 1


        # Por cada posicion destino:
        for square in next_squares:

            # full_path es una lista de todas las posiciones
            # por las que puede pasar la ficha.
            full_path = self.get_route_to(position, square)

            # Quita la primer casilla porque es la que esta usando
            # la dama en ese momento.
            full_path = full_path[1:]

            # Luego, el camino sirve si se producen dos condiciones
            #
            #  - que el ultimo casillero en donde puede pisar este vacio.
            #  - que en el camino existan 1 o ninguna pieza enemiga.

            # Se asegura de analizar un camino existente.
            if len(full_path) < 1:
                continue

            # Se asegura de no pasar por arriba de una pieza de su
            # equipo.
            if self.count_pieces_of_player(player, full_path) > 0:
                print "-- se descarta", full_path, "por tener fichas de su equipo ahi."
                continue

            if self.count_pieces_of_player(player, full_path) > 0:
                print "-- se descarta", full_path, "por tener fichas de su equipo ahi."
                continue

            if self.count_pieces_of_player(opponent_player, full_path) > 1:
                print "-- se descarta", full_path, "porque hay mas de un opoente ahi."
                continue

            if self.square_occupied(full_path[-1]):
                print "-- se descarta", full_path, "porque esta ocupada la ultima pos."
                continue

            yield full_path


    def count_pieces_of_player(self, player, path):
        "retorna la cantidad de piezas del jugador indicado por parametros."

        count = 0

        for x in path:
            checker = self.get_checker_at_position(x)

            if checker and checker.player == player:
                count += 1

        return count

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

        if position[0] < square[0]:
            return (r+2, c+dt)
        else:
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

        self._create_path_dictionary()

        print "En 'change_turn' se genera este diccionario:"

        for k, v in self._path_dictionary.items():
            print "\t", k, ":", v

        # Si está activada la opcion de mostrar consejos
        # le dice al jugador que piezas puede mover.
        if config.show_tips:
            self.blink_checkers_that_can_move()


    def _create_path_dictionary(self):
        all_checkers = self._get_all_checkers_from_player(self.player_move)

        print "all", all_checkers

        # Toma todas las piezas y genera un lista con fichas y los caminos
        # que puede realizar.
        all_paths = [(checker, self._get_best_path_for_a_checker(checker)) 
                        for checker in all_checkers]

        # filtra la lista para que solo esten las fichas que se pueden mover.
        all_paths = self._filter_only_the_best_paths(all_paths)
        self._path_dictionary = dict(all_paths)

        import pprint
        pprint.pprint(all_paths)

    def blink_checkers_that_can_move(self):
        """Hace destellar las piezas que se pueden mover en este turno."""
        for checker in self._path_dictionary.keys():
            if checker.can_drag:
                checker.do_blink()

    def _lenght_of_best_path(self, paths):
        """Determina los caminos mas largos para una pieza."""
        lenghts = [len(path) for path in paths]

        if lenghts:
            return lenghts[0]
        else:
            return 0

    def filter_only_path_checker(self, checker_mov):
        """ Elimina los caminos de otra ficha """
        for checker in self._path_dictionary.keys():
            if checker_mov != checker:
                del(self._path_dictionary[checker])

    def _filter_only_the_best_paths(self, paths_list):
        """Filtra los mejores movimientos de las piezas.

        Este filtro se utiliza para generar un diccionario de los mejores
        movimientos permitidos."""

        long_paths = [self._lenght_of_best_path(paths) for checker, paths in paths_list]


        #Este checkeo lo tenemos que hacer porque sino cuando un jugador gana
        #se produce una exepcion
        if long_paths:
            best_lenght = max(long_paths)
        else:
            longest_paths = 0


        longest_paths = [(ckecker, path) for ckecker, path in paths_list
                if self._lenght_of_best_path(path) == best_lenght]

        return longest_paths

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
        
        table =  \
"""
 x x x x
x x x x 
 x x x x

     -
  -   -
 - x - -
-   - -
"""


        for x in xrange(8):
            self.positions.append([None, None, None, None, None, None, None, None])

        for row, line in enumerate(table.split('\n')):
            row = row - 1

            for col, item in enumerate(line):
        
                if item in ['-', 'x']:

                    if item == '-':
                        checker = Checker(2, (row,col), self)
                    elif item == 'x':
                        checker = Checker(1, (row,col), self)

                    self.positions[row][col] = checker
                    self.checkers.append(checker)

        self.group.add(self.checkers)


    def _get_best_path_for_a_checker(self, checker):
        """Obtiene el mejor camino para una ficha."""
        if checker.king:
            next_squares = self.squares_adyacent_for_king(checker)
            path_list = list(self._get_path_for_king(checker.position, checker.player, next_squares))
        else:
            next_squares = self.squares_adyacent(checker)
            path_list = list(self._get_path(checker.position, checker.player, next_squares))

        if path_list == []:
            path_list = [[]]


        # La seleccion de mejores caminos se deshabilita para las
        # damas, porque tienen mas libertad que las damas.
        if checker.king:
            return path_list


        # intenta quedarse solamente con los mejores caminos
        # para recorrer.
        try:
            best_length = max([len(path) for path in path_list])
        except ValueError:
            best_path = [[]]

        best_path = [path for path in path_list if len(path) == best_length]
        return best_path

    def _get_all_checkers_from_player(self, player):
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

    def _get_path(self, position, player, next_squares, must_jump_to_continue=False, last=[]):
        """ Retorna todos los caminos posibles para una ficha """
        # evalua cada uno de los posibles cuadrados a pisar.
        #print "Proximos casilleros:", next_squares

        for square in next_squares:
            # hace la primer busqueda sin comer
            if not must_jump_to_continue and not self.square_occupied(square):
                #print "\ten un primer movimiento se puede pisar en", square
                yield last + [square]
            elif self.square_occupied_by_oponent(square, player):
                #print "\tcomo", square, "esta ocupada por un rival, se busca saltarla"

                possible_destiny_square = self.get_possible_next_square_by_position(square, 
                        player, position)
                #print "\t si la salto tendría que pisar en", possible_destiny_square

                if (not self.square_occupied(possible_destiny_square) and \
                        possible_destiny_square in match_position.values()):
                    #print "\t  y esta libre, osea que puedo comer."
                    yield last + [square, possible_destiny_square]

                    #print "\t   pero luego de comer intento seguir desde la", possible_destiny_square

                    new_pos = possible_destiny_square
                    possible_next_squares = self.squares_adyacent_by_position(new_pos, player)

                    # Obtiene los siguientes movimientos, pero solo buscando
                    # aquellos que comerán una ficha.
                    new_paths = self._get_path(new_pos, player, possible_next_squares, True, [square, possible_destiny_square])

                    for path in new_paths:
                        yield path
                else:
                    pass
                    #print "\tpero como está ocupada se descarta el camino."

    def are_checker_in_path(self, checker):
        return self._path_dictionary.has_key(checker)

    def remove_checker_at(self, (row, column)):
        checker = self.get_checker_at_position((row, column))

        if not checker:
            raise ValueError("There is no checker in this position.")

        self.positions[row][column] = None
        checker.kill()
        self.checkers.remove(checker)

    def can_move_to_this_position(self, checker, position):
        """Informa si se puede mover una ficha a una determinada posición."""

        if not self.are_checker_in_path(checker):
            return False

        paths = self._path_dictionary[checker]

        for path in paths:
            es_impar = len(path) % 2 == 1

            print 'paths', paths

            if es_impar:
                if path[0] == position:
                    return True
            else:
                if path[1] == position:
                    return True

        return False

    def do_this_checker_motion(self, checker, destination):
        "Dá la orden de mover la pieza a un camino del path ya verificado."

        if checker.king:
            self.do_this_checker_king_motion(checker, destination)
        else:
            self.do_this_checker_normal_motion(checker, destination)


    def do_this_checker_king_motion(self, checker, destination):
        paths = self._path_dictionary[checker]
        selected_path = None
        eat_any = False

        # Selecciona el path que el usuario va a utilizar.
        for p in paths:
            if p[-1] == destination:
                selected_path = p

        # Elimina todas las fichas que se crucen en su camino.
        # Si come alguna lo guarda en una variable 'eat_any'.
        for pos in selected_path:
            if self.square_occupied(pos):
                print "Borrando pieza"
                self.remove_checker_at(pos)
                eat_any = True

        print "CONCLUSION!!!! he comido:", eat_any

        if eat_any:
            # Si ha comido calcula nuevamente los caminos que puede
            # hacer con esa ficha.
            self._create_path_dictionary()
        else:
            self._path_dictionary[checker] = [None]


    def do_this_checker_normal_motion(self, checker, destination):
        "Realiza el movimiento si la ficha es normal."
        #TODO ver si hay algo que hace esto

        paths = self._path_dictionary[checker]
        es_impar = len(paths[0]) % 2 == 1

        if es_impar:
            path_selected = [p for p in paths if destination == p[0]]
        else:
            path_selected = [p for p in paths if destination == p[1]]
            self.remove_checker_at(path_selected[0][0])

        self._path_dictionary[checker] = [path[2:] for path in path_selected]

    def check_end_path(self, checker):
        """ Verifica si tengo que seguir haciendo movimientos
        en base al camino """

        #verifico el largo del camino
        if self._path_dictionary[checker][0]:
            return False
        else:
            return True

    def move_this_checker_to(self, checker, destination_index, interpolate=False):
        self.do_this_checker_motion(checker, destination_index)
        self.move(checker.position, destination_index)
        checker.set_position(destination_index, interpolate)

        if self.check_end_path(checker):
            if (checker.must_crown()):
                self.convert_to_king(destination_index)
            self.change_turn()

    def convert_to_king(self, position):
        """Convierte una ficha normal en dama."""
        checker = self.get_checker_at_position(position)

        new_king = King(checker.player, checker.position, self)
        self.remove_checker_at(checker.position)

        row, column = checker.position
        self.positions[row][column] = new_king
        self.checkers.append(new_king)
        self.group.add(new_king)
        self.gui.add(new_king)
        self.group.set_mouse_on_top()
    
    def get_route_to(self, position, square):
        "Retorna la ruta completa desde una posición hasta otra."
        path = []
        
        x, y = position
        to_x, to_y = square

        x_range = common.full_range(x, to_x)
        y_range = common.full_range(y, to_y)

        return zip(x_range, y_range)





#print get_route_to((7,2), (5,0))
#print get_route_to((7,2), (5,4))
#print get_route_to((6,3), (5,4))
#print get_route_to((6,3), (7,2))
