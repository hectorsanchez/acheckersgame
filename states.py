import common
from config import PIECE_POSITIONS

class Starting:

    def __init__(self, checker, position, player):
        self.checker = checker
        to_x, to_y = PIECE_POSITIONS[position]
        to = to_x, to_y

        checker.can_drag = False
        checker.rect.x = to_x
        checker.rect.y = -100 if player == 1 else 710
        self.moves = common.interpolate(checker.rect.topleft, to)

    def update(self):
        self.checker.image.set_alpha(100)
        try:
            self.checker.rect.topleft = self.moves.next()
        except StopIteration:
            self.checker.change_state(Normal(self.checker))


class Normal:

    def __init__(self, checker):
        self.checker = checker
        self.checker.can_drag = True

    def update(self):
        pass


class Moving:

    def __init__(self, checker, to_x, to_y):
        self.checker = checker
        to = to_x, to_y
        self.moves = common.interpolate(checker.rect.topleft, to)
        self.checker.can_drag = False
        
    def update(self):
        try:
            self.checker.rect.topleft = self.moves.next()
        except StopIteration:
            self.checker.change_state(Normal(self.checker))

