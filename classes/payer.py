# -*- coding: utf8 -*-
# player
# helper class for bot_war
# Alfredo Martin 2021

version = 'player.v.1.0.0'
import pygame
import numpy as np


class Player:

    def __init__(self, pos, sprite_sheet, name, index):
        """intiallizes the player class
        pos: nupy array of size 2 containing the initial position of the player
        sprite_sheet: filename of the sprite sheet corresponding to this player
        name: str: name of the player
        index: int: index corresponding to this player"""
        self.name = name
        self.index = index
        self.size = (25, 50)
        self.radius = 12.5  # collision radius for this object
        self.sprite_sheet = pygame.image.load(sprite_sheet)
        # add transparent pixels to the sprite sheet
        _, _, w, h = self.sprite_sheet.get_rect()
        for i in range(w):
            for j in range(h):
                if self.sprite_sheet.get_at((i, j)) == (255, 255, 255):
                    self.sprite_sheet.set_at((i, j), (255, 255, 255, 0))
        self.orientations = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}  # dict with sprite lines
        self.orientation = (0, 1)  # orientation
        self.step = 1  # sprite to be render for the current orientation
        self.line = self.orientations[self.orientation]  # line indicating the orientation
        self.speed = 0.  # module of the velocity vector
        self.max_speed = 3.
        self.velocity = np.array(self.orientation) * self.speed  # vector veocity
        self.shot = False
        self.pos = np.array(pos)  # vector position
        self.center = np.array([[self.pos - np.array([0, self.radius])],
                               [self.pos - np.array([0, self.radius])]])
        self.active = True  # whether the player has any life left
        self.lives = 3  # remaining lives
        self.t = 0  # time ??

    def get_next_step(self):
        """gets the next step"""
        if self.step == 4:
            self.step = 1
        else:
            self.step += 1

    def get_center(self):
        """gets a new collision center based on the new pos"""
        self.center = np.array([[self.pos - np.array([0, self.radius])],
                               [self.pos - np.array([0, self.radius])]])

    def inside_screen(self, res):
        """returns movement options
        res: tuple of two ints containing the screen resolution
        returns: tuple of four bools"""
        result = list()
        result.append(self.pos[0] + self.size[0] / 2 < res[0])
        result.append(self.pos[1] + self.size[1] / 2 < res[1])
        result.append(self.pos[0] - self.size[0] / 2 < 0)
        result.append(self.pos[1] - self.size[1] / 2 < 0)
        return result

    def get_collision(self, objects):
        """gets any collision to a list of objects
        objects: list of instances of collision-able objects. objects must have one or more centers and collision
            radius
        returns: bool (whether there is a collision or not"""
        for obj in objects:
            dist2 = self.center.reshape(1, self.center.shape[0], 2) - obj.center.reshape(obj.center.shape[0], 1, 2)
            dist2 = (dist2 ** 2).sum(axis=2)
            min_dist = dist2.min()
            if min_dist < (self.radius + obj.radius) ** 2:
                return True
        return False

    def move(self, joystick, screen):
        """moves the player in the direction indicated by the joystick
         joystick: instance of Joystick pygame class
         screen: instance of screen canvas
         returns: bool: whether a shot has been done"""
        command = joystick.get_hat(0)
        shot = not self.shot and joystick.get_button(1)
        _, _, w, h = screen.get_rect()
        if self.shot:
            self.step = 0
            self.speed = 0
            self.velocity = np.array(self.orientation) * self.speed
            return True
        if command != (0, 0) and 0 in command:
            self.orientation = command
            self.speed = self.max_speed
            self.velocity = np.array(self.orientation) * self.speed
            self.line = self.orientations[self.orientation]
            self.get_next_step()  # gets the next step
            if all(self.inside_screen((w, h))):  # move only we are within boundaries
                self.pos += self.velocity
                self.get_center()
            return False
        # No command has been added, so position does not chanve
        self.orientation = (1, 0)
        self.step = 1
        self.line = 0
        self.speed = 0.
        self.velocity = np.array(self.orientation) * self.speed
        return False

    def draw(self, screen):
        """blits the player into the screen
        screen: instance of pygame.surface object"""

        screen.blit(self.sprite_sheet, self.pos,
                    area=(self.step * self.size[0], self.line * self.size[1],
                          (self.step + 1) * self.size[0], (self.line + 1) * self.size[1]))
        return


if __name__ == '__main__':
    print(version)
