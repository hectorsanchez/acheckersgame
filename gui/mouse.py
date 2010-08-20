# -*- coding: utf-8 -*-
import common
import pygame
from pygame.sprite import Sprite
from pygame import MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, ACTIVEEVENT

class Mouse(Sprite):
    """Representa al puntero del mouse, conoce todos los elementos
    de la interfaz y administrar las funcionalidades de
    'arrastrar/soltar' y 'seleccionar'."""

    def __init__(self, gui):
        Sprite.__init__(self)
        self._load_images()
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.gui = gui
        self.visible = True
        self.widget_on_drag = None
        pygame.mouse.set_visible(False)

    def update(self):
        if not self.visible:
            self.image = self.hide

    def send_event(self, event):
        self.image = self.normal_image

        callbacks = {
                MOUSEMOTION: self.on_mouse_motion,
                MOUSEBUTTONUP: self.on_mouse_button_up,
                MOUSEBUTTONDOWN: self.on_mouse_button_down,
                ACTIVEEVENT: self.on_mouse_active,
                }

        callbacks[event.type](event)

    def on_mouse_button_up(self, event):
        if self.widget_on_drag:
            self.widget_on_drag.on_mouse_drag_end()
            self.widget_on_drag = None
        else:
            obj = self.gui.on_mouse_move(self.rect.x, self.rect.y)

            if obj and obj.can_click:
                obj.on_mouse_click()
                self.image = self.over_click_image

    def on_mouse_motion(self, event):
        self.rect.x, self.rect.y = event.pos

        if self.widget_on_drag:
            self.image = self.drag_image
            self._drag_widget(event)
        else:
            obj = self.gui.on_mouse_move(self.rect.x, self.rect.y)

            if obj:
                if obj.can_click:
                    self.image = self.over_click_image
                elif obj.can_drag:
                    if obj.are_in_path_dictionary():
                        self.image = self.over_drag_image
                    else:
                        self.image = self.over_cant_image
            else:
                self.image = self.normal_image

    def on_mouse_button_down(self, event):
        obj = self.gui.on_mouse_move(self.rect.x, self.rect.y)

        if obj:
            if obj.can_click:
                self.image = self.click_image
            elif obj.can_drag:
                self.image = self.drag_image
                obj.on_mouse_drag_start()
                self.widget_on_drag = obj
                common.bring_to_front(obj)
                self.bring_to_front()

    def on_mouse_active(self, event):
        self.visible = True

    def _drag_widget(self, event):
        dx, dy = event.rel
        self.widget_on_drag.on_mouse_drag(dx, dy)

    def _load_images(self):
        load = common.load_image

        self.normal_image = load("normal.png", 'mouse')
        self.over_click_image = load("yes.png", 'mouse')
        self.over_drag_image = load("yes.png", 'mouse')
        self.over_cant_image = load("no.png", 'mouse')
        self.click_image = load("click.png", 'mouse')
        self.drag_image = load("drag.png", 'mouse')
        self.hide = load("hide.png", 'mouse')

    def bring_to_front(self):
        common.bring_to_front(self)
