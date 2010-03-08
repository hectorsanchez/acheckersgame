import pygame

class Group(pygame.sprite.OrderedUpdates):

    def __init__(self, *s):
        pygame.sprite.OrderedUpdates.__init__(self, *s)

    def add_mouse(self, mouse):
        self.mouse = mouse
        self.add(mouse)

    def set_mouse_on_top(self):
        self.remove(self.mouse)
        self.add(self.mouse)
