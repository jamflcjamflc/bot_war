#tanks

import pygame
import sys
import time
import random as rnd
import cPickle as pic

pygame.display.init()
pygame.mixer.init()
pygame.font.init()

path = 'C:\\Users\\JoseAlfredo\\Desktop\\LUCAS BOT GAME\\'
bomb_sound = pygame.mixer.Sound('SOUNDS\explosion_al.wav')
bomb_sound.set_volume(0.1)
menu_sound = pygame.mixer.Sound('SOUNDS\epic_orchestra_al.wav')
menu_sound.set_volume(0.1)
shot_1_sound = pygame.mixer.Sound('SOUNDS\lasser_1_al.wav')
shot_1_sound.set_volume(0.03)
shot_2_sound = pygame.mixer.Sound('SOUNDS\lasser_2_cc.wav')
shot_2_sound.set_volume(0.03)
shot_4_sound = pygame.mixer.Sound('SOUNDS\lasser_4_cc.wav')
shot_4_sound.set_volume(0.03)
shot_sound = [shot_1_sound, shot_1_sound, shot_2_sound, shot_2_sound, shot_2_sound]
lose_sound = pygame.mixer.Sound('SOUNDS\lose_cc.wav')
lose_sound.set_volume(0.5)
background_sound = pygame.mixer.Sound('SOUNDS\musica_lucasbot.wav')
background_sound.set_volume(0.3)
pick_coffin = pygame.mixer.Sound('SOUNDS\coger_pistola.wav')
pick_coffin.set_volume(0.3)

def screen_pos(pos):
    xm = screen_width / 2.0
    dx = xm - pos[0]
    per_dy = pos[1] / float(screen_height - horizon)
    dx_screen = dx * (0.9 + per_dy * 0.1)
    x_screen = xm - dx_screen
    y_screen = pos[1] + horizon
    return (int(x_screen), int(y_screen))

def v_multiply(vector, scalar):
    return (vector[0] * scalar, vector[1] * scalar)

def v_divide(vector, scalar):
    return (vector[0] / scalar, vector[1] / scalar)

def v_invert(vector):
    return (- vector[0], - vector[1])

def v_add(vector1, vector2):
    return (vector1[0] + vector2[0], vector1[1] + vector2[1])

def v_substract(vector1, vector2):
    return (vector1[0] - vector2[0], vector1[1] - vector2[1])

def v_normalize(vector):
    module = (vector[0] * vector[0] + vector[1] * vector[1]) ** 0.5
    return (vector[0] / module, vector[1] / module)

def v_module(vector):
    return (vector[0] * vector[0] + vector[1] * vector[1]) ** 0.5

def within_limits(pos, size, min_limit, max_limit):
    resultado = True
    if pos[0] < min_limit[0]:
        resultado = False
    if pos[1] < min_limit[1]:
        resultado = False
    if pos[0] + size[0] > max_limit[0]:
        resultado = False
    if pos[1] + size[1] > max_limit[1]:
        resultado = False
    return resultado

class gun:
    def __init__(self, pos, tipo):
        self.pos = pos
        self.t = 0
        self.tipo = tipo
        self.size = (30, 30)
        self.active = True
        self.score = 100 * self.tipo
        if self.tipo == 1:
            self.image = gun_1
        elif self.tipo == 2:
            self.image = gun_2
        elif self.tipo == 3:
            self.image = gun_3
        elif self.tipo == 4:
            self.image = gun_4
        else:
            self.image = gun_1
    def update(self):
        self.t += 1
        if self.tipo == 1 and self.t > 250:
            self.active == False
        elif self.tipo == 2 and self.t > 250:
            self.active == False
        elif self.tipo == 3 and self.t > 250:
            self.active == False
        elif self.tipo == 4 and self.t > 250:
            self.active == False
        return
    def draw(self):
        screen.blit(self.image, screen_pos(self.pos))
        style = pygame.font.SysFont('comicsans', 20)
        text_gun = style.render('gun' + str(self.tipo), False, blue)
        screen.blit(text_gun, (screen_pos(self.pos)[0], screen_pos(self.pos)[1] - 20))
        return
                
            

