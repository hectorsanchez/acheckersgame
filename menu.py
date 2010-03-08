# -*- encoding: utf-8 -*-

import pygame
import scene
import sys
from  config import *

class Menu(scene.Scene):

    def __init__(self, world):

        self.opciones = opciones = [
            ("Jugar", self.jugar),
            ("Opciones", self.mostrar_opciones),
            ("Creditos", self.mostrar_creditos),
            ("Ayuda", self.mostrar_ayuda),
            ("Salir", self.salir_menu)
        ]
        self.world = world
        # self.sonido_menu = pygame.mixer.Sound(KEY_SOUND)
        self.font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        self.fondo = pygame.image.load(MENU_IMAGE).convert()
        self.colorEncendido = (200,0,0)
        self.colorApagado = (0,0,0)
        self.seleccionado = 0

    def update(self):
        self.imagenes = []
        for texto, funcion in self.opciones:
            imagen0 = self.font.render(texto, 1, self.colorApagado)
            imagen1 = self.font.render(texto, 1, self.colorEncendido)
            self.imagenes.append( [imagen0, imagen1] )

        pass

    def draw(self, screen):
        screen.blit(self.fondo, (0,0))
        self.dibujarOpciones(screen)
        pygame.display.flip()
        pass

    def on_event(self, event):
        pass

    def dibujarOpciones(self, screen):
        altura_de_opcion = 60
        x = 250
        y = 80

        for indice, imagenes in enumerate(self.imagenes):
            posicion = (x, y + altura_de_opcion * indice)
            area = imagenes[0].get_rect(topleft=posicion)
            screen.blit(self.fondo, posicion, area)

        for indice, imagenes in enumerate(self.imagenes):
            if indice == self.seleccionado:
                imagen = imagenes[1]
            else:
                imagen = imagenes[0]
            posicion = (x, y + altura_de_opcion * indice)
            screen.blit(imagen, posicion)

    def moverSeleccion(self, direccion):
        self.seleccionado += direccion
        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > len(self.opciones) - 1:
            self.seleccionado = len(self.opciones) - 1
        self.sonido_menu.play()
        self.dibujarOpciones()

    def jugar(self):
        pass

    def mostrar_opciones(self):
        pass

    def mostrar_creditos(self):
        pass

    def mostrar_ayuda(self):
        pass

    def salir_menu(self):
        pass

    def salir_del_programa(self):
        sys.exit(0)
