import pygame
import scene

class Intro(scene.Scene):

    def __init__(self, world):
        self.counter = 0
        self.world = world
        self.load_image()

    def draw(self, screen):
        screen.blit(self.fondo, (0, 0))
        pygame.display.flip()

        if self.counter > 60 * 4:
            self.go_to_next()
        else:
            self.counter += 1

    def on_event(self, event):
        if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
            self.go_to_next()
