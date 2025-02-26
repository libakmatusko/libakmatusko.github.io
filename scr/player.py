import pygame
import asyncio

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Rectangle shape
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.vertical_v = 0 #vertical veliocity for jumping and falling + for down, - for up

    def update(self, keys, platforms) -> int: #return how much to scroll
        JUMP_STRENGHT = 23

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        self.rect.y += self.vertical_v
        scroll = 0
        if self.rect.y < 400:
            scroll = 400 - self.rect.y
            self.rect.y += scroll
        self.vertical_v += 1

        if self.vertical_v > 0:
            for platform in platforms:
                if pygame.sprite.collide_rect(platform, self):
                    if self.rect.y < platform.rect.y + self.vertical_v:
                        self.rect.y = platform.rect.y - self.rect.height
                        self.vertical_v = -JUMP_STRENGHT
                        break
        return scroll
