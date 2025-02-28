import pygame
import asyncio
from typing import Union

class Button:
    def __init__(self, screen, s_f, x:int, y:int, width:int, height:int, text:str, font,
        text_color:tuple[int, int, int]=(0, 0, 0),
        color:tuple[int, int, int]=(255, 255, 255),
        hover_color:Union[None, tuple[int, int, int]]=None,
        action=None
    ):
        self.screen = screen
        self.s_f = s_f
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.color = color
        if hover_color==None:
            self.hover_color = color
        else:
            self.hover_color = hover_color
        self.action = action  # Function to call when clicked

    def draw(self):
        mouse_pos = [x/self.s_f for x in pygame.mouse.get_pos()]
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(self.screen, color, self.rect, border_radius=10)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def check_click(self, pos):
        print(pos)
        if self.rect.collidepoint([x/self.s_f for x in pos]):
            if self.action:
                return self.action()
        return False


class EndScreen:
    def __init__(self, screen, s_f):
        self.screen = screen
        self.s_f = s_f
        self.font = pygame.font.Font(None, 36)
        self.buttons = []
        self.create_button(230, 800, 260, 100, 'Play again', self.font, hover_color=(255, 0, 0), action=lambda: 1)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        for button in self.buttons:
            button.draw()

    async def update(self):
        keys = pygame.mouse.get_pressed()
        if keys[0]:
            click_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                r = button.check_click(click_pos)
                if r:
                    return r

    def create_button(self, x:int, y:int, width:int, height:int, text:str, font,
        text_color:tuple[int, int, int]=(0, 0, 0),
        color:tuple[int, int, int]=(255, 255, 255),
        hover_color:Union[None, tuple[int, int, int]]=None,
        action=None
    ):
        self.buttons.append(Button(self.screen, self.s_f, x, y, width, height, text, font,text_color, color, hover_color, action))
