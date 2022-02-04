import pygame
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import uic, QtWidgets
from only_hero import load_image
import sys
import sqlite3


FPS = 50
WIND_SIZE = WIND_WIDTH, WIND_HEIGHT = 1500, 900
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WIND_SIZE)


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    skale = 0.1
    while skale * WIND_WIDTH < WIND_WIDTH:
        skale += 1.25 / FPS
        fon = pygame.transform.scale(load_image('start.png'), (WIND_WIDTH * skale, WIND_HEIGHT * skale))
        screen.blit(fon, ((WIND_WIDTH - (WIND_WIDTH * skale))//2, (WIND_HEIGHT - (WIND_HEIGHT * skale))//2))
        pygame.display.flip()
        clock.tick(FPS)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 50 and event.pos[0] < 470:
                    if event.pos[1] > 255 and event.pos[1] < 370:
                        print('play')
                        return

                    elif event.pos[1] > 450 and event.pos[1] < 590:
                        records()
                        #return

                    elif event.pos[1] > 645 and event.pos[1] < 815:
                        print('esc')
                        terminate()


        pygame.display.flip()
        clock.tick(FPS)

def records():
    con = sqlite3.connect("game.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM records""").fetchall()
    if not result:
        result = [['Данных нет', 0]]

    skale = 0.1
    while skale * WIND_WIDTH < WIND_WIDTH:
        skale += 1.25 / FPS
        fon = pygame.transform.scale(load_image('rec.png'), (WIND_WIDTH * skale, WIND_HEIGHT * skale))
        screen.blit(fon, ((WIND_WIDTH - (WIND_WIDTH * skale))//2, (WIND_HEIGHT - (WIND_HEIGHT * skale))//2))
        pygame.display.flip()
        clock.tick(FPS)
    font = pygame.font.Font(None, 50)
    btm_rerun = pygame.sprite.Sprite()
    btms = pygame.sprite.Group()
    btms.add(btm_rerun)
    btm_rerun.image = load_image('menue.png')
    btm_rerun.rect = btm_rerun.image.get_rect().move((55, 750))
    #print(btm_main.rect, btm_rerun.rect)

    string_rendered = font.render('ЛИДЕРЫ', True, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = 100, 50
    x, y, add = 50, 100, 50
    screen.blit(string_rendered, intro_rect)

    result = sorted(result, key=lambda x: -1 * x[1])
    max_len = max([len(i[0]) for i in result])
    print(max_len)
    c = 10

    for line in result:
        if line[0] == 'Данных нет':
            string_rendered = font.render(line[0], True, pygame.Color('white'))
        else:
            help_str = ' '*(max_len-len(line[0]))
            s = line[0] + help_str
            print(s)
            string_rendered = font.render(f'{s}   {line[1]} очков', True, pygame.Color('white'))
        if c == 0:
            break
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = x, y + add
        add += 50
        screen.blit(string_rendered, intro_rect)
        c -= 1
    btms.draw(screen)
    con.commit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 55 and event.pos[0] < 255:
                    if event.pos[1] > 750 and event.pos[1] < 800:
                        start_screen()
                        return

        pygame.display.flip()
        clock.tick(FPS)

class Pre_play(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("name.ui", self)
        self.nam = ''
        self.but.clicked.connect(self.get_nam)

    def get_nam(self):
        self.nam = self.line.text()
        print(self.nam)
        return self.nam

def main():
    pygame.init()
    #app = QApplication(sys.argv)
    running = True
    start_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    #sys.exit(app.exec())


#main()