# -*- encoding: utf-8 -*-
import pygame
import config
import common
from checker import Checker

class Table:
    """ Utilizada para el manejo de las piezas en el tablero y consultas sobre su estado"""    
    
    # Posiciones de las fichas que se encuentran contra
    # las paredes. Utilizado para los moviemientos posibles
    # TODO: cambiar los diccionarios por listas
    column1_positions = {29:True, 21:True, 13:True, 5:True}
    column8_positions = {28:True, 20:True, 12:True, 4:True}

    column2_positions = [1,9,17,25]
    column7_positions = [8,16,24,32]

    # Casilleros en los que coronan los distintos jugadores
    crown_player1 = [29,30,31,32]
    crown_player2 = [1,2,3,4]

    # Casilleros en los que las columnas son pares
    squares_even_column = [1,2,3,4,9,10,11,12,17,18,19,20,25,26,27,28]

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

        # setea las posiciones iniciales de las
        # piezas ocupadas
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
        increment_pos = self.increment_pos(checker.position, player)
        result = []
        for pos in increment_pos:
            adjacent_position = checker.position + pos
            if not self.square_occupied(adjacent_position):
                result.append(adjacent_position)

        print "Posicion de la pieza:", checker.position
        print "Casillas adyacentes libres:", result
        return result


    def forced_jump(self, player):
        """Devuelve una lista de piezas que pueden comer"""
        #print "Comprobando para: ",
        #print "Blanco" if player == 1 else "Negro"
        # lista de piezas que pueden comer
        jump_checkers = []
        # para cada una de las piezas del jugador en
        # en el turno
        for checker in self.checkers:
            if checker.player == player:
                # obtiene los valores a sumar para adquirir los
                # adyacentes
                increment_pos = self.increment_pos(checker.position, player)
                for pos in increment_pos:
                    # compruebo que si estoy en la columna dos no puedo comer
                    # para la izquiera y si estoy en la columna 7 no puedo comer
                    # a la derecha
                    if checker.position in self.column2_positions:
                        if player == 1 and pos == 4:
                            continue
                        elif player == 2 and pos == -4:
                            continue
                    elif checker.position in self.column7_positions:
                        if player == 1 and pos == 4:
                            continue
                        elif player == 2 and pos == -4:
                            continue
                    adjacent_position = checker.position + pos
                    
                    # comprobar que no se vaya del tablero
                    #print "adj + pos", adjacent_position + pos
                    if not adjacent_position + pos in range(1,33):
                        continue
                        
                    # si el casillero adyacente esta ocupado y
                    # si no es una ficha del jugador en turno y
                    # si el siguiente adyacente esta libre
                    # esta ficha se agrega a la lista de fichas que
                    # pueden comer
                    if self.square_occupied(adjacent_position) \
                       and not self.checker_of_player(adjacent_position, player):
                            if not self.even_column(adjacent_position):
                                if not self.square_occupied(adjacent_position + pos - 1):
                                    jump_checkers.append(checker)
                            else:
                                if not self.square_occupied(adjacent_position + pos + 1):
                                    jump_checkers.append(checker)
        return jump_checkers

    def checker_of_player(self, position, player):
        """Chequea si la ficha de la posicion es del jugador"""
        for checker in self.checkers:
            if checker.position == position and \
               checker.player == player:
                return True
        return False

    def crown(self, checker, player):
        """Devuelve verdadero si corono o falso en otro caso"""
        if player == 1:
            return checker.position in self.crown_player1
        else:
            return checker.position in self.crown_player2

    def increment_pos(self, position, player):
        """Devuelve la lista a sumar a la posicion actual de la ficha
        del jugador para obtener las posiciones adyacentes"""
        if player == 1:
            if self.column1_positions.get(position, False) \
            or self.column8_positions.get(position, False):
                return [4]
            if not self.even_column(position):
                return [3, 4]
            return [4, 5]
        else:
            if self.column1_positions.get(position, False) \
            or self.column8_positions.get(position, False):
                return [-4]
            if self.even_column(position):
                return [-4, -3]
            else:
                return [-5, -4]

    def even_column(self, position):
        """Indica si la ficha esta en un columna par"""
        return position in self.squares_even_column

    def my_turn(self, player):
        """Indica si es el turno del jugador"""
        if player == self.player_move:
            return True
        else:
            return False

    def change_turn(self):
        """Cambia el jugador actual"""
        if self.player_move == 1:
            self.player_move = 2
        else:
            self.player_move = 1

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
        """Genera todas las fichas de ambos jugadores"""
        self.checkers = []

        for position in xrange(1, 13):
            c = Checker(1, position, self)
            self.checkers.append(c)

        for position in xrange(21, 33):
            c = Checker(2, position, self)
            self.checkers.append(c)

        self.group.add(self.checkers)
