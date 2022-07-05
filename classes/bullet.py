import numpy as np
import pygame as pg
from classes.utils import screen_pos

class Bullet:
    def __init__(self, pos=None, velocity=np.array([0., 0.]), active=False, color=(255, 0, 0), shape=(1000, 700),
                 radius=4):
        self.color = color
        self.pos = pos
        self.velocity = velocity
        self.active = active
        self.size = (3, 3)
        self.shape = shape
        self.alive = True
        self.radius = radius

    def update_pos(self, screen):
        if self.pos is not None and self.alive and self.active:
            self.pos += self.velocity
            self.alive = (0. <= self.pos[0] <= self.shape[0]) and (0. <= self.pos[1] <= self.shape[1])
            if self.alive:
                pg.draw.circle(screen, self.color, screen_pos(self.shape, self.pos), self.radius)