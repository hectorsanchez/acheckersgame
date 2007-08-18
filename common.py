import pygame

def load_image(file, theme):
    image = pygame.image.load('ima/%s/%s' %(theme, file))
    return image
