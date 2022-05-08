# -*- coding: utf8 -*-
# warfield
# helper class for bot_war
# Alfredo Martin 2021

import pygame
from classes.utils import screen_pos
import sys

version = 'warfield.v.1.0.0'


class WarField:

    def __init__(self):
        """
        horizon: int
        """
        self.success = True

    def get_grid(self, screen):
        """
        screen: pygame canvas instance
        returns: None
        """
        _, _, w, h = screen.get_rect()
        ho = wo = h // 7
        res = (w, h)
        grid = pygame.Surface((w, h))
        grid.fill((145, 230, 12))
        pygame.draw.rect(grid, (0, 0, 0), (0, 0, w, ho))
        pygame.draw.polygon(grid, (0, 0, 0), [(0, ho), (wo, ho), (0, h)])
        pygame.draw.polygon(grid, (0, 0, 0), [(w - wo, ho), (w, ho), (w, h)])
        step = w // 20
        #Vertical
        for i in range(21):
            pos_g_i = (i * step, 0)
            pos_g_f = (i * step, h)
            pos_i = screen_pos(res, pos_g_i, ho, wo)
            pos_f = screen_pos(res, pos_g_f, ho, wo)
            pygame.draw.line(grid, (0, 0, 0), pos_i, pos_f, 1)
        step = h // 20
        #Horizontal
        for i in range(21):
            pos_g_i = (0, step * i)
            pos_g_f = (w, step * i)
            pos_i = screen_pos(res, pos_g_i, ho, wo)
            pos_f = screen_pos(res, pos_g_f, ho, wo)
            pygame.draw.line(grid, (0, 0, 0), pos_i, pos_f, 1)
        pygame.draw.line(grid, (255, 255, 255), (wo, ho), (0, 0), 1)
        pygame.draw.line(grid, (255, 255, 255), (w, 0), (w - wo, ho), 1)
        # sys.exit(1)
        return grid


if __name__ == '__main__':
    print(version)
