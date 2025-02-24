import pygame
import asyncio

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, x, y):
        super().__init__()
        self.image = pygame.Surface((width, 10))  # Rectangle shape
        self.image.fill((88, 57, 39))
        self.rect = self.image.get_rect(topleft=(x, y))