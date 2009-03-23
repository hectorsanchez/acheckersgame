# -*- encoding: utf-8 -*-
"""Modulo para manejo de fichas reina"""
from checker import Checker
import common
from config import *

class King(Checker):
    """Representa una pieza reina del juego.

    Realiza un comportamiento similar a Checker, solo que las
    finas dama pueden avanzar varios casilleros a la vez.
    """

    def __init__(self, player, initial_position, table):
        Checker.__init__(self, player, initial_position, table)
        self._load_images(player, THEME)
        self.quality = 10

    def _load_images(self, player, theme):
        """Carga todas las imagenes del tema"""
        prefix = "p%d_"% player
        names =  ['normal', 'over', 'drag']
        filenames = [prefix + name + "_king" + '.png' for name in names]
        self.images = [common.load_image(name, theme) for name in filenames]

    def must_crown(self):
        """La dama nunca debe coronar."""
        return False
