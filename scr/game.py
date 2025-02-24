import pygame
import asyncio
import sys

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

        self.screen = pygame.display.set_mode((SCREEN_WIDTH*self.s_f, SCREEN_HEIGHT*self.s_f))
        self.clock = pygame.time.Clock()
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.vertical_v = 0 #vertical veliocity for jumping and falling + for down, - for up

    async def run(self):
        while True:
            await self.handle_events()
            await self.update()
            self.draw()
            self.clock.tick(FPS)

    async def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    async def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_pos[0] -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player_pos[0] += PLAYER_SPEED
        self.player_pos[1] += self.vertical_v
        self.vertical_v += 1
        if self.player_pos[1] >= SCREEN_HEIGHT - PLAYER_SIZE:
            self.vertical_v = -30

        # Keep player within screen bounds
        self.player_pos[0] = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, self.player_pos[0]))
        self.player_pos[1] = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, self.player_pos[1]))

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)  # Fill the background
        pygame.draw.rect(self.screen, PLAYER_COLOR, (*[x*self.s_f for x in self.player_pos], PLAYER_SIZE*self.s_f, PLAYER_SIZE*self.s_f))  # Draw player
        pygame.display.flip()  # Update the display