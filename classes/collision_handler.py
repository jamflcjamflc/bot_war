# -*- coding: utf8 -*-
# collision_handler
# helper class for bot_war
# Alfredo Martin 2021

version = 'bot.v.1.0.0'

import numpy as np
import pygame as pg
from classes.utils import screen_pos
from classes.bullet import Bullet

class CollisionHandler:
    def __init__(self):
        self.success = True

    def detect_bullet(self, players, bots):
        for i, bot in enumerate(bots):
            for j, player in enumerate(players):
                for k, bullet in enumerate(player.gun.cartridge):
                    if bullet.alive and bullet.active:
                        if np.linalg.norm(bot.center - bullet.pos) <= 25:
                            bots[i].shield -= 1
                            players[j].gun.cartridge[k].alive = False
                            players[j].gun.cartridge.append(Bullet(color=players[j].gun.color))
                            bots[i].shot = players[j].gun.color
                            if bots[i].shield < 0:
                                bots[i].active = False
                                players[j].gun.cartridge += [Bullet(color=players[j].gun.color) for _ in range(5)]
        return players, bots

