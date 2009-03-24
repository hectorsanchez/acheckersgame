# -*- coding: utf-8 -*-
"""Administrador de GUI"""
from pygame.sprite import Group

class Gui(Group):
    """Administra todos los componentes de la interfaz.

    Gui recibe consultas y órdenes directamente desde el objeto
    Mouse."""

    def __init__(self):
        Group.__init__(self)

    def add_widgets(self, widgets):
        for wid in widgets:
            self.add(wid)

        self.last_widget_bellow_mouse = None


    def on_mouse_move(self, pos_x, pos_y):
        """Avisa a todos los componentes el movimiento del mouse, retorna
        aquel componente que se encuentra debajo del mouse o None."""

        for spri in self.sprites():
            if spri.rect.collidepoint(pos_x, pos_y):
                spri.on_mouse_move()

                if spri != self.last_widget_bellow_mouse:
                    self._leave_last_widget()

                self.last_widget_bellow_mouse = spri
                return spri
        else:
            self._leave_last_widget()

    def _leave_last_widget(self):
        """Dejar el ultimo widget"""
        if self.last_widget_bellow_mouse:
            self.last_widget_bellow_mouse.on_mouse_leave()
            self.last_widget_bellow_mouse = None

if __name__ == '__main__':
    from mouse import Mouse
    GUI = Gui()
    MOUSE = Mouse(GUI)


