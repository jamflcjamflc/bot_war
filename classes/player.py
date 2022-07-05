# -*- coding: utf8 -*-
# player
# helper class for bot_war
# Alfredo Martin 2021

version = 'player.v.1.0.0'

import pygame
import numpy as np
from classes.utils import screen_pos
from classes.gun import Gun

pygame.joystick.init()

class Player:

    def __init__(self, pos, sprite_sheet, name, index, joystick, color):
        """intiallizes the player class
        pos: numpy array of size 2 containing the initial position of the player
        sprite_sheet: filename of the sprite sheet corresponding to this player
        name: str: name of the player
        index: int: index corresponding to this player
        joystick: instance of Joystick pygame class
        horizon: """
        self.joystick = joystick
        self.name = name
        self.index = index
        self.size = (25, 50)
        self.radius = 12.5  # collision radius for this object
        self.color = color
        self.pos = np.array(pos).astype('float64')  # vector position
        self.gun = Gun(self.pos.copy(), self.color)
        self.sprite_sheet = pygame.image.load(sprite_sheet)
        # add transparent pixels to the sprite sheet
        _, _, w, h = self.sprite_sheet.get_rect()
        self.sprite_sheet = self.sprite_sheet.convert_alpha()
        for i in range(w):
            for j in range(h):
                if self.sprite_sheet.get_at((i, j)) == (255, 255, 255, 255):
                    self.sprite_sheet.set_at((i, j), (255, 255, 255, 0))
        self.orientations = {(0, -1): 0, (1, 0): 1, (0, 1): 2, (-1, 0): 3}  # dict with sprite lines
        self.orientation = (0, 1)  # orientation
        self.step = 1  # sprite to be render for the current orientation
        self.line = self.orientations[self.orientation]  # line indicating the orientation
        self.speed = 0.  # module of the velocity vector
        self.max_speed = 3.
        self.velocity = np.array(self.orientation) * self.speed  # vector veocity
        self.shot = False
        self.center = np.array([[self.pos + np.array([self.radius, self.radius])],
                               [self.pos + np.array([self.radius, 3 * self.radius])]])
        self.active = True  # whether the player has any life left
        self.lives = 3  # remaining lives
        self.t = 0  # time ??
        self.mask = np.array([1., -1.])  # modifier for the joystic hat

    def shoot(self):
        """shoots a bullet"""
        self.gun.t += 1  # this increases the t in gun to be able to shot
        if self.joystick.get_button(1):
            self.gun.pos = self.pos + np.array([25., 50.]) / 2
            self.gun.shoot(7 * np.array(self.orientation).astype('float64'))

        #print(self.color, len([bullet for bullet in self.gun.cartridge if bullet.active]))


    def get_next_step(self):
        """gets the next step"""
        if self.step == 4:
            self.step = 1
        else:
            self.step += 1

    def get_center(self):
        """gets a new collision center based on the new pos"""
        self.center = np.array([[self.pos + np.array([self.radius, self.radius])],
                               [self.pos + np.array([self.radius, 3 * self.radius])]])

    def inside_screen(self, res):
        """returns movement options
        screen: pygame canvas instance
        returns: tuple of four bools"""
        w, h = res
        result = list()
        result.append(self.pos[1] + self.size[1] <= h)
        result.append(self.pos[0] + self.size[0] <= w)
        result.append(self.pos[1] >= 0)
        result.append(self.pos[0] >= 0)
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

    def move(self, res):
        """moves the player in the direction indicated by the joystick
         res: tuple with the resolution of the screen
         returns: bool: whether a shot has been done"""
        command = self.joystick.get_hat(0)
        self.shot = not self.shot and self.joystick.get_button(1)
        if self.shot:
            self.step = 0
            self.speed = 0.
            self.velocity = np.array(self.orientation) * self.speed
            return True
        if command != (0, 0) and 0 in command:
            self.orientation = self.mask * np.array(command).astype('float64')
            self.speed = self.max_speed
            self.velocity = np.array(self.orientation).astype('float64') * self.speed
            #self.velocity = self.mask * np.array(self.orientation).astype('float64') * self.speed
            #self.line = self.orientations[self.orientation]
            self.line = self.orientations[command]
            self.get_next_step()  # gets the next step
            if self.inside_screen(res)[self.line]:
                self.pos += self.velocity
                self.get_center()
            if all(self.inside_screen(res)):  # move only we are within boundaries
                self.pos += self.velocity
                self.get_center()
            return False
        else:
        # No command has been added, so position does not change
            #self.orientation = (1, 0)
            self.step = 1
            #self.line = 0
            self.speed = 0.
            self.velocity = np.array(self.orientation).astype('float64') * self.speed
            return False

    def screen_pos(self, screen):
        """screen: pygame canvas instance"""
        _, _, w, h = screen.get_rect()
        ho = wo = h // 7
        x_screen, y_screen = screen_pos((w, h), self.pos, ho, wo)
        return np.array([x_screen, y_screen])

    def draw(self, screen):
        """blits the player into the screen
        screen: instance of pygame.surface object
        returns: screen"""
        #The next line draws the player into the screen
        screen.blit(self.sprite_sheet, self.screen_pos(screen),
                    area=(self.step * self.size[0], self.line * self.size[1],
                          self.size[0], self.size[1]))
        #The next loop moves the bullets and draws them into the screen
        for i, bullet in enumerate(self.gun.cartridge):
            self.gun.cartridge[i].update_pos(screen)
        # The next line eliminates alll the bullets that are destroyed
        self.gun.cartridge = [bullet for bullet in self.gun.cartridge if bullet.alive]
        return screen


if __name__ == '__main__':
    print(version)
