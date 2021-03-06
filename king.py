"""Modulo para manejo de fichas reina"""
from checker import Checker
import common
import config

class King(Checker):
    """Representa una pieza reina del juego.

    Realiza un comportamiento similar a Checker, solo que las
    finas dama pueden avanzar varios casilleros a la vez.
    """

    def __init__(self, player, initial_position, table):
        Checker.__init__(self, player, initial_position, table)
        self._load_images(player)
        self.quality = 10
        self.king = True

    def _load_images(self, player):
        """Carga todas las imagenes del tema"""
        prefix = "p%d_"% player
        names =  ['normal', 'over', 'drag']
        filenames = [prefix + name + "_king" + '.png' for name in names]
        self.images = [common.load_image(name) for name in filenames]

    def must_crown(self):
        """La dama nunca debe coronar."""
        return False

    def __repr__(self):
        return "<King at %s>" %str(self.position)
