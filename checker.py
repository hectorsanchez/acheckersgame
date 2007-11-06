from pygame.sprite import Sprite

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
        self.position = position
        # FIXME: no es recomendable utilizar el nombre "list" para una variable
        # ya que estamos pisando la funcion built-in "list"
        list = [1, 2, 3, 4, 9, 10, 11, 12, 17, 18, 19, 20, 25, 26, 27, 28]

        if position in list:
            offset = 1
        else:
            offset = 2

        position = position * 2 - offset

        x, y = 9, 46

        dy = (position / 8) * 50
        dx = (position % 8) * 50

        self.rect.x = x + dx
        self.rect.y = y + dy
