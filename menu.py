# -*- encoding: utf-8 -*-

import pygame
import scene
import sys
from  config import *
from pygame.locals import *
import game
import options
import about
import help

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
        self.colorEncendido = (255,255,255)
        self.colorApagado = (0,0,0)
        self.seleccionado = 0
        self.screen = None

    def update(self):
        self.imagenes = []
        for texto, funcion in self.opciones:
            imagen0 = self.font.render(texto, 1, self.colorApagado)
            imagen1 = self.font.render(texto, 1, self.colorEncendido)
            self.imagenes.append( [imagen0, imagen1] )

        pass

    def draw(self, screen):
        self.screen = screen
        self.screen.blit(self.fondo, (0,0))
        self.dibujarOpciones()
        pygame.display.flip()
        pass

    def on_event(self, e):
        if e.type == KEYDOWN:
            if e.key in [K_UP, K_KP8]:
                self.moverSeleccion(-1)
            elif e.key in [K_DOWN, K_KP2]:
                self.moverSeleccion(1)
            elif e.key in [K_RETURN, K_KP7, K_KP1, K_KP3, K_KP9]:
                #self.sonido_menu.play()
                titulo, funcion = self.opciones[self.seleccionado]
                funcion()
        pass

    def dibujarOpciones(self):
        altura_de_opcion = 60
        x = 250
        y = 80

        for indice, imagenes in enumerate(self.imagenes):
            posicion = (x, y + altura_de_opcion * indice)
            area = imagenes[0].get_rect(topleft=posicion)
            self.screen.blit(self.fondo, posicion, area)

        for indice, imagenes in enumerate(self.imagenes):
            if indice == self.seleccionado:
                imagen = imagenes[1]
            else:
                imagen = imagenes[0]
            posicion = (x, y + altura_de_opcion * indice)
            self.screen.blit(imagen, posicion)

    def moverSeleccion(self, direccion ):
        self.seleccionado += direccion
        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > len(self.opciones) - 1:
            self.seleccionado = len(self.opciones) - 1
        #self.sonido_menu.play()
        self.dibujarOpciones()

    def jugar(self):
        new_scene = game.Game(self.world)
        self.world.change_scene(new_scene)

    def mostrar_opciones(self):
        new_scene = options.Options(self.world)
        self.world.change_scene(new_scene)

    def mostrar_creditos(self):
        new_scene = about.About(self.world)
        self.world.change_scene(new_scene)

    def mostrar_ayuda(self):
        new_scene = help.Help(self.world)
        self.world.change_scene(new_scene)

    def salir_menu(self):
        sys.exit(0)
