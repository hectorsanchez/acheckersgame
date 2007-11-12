# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Group

class Gui(Group):
    """Administra todos los componentes de la interfaz.

    Gui recibe consultas y órdenes directamente desde el objeto
    Mouse."""

    def __init__(self, widgets=[]):
        Group.__init__(self)

        for x in widgets:
            self.add(x)

        self.last_widget_bellow_mouse = None

    def on_mouse_move(self, x, y):
        """Avisa a todos los componentes el movimiento del mouse, retorna
        aquel componente que se encuentra debajo del mouse o None."""

        for s in self.sprites():
            if s.rect.collidepoint(x, y):
                s.on_mouse_move()

                if s != self.last_widget_bellow_mouse:
                    self._leave_last_widget()

                self.last_widget_bellow_mouse = s
                return s
        else:
            self._leave_last_widget()

    def _leave_last_widget(self):
        if self.last_widget_bellow_mouse:
            self.last_widget_bellow_mouse.on_mouse_leave()
            self.last_widget_bellow_mouse = None



if __name__ == '__main__':
    from mouse import Mouse
    gui = Gui()
    mouse = Mouse(gui)


