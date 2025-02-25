import pygame
import random
import asyncio

class Platforms(pygame.sprite.Group):
    def __init__(self, s_width:int=720):
        super().__init__()
        for i in range(10):
            self.add(Platform(150, random.randint(0, s_width-450), i*200, 300))

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, x, y, range):
        super().__init__()
        self.image = pygame.Surface((width, 20))  # Rectangle shape
        self.image.fill((88, 57, 39))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.range = range
        self.pos = 0


    def update(self, scroll_lenght:int=0, s_height:int=128):
        self.rect.y += scroll_lenght
        if self.rect.y > s_height:
            self.kill()
        if self.pos < self.range:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        self.pos += 1
        self.pos %= self.range*2
