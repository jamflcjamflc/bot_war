# -*- coding: utf8 -*-
# battle
# helper class for bot_war
# Alfredo Martin 2021

version = 'battle.v.1.0.0'
from classes.warfield import WarField
import pygame

pygame.joystick.init()

class Battle:

    def __init__(self, screen, players):
        """
        screen: pygame display instance
        players: list of Player class instance
        """
        self.screen = screen
        _, _, w, h = self.screen.get_rect()
        self.res = (w, h)
        self.players = players
        battle_field = WarField()
        self.grid = battle_field.get_grid(self.screen)
        self.game_exit = False

    def run_battle(self, level=0):
        """runs the battle corresponding to this level
        level: int"""
        clock = pygame.time.Clock()
        game_exit = False
        while not game_exit:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    self.game_exit = True
            self.screen.fill((145, 230, 12))
            self.screen.blit(self.grid, (0, 0))
            for player in self.players:
                player.move(self.res)
                self.screen = player.draw(self.screen)
            pygame.display.update()
            clock.tick(20)
        return self.game_exit


if __name__ == '__main__':
    print(version)
