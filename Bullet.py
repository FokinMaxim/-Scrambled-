from random import randint
import os
import sys
import pygame
import math

W_SIZE = 500, 350


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
        self.image = load_image("Bullet.png")

    def move(self):
        self.pos = (self.pos[0] + int(self.vect[0] * 4), self.pos[1] - int(self.vect[1] * 4))
        self.board_out()

    def board_out(self):
        if self.pos[0] - self.radius < 0:
            self.pos = (self.radius, self.pos[1])
            self.vect[0] *= -1
        elif self.pos[0] + self.radius > W_SIZE[0]:
            self.pos = (W_SIZE[0] - self.radius, self.pos[1])
            self.vect[0] *= -1
        if self.pos[1] - self.radius < 0:
            self.pos = (self.pos[0], self.radius)
            self.vect[1] *= -1
        elif self.pos[1] + self.radius > W_SIZE[1]:
            self.pos = (self.pos[0], W_SIZE[1] - self.radius)
            self.vect[1] *= -1


def moves(bullets):
    for i in bullets:
        i.move()


def render(scr, bullets):
    scr.fill((0, 0, 0))
    for i in bullets:
        pygame.draw.circle(scr, i.color, i.pos, i.radius, 0)
    pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption('Шарики')
    running = True
    screen = pygame.display.set_mode(W_SIZE)
    bullets = []
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                color = [randint(0, 255), randint(0, 255), randint(0, 255)]
                bullets.append(Bullet(event.pos, color, math.pi))
            if event.type == pygame.QUIT:
                running = False
        moves(bullets)
        render(screen, bullets)
        clock.tick(60)

main()