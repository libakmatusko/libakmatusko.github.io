import pygame
import asyncio

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, x, y):
        self.center = [x, y]