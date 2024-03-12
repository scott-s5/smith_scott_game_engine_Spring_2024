# this file was created by Scott Smith

#Create a player class 

#Create a wall class 

#importing modules
import pygame as pg
from pygame.sprite import Sprite
from settings import * 

#creating player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        #instantiate super class
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE   
        self.speed = 300
        self.hitpoints = 100
        self.cooling = False
        # self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # self.running = True
    # def input(self):
    #     keys = pg.key.get_pressed()
    #     if keys[pg.K_LEFT]:
    #         print("I hit the left arrow...")
    #     if keys[pg.K_RIGHT]:
    #         print("I hit the right arrow...")7
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy   
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
    def collide_with_obj(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                effect = choice(POWER_UP_EFFECTS)
                self.game.cooldown.cd = 5
                self.cooling = True
                print(effect)
                print(self.cooling)
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

    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add x collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add y collision later
        self.collide_with_walls('y')
        self.collide_with_obj(self.game.power_ups, "powerup")
        # if self.game.cooldown.cd < 1:
        #     self.cooling = False
        # self.collide_with_obj(self.game.foods, "food")
        self.rect.width = self.rect.width
        self.rect.height = self.rect.height
        if not self.cooling:
            self.collide_with_obj(self.game.power_ups, True)
        # self.collide_with_obj(self.game.mobs, False)
        
#creating wall class
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class PowerUp(Sprite):
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.power_ups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Mob(Sprite):
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.mob
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x < self.game.player.rect.x:   
            self.vx = -100
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y < self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x 
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')




# g = Player(), Wall()

# g.run