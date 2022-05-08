# -*- coding: utf8 -*-
# bot_war
# main bot_war script
# Alfredo Martin 2021

from classes.battle import Battle
import pygame
import os
from classes.player import Player
import sys

__version__ = 'bot_war.v.1.0.0'
__author__ = 'Lucas and Alfredo 2022'

# teporary variables before coding argparse
pos = [(200, 200), (600, 600)]


if __name__ == '__main__':
    print(__version__)
    print(__author__)
    folder, _ = os.path.split(sys.argv[0])
    screen_width = 1000
    screen_height = 700
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.joystick.init()
    pygame.display.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    njoys = len(joysticks)
    for i in range(njoys):
        joysticks[i].init()
    if njoys == 0:
        print("There are no joysticks plugged ")
        print("You can't play without joysticks")
        sys.exit(1)
    sprites = [os.path.join(folder, 'sprites', 'player' + str(i+1) + '.png') for i in range(njoys)]
    players = [Player(pos[i], sprites[i], 'player ' + str(i+1), i, joysticks[i]) for i in range(njoys)]
    battle = Battle(screen, players)
    game_exit = battle.run_battle()
    if game_exit:
        pygame.quit()
        sys.exit(0)
        #no tengo ni la menor idea
