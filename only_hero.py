import os
import sys
import pygame
import math

FPS = 60
death = pygame.sprite.Group()
item_group = pygame.sprite.Group()


def ygol(vect):
    ax, ay = 1, 0
    bx, by = vect
    ma = math.sqrt(ax * ax + ay * ay)
    mb = math.sqrt(bx * bx + by * by) + 0.0001
    sc = ax * bx + ay * (-by)
    res = math.acos(sc / ma / mb) * 180 / math.pi
    if -by <= 0:
        res = 360 - res
    return res, bx >= 0


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


class Entity(pygame.sprite.Sprite):
    def __init__(self, speed, pos, health, image, vulnerability=True, *groups):
        super().__init__(*groups)#спрайт группы
        self.health = health
        self.speed = speed
        self.pos = pos
        self.vul = vulnerability
        self.image = load_image(image, -1)
        self.rect = self.image.get_rect().move(pos)
        self.vect = -1 # вектор передвижения (синус и косинус для скорости по x и y, -1 значит что вектора нет)

    def move(self):
        if self.vect != -1:
            vx = math.cos(self.vect) * self.speed
            vy = math.sin(self.vect) * self.speed
            self.pos = self.pos[0] + int(vx / FPS), self.pos[1] - int(vy / FPS)
            self.rect.move_ip(int(vx / FPS), -int(vy / FPS))

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.pos = x, y

    def damaged(self, damage):
        if self.vul:
            self.health -= damage
            if self.health <= 0:
                self.kill()# убит
                #TODO дорисовать смэрт


class Hero(Entity):
    def __init__(self, screen, speed, pos, health, image, money=0, vulnerability=True, *groups):
        super().__init__(speed, pos, health, image, vulnerability, *groups)
        self.hearts_points = int(self.health / 2)
        self.hearts = [load_image('heart1.png', -1), load_image('heart0.5.png', -1), load_image('heart0.png', -1),
                       load_image('money.png', -1)]
        self.last_pos_y = 0
        self.last_pos_x = 0
        self.armed = []
        self.screen = screen
        self.mon = money
        self.jo = [load_image('jo1.png', -1), load_image('jo2.png', -1), load_image('jo3.png', -1),
                   load_image('jo4.png', -1), load_image('jo5.png', -1), load_image('jo6.png', -1)]
        self.img_update([500, 500])

    def img_update(self, mpos):
        pos = (self.pos[0] + 24, self.pos[1] + 48)
        x = mpos[0] - pos[0]
        y = mpos[1] - pos[1]
        gip = (x ** 2 + y ** 2) ** (1/2)
        if not gip:
            gip = 0.0001
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
        if self.armed:
            i, left_right = ygol((mpos[0] - pos[0], mpos[1] - pos[1]))
            print(i)
            if left_right:
                self.armed[0].blitRotate(left_right, self.screen, (7, 20), i)
                self.armed[0].change_coords((self.pos[0] + 40, self.pos[1] + 70))
            else:
                self.armed[0].blitRotate(left_right, self.screen, (41, 20), i - 180)
                self.armed[0].change_coords((self.pos[0] + 6, self.pos[1] + 70))

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
                self.kill()# убит
                img = load_image('jorik.png', -1)
                sp = pygame.sprite.Sprite()
                sp.image = img
                sp.rect = sp.image.get_rect().move((self.pos[0], self.pos[1] + 48))
                death.add(sp)
                self.armed.clear()

    def equip(self, gun):
        x_e, y_e = self.rect.x, self.rect.y
        x_g, y_g = gun.rect.x, gun.rect.y
        delta = x_e - x_g + 5, y_e - y_g + 10
        print(delta)
        if delta[0] < 60 and delta[1] < 60:
            self.armed.append(gun)

    def shoot(self, mouse):
        if self.armed:
            self.armed[0].shoot(mouse)

    def draw_hearts(self):
        h = self.health
        for i in range(self.hearts_points):
            if h - i * 2 >= 2:
                self.screen.blit(self.hearts[0], (25 + i * 35, 25))
            elif h - i * 2 == 1:
                self.screen.blit(self.hearts[1], (25 + i * 35, 25))
            elif h - i * 2 <= 0:
                self.screen.blit(self.hearts[2], (25 + i * 35, 25))
        # рисовка МОНЕТОК
        self.screen.blit(self.hearts[3], (25, 65))
        font = pygame.font.Font(None, 40)
        text = font.render(str(self.mon), True, (255, 255, 255))
        text_x = 65
        text_y = 65
        self.screen.blit(text, (text_x, text_y))

    def move(self):
        if self.vect != -1:
            vx = math.cos(self.vect) * self.speed
            vy = math.sin(self.vect) * self.speed
            self.pos = self.pos[0] + int(vx / FPS), self.pos[1] - int(vy / FPS)
            self.rect.move_ip(int(vx / FPS), -int(vy / FPS))
