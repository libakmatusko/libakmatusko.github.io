# utils.py
import pygame
import asyncio

async def load_image(path):
    """Loads an image asynchronously (required for pygbag)."""
    while not pygame.image.get_extended():  # Ensure Pygame is initialized
        await asyncio.sleep(0.1)
    return pygame.image.load(path)

async def load_sound(path):
    """Loads a sound asynchronously (required for pygbag)."""
    while not pygame.mixer.get_init():
        await asyncio.sleep(0.1)
    return pygame.mixer.Sound(path)
