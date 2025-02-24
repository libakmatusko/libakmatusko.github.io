# player.py
import pygame
import asyncio
from utils import load_image

class Player(pygame.sprite.Sprite):
    async def init(self, x, y):
        super().__init__()
        self.image = await load_image("assets/player.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
