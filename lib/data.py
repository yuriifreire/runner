import pygame
from pygame import Rect,Surface
from pygame.locals import SRCALPHA

import os.path

data_dir = os.path.normpath(os.path.join(__file__,'..','..','data'))

def load_file(filename):
    name,dummy,ext = filename.partition('.')

    if ext == 'png':
        if 'Player' in name:
            images = {}
            images[False] = pygame.image.load(os.path.join(data_dir,(name+'-img.png')))
            images[True] = pygame.transform.flip(images[False],True,False)
            return images
        else:
            return pygame.image.load(os.path.join(data_dir,(name+'-img.png')))
    elif ext == 'wav':
        return pygame.mixer.Sound(os.path.join(data_dir,(name+'-snd.wav')))

def load_images():
    images = {}

    images['Terrain'] = {}

    images['Terrain'][False] = load_file('Terrain-Solid.png')
    images['Terrain'][True] = load_file('Terrain-Spikes.png')
    images['Terrain']['Goal'] = load_file('Goal.png')

    images['Player'] = {}
    images['Player']['Idle'] = load_file('Player-Idle.png')
    images['Player']['Jump'] = load_file('Player-Jump.png')
    images['Player']['Fall'] = load_file('Player-Fall.png')
    images['Player']['Dead'] = load_file('Player-Dead.png')

    images['Player']['Run'] = [load_file(('Player-Run-'+str(frame)+'.png')) for frame in range(1,3)]
    images['Player']['Walk'] = [load_file(('Player-Walk-'+str(frame)+'.png')) for frame in range(1,3)]

    images['Player']['Run'].insert(0,images['Player']['Idle'])
    images['Player']['Walk'].insert(0,images['Player']['Idle'])

    images['Digits'] = []

    digit_rect = Rect(0,0,5,8)
    digit_image = load_file('Digits.png')

    for digit_number in range(10):
        images['Digits'].append(Surface([5,8],SRCALPHA,32))
        images['Digits'][-1].blit(digit_image,[0,0],digit_rect)
        digit_rect.left = digit_rect.right
        digit_rect.left += 1

    images['Splash'] = {}

    images['Splash']['Logo'] = load_file('yuriifreire.png')
    images['Splash']['Title'] = load_file('Title.png')
    images['Splash']['Presents'] = load_file('Presents.png')
    images['Splash']['Press-Any-Key'] = load_file('Press-Any-Key.png')

    return images

def load_sounds():
    sounds = {}

    sounds['Game'] = {}
    sounds['Game']['Start'] = load_file('Game-Start.wav')
    sounds['Game']['Title'] = load_file('Game-Title.wav')

    sounds['Player'] = {}
    for sound_name in ['Jump','Land','Win','Die','Start']:
        sounds['Player'][sound_name] = load_file('Player-'+sound_name+'.wav')

    return sounds