class player:
    def __init__(self, pos):
        self.size = (25, 50)
        self.image = [[pygame.image.load('SPRITES\Lucas_Front_0.png'),
                      pygame.image.load('SPRITES\Lucas_Front_1.png'),
                      pygame.image.load('SPRITES\Lucas_Front_0.png'),
                      pygame.image.load('SPRITES\Lucas_Front_3.png'),
                      pygame.image.load('SPRITES\Lucas_Front_shot.png')],
                      [pygame.image.load('SPRITES\Lucas_Right_0.png'),
                      pygame.image.load('SPRITES\Lucas_Right_1.png'),
                      pygame.image.load('SPRITES\Lucas_Right_0.png'),
                      pygame.image.load('SPRITES\Lucas_Right_3.png'),
                      pygame.image.load('SPRITES\Lucas_Right_shot.png')],
                      [pygame.image.load('SPRITES\Lucas_Back_0.png'),
                      pygame.image.load('SPRITES\Lucas_Back_1.png'),
                      pygame.image.load('SPRITES\Lucas_Back_0.png'),
                      pygame.image.load('SPRITES\Lucas_Back_3.png'),
                      pygame.image.load('SPRITES\Lucas_Back_shot.png')],
                      [pygame.image.load('SPRITES\Lucas_Left_0.png'),
                      pygame.image.load('SPRITES\Lucas_Left_1.png'),
                      pygame.image.load('SPRITES\Lucas_Left_0.png'),
                      pygame.image.load('SPRITES\Lucas_Left_3.png'),
                      pygame.image.load('SPRITES\Lucas_Left_shot.png')]]           
        for i in range(len(self.image)):
            for j in range(len(self.image[i])):
                stdcolor = self.image[i][j].get_at((0, 0))
                for k in range(self.size[0]):
                    for l in range(self.size[1]):
                        color = self.image[i][j].get_at((k, l))
                        if color == stdcolor:
                            self.image[i][j].set_at((k, l), (255, 255, 255, 0))
        self.orientation = (0, 1)
        self.speed = 0
        self.shot = False
        self.pos = pos
        self.velocity = v_multiply(self.orientation, self.speed)
        self.active = True
        self.t = 0
        
    def move(self):
        if self.speed > 0:
            if self.t == 3:
                self.t = 0
            else:
                self.t += 1
        if self.shot:
            self.t = 4
            self.speed = 0
        if within_limits(self.pos, self.size, min_limit, max_limit):
            self.velocity = v_multiply(self.orientation, self.speed)
            self.pos = v_add(self.pos, self.velocity)
        else:
            if self.pos[0] < min_limit[0]:
                self.pos = (min_limit[0], self.pos[1])
            if self.pos[0] + self.size[0] > max_limit[0]:
                self.pos = (max_limit[0] - self.size[0], self.pos[1])
            if self.pos[1] < min_limit[1]:
                self.pos = (self.pos[0], min_limit[1])
            if self.pos[1] + self.size[1] > max_limit[1]:
                self.pos = (self.pos[0], max_limit[1] - self.size[1])
        return
    def draw(self):
        num_orientation = vector_orientation.index(self.orientation)
        screen.blit(self.image[num_orientation][self.t], screen_pos(self.pos))
        return



class shot:
    def __init__(self, pos, velocity):
        self.color = red
        self.pos0 = pos
        self.pos = self.pos0
        self.velocity = velocity
        self.active = True
        self.t = 0
        self.size = (3, 3)
    def update_pos(self):
        self.t += 1
        self.pos = v_add(self.pos0, v_multiply(self.velocity, self.t))
        if within_limits(self.pos, self.size, min_limit, max_limit):
            pygame.draw.circle(screen, self.color, screen_pos(self.pos), self.size[0])
        else:
            self.active = False
        
    
