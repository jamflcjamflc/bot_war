# -*- coding: utf8 -*-
# gun
# helper class for bot_war
# Alfredo Martin 2021

version = 'gun.v.1.0.0'

import numpy as np
import pygame


class Gun:

    def __init__(self, pos, sprite_sheet, g_type, horizon):
        """initiallizes the instance for a given position and gun type
        pos: numpy array of shape (2,)
        sprite_sheet: path to a file containing the sprite sheet for the guns
        g_type: int: type of gun (0, 1, 2)
        horizon"""
        self.horizon = horizon
        self.pos = pos
        self.size = (50, 25)
        self.radius = 12.5  # collision radius for this object
        self.center = np.array([[self.pos + np.array([self.radius, self.radius])],
                               [self.pos + np.array([3 * self.radius, self.radius])]])
        self.t = 0  # how many frames ago the gun was created
        self.g_type = g_type
        self.active = True
        self.score = 100 * (self.g_type + 1)
        self.sprite_sheet = pygame.image.load(sprite_sheet)
        # add transparent pixels to the sprite sheet
        _, _, w, h = self.sprite_sheet.get_rect()
        for i in range(w):
            for j in range(h):
                if self.sprite_sheet.get_at((i, j)) == (255, 255, 255):
                    self.sprite_sheet.set_at((i, j), (255, 255, 255, 0))

    def update(self):
        self.t += 1
        if self.t > 250:
            self.active = False
        return

    def screen_pos(self, screen):
        """screen: pygame canvas instance"""
        _, _, w, h = screen.get_rect()
        xm = w / 2
        dx = xm - self.pos[0]
        per_dy = self.pos[1] / (h - self.horizon)
        dx_screen = dx * (0.9 + per_dy * 0.1)
        x_screen = xm - dx_screen
        y_screen = self.pos[1] + self.horizon
        return np.array([x_screen, y_screen])

    def draw(self, screen):
        """blits the gun into the screen
        screen: instance of pygame.surface object"""
        screen.blit(self.sprite_sheet, self.screen_pos(screen),
                    area=(self.g_type * self.size[0], 0,
                          (self.g_type + 1) * self.size[0], self.size[1]))
        return


if __name__ == '__main__':
    print(version)
