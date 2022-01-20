import os
import sys
import pygame
import math

FPS = 60

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bullet:
    def __init__(self, pos, spr, speed=2, vector=math.pi * 3 / 4, rico=9999):
        self.speed = speed
        self.rico = rico
        self.pos = pos
        self.vect = [math.cos(vector) * speed, math.sin(vector) * speed]
        self.spr = spr
        self.spr.rect.x = pos[0]
        self.spr.rect.y = pos[1]

    def move(self):
        self.pos = (self.pos[0] + int(self.vect[0] * 4), self.pos[1] - int(self.vect[1] * 4))
        self.spr.rect.x, self.spr.rect.y = self.pos


class Entity(pygame.sprite.Sprite):
    def __init__(self, speed, pos, health, image, vulnerability=True, *groups):
        super().__init__(*groups)#спрайт группы
        self.armed = []
        self.health = health
        self.speed = speed
        self.pos = pos
        self.armed = []
        self.vul = vulnerability
        self.image = load_image(image, -1)
        self.rect = self.image.get_rect().move(pos)
        self.vect = -1 # вектор передвижения (синус и косинус для скорости по x и y)

    def move(self):
        if self.vect != -1:
            vx = math.cos(self.vect) * self.speed
            vy = math.sin(self.vect) * self.speed
            self.pos = self.pos[0] + int(vx / FPS), self.pos[1] - int(vy / FPS)
            print(self.pos, self.rect)
            self.rect.move_ip(int(vx / FPS), -int(vy / FPS))
            if self.armed:
                self.armed[0].change_coords((self.pos[0]+35, self.pos[1]+65))

    def equip(self, gun):
        x_e, y_e = self.rect.x, self.rect.y
        x_g, y_g = gun.rect.x, gun.rect.y
        delta = (abs(x_e - x_g + 5), abs(y_e - y_g + 10))
        print(delta)
        if delta[0] < 30 and delta[1] < 30:
            self.armed.append(gun)

    def shoot(self, coords, mouse):
        if self.armed:
            self.armed[0].shoot(coords, mouse)

    def get_pos(self):
        return self.pos

    def set_pos(self, x, y):
        print(self.pos, x, y)
        self.rect.x, self.rect.y = x, y
        self.pos = x, y

    def damaged(self, damage):
        if self.vul:
            self.health -= damage
            if self.health <= 0:
                self.kill()# убит


class Hero(Entity):
    def __init__(self, speed, pos, health, image, vulnerability=True,  *groups):
        super().__init__(speed, pos, health, image, vulnerability, *groups)
        self.hearts_points = int(self.health / 2)
        self.armed = []
        self.hearts = [load_image('heart1.png', -1), load_image('heart0.5.png', -1), load_image('heart0.png', -1)]
        self.last_pos_y = 0
        self.last_pos_x = 0
        self.jo = [load_image('jo1.png', -1), load_image('jo2.png', -1), load_image('jo3.png', -1),
                   load_image('jo4.png', -1), load_image('jo5.png', -1), load_image('jo6.png', -1)]

    def vector_update(self, keys):
        self.vect = -1
        if keys[pygame.K_w]:
            self.vect = 0.5 * math.pi
        if keys[pygame.K_a]:
            self.vect = 1 * math.pi
        if keys[pygame.K_d]:
            self.vect = 0 * math.pi
        if keys[pygame.K_s]:
            self.vect = 1.5 * math.pi
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.vect = 0.25 * math.pi
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.vect = 0.75 * math.pi
        if keys[pygame.K_s] and keys[pygame.K_a]:
            self.vect = 1.25 * math.pi
        if keys[pygame.K_s] and keys[pygame.K_d]:
            self.vect = 1.75 * math.pi

        if keys[pygame.K_v]:
            self.damaged(1)

    def damaged(self, damage):
        if self.vul:
            self.health -= 1
            if self.health <= 0:
                self.kill()  # убит
                # TODO можно нарисовать гробик


    def draw_hearts(self, screen):
        h = self.health
        for i in range(self.hearts_points):
            if h - i * 2 >= 2:
                screen.blit(self.hearts[0], (25 + i * 35, 25))
            elif h - i * 2 == 1:
                screen.blit(self.hearts[1], (25 + i * 35, 25))
            elif h - i * 2 <= 0:
                screen.blit(self.hearts[2], (25 + i * 35, 25))
            # TODO рисовка МОНЕТОК

    def img_update(self, mpos):
        pos = (self.pos[0] + 24, self.pos[1] + 48)
        x = mpos[0] - pos[0]
        y = mpos[1] - pos[1]
        gip = (x ** 2 + y ** 2) ** (1 / 2)
        si = y / gip
        co = x / gip
        if 0.5 <= co <= 1:
            if si <= 0:
                self.image = self.jo[2]
            else:
                self.image = self.jo[1]
        elif -0.5 >= co >= -1:
            if si <= 0:
                self.image = self.jo[4]
            else:
                self.image = self.jo[5]
        else:
            if si <= 0:
                self.image = self.jo[3]
            else:
                self.image = self.jo[0]
        self.rect = self.image.get_rect().move(self.pos)


class Enemy(Entity):
    def __init__(self, speed, pos, health, image, vulnerability=True,  *groups):
        super().__init__(speed, pos, health, image, vulnerability, *groups)
        self.hearts_points = int(self.health / 2)
        self.armed = []
        self.last_pos_y = 0
        self.last_pos_x = 0
        self.jo = [load_image('jo1.png', -1), load_image('jo2.png', -1), load_image('jo3.png', -1),
                   load_image('jo4.png', -1), load_image('jo5.png', -1), load_image('jo6.png', -1)]