class derbis:
    def __init__(self, pos):
        self.color = black
        self.pos0 = pos
        self.pos = pos
        self.velocity = (10.0 * (rnd.random() - 0.5), - 10.0 * rnd.random())
        self.t = 0
        self.acceleration = (0, 1.0)
        self.active = True
        self.size = (3, 3)
        
    def update_pos(self):
        self.t += 1
        self.velocity = v_add(self.velocity, self.acceleration)
        self.pos = v_add(self.pos, self.velocity)
        if self.pos[1] < self.pos0[1] + self.size[1] / 2:
            pygame.draw.circle(screen, self.color, screen_pos(self.pos), self.size[0])
        else:
            self.active = False
            
class robot:
    def __init__(self, pos, r_type):
        self.color = black
        self.pos = pos
        self.size = (50, 50)
        self.t = 0
        if r_type == 'smart':
            self.score = 200
        elif r_type == 'coward':
            self.score = 400
        else:
            self.score = 100
        self.r_type = r_type
        self.orientation = (0, 1)
        if r_type == 'dumb':
            self.image = [pygame.image.load(path + 'SPRITES\Dumb_front.png'),
                            pygame.image.load('SPRITES\Dumb_right.png'),
                            pygame.image.load('SPRITES\Dumb_back.png'),
                            pygame.image.load('SPRITES\Dumb_left.png')
                          ]
        if r_type == 'smart':
            self.image = [pygame.image.load('SPRITES\Smart_front.png'),
                            pygame.image.load('SPRITES\Smart_right.png'),
                            pygame.image.load('SPRITES\Smart_back.png'),
                            pygame.image.load('SPRITES\Smart_left.png')
                          ]
        if r_type == 'coward':
            self.image = [pygame.image.load('SPRITES\Coward_front.png'),
                            pygame.image.load('SPRITES\Coward_right.png'),
                            pygame.image.load('SPRITES\Coward_back.png'),
                            pygame.image.load('SPRITES\Coward_left.png')
                          ]
        for i in range(len(self.image)):
            stdcolor = self.image[i].get_at((0, 0))
            for k in range(self.size[0]):
                for l in range(self.size[1]):
                    color = self.image[i].get_at((k, l))
                    if color == stdcolor:
                        self.image[i].set_at((k, l), (255, 255, 255, 0))
        #for i in range(len(self.image)):
            #self.image[i].set_colorkey((255, 255, 255))
        if r_type == 'dumb':
            self.speed = 5
        elif r_type in ['smart', 'coward']:
            self.speed = 5
        self.velocity = v_multiply(self.orientation, self.speed)
        self.score = 100
        self.active = True

    def move(self, lpos):
        self.t += 1
        if self.t > rnd.randint(0, 200):
            self.t = 0
            if self.r_type == 'smart':
                difference_pos = v_substract(self.pos, lpos)
                if abs(difference_pos[0])>= abs(difference_pos[1]):
                    if difference_pos[0] > 0:
                        self.orientation = (-1, 0)
                    else:
                        self.orientation = (1, 0)
                else:
                    if difference_pos[1] >= 0:
                        self.orientation = (0, -1)
                    else:
                        self.orientation = (0, 1)
            elif self.r_type == 'dumb':
                new_scalar_orientation = rnd.randint(0, 3)
                if new_scalar_orientation == 0:
                    self.orientation = (0, 1)
                elif new_scalar_orientation == 1:
                    self.orientaion = (1, 0)
                elif new_scalar_orientation == 2:
                    self.orientation = (0, -1)
                else:
                    self.orientation = (-1, 0)
            elif self.r_type == 'coward':
                difference_pos = v_substract(self.pos, lpos)
                if abs(difference_pos[0] )<= abs(difference_pos[1]):
                    if difference_pos[0] < 0:
                        self.orientation = (-1, 0)
                    else:
                        self.orientation = (1, 0)
                else:
                    if difference_pos[1] < 0:
                        self.orientation = (0, 1)
                    else:
                        self.orientation = (0, -1)
        if within_limits(self.pos, self.size, min_limit, max_limit):
            pass
        else:
            if self.pos[0] < min_limit[0]:
                self.pos = (min_limit[0], self.pos[1])
            if self.pos[0] + self.size[0] > max_limit[0]:
                self.pos = (max_limit[0] - self.size[0], self.pos[1])
            if self.pos[1] < min_limit[1]:
                self.pos = (self.pos[0], min_limit[1])
            if self.pos[1] + self.size[1] > max_limit[1]:
                self.pos = (self.pos[0], max_limit[1] - self.size[1])
            self.orientation = v_multiply(self.orientation, -1)
        self.velocity = v_multiply(self.orientation, self.speed)
        self.pos = v_add(self.pos, self.velocity)
        return

    def draw(self):
        num_orientation = vector_orientation.index(self.orientation)
        screen.blit(self.image[num_orientation], screen_pos(self.pos))
        return


