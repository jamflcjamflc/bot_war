# -*- coding: utf8 -*-
# utils
# helper functions for bot_war
# Alfredo Martin 2022
# Lucas Martin 2022

def screen_pos(res, pos, ho=100, wo=100):
    """res: tuple (resolution of the screen)
    pos: sequence of two numbers
    returns: tuple"""
    w, h = tuple(res)
    x, y = tuple(pos)
    y_screen = ho + (h - ho) * (y / h)
    cwo = wo * (1 - (y / h))
    xl = (w - 2 * cwo) * (x / w)
    x_screen = cwo + xl
    return x_screen, y_screen


if __name__ == "__main__":
    print("utils")