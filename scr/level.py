# level.py
import pygame
import asyncio
from utils import load_image

class Level:
    async def init(self, background_path):
        self.background = await load_image(background_path)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
