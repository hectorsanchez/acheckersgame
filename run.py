#!/usr/bin/python
# -*- encoding: utf-8 -*-
from world import *
import intro1

def main():
    world = World(do_center_window=True)
    #new_scene = game.Game(world)
    new_scene = intro1.Intro1(world)
    world.change_scene(new_scene)
    world.loop()


if __name__ == '__main__':
    main()
