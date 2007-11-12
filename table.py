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
