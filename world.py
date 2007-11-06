import pygame
import mouse
from checker import Checker
from common import *

import pdb

class World:
    
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Another Checkers Game - beta")

        self.theme = 'classic'

        self._create_checkers()
        self.background = load_image('table.png', self.theme)

        # REMOVE
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        # END REMOVE 


    def _create_checkers(self):
        self.group = pygame.sprite.RenderUpdates()

        p1 = load_image('p1.png', self.theme)
        p2 = load_image('p2.png', self.theme)

        # FIXME: a la variable "p" le pondria "position"
        for p in xrange(1, 13):
            c = Checker(1, p1, p)
            self.group.add(c)

        for p in xrange(21, 33):
            c = Checker(2, p2, p)
            self.group.add(c)


    def loop(self):

        quit = False
        
        while not quit:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit = True
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        quit = True
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    ficha = self._get_checker_at(pygame.mouse.get_pos())
                    if ficha:
                        print ficha.position
                        ficha._move(17)

            self.group.update()
            self._update_view()

    def _get_checker_at(self, (x,y)):
        """Devuelve el sprite que se encuentra en la posicion en la que se
        hizo click con el mouse"""
        for sprite in self.group.sprites():
            if sprite.rect.x < x < (sprite.rect.x + sprite.rect.w):
                if sprite.rect.y < y < (sprite.rect.y + sprite.rect.h):
                    return sprite

    
    def _update_view(self):
        self.group.clear(self.screen, self.background)
        pygame.display.update(self.group.draw(self.screen))
        self.clock.tick(60)
