import pygame
import asyncio
import sys
from platform import Platform
from player import Player
import random

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1280
FPS = 60
PLAYER_COLOR = (0, 128, 255)  # Blue
BACKGROUND_COLOR = (50, 50, 50)  # Dark gray
PLAYER_SIZE = 50
PLAYER_SPEED = 5

class Game:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        screen_width = info.current_w  # Get the current width
        screen_height = info.current_h  # Get the current height
        self.s_f = min(screen_height/SCREEN_HEIGHT, screen_width/SCREEN_WIDTH) * 0.90 #only in rendering

        self.screen = pygame.display.set_mode((SCREEN_WIDTH*self.s_f, SCREEN_HEIGHT*self.s_f), pygame.RESIZABLE)
        pygame.display.set_caption("Scaled Game Window")
        self.internal_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.objects = pygame.sprite.Group()
        self.objects.add(self.player)

        self.platforms = pygame.sprite.Group()
        base = Platform(719, 0, 1260, 1)
        self.objects.add(base)
        self.platforms.add(base)

        self.score = 0


        for i in range(30):
            base = Platform(219, random.randint(0, 200), 1260-200*i, 301)
            self.objects.add(base)
            self.platforms.add(base)

    async def run(self):
        while True:
            await self.handle_events()
            await self.update()
            self.draw()
            self.clock.tick(FPS)

            print(self.platforms)

    async def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    async def update(self):
        keys = pygame.key.get_pressed()
        scroll = self.player.update(keys=keys, platforms=self.platforms)  
        self.platforms.update(scroll_lenght=scroll, s_height=SCREEN_HEIGHT)
        self.score += scroll
        if self.player.rect.y > SCREEN_HEIGHT:
            self.player.kill() #dat koniec hry

    def draw(self):
        self.internal_surface.fill(BACKGROUND_COLOR)  # Fill the background
        self.objects.draw(self.internal_surface)
        scaled_surface = pygame.transform.scale(self.internal_surface, (SCREEN_WIDTH*self.s_f, SCREEN_HEIGHT*self.s_f))
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()  # Update the display