import pygame
import asyncio
import sys
from platform import Platform, Platforms
from player import Player
from menus import EndScreen
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
        self.state = 2 #1 for playinf, 2 for end screen
        self.menu = None

        info = pygame.display.Info()
        screen_width = info.current_w  # Get the current width
        screen_height = info.current_h  # Get the current height
        self.s_f = min(screen_height/SCREEN_HEIGHT, screen_width/SCREEN_WIDTH) * 0.90 #only in rendering

        self.screen = pygame.display.set_mode((SCREEN_WIDTH*self.s_f, SCREEN_HEIGHT*self.s_f), pygame.RESIZABLE)
        pygame.display.set_caption("Scaled Game Window")
        self.internal_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.menu = EndScreen(self.internal_surface, self.s_f) #debuging

        self.clock = pygame.time.Clock()

        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.objects = pygame.sprite.Group()
        self.objects.add(self.player)

        self.platforms = Platforms(s_width=SCREEN_WIDTH)
        self.platforms.add(Platform(719, 0, 1260, 1))

        self.score = 0
        self.font = pygame.font.Font(None, 36)

    async def run(self):
        while True:
            await self.handle_events()

            match self.state:
                case 1:
                    await self.update()
                    self.draw()
                    self.clock.tick(FPS)
                case 2 if self.menu != None:
                    match await self.menu.update():
                        case 1:
                            self.re_init()
                            continue
                    self.menu.draw()
                    scaled_surface = pygame.transform.scale(self.internal_surface, (SCREEN_WIDTH*self.s_f, SCREEN_HEIGHT*self.s_f))
                    self.screen.blit(scaled_surface, (0, 0))
                    pygame.display.flip()
                    self.clock.tick(FPS)
                case _:
                    Exception('game state not valid')

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

        self.platforms.draw(self.internal_surface)
        self.objects.draw(self.internal_surface)

        self.internal_surface.blit(self.font.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))

        scaled_surface = pygame.transform.scale(self.internal_surface, (SCREEN_WIDTH*self.s_f, SCREEN_HEIGHT*self.s_f))
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()  # Update the display
    
    def re_init(self):
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.objects = pygame.sprite.Group()
        self.objects.add(self.player)

        self.platforms = Platforms(s_width=SCREEN_WIDTH)
        self.platforms.add(Platform(719, 0, 1260, 1))

        self.score = 0
        self.state = 1
        del self.menu