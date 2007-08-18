import pygame
import mouse
from checker import Checker
from common import *

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
        list =[1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,
        35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]
        x = x - 9
        y = y - 46
        i = y / 50
        j = x /50
        pos = i * 8 + j
        if pos not in list:
            return None
        pos = pos / 2 + 1
        for c in self.group.sprites():
            if pos == c.position:
                print "hay una pieza --  %d" %(pos)
                return c

    def _update_view(self):
        self.group.clear(self.screen, self.background)
        pygame.display.update(self.group.draw(self.screen))
        self.clock.tick(60)
