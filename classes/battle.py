# -*- coding: utf8 -*-
# battle
# helper class for bot_war
# Alfredo Martin 2021

version = 'battle.v.1.0.0'
from classes.warfield import WarField
import pygame
from classes.bot import Bot
import numpy as np
from classes.collision_handler import CollisionHandler

pygame.joystick.init()

class Battle:

    def __init__(self, screen, players, bot_sprite):
        """
        screen: pygame display instance
        players: list of Player class instance
        """
        self.screen = screen
        _, _, w, h = self.screen.get_rect()
        self.res = (w, h)
        self.players = players
        self.bot_sprite = bot_sprite
        battle_field = WarField()
        self.grid = battle_field.get_grid(self.screen)
        self.bots = []
        self.game_exit = False
        self.t = 0
        self.c_handler = CollisionHandler()

    def run_battle(self, level=0):
        """runs the battle corresponding to this level
        level: int"""
        clock = pygame.time.Clock()
        game_exit = False
        while not game_exit:
            self.t += 1

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    self.game_exit = True
            self.screen.fill((145, 230, 12))
            self.screen.blit(self.grid, (0, 0))
            if np.random.random() < 0.01:
                self.bots.append(Bot([player.pos for player in self.players], self.bot_sprite, 0, self.screen))
            self.players, self.bots = self.c_handler.detect_bullet(self.players, self.bots)
            for bot in self.bots:
                bot.move(self.screen)
            for player in self.players:
                player.shoot()
                player.move(self.res)
                self.screen = player.draw(self.screen)
            self.bots = [bot for bot in self.bots if bot.active]
            for bot in self.bots:
                bot.draw(self.screen)
            pygame.display.update()
            clock.tick(20)
        return self.game_exit


if __name__ == '__main__':
    print(version)
