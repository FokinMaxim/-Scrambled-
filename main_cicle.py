import os
import sys
import pygame


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

class Weapon:
    def __init__(self, screen, x, y, sprite, shooting_sprite): # + sprite
        self.x, self.y = x, y
        self.spr = sprite
        self.shoot_spr = shooting_sprite
        self.V = [0, 0]  # y x

class Entity:
    def __init__(self, screen, x, y, max_health, sprite): # + sprite
        self.max_health, self.health = max_health, max_health
        self.x, self.y = x, y
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

    all_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Sprite()
    hero_sprite.image = load_image("mouse.png", colorkey=-1)
    hero_sprite.rect = hero_sprite.image.get_rect()
    hero_sprite.rect.x = 5
    hero_sprite.rect.y = 20
    all_sprites.add(hero_sprite)
    all_sprites.draw(screen)

    hero = Hero(hero_sprite)

    running = True
    while running:
        pygame.display.flip()
        t = clock.tick()
        hero.move()
        clock.tick(fps)
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                hero.change_v([-200], [])
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                hero.change_v([0], [])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                hero.change_v([200], [])
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                hero.change_v([0], [])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                hero.change_v([], [-200])
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                hero.change_v([], [0])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                hero.change_v([], [200])
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                hero.change_v([], [0])
    pygame.quit()

# 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
# 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
 # $ git config --global user.email 'mail@yourmail.ru'