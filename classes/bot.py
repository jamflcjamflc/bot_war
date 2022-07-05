# -*- coding: utf8 -*-
# bot
# helper class for bot_war
# Alfredo Martin 2021

version = 'bot.v.1.0.0'

import numpy as np
import pygame as pg
from classes.utils import screen_pos

class Bot:

    def __init__(self, p_pos, sprite_sheet, b_type, screen):
        """initializes the instance with the initial position of the bot, the bot class and
        the sprite_sheet with bot sprites
        pos: list of numpy array of size 2 containing the initial position of the players
        sprite_sheet: filename of the sprite sheet corresponding to the bots
        b_type: int: type of bot (0, 1 or 2)
        screen : pygame screen object
        """
        self.p_pos = np.array(p_pos)
        self.b_type = b_type
        self.size = (50, 50)
        self.offset = np.array([25., 25.])
        _, _, w, h = screen.get_rect()
        self.shape = w, h
        exit_while = False
        while not exit_while:
            self.pos = np.random.random(2) * np.array([w - 50, h - 50])
            d = ((((self.p_pos - self.pos[None, :]) ** 2).sum(axis=1)) ** 0.5).min()
            if d > 200:
                exit_while = True
        self.center = self.pos + self.offset
        self.radius = 25  # collision radius for this object
        self.sprite_sheet = pg.image.load(sprite_sheet)
        # add transparent pixels to the sprite sheet
        _, _, w, h = self.sprite_sheet.get_rect()
        self.sprite_sheet = self.sprite_sheet.convert_alpha()
        for i in range(w):
            for j in range(h):
                if self.sprite_sheet.get_at((i, j)) == (255, 255, 255, 255):
                    self.sprite_sheet.set_at((i, j), (255, 255, 255, 0))
        self.orientations = [np.array([1., 0.]), np.array([0., 1.]),
                             np.array([-1., 0.]), np.array([0., -1.])]
        self.speed = 5
        self.step = np.random.choice([0, 1, 2, 3])  # orientation
        self.orientation = self.orientations[self.step] # sprite to be render for the current orientation
        self.velocity = self.orientation * self.speed
        self.score = (1 + self.b_type) * 10
        self.shield = 5

        self.t = 0   # time from the last change of orientation
        self.active = True
        self.shot = None

    def move(self, screen):
        """moves the bot into its position in the next frame
        players: list of Player instances
        screen: instance of pygame canvas class"""
        _, _, w, h = screen.get_rect()
        self.t += 1
        if np.random.random() < 0.01:
            self.step = np.random.choice([0, 1, 2, 3])  # orientation
        if self.pos[0] + self.size[0] > w and self.step == 0:
            self.step = 2
        if self.pos[0] < 0 and self.step == 2:
            self.step = 0
        if self.pos[1] + self.size[1] > h and self.step == 1:
            self.step = 3
        if self.pos[1] < 0 and self.step == 3:
            self.step = 1

        self.orientation = self.orientations[self.step]  # sprite to be render for the current orientation
        self.velocity = self.orientation * self.speed
        self.pos += self.velocity
        self.center += self.velocity
        return

    def draw(self, screen):
        """blits the player into the screen
        screen: instance of pygame.surface object"""
        #todo fix this because it is wrong
        _, _, w, h = screen.get_rect()
        screen.blit(self.sprite_sheet, screen_pos((w, h), self.pos),
                    area=(self.step * self.size[0], self.b_type * self.size[1],
                          self.size[0], self.size[1]))
        if self.shot is not None:
            pg.draw.circle(screen, self.shot, screen_pos(self.shape, self.center), 25 - self.shield, 2)
            self.shot = None
        return


class Old_Bot:
    def move(self, players, screen):
        """moves the bot into its position in the next frame
        players: list of Player instances
        screen: instance of pygame canvas class"""
        _, _, w, h = screen.get_rect()
        self.t += 1
        if self.pos[0] + self.size[0] / 2 > w:
            self.orientation = np.array([-1., 0.])
        elif self.pos[0] - self.size[0] / 2 < 0:
            self.orientation = np.array([-1., 0.])
        elif self.pos[1] + self.size[0] / 2 > h:
            self.orientation = np.array([0., -1.])
        elif self.pos[1] - self.size[0] / 2 < 0:
            self.orientation = np.array([0., 1.])
        else:
            if self.t > np.random.randint(0, 200):
                self.t = 0
                if self.b_type == 1 or self.b_type == 2:
                    distances = [np.linalg.norm(self.pos - player.pos) for player in players]
                    closest = distances.index(min(distances))
                    min_vector = self.pos - players[closest].pos
                    if abs(min_vector[0]) > abs(min_vector[1]):
                        self.orientation = np.array([int(min_vector[0] / abs(min_vector[0])), 0])
                    elif abs(min_vector[0]) < abs(min_vector[1]):
                        self.orientation = np.array([0, int(min_vector[1] / abs(min_vector[1]))])
                    elif min_vector[0] != 0:
                        self.orientation = np.array([int(min_vector[0] / abs(min_vector[0])), 0])
                    else:
                        self.orientation = np.array([0, int(min_vector[1] / abs(min_vector[1]))])
                    if self.b_type == 2:
                        self.orientation *= -1
                elif self.b_type == 0:
                    self.orientation = np.random.choice(self.orientations)  # orientation
        self.velocity = self.orientation * self.speed
        self.pos += self.velocity
        self.center = np.array([self.pos + self.offset])
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
        """blits the player into the screen
        screen: instance of pygame.surface object"""
        #todo fix this because it is wrong
        screen.blit(self.sprite_sheet, self.screen_pos(screen),
                    area=(self.b_type * self.size[0], self.step * self.size[1],
                          (self.b_type + 1) * self.size[0], (self.step + 1) * self.size[1]))
        return


if __name__ == '__main__':
    print(version)
