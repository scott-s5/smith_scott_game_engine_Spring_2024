# This file was created by: Scott Smith
# sources: Mr. Cozort's github (direct), Mr. Cozort's github (reference), My code from last year (for using images & misc.)
# ... talking to Mr. Cozort for troubleshoot, classmate help, chatGPT (to be explained when used)

'''
goals: moving obstacles that kill player, 
+ force field protecting player, + winning sound+text+effect when all coins are collected
verbs: Walks (WIP)
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
#initilizing the game class
class Game:
# Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        # setting the code so that it draws from the .wav files in my sounds folder in my game engine. 
        # also using pg.mixer to essentially make the sound play
        # looked at Mr. Cozort's code to see how he did sounds, then used chatGPT to integrate what he did into
        # my code specifically, and it proved mostly unhelpful, so I manually separated the sound files into 
        # different lines of code rather than a megafolder like it tried to have me do.
        pg.mixer.init()
        sound_file1 = os.path.join(os.path.dirname(__file__), 'sounds', 'cleveland1.wav')
        sound_file2 = os.path.join(os.path.dirname(__file__), 'sounds', 'Magic.wav')
        sound_file3 = os.path.join(os.path.dirname(__file__), 'sounds', 'powerup.mp3')
        self.coin_sound = pg.mixer.Sound(sound_file1)
        self.win_sound = pg.mixer.Sound(sound_file2) 
        self.powerup_sound = pg.mixer.Sound(sound_file3)
        # self.game_over = false  just shows that the game is being played and isn't over, &
        # win_sound shows that the win sound isn't playing during start of game.
        # (working on it so that when game is over-> things happen)
        self.load_data()
        self.game_over = False
        self.win_sound_playing = False
    #runs the data from other files, like the map. also sets up total_coins (I'll go over later)
    def load_data(self):
        game_folder = os.path.dirname(__file__)
        self.map_data = []
        self.total_coins = 0
        #this essentially checks the map for how many coins are currently in the game and makes that the total
        # coin count (ChatGPT helped me with the 'linecount'; basically it's easier to count down from the amount
        # of total coins than use moneybag for the feature I am about to use)
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
                self.total_coins += line.count('C')

    #tells the game class all the other sprites that in the game
    # also names the sprite classes so that the can be inserted into the map easily
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
        # # Create run method which runs the whole GAME
        # makes it so that if the code ever encounters a scenario in which game_over is executed, the game 
        # literally closes (print function is for debugging)
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
        # makes it so that when the game ends, the game - ends, essentially
    def quit(self):
      pg.quit()
      sys.exit()
   # neccesary function so that the sprites can run. also sets up the 'winning' sound effect-
   #  when the coins left hits 0, the winning sound can play
    def update(self):
        self.all_sprites.update()
        if self.total_coins == 0 and not self.win_sound_playing:
            self.win_sound.play()
            self.win_sound_playing = True


    #setting up the game screen when the code is actually ran, including the text aspect and tne games dimensions
    # also sets it up so that the existing sprites are actually drawn within the game
    # uses pg.font to give the code a font to draw with, and sets up the size of that text.
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
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
        # sets up using the text within pg.font and draw_text
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            #this displays the number of coins *collected* via the moneybag variable using draw_text
            self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
            #this displays a winning screen text using draw-text
            if self.total_coins == 0:
                self.draw_text(self.screen, "You win!", 64, GREEN, 13, 12)

            pg.display.flip()
 # makes it so that in the event of an attempt to quit the game is executed, the game.. actually quits.

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
# I have instantiated the game
g = Game()
# g.show_start_screen()
#I told the game to run.
while True:
    g.new()
    g.run()