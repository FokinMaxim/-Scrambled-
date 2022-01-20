import pygame
import pytmx
import math
from nt_hero import Hero, Entity, Bullet, load_image



TILE_SIZE = 64
WIND_SIZE = WIND_WIDTH, WIND_HEIGHT = 1000, 1000
FPS = 80
MAPS_DIR = 'тайлы'

class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, shooting_im, *groups): # + sprite
        super().__init__(*groups)
        self.x, self.y = x, y
        self.image = load_image(sprite, -1)
        self.rect = self.image.get_rect().move((x, y))
        self.im = shooting_im


    def shoot(self, coords, mouse):
        global entity_list, moving_objects
        bullet_sprite = pygame.sprite.Sprite()
        bullet_sprite.image = load_image(self.im, colorkey=-1)
        bullet_sprite.rect = bullet_sprite.image.get_rect()
        moving_objects.add(bullet_sprite)

        delta = (mouse[0] - coords[0], mouse[1] - coords[1])
        cos = delta[1] / math.sqrt(delta[1]**2 + delta[0]**2)
        if delta[0] < 0:
            vec = math.asin(cos) + math.pi
        else:
            vec = math.asin(cos) * -1

        entity_list.append(Bullet(coords, bullet_sprite, vector=vec, speed=2))

    def change_coords(self, coords):
        self.rect.x, self.rect.y = coords


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__(all_sprites, floor_sprites)
        self.rect = pygame.Rect(x, y, size, size)


class Room:
    def __init__(self, filename):
        global TILE_SIZE, K_HEIGHT, K_WIDTH
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}")
        K_HEIGHT = self.height = self.map.height
        K_WIDTH = self.width = self.map.width
        TILE_SIZE = self.tile_size = self.map.tilewidth
        self.fset = 0, 0#((WIND_WIDTH - self.width * self.tile_size) // 2, (WIND_HEIGHT - self.height * self.tile_size) // 2)
        self.creating_sprites()

    def creating_sprites(self):
        for y in range(self.height):
            for x in range(self.width):
                a = self.get_tile_id((x, y))
                if a == 0:
                    Border(x * self.tile_size, y * self.tile_size, (1 + x) * self.tile_size, y * self.tile_size)
                    Border(x * self.tile_size, y * self.tile_size, x * self.tile_size, (1 + y) * self.tile_size)
                if a == 1:
                    Border(x * self.tile_size, y * self.tile_size, (1 + x) * self.tile_size, y * self.tile_size)
                if a == 2:
                    Border(x * self.tile_size, y * self.tile_size, (1 + x) * self.tile_size, y * self.tile_size)
                    Border((1 + x) * self.tile_size, y * self.tile_size, (x + 1) * self.tile_size,
                           (1 + y) * self.tile_size)
                if a == 6:
                    Border(x * self.tile_size, y * self.tile_size, x * self.tile_size,
                           (1 + y) * self.tile_size)
                if a == 8:
                    Border((1 + x) * self.tile_size, y * self.tile_size, (x + 1) * self.tile_size,
                           (1 + y) * self.tile_size)
                if a == 12:
                    Border(x * self.tile_size, (1 + y) * self.tile_size, (1 + x) * self.tile_size,
                           (1 + y) * self.tile_size)
                    Border(x * self.tile_size, y * self.tile_size, x * self.tile_size, (1 + y) * self.tile_size)
                if a == 13:
                    Border(x * self.tile_size, (1 + y) * self.tile_size, (1 + x) * self.tile_size,
                           (1 + y) * self.tile_size)
                if a == 14:
                    Border(x * self.tile_size, (1 + y) * self.tile_size, (1 + x) * self.tile_size,
                           (1 + y) * self.tile_size)
                    Border((1 + x) * self.tile_size, y * self.tile_size, (1 + x) * self.tile_size, (1 + y) * self.tile_size)
                if a in (3, 4, 5, 9, 10, 11, 15, 16, 17, 18, 21, 22, 23, 7, 27, 28, 29):
                    Floor(x * self.tile_size, y * self.tile_size, self.tile_size)

    def render(self, screen, pos):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size - pos[0] + self.fset[0],
                                    y * self.tile_size - pos[1] + self.fset[1]))

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)] - 1


def main():
    pygame.init()
    screen = pygame.display.set_mode(WIND_SIZE)

    room = Room('1.tmx')
    pos = [0, 0]
    wep_list = []

    clock = pygame.time.Clock()
    running = True
    gameover = False
    hero = Hero(120, (500, 500), 100, 'jo1.png', True, all_sprites, hero_sprite, moving_objects)
    entity_list.append(hero)
    wep = Weapon(500, 500, 'tomato_gun.png', 'tomato_bullet.png', all_sprites, moving_objects)
    wep_list.append(wep)
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                hero.vector_update(key)
            if event.type == pygame.KEYUP:
                key = pygame.key.get_pressed()
                hero.vector_update(key)
            if event.type == pygame.MOUSEMOTION:
                hero.img_update(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = hero.get_pos()
                hero.shoot((x + 35, y + 65), event.pos)
            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                for i in wep_list:
                    hero.equip(i)

        for i in entity_list:
            i.move()

        if len(pygame.sprite.spritecollide(hero, horizontal_borders, False, pygame.sprite.collide_rect)) == 0:
            hero.last_pos_y = hero.pos[1]
        else:
            hero.set_pos(hero.pos[0], hero.last_pos_y)
            print(1)
        if len(pygame.sprite.spritecollide(hero, vertical_borders, False, pygame.sprite.collide_rect)) == 0:
            hero.last_pos_x = hero.pos[0]
        else:
            hero.set_pos(hero.last_pos_x, hero.pos[1])

        screen.fill((8, 10, 10))
        room.render(screen, pos)
        hero_sprite.draw(screen)
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        moving_objects.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


entity_list = []
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
hero_sprite = pygame.sprite.Group()
floor_sprites = pygame.sprite.Group()
moving_objects = pygame.sprite.Group()
main()
