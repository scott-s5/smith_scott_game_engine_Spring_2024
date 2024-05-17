# This file was created by: Scott Smith
# sources: Mr. Cozort's github (direct), Mr. Cozort's github (reference), My code from last year (for using images & misc.)
# ... talking to Mr. Cozort for troubleshoot, classmate help, chatGPT (to be explained when used)

'''
goals: moving obstacles that kill player, 
+ force field protecting player, + winning sound+text+effect when all coins are collected
verbs: Walks (WIP)

beta goal: levels/secret levels (fixing animating sprites too)
'''
#import neccesary modules
import pygame as pg 
import sys
import random
import os
from settings import *
from sprites import *
from random import randint
from os import path 
from time import sleep
from math import floor

# Initializing the game class
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.mixer.init()
        sound_file1 = os.path.join(os.path.dirname(__file__), 'sounds', 'cleveland1.wav')
        sound_file2 = os.path.join(os.path.dirname(__file__), 'sounds', 'Magic.wav')
        sound_file3 = os.path.join(os.path.dirname(__file__), 'sounds', 'powerup.mp3')
        self.coin_sound = pg.mixer.Sound(sound_file1)
        self.win_sound = pg.mixer.Sound(sound_file2) 
        self.powerup_sound = pg.mixer.Sound(sound_file3)
        self.map_file = 'map.txt'  # Initial map file
        self.load_data()
        self.game_over = False
        self.win_sound_playing = False
        self.start_time = pg.time.get_ticks()
        self.time_limit = 30000

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        self.map_data = []
        self.total_coins = 0
        with open(path.join(game_folder, self.map_file), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
                self.total_coins += line.count('C')

    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            if self.game_over:
                print("Game over!")
                self.playing = False
                pg.quit()
                sys.exit()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        if self.total_coins == 0 and not self.win_sound_playing:
            self.win_sound.play()
            self.win_sound_playing = True
            self.map_file = 'map2.txt'  # Update to the next map
            self.load_data()  # Load the new map data
            self.new()  # Start a new game with the new map
            self.run()  # Run the new game

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        rainbow_index = (pg.time.get_ticks() // 100) % len(RAINBOW_COLORS)
        rainbow_color = RAINBOW_COLORS[rainbow_index]
        elapsed_time = pg.time.get_ticks() - self.start_time
        if self.total_coins == 0:
            if elapsed_time <= self.time_limit:
                self.draw_text(self.screen, "You unlocked secret level!", 64, rainbow_color, 9, 7)
            else:
                self.draw_text(self.screen, "You win! Loading next level!", 64, rainbow_color, 9, 7)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

g = Game()
while True:
    g.new()
    g.run()