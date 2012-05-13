#!/usr/bin/python
# -*- encoding: utf-8 -*-
from world import *
import menu

def main():
    world = World(do_center_window=True)
    world.change_scene(menu.Menu(world))
    world.loop()


if __name__ == '__main__':
    main()