def draw_grid():
    pygame.draw.rect(screen, black, (0, 0, screen_width, horizon))
    pygame.draw.polygon(screen, black, [(0, horizon), screen_pos((0, 0)), screen_pos((0, max_limit[1]))])
    pygame.draw.polygon(screen, black, [(screen_width, horizon), screen_pos((max_limit[0], 0)), screen_pos((max_limit[0], max_limit[1]))])
    for i in range(21):
        pygame.draw.line(screen, black, screen_pos((i * 50, 0)), screen_pos((i * 50, 600)), 1)
    for i in range(12):
        pygame.draw.line(screen, black, screen_pos((0, 50 * i)), screen_pos((screen_width, 50 * i)), 1)
    pygame.draw.line(screen, white, screen_pos(min_limit), (0, 0), 1)
    pygame.draw.line(screen, white, (screen_width, 0), screen_pos((max_limit[0], min_limit[1])), 1)
    style = pygame.font.SysFont('comicsans', 30)
    
    
    text = style.render('Score: ' + str(score), False, white)
    screen.blit(text, (screen_width / 8, 10 * horizon / 100))
    text = style.render('Level: ' + str(level), False, white)
    screen.blit(text, (screen_width / 8, 40 * horizon / 100))
    text = style.render('Robots_killed: ' + str(robots_killed), False, white)
    screen.blit(text, (screen_width / 8, 70 * horizon / 100))    
    text = style.render('Bonus: ' + str(max(bonus_t - level_t, 0)), False, white)
    screen.blit(text, (screen_width / 3, 10 * horizon / 100))
    text = style.render('Next_split: ' + str(max(int(new_robot_time - game_t), 0)), False, white)
    screen.blit(text, (screen_width / 3, 40 * horizon / 100))
    text = style.render('Robots_to_go: ' + str(level * robots_per_level - robots_killed), False, white)
    screen.blit(text, (screen_width / 3, 70 * horizon / 100))
    if current_gun == 1:
        screen.blit(gun_1, (6 * screen_width / 8, 10 * horizon / 100))
    elif current_gun == 2:
        screen.blit(gun_2, (6 * screen_width / 8, 10 * horizon / 100))
    elif current_gun == 3:
        screen.blit(gun_3, (6 * screen_width / 8, 10 * horizon / 100))
    elif current_gun == 4:
        screen.blit(gun_4, (6 * screen_width / 8, 10 * horizon / 100))
    return

