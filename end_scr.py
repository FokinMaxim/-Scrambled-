import pygame
from nt_hero import load_image
import sys
import sqlite3


FPS = 50
WIND_SIZE = WIND_WIDTH, WIND_HEIGHT = 900, 900
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WIND_SIZE)


def terminate():
    pygame.quit()
    sys.exit()

def end_screen(name, time, money, kills):
    con = sqlite3.connect("game.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM records""").fetchall()
    if not result:
        result = [0]
    intro_text = [("ВЫ ПРОИГРАЛИ...опять", (100, 80)),
                  (f"Времени просрано: {time}", (70, 240)),
                  (f"Нереальных денег: {money}", (70, 320)),
                  (f"Твои грехи: {kills}", (70, 400)),
                  (f"Результат: {money+2*kills}", (70, 520)),
                  (f"Сомнительное достижение: {max(result)[1]}", (500, 750))]

    fon = pygame.transform.scale(load_image('end.png'), (WIND_WIDTH * 0.75, WIND_HEIGHT * 0.75))
    help_spr = pygame.sprite.Sprite()
    help_spr.image = fon
    help_spr.rect = (0, WIND_HEIGHT * 0.125)
    fon_group = pygame.sprite.Group()
    fon_group.add(help_spr)

    pos = -(WIND_WIDTH * 0.75)
    while pos < WIND_WIDTH * 0.125:
        pos += int(300 / FPS)
        help_spr.rect = pos, WIND_HEIGHT * 0.125
        fon_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    font = pygame.font.Font(None, 25)
    for line in intro_text:
        string_rendered = font.render(line[0], True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = line[1][0] * 0.75 + WIND_WIDTH * 0.125, line[1][1]* 0.75 + WIND_HEIGHT * 0.125
        screen.blit(string_rendered, intro_rect)

    #cur.execute("""INSERT INTO records(nam, score) VALUES(?, ?)""", (name, money))
    con.commit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    running = True
    end_screen('dude', 200, 3300, 5)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

main()