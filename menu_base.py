# -*- encoding: utf-8 -*-
from pygame.locals import *
import pygame
from  config import *

class MenuBase:

    def __init__(self, options, initial_position):
        self.opciones = options
        self.colorEncendido = (255,255,255)
        self.colorApagado = (0,0,0)
        self.seleccionado = initial_position
        self.font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)

        self.create_image_options()

    def create_image_options(self):
        self.imagenes = []
        for texto, funcion in self.opciones:
            imagen0 = self.font.render(texto, 1, self.colorApagado)
            imagen1 = self.font.render(texto, 1, self.colorEncendido)
            self.imagenes.append( [imagen0, imagen1] )

    def change_text(self, item_index, new_text):
        "Cambia el texto de una de las opciones del menu."
        imagen0 = self.font.render(new_text, 1, self.colorApagado)
        imagen1 = self.font.render(new_text, 1, self.colorEncendido)

        self.imagenes[item_index] = [imagen0, imagen1]


    def draw(self, screen, fondo):
        altura_de_opcion = 200
        interlineado = 40
        x = 250
        y = 80

        # Limpia las zonas que se van a dibujar con el fondo
        # de pantalla.
        for indice, imagenes in enumerate(self.imagenes):
            posicion = (x, y + altura_de_opcion * indice)
            area = imagenes[0].get_rect(topleft=posicion)
            screen.blit(fondo, posicion, area)

        # Dibuja las opciones sobre la pantalla.
        # pintado de otro color la opcion seleccionada.
        for indice, imagenes in enumerate(self.imagenes):
            if indice == self.seleccionado:
                imagen = imagenes[1]
            else:
                imagen = imagenes[0]

            posicion = (x, y + altura_de_opcion + interlineado * indice)
            screen.blit(imagen, posicion)


    def on_key_down(self, e):
        if e.key in [K_UP, K_KP8]:
            self.moverSeleccion(-1)
        elif e.key in [K_DOWN, K_KP2]:
            self.moverSeleccion(1)
        elif e.key in [K_RETURN, K_KP7, K_KP1, K_KP3, K_KP9]:
            #self.sonido_menu.play()
            titulo, funcion = self.opciones[self.seleccionado]
            funcion()

    def moverSeleccion(self, direccion ):
        self.seleccionado += direccion
        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > len(self.opciones) - 1:
            self.seleccionado = len(self.opciones) - 1
        #self.sonido_menu.play()