class button:
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        self.text = text
        self.pressed = False
        style = pygame.font.SysFont('comicsans', 30)
        self.text = style.render(text, False, black)
        text_rect = self.text.get_rect()
        self.dpos = ((size[0] / 2) - (text_rect[2] / 2), (size[1] / 2) - (text_rect[3] / 2))
    def update(self):
        m_pos = pygame.mouse.get_pos()
        p1 = pygame.mouse.get_pressed()[0]
        if self.pos[0]  < m_pos[0] < self.pos[0] + self.size[0]  and self.pos[1] < m_pos[1] < self.pos[1] + self.size[1]:
            pygame.draw.rect(screen, red, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            if p1:
                self.pressed = True
        else:
            pygame.draw.rect(screen, light_red, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        screen.blit(self.text, v_add(self.pos, self.dpos))        

class announcement:
    def __init__(self, texts, time):
        pick_coffin.play()
        self.t = 0
        self.time = time
        self.text = []
        self.pos = []
        self.active = True
        for i in range(len(texts)):
            style = pygame.font.SysFont('comicsans', 70)
            self.text.append(style.render(texts[i], False, tansparent_blue))
            x, y, w, h = self.text[i].get_rect()
            text_x = (screen_width / 2) - (w / 2)
            text_y = (i + 2) * screen_height /(4 + len(texts))
            self.pos.append((text_x, text_y))
    def update(self):
        self.t += 1
        if self.t > self.time:
            self.active = False
        for i in range(len(self.text)):
            screen.blit(self.text[i], self.pos[i])        
        

            
def menu(main_text, secondary_text, buttons, sprite = None, music = None):
    resultado = 0
    keep_menu = True
    button_list = []
    button_width = int(0.8 * screen_width / (len(buttons) + 1))
    button_height = int(0.8 * screen_height / 6)
    for i in range(len(buttons)):
        button_pos_x = (i +1) * (screen_width / (len(buttons) + 1)) - (button_width / 2)
        button_pos_y = int(4.5 * screen_height / 6)
        button_list.append(button((button_pos_x, button_pos_y), (button_width, button_height), buttons[i]))
    if music is not None:
        music.play(loops = -1)
    while keep_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_menu = False
                pygame.quit()
                quit()
        xm, ym = pygame.mouse.get_pos()
        pm = pygame.mouse.get_pressed()[0]            
        screen.fill(white)
        if sprite is not None:
            x, y, w, h = sprite.get_rect()
            sprite_x = (screen_width / 2) - (w / 2)
            sprite_y = (screen_height / 2) - (h / 2)
            screen.blit(sprite, (sprite_x, sprite_y))
        style = pygame.font.SysFont('comicsans', 50)
        text = style.render(main_text, False, black)
        x, y, w, h = text.get_rect()
        text_x = (screen_width / 2) - (w / 2)
        text_y = screen_height / (4 + len(secondary_text))
        screen.blit(text, (text_x, text_y))
        for i in range(len(secondary_text)):
            style = pygame.font.SysFont('comicsans', 30)
            text = style.render(secondary_text[i], False, black)
            x, y, w, h = text.get_rect()
            text_x = (screen_width / 2) - (w / 2)
            text_y = (i + 2) * (screen_height / (4 + len(secondary_text)))
            screen.blit(text, (text_x, text_y))
        for i in range(len(button_list)):
            button_list[i].update()
            if button_list[i].pressed:
                resultado = i
                keep_menu = False
        pygame.display.update()            
        clock.tick(FPS)
    if music is not None:
        music.stop()
    return resultado


def new_shot(pos, orientation, gun):
    these_shots = []
    if gun == 0:
        these_shots.append(shot(pos, (8 * orientation[0], 8 * orientation [1])))
    elif gun == 1:
        these_shots.append(shot(pos, (8 * orientation[0], 8 * orientation [1])))
        these_shots.append(shot(pos, (9 * orientation[0], 9 * orientation [1])))
        these_shots.append(shot(pos, (10 * orientation[0], 10 * orientation [1])))
        these_shots.append(shot(pos, (11 * orientation[0], 11 * orientation [1])))             
    elif gun == 2:
        if orientation[0] == 0:
            these_shots.append(shot(pos, (0, 8 * orientation [1])))
            these_shots.append(shot(pos, (2, 8 * orientation [1])))
            these_shots.append(shot(pos, (-2, 8 * orientation [1])))
        else:
            these_shots.append(shot(pos, (8 * orientation[0], 0)))
            these_shots.append(shot(pos, (8 * orientation[0], 2)))
            these_shots.append(shot(pos, (8 * orientation[0], -2)))
    elif gun == 3:
        if orientation[0] == 0:
            these_shots.append(shot(pos, (0, 8 * orientation [1])))
            these_shots.append(shot(pos, (1, 9 * orientation [1])))
            these_shots.append(shot(pos, (-1, 9 * orientation [1])))
            these_shots.append(shot(pos, (2, 10 * orientation [1])))
            these_shots.append(shot(pos, (-2, 10 * orientation [1])))
            these_shots.append(shot(pos, (1, 11 * orientation [1])))
            these_shots.append(shot(pos, (-1, 11 * orientation [1])))
            these_shots.append(shot(pos, (0, 12 * orientation [1])))
        else:
            these_shots.append(shot(pos, (8 * orientation[0], 0)))
            these_shots.append(shot(pos, (9 * orientation [0], 1)))
            these_shots.append(shot(pos, (9 * orientation [0], -1)))
            these_shots.append(shot(pos, (10 * orientation [0], 2)))
            these_shots.append(shot(pos, (10 * orientation [0], -2)))
            these_shots.append(shot(pos, (11 * orientation [0], 1)))
            these_shots.append(shot(pos, (11 * orientation [0], -1)))
            these_shots.append(shot(pos, (12 * orientation [0], 0)))
    elif gun == 4:
            these_shots.append(shot(pos , (0, 8)))
            these_shots.append(shot(pos , (8, 0)))
            these_shots.append(shot(pos , (0, -8)))
            these_shots.append(shot(pos , (-8, 0)))
    return these_shots
    
#initiallize game variables
try:
    f = open('DATA\highest_scores.pic', 'rb')
except:
    highest_scores = [0, 0, 0]
    print 'file not found'
else:
    highest_scores = pic.load(f)
    print highest_scores
    print 'generated from file'
    f.close()
vector_orientation = [(0, 1), (1, 0), (0, -1), (-1, 0)]
screen_width = 1000
screen_height = 700
horizon = screen_height / 7
min_limit = (0, 0)
max_limit = (screen_width, screen_height - horizon)
red = (255, 0, 0)
light_red = (200, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
tansparent_blue = (0, 0, 255, 0.2)
green = (0, 255, 0)
terrain = (145, 230, 12)
terrain_dark = (125, 210, 2)
yellow = (255, 255, 0)
FPS = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
#superspeed = pygame.image.load('SPRITES\superspeed.png')
#stdcolor = superspeed.get_at((0, 0))
#for k in range(40):
    #for l in range(40):
        #color = superspeed.get_at((k, l))
        #if color == stdcolor:
            #superspeed.set_at((k, l), (255, 255, 255, 0))
gun_1 = pygame.image.load('SPRITES\pistola1.png')
x, y, w, h = gun_1.get_rect()
stdcolor = gun_1.get_at((0, 0))
for k in range(w):
    for l in range(h):
        color = gun_1.get_at((k, l))
        if color == stdcolor:
            gun_1.set_at((k, l), (255, 255, 255, 0))
gun_2 = pygame.image.load('SPRITES\pistola2.png')
x, y, w, h = gun_2.get_rect()
stdcolor = gun_2.get_at((0, 0))
for k in range(w):
    for l in range(h):
        color = gun_2.get_at((k, l))
        if color == stdcolor:
            gun_2.set_at((k, l), (255, 255, 255, 0))
gun_3 = pygame.image.load('SPRITES\pistola3.png')
x, y, w, h = gun_3.get_rect()
stdcolor = gun_3.get_at((0, 0))
for k in range(w):
    for l in range(h):
        color = gun_3.get_at((k, l))
        if color == stdcolor:
            gun_3.set_at((k, l), (255, 255, 255, 0))            
gun_4 = pygame.image.load('SPRITES\pistola4.png')
x, y, w, h = gun_4.get_rect()
stdcolor = gun_4.get_at((0, 0))
for k in range(w):
    for l in range(h):
        color = gun_4.get_at((k, l))
        if color == stdcolor:
            gun_4.set_at((k, l), (255, 255, 255, 0))

#initiallize elements variables variables
robots_killed = 0
robots_per_level = 12
bonus_t = 1500
gun_time = rnd.randint(0, 1000)
score = 0
level = 1
game_t = 0
level_t = 0
current_gun = 0
old_speed = 0
default_speed = 5
explosion = []
shots = []
robots = []
guns = []
announcements = []
robots.append(robot((10, 10), 'dumb'))
lucas = player((screen_width / 2, screen_height / 2))
smart_freq = 0.0
coward_freq = 0.0
new_robot_time = 240 - (200 * level / float(10 + level))


# show intro
menu('Welcome to LucasBot', ['Shoot the robots to get points. If a robot shoots you or crashes into you, you die.','Use the arrow keys to walk and the space bar to shoot.','Pick up weapons to improve your gun'], ['Play'], music = menu_sound)

background_sound.play(loops = -1)
game_exit = False
while not game_exit:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            game_exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lucas.shot = True
                shot_sound[current_gun].play()
                shots += new_shot((lucas.pos[0] + 12, lucas.pos[1] + 19), lucas.orientation, current_gun)
                old_speed = lucas.speed
                lucas.speed = 0
                lucas.t = 4                    
            elif event.key == pygame.K_UP:
                lucas.orientation = (0, -1)
                lucas.speed = default_speed
            elif event.key == pygame.K_DOWN:
                lucas.orientation = (0, 1)
                lucas.speed = default_speed
            elif event.key == pygame.K_RIGHT:
                lucas.orientation = (1, 0)
                lucas.speed = default_speed
            elif event.key == pygame.K_LEFT:
                lucas.orientation = (-1, 0)
                lucas.speed = default_speed            
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]:
                lucas.speed = 0
                old_speed = 0
                lucas.t = 0
            elif event.key == pygame.K_SPACE:
                lucas.speed = old_speed
                lucas.shot = False
                lucas.t = 0
                
    # colision checks
    # computing lucas target
    lucas_target = v_add(lucas.pos, v_divide(lucas.size, 2))
    # colision  beween robots and shots
    kill_all = False
    for i in range(len(robots)):
        robot_target = v_add(robots[i].pos, v_divide(robots[i].size, 2))
        for j in range(len(shots)):
            if v_module(v_substract(robot_target, shots[j].pos)) < robots[i].size[0] * 0.5:
                if robots[i].r_type == 'coward':
                    kill_all = True
                else:
                    robots[i].active = False
                    score += robots[i].score
                    robots_killed += 1
                    break
    if kill_all:
        for i in range(len(robots)):
            robots[i].active = False
            score += robots[i].score
            robots_killed += 1          
    for i in range(len(robots)):
        if not robots[i].active:
            bomb_sound.play(fade_ms = 500)
            explosion.append([derbis(v_add(robots[i].pos, v_divide(robots[i].size, 2))) for j in range(20)])
    if kill_all:
        new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
        while v_module(v_substract(lucas_target, new_robot_pos)) <= screen_width / 2:
            new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
        rnd_number = rnd.random()
        if rnd_number < coward_freq:
            robots.append(robot(new_robot_pos, 'coward'))
        elif rnd_number < smart_freq:
            robots.append(robot(new_robot_pos, 'smart'))
        else:
            robots.append(robot(new_robot_pos, 'dumb'))
        game_t = 0
    else:    
        for i in range(len(robots)):
            if not robots[i].active:    
                new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
                while v_module(v_substract(lucas_target, new_robot_pos)) <= screen_width / 2:
                    new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
                rnd_number = rnd.random()
                if rnd_number < coward_freq:
                    robots.append(robot(new_robot_pos, 'coward'))
                elif rnd_number < smart_freq:
                    robots.append(robot(new_robot_pos, 'smart'))
                else:
                    robots.append(robot(new_robot_pos, 'dumb'))
                game_t = 0

    
    # colisions between gun and lucas
    for i in range(len(guns)):
        gun_target = v_add(guns[i].pos, v_divide(guns[i].size, 2))
        if v_module(v_substract(lucas_target, gun_target)) <= lucas.size[0]:
            pick_coffin.play()
            current_gun = guns[i].tipo
            score += guns[i].score
            guns[i].active = False
    
    # colisiona bewteen robots and lucas
    for i in range(len(robots)):
        robot_target = v_add(robots[i].pos, v_divide(robots[i].size, 2)) 
        if v_module(v_substract(lucas_target, robot_target)) <= (robots[i].size[0] + lucas.size[0]) * 0.4:
            print lucas_target
            print robot_target
            print v_module(v_substract(lucas_target, robot_target))
            print robots[i].size[0]
            print lucas.size[0]
            
            lucas.active = False
            background_sound.stop()
            lose_sound.play()
    if not lucas.active:
        time.sleep(5)
        highest_scores.append(score)
        highest_scores.sort(reverse = True)
        highest_scores = highest_scores[:3]
        if menu('you have been killed',['your score is ' + str(score),'highest scores:', str(highest_scores[0]), str(highest_scores[1]), str(highest_scores[2]), ''],['Quit', 'Play again'], music = menu_sound) == 0:
            game_exit = True
        else:
            robots_killed = 0
            robots_per_level = 12
            bonus_t = 1500
            gun_time = rnd.randint(0, 1000)
            score = 0
            level = 1
            game_t = 0
            level_t = 0
            current_gun = 0
            old_speed = 0
            default_speed = 5
            explosion = []
            shots = []
            robots = []
            guns = []
            announcements = []
            robots.append(robot((10, 10), 'dumb'))
            lucas = player((screen_width / 2, screen_height / 2))
            smart_freq = 0.0
            coward_freq = 0.0
            new_robot_time = 240 - (200 * level / float(5 * level))
            background_sound.play(loops = -1)
        f = open('DATA\highest_scores.pic', 'wb')
        pic.dump(highest_scores, f)
        print highest_scores
        print 'dumped to file'
        
        f.close()

    # cleanup
    robots = [robots[i] for i in range(len(robots)) if robots[i].active] #cleans robots
    guns = [guns[i] for i in range(len(guns)) if guns[i].active] # clean guns
    explosion = [explosion[i] for i in range(len(explosion)) if len(explosion[i]) >0] # clean explossions
    shots = [shots[i] for i in range(len(shots)) if shots[i].active]  # clean shots
    announcements = [announcements[i] for i in range(len(announcements)) if announcements[i].active]  # clean announcements
    
    #level check
    game_t += 1
    level_t += 1
    if robots_killed >= level * robots_per_level:
        bonus = max(0, level * (bonus_t - level_t))
        score += bonus
        level += 1
        announcements.append(announcement(['CONGRATULATIONS! ', 'You have reached level ' + str(level), 'bonus: ' + str(bonus)], 100))
        gun_time = rnd.randint(100, 1000)
        new_robot_time = 240.0 - (200.0 * level / (5.0 * float(level)))
        smart_freq = 5.0 * level / 100.0
        
        if level <4:
            coward_freq = 0.0
        else:
            coward_freq = level / 100.0
        game_t = 0
        level_t = 0
        current_gun = 0
        old_speed = 0
        lucas.speed = 0
        guns = []
        if len(robots) > 1:
            robots = [robots[i] for i in range(1)]
    if level_t == gun_time:
        new_gun_pos = (rnd.randint(0, max_limit[0] -100), rnd.randint(0, max_limit[1] - 100))
        while v_module(v_substract(lucas_target, new_gun_pos)) <= screen_width / 2:
            new_gun_pos = (rnd.randint(0, max_limit[0] -100), rnd.randint(0, max_limit[1] - 100))
        random_number = rnd.randint(1, 4)
        guns.append(gun(new_gun_pos, random_number))
    if game_t > new_robot_time:
        new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
        while v_module(v_substract(lucas_target, new_robot_pos)) <= screen_width / 2:
            new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
        rnd_number = rnd.random()
        if rnd_number < coward_freq:
            robots.append(robot(new_robot_pos, 'coward'))
        elif rnd_number < smart_freq:
            robots.append(robot(new_robot_pos, 'smart'))
        else:
            robots.append(robot(new_robot_pos, 'dumb'))
        game_t = 0
        
    # draw the different elements on the screen
    screen.fill(terrain)
    draw_grid()
    
    for i in range(len(explosion)):
        for j in range(len(explosion[i])):
            explosion[i][j].update_pos()
        explosion[i] = [explosion[i][j] for j in range(len(explosion[i])) if explosion[i][j].active]
    
    for i in range(len(shots)):
        shots[i].update_pos()
      
    for i in range(len(robots)):
        robots[i].move(lucas.pos)
        robots[i].draw()
    for i in range(len(guns)):
        guns[i].update()
        guns[i].draw()           
    lucas.move()
    lucas.draw()
    for i in range(len(announcements)):
        announcements[i].update()
    pygame.display.update()            
    clock.tick(FPS)

pygame.quit()
quit()











        
