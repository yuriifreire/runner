import pygame
from pygame.locals import *

pygame.mixer.pre_init(22050,-16,2,1024)
pygame.init()

from player import Player
from world import GameWorld

from data import load_images #,load_sounds
from display import draw_screen

from random import choice, randint

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode([350,250],0,32)
        pygame.display.set_caption('Runner -- A YuriiFreire Productions')

        self.image_set = data.load_images()
        self.sound_set = data.load_sounds()

        self.current_level = None
        self.player = None
        self.level_number = 0
        self.score = 0
        self.points_until_next_life = 25000
        self.lives_remaining = 3

        self.new_level()

        self.running = True

        self.status = 'Intro'
        self.controls = {'Left':False,'Right':False,'Run':False,'Jump':False}

        self.timer = pygame.time.Clock()

    def new_level(self):
        self.current_level = GameWorld(randint(10,25),self.image_set,self.sound_set,
                                Flat=0.05,Platform=0.75,Uneven=0.75,Platform_Chain=0.5)

        self.player = self.current_level.player

    def go(self):
        while self.running:
            self.timer.tick(30)
            self.step()

    def step(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.quit()
                self.running = False
                return None
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.quit()
                    self.running = False
                    return None
                
                elif event.key == K_LEFT:
                    self.controls['Left'] = True
                elif event.key == K_RIGHT:
                    self.controls['Right'] = True
                elif event.key == K_z:
                    self.controls['Jump'] = True
                elif event.key == K_x:
                    self.controls['Run'] = True
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.controls['Left'] = False
                elif event.key == K_RIGHT:
                    self.controls['Right'] = False
                elif event.key == K_z:
                    self.controls['Jump'] = False
                elif event.key == K_x:
                    self.controls['Run'] = False

        self.current_level.update(self.controls['Left'],
                    (self.controls['Right'] or self.controls['Left']),
                    self.controls['Run'], self.controls['Jump'])

        if self.player.rect.top > 300:
            if self.lives_remaining > 1:
                self.lives_remaining -= 1
                self.current_level.reset_player()
                self.player = self.current_level.player
            else:
                self.lives_remaining = 3
                self.sound_set['Game']['Start'].play()
                self.timer.tick(5)
                self.new_level()

        draw_screen(self.screen,self.current_level.area,self.player,
                    self.current_level.spike_tiles+self.current_level.terrain_tiles+[self.current_level.goal],None)

        if self.player.done:
            self.new_level()

        pygame.display.update()
        
