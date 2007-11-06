from pygame.sprite import Sprite
from config import PIECE_POSITIONS

class Checker(Sprite):
    
    def __init__(self, player, image, initial_position):
        Sprite.__init__(self)
        self.player = player
        self.image = image
        self.rect = self.image.get_rect()
        self._move(initial_position)

    def update(self):
        pass

    def _move(self, position):
        """Mueve la ficha a la posicion indicada por position. Las posiciones
        corresponden al numero en el tablero"""
        self.position = position
        self.rect.x, self.rect.y = PIECE_POSITIONS[position]