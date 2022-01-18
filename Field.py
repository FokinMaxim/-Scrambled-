import pygame
import pytmx
import random
from only_hero import Hero, Entity
from win32api import GetSystemMetrics


WIND_SIZE = WIND_WIDTH, WIND_HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1) - 60
FPS = 80
MAPS_DIR = 'тайлы'


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

    clock = pygame.time.Clock()
    running = True
    gameover = False
    hero = Hero(256, (500, 500), 10, 'jo1.png', True, all_sprites, hero_sprite)
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
        hero.move()
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
        hero.draw_hearts(screen)
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
hero_sprite = pygame.sprite.Group()
floor_sprites = pygame.sprite.Group()
main()
