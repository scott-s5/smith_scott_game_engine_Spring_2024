# this file was created by Scott Smith

#importing modules
import pygame as pg
from pygame.sprite import Sprite
from settings import * 
import os 
import random
import time
from random import randint

#this makes it so that the image files can actually be drawn from the character folder in my game engine
# basically I drew the image idea from last years code, but I didn't import os so when I went to troubleshoot
# my code from chatGPT I was reminded that import os was missing and these lines of code were needed.
# not sure where to put it so it is here for now.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'characters')
SPRITESHEET = '....png'


#incorporating the spritesheet class to allow animated sprites
'''class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
        return image'''
#creating player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        # this also sets it up so that the Player class is actually shown as a png, from my characters folder
        # sets up the size of the tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'BronBron.png')).convert()
        self.image.set_colorkey(BLACK)
        '''
        # self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        # self.load_images()
        # self.image = self.standing_frames[0]  
        # self.rect = self.image.get_rect()
        # self.jumping = False
        # self.walking = False
        # self.current_frame = 0
        # self.last_update = 0
        # self.material = True
        '''
        self.rect = self.image.get_rect() 
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # sets the moneybag variable to 0, and makes sure invincibility is off (until activated)
        self.moneybag = 0
        self.invincible = False
        self.invincibility_duration = 0
        self.invincibility_timer = 0
 # this sets up the movement of the player class, so that when certain keys are pressed, certain 'movements' 
 # are executed
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    '''
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
    '''
 # this makes it so that when the player class interacts with the wall class (both horizontally and vertically),
 # the walls act as a wall and do not let the player through, or stop it. 
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
 #this covers the player class' interaction with all the other classes.
# First, if the player interacts with the coin class:
#  the counter goes up (drawn from the moneybag variable) and the coin collecting sound effect plays.
# Next, if the player hits the powerup, the powerup is applied and invincibility kicks on.
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                if self.game.total_coins > 0:
                    self.game.total_coins -= 1
                    self.game.coin_sound.play()
        if hits:
            if str(hits[0].__class__.__name__) == "PowerUp":
                hits[0].apply_power_up(self)
                self.game.powerup_sound.play()
    # clicks invincibility on when activated and sets a timer for how long it lasts. used pg.time for this.
    def active_invincibility(self):
        self.invinciblity = True
        self.invincibility_duration = 5000
        self.invincibility_timer = pg.time.get_ticks() 
 # update so that the player has its controls, collision with all groups including walls, and
    def update(self):
        '''self.animate()'''
        self.get_keys()
        '''self.chasing()'''
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        #  updated interaction so that when mobs reach player, the game ends, 
        # the 'if not' part of this was chatgpt that made my life endlessly easier, 
        # didn't know you could incorporate an if statement like this, makes it much easier to incorporate 
        # invincibility - now, in all other scenarios, collision with mob= game over, and with invincibility, that is false
        '!!!'
        if not self.invincible:
         mob_hits = pg.sprite.spritecollide(self, self.game.mobs, False)
         self.image = pg.image.load(os.path.join(img_folder, 'BronBron.png')).convert()   
         self.image.set_colorkey(BLACK)
         if mob_hits:
            print("Player collided w mob!")
            self.game.game_over = True
 # updated it so that when player interacts with coin, print "i got a coin" for my troubleshooting purposes, & sets the timer to decrease on its own and that
 # when the timer expires, invincibility ticks off (chat gpt helped me with the composition of that code - 
 # the equation showing 'now - timer >= duration' which is just the code checking when the timer exceedes 
 # the given 'duration', the invincibility ticks off)    
        coin_hits = pg.sprite.spritecollide(self, self.game.coins, True)
        if coin_hits:
            print("I got a coin")
        # powerup_hits = pg.sprite.spritecollide(self, self.game.power_ups, True)
        if self.invincible:
            now = pg.time.get_ticks()
            self.image = pg.image.load(os.path.join(img_folder, 'Broncavs.png')).convert()
            self.image.set_colorkey(BLACK)
            if now - self.invincibility_timer >= self.invincibility_duration:
                self.invinciblity = False
                self.image = pg.image.load(os.path.join(img_folder, 'BronBron.png')).convert()   
                self.image.set_colorkey(BLACK)
#sets up the wall class and its dimensions and color.
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
#sets up the coin class and uses pg.image to load a png from my characters foler as its image. sets up its dimensions
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'NBAtrophy.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    #sets up the mob class with ITS respective png as well as its speed.
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'steph.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
  #sets up its collision with walls interaction so that it can hit walls during gameplay.
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    # update method relating the mob class to the player so that it tries to approach player with its current speed.
    # runs collide with walls like previously set up.
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
#powerup class with its respective png and size, and also has the apply_power_up method 
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'kyrie.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        # defines what happens when the power up is applied (invincibility is ticked on)
    def apply_power_up(self, player):
        player.active_invincibility()
        player.invincible = True