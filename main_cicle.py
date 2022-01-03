import os
import sys
import pygame
import math


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
    def __init__(self, pos, color=pygame.Color('white'), speed=10, vector=math.pi * 3 / 4, radius=10, rico=9999):
        self.speed = speed
        self.rico = rico
        self.pos = pos
        self.vect = [math.cos(vector), math.sin(vector)]
        self.radius = radius
        self.color = color

    def move(self):
        self.pos = (self.pos[0] + int(self.vect[0] * 4), self.pos[1] - int(self.vect[1] * 4))
        pygame.draw.circle(screen, self.color, self.pos, self.radius, 0)


class Weapon:
    def __init__(self, x, y, sprite, shooting_sprite): # + sprite
        self.x, self.y = x, y
        self.spr = sprite
        self.shoot_spr = shooting_sprite

    def shoot(self, coords, mouse):
        global entity_list
        delta = (mouse[0] - coords[0], mouse[1] - coords[1])
        cos = delta[1] / math.sqrt(delta[1]**2 + delta[0]**2)
        color = (255, 255, 255)
        if delta[0] < 0:
            vec = math.asin(cos) + math.pi
        else:
            vec = math.asin(cos) * -1
        entity_list.append(Bullet(coords, color, vector=vec, radius=2))




class Entity:
    def __init__(self, max_health, sprite): # + sprite
        self.max_health, self.health = max_health, max_health
        self.spr = sprite
        self.V = [0, 0]  # y x

    def move(self):
        global t, screen
        screen.fill((0, 0, 0))
        x = self.spr.rect.x
        y = self.spr.rect.y
        x_pos, y_pos = (x + self.V[1] * t / 100), (y + self.V[0] * t / 100)
        self.spr.rect.x = x_pos
        self.spr.rect.y = y_pos
        #all_sprites.draw(screen)

    def change_v(self, yv, xv):
        if yv and not xv:
            self.V = [yv[0], self.V[1]]
        elif xv and not yv:
            self.V = [self.V[0], xv[0]]

    def get_v(self):
        return self.V

    def get_coords(self):
        return self.spr.rect.y, self.spr.rect.x

class Hero(Entity):
    pass



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('игра')
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    fps = 60
    #Ve = [0, 0, 0, 0]  # w s a d
    clock = pygame.time.Clock()
    f = False

    entity_list = []
    all_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Sprite()
    hero_sprite.image = load_image("dude.png", colorkey=-1)
    hero_sprite.rect = hero_sprite.image.get_rect()
    hero_sprite.rect.x = 5
    hero_sprite.rect.y = 20
    all_sprites.add(hero_sprite)
    all_sprites.draw(screen)
    wep = Weapon(1, 1, hero_sprite, hero_sprite)
    hero = Hero(20, hero_sprite)
    entity_list.append(hero)

    running = True
    while running:
        pygame.display.flip()
        t = clock.tick()
        for i in entity_list:
            i.move()
        clock.tick(fps)
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                hero.change_v([-300], [])
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                hero.change_v([0], [])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                hero.change_v([300], [])
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                hero.change_v([0], [])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                hero.change_v([], [-300])
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                hero.change_v([], [0])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                hero.change_v([], [300])
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                hero.change_v([], [0])
            if event.type == pygame.MOUSEBUTTONDOWN:
                f = True
            if f:
                y, x = hero.get_coords()
                wep.shoot((x + 10, y + 20), event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                f = False
    pygame.quit()

# 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
# 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
 # $ git config --global user.email 'mail@yourmail.ru'