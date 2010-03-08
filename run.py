#!/usr/bin/python
# -*- encoding: utf-8 -*-
from world import *

def main():
    world = World(do_center_window=True)
    world.change_scene(Menu(world))

if __name__ == '__main__':
    main()
