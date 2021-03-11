# -*- coding: utf8 -*-
# shot
# helper class for bot_war
# Alfredo Martin 2021

version = 'shot.v.1.0.0'


class Shot:

    def __init__(self, pos, velocity, horizon):
        """initiallizes the shot class
        pos: initial position: numpy array of shape (2,)
        velocity: numpy array of shape (2,)
        horizon:"""
        self.color = (255, 0, 0)
        self.pos = pos
        self.velocity = velocity
        self.active = True
        self.t = 0  # number of frames from when the shot was created
        self.size = (3, 3)
        self.center = self.pos
        self.radius = 3

    def inside_screen(self, screen):
        """returns movement options
        screen: pygame canvas instance
        returns: tuple of four bools"""
        _, _, w, h = screen.get_rect()
        result = list()
        result.append(self.pos[0] + self.size[0] / 2 < w)
        result.append(self.pos[1] + self.size[1] / 2 < h)
        result.append(self.pos[0] - self.size[0] / 2 < 0)
        result.append(self.pos[1] - self.size[1] / 2 < 0)
        return result

    def update_pos(self):
        self.t += 1
        self.pos = self.pos + self.velocity
        if within_limits(self.pos, self.size, min_limit, max_limit):
            pygame.draw.circle(screen, self.color, screen_pos(self.pos), self.size[0])
        else:
            self.active = False





if __name__ == '__main__':
    print(version)
