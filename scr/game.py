import pygame
import asyncio
import sys
import random
from typing import Union
import json
import js
from pygbag.aio.fetch import RequestHandler
import time

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1280
FPS = 60
PLAYER_COLOR = (0, 128, 255)  # Blue
BACKGROUND_COLOR = (50, 50, 50)  # Dark gray
PLAYER_SIZE = 50
PLAYER_SPEED = 5


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Rectangle shape
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.vertical_v = 0 #vertical veliocity for jumping and falling + for down, - for up

    def update(self, platforms, power_ups, s_f) -> (int, int): #return how much to scroll
        JUMP_STRENGHT = 23
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        pressed, _, _ = pygame.mouse.get_pressed()

        if keys[pygame.K_LEFT] or (mouse_pos[0] < 360*s_f and pressed):
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] or (mouse_pos[0] > 360*s_f and pressed):
            self.rect.x += 5
        self.rect.y += self.vertical_v
        scroll = 0
        if self.rect.y < 400:
            scroll = 400 - self.rect.y
            self.rect.y += scroll
        self.vertical_v += 1

        self.rect.x = (self.rect.x + SCREEN_WIDTH) % SCREEN_WIDTH

        if self.vertical_v > 0:
            for platform in platforms:
                if pygame.sprite.collide_rect(platform, self):
                    if self.rect.y < platform.rect.y + self.vertical_v:
                        self.rect.y = platform.rect.y - self.rect.height
                        self.vertical_v = -JUMP_STRENGHT
                        break
        for power_up in power_ups:
            if pygame.sprite.collide_rect(power_up, self):
                if power_up.power == 'coin':
                    power_up.kill()
                    return (scroll, 500)

        return (scroll, 0)


class PowerUps (pygame.sprite.Group):
    def __init__(self, s_width:int=720):
        super().__init__()
        self.s_width = s_width
        self.scrolled = 0
        self.score = 0

    def update(self, scroll_lenght:int=0, s_height:int=128):
        self.scrolled += scroll_lenght
        if self.scrolled >= 2550:
            self.scrolled -= 2550
            self.add(Coin(random.randint(25, 695), -200+self.scrolled))

        for sprite in self.sprites():
            sprite.update(scroll_lenght=scroll_lenght, s_height=s_height)



class Coin (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (25, 25), 25)  # Gold color
        self.rect = self.image.get_rect(center=(x, y))
        self.power = 'coin'

    def update(self, scroll_lenght:int=0, s_height:int=128):
        self.rect.y += scroll_lenght
        if self.rect.y > s_height:
            self.kill()


class Platforms(pygame.sprite.Group):
    def __init__(self, s_width:int=720):
        super().__init__()
        self.s_width = s_width
        self.scrolled = 0
        self.score = 0
        for i in range(10):
            self.add(Platform(150, random.randint(0, s_width-450), i*200-200, 300))

    def update(self, scroll_lenght:int=0, s_height:int=128):
        self.scrolled += scroll_lenght
        self.score += scroll_lenght
        if self.scrolled >= 200:
            self.scrolled -= 200
            self.add(Platform(
                150,
                random.randint(150, self.s_width-300),
                -200+self.scrolled,
                300,
                pos=random.randint(0, 599),
                speed=random.gauss(1+(self.score/10000), 0.5*self.score/10000)
            ))

        for sprite in self.sprites():
            sprite.update(scroll_lenght=scroll_lenght, s_height=s_height)

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, x, y, range, pos=0, speed=1):
        super().__init__()
        self.image = pygame.Surface((width, 20))  # Rectangle shape
        self.image.fill((88, 57, 39))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.range = range
        self.pos = pos
        self.speed = speed
        self.x = self.rect.x


    def update(self, scroll_lenght:int=0, s_height:int=128):
        self.rect.y += scroll_lenght
        if self.rect.y > s_height:
            self.kill()
        if self.pos < self.range:
            self.x += self.speed
        else:
            self.x -= self.speed
        self.rect.x = self.x
        self.pos += 1
        self.pos %= self.range*2


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
        if self.rect.collidepoint([x/self.s_f for x in pos]):
            if self.action:
                return self.action()
        return False
    

class EndScreen:
    def __init__(self, screen, s_f, score=None, name='Meno...'):
        self.score = score
        self.screen = screen
        self.s_f = s_f
        self.font = pygame.font.Font(None, 36)
        self.name = name
        self.buttons = []
        self.leaderboard_menu = None
        self.log_in_menu = None

        self.focused = True

        self.create_button(230, 900, 260, 70, 'Play again', self.font, hover_color=(255, 0, 0), action=lambda: (1, self.name))
        self.create_button(200, 400, 320, 70, self.name, self.font, action=self.js_input)
        if score:
            self.create_button(200, 600, 320, 100, f'Score: {score}', pygame.font.Font(None, 72), text_color=(255, 255, 255), color=(0, 255, 0), action=lambda: 3)
        self.create_button(230, 700, 260, 100, '', pygame.font.Font(None, 72), text_color=(255, 255, 255), color=(0, 0, 0), action=lambda: 3)
        self.create_button(230, 500, 260, 70, 'Log in', self.font, action=lambda: 4)

        self.data_send()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        for button in self.buttons:
            button.draw()

    async def update(self):
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            return (1, self.name)
        keys = pygame.mouse.get_pressed()
        if keys[0] and self.focused:
            click_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                r = button.check_click(click_pos)
                if r:
                    return r
        elif not keys[0] and (not self.focused):
            self.focused = True
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

    def js_input(self):
        butt = self.buttons[1] #lebo pole s menom vytvaram ako druhe ale je to konkretny nie vseobecny pristup
        try:
            self.name = str(js.window.prompt("Enter your name:")).strip()
            if len(self.name) < 20:
                butt.text = self.name
                butt.action = None
            self.focused = False
        except AttributeError:
            print('js.window nefunguje')
    
    async def data_fetch(self):
        if self.score:
            handler = RequestHandler()
            try:
                response = await handler.post(
                    r'https://krabica.pythonanywhere.com/new_run',
                    data={'score':self.score, 'name':self.name}
                )
                if response:
                    response_data = json.loads(response)
                    rank = response_data.get('position')
                    self.buttons[3].text = f'rank: {rank}'
                    self.buttons[2].color = (255-max(255*self.score//response_data.get('max', self.score), 0), 255, 0)
                    self.buttons[2].hover_color = (255-max(255*self.score//response_data.get('max', self.score), 0), 255, 0)
                    self.buttons[2].text_color = (max(255*self.score//response_data.get('max', self.score), 0), )*3
                else:
                    print("POST Failed")
            except Exception as e:
                print("Failed to post data:", e)
            print('data fetched')
        else:
            print('score is None')

    def data_send(self):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.data_fetch())


class LeaderboardScreen:
    def __init__(self, screen, s_f, name='', color=(255, 255, 255)):
        self.screen = screen
        self.s_f = s_f
        self.name = name
        self.color = color
        self.scrolled = 0
        self.buttons = []
        self.leaderboard = [{'name':'. . .', 'score':-1}]
        self.font = pygame.font.Font(None, 36)

        self.create_button(150, 70, 40, 70, '#', pygame.font.Font(None, 54))
        self.create_button(190, 70, 190, 70, 'Name', pygame.font.Font(None, 54))
        self.create_button(380, 70, 190, 70, 'Score', pygame.font.Font(None, 54))

        self.create_button(670, 10, 40, 40, 'X', pygame.font.Font(None, 66), color=(255, 0, 0), action=lambda: 2)

        self.data_get()

    def draw(self):
        self.screen.fill((0, 0, 0))

        table = pygame.Surface((420, len(self.leaderboard) * 50))
        for i, entry in enumerate(self.leaderboard):
            rect = pygame.Rect(0, i*50, 38, 50)
            pygame.draw.rect(table, self.color if self.name==entry['name'] else (255, 255, 255), rect)
            text_surface = self.font.render(f'{i+1}.', True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            table.blit(text_surface, text_rect)

            
            rect = pygame.Rect(41, i*50, 188, 50)
            pygame.draw.rect(table, self.color if self.name==entry['name'] else (255, 255, 255), rect)
            text_surface = self.font.render(f'{entry['name']}', True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            table.blit(text_surface, text_rect)

            
            rect = pygame.Rect(231, i*50, 188, 50)
            pygame.draw.rect(table, self.color if self.name==entry['name'] else (255, 255, 255), rect)
            text_surface = self.font.render(f'{entry['score']}', True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            table.blit(text_surface, text_rect)
        self.screen.blit(table, (150, 150), (0, self.scrolled, 420, 1000))

        for button in self.buttons:
            button.draw()
        
    async def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self.scrolled -= event.y*15
        self.scrolled = max(min((len(self.leaderboard)-20)*50, self.scrolled), 0)

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
    
    async def data_fetch(self):
        handler = RequestHandler()
        try:
            response = await handler.get(
                r'https://krabica.pythonanywhere.com/leaderboard'
            )
            if response:
                self.leaderboard = json.loads(response)
            else:
                print("GET Failed")
        except Exception as e:
            print("Failed to get data:", e)
        print('data fetched')

    def data_get(self):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.data_fetch())


class LogInScreen:
    def __init__(self, screen, s_f, name):
        self.screen = screen
        self.s_f = s_f
        self.font = pygame.font.Font(None, 54)
        self.inputs = ['meno/email' if name in ('Meno...', '') else name, 'heslo']
        self.buttons = []

        self.create_button(200, 400, 320, 100, self.inputs[0], self.font, action=lambda: self.js_input(0))
        self.create_button(200, 550, 320, 100, self.inputs[1], self.font, action=lambda: self.js_input(1))
        self.create_button(200, 750, 320, 100, 'LOG IN', self.font, color=(118, 255, 3), action=lambda: asyncio.run(self.log_in()))
        self.create_button(200, 900, 320, 100, 'SIGN IN', self.font, color=(29, 233, 182), action=lambda: js.window.open(r'https://libakmatusko.github.io/sing_in', "_blank"))
        
        self.create_button(670, 10, 40, 40, 'X', pygame.font.Font(None, 66), color=(255, 0, 0), action=lambda: 2)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        for button in self.buttons:
            button.draw()

    async def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.log_in()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_pos = event.pos
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

    def js_input(self, i):
        butt = self.buttons[i] #lebo pole s menom vytvaram ako druhe ale je to konkretny nie vseobecny pristup
        try:
            self.inputs[i] = str(js.window.prompt("Enter here:")).strip()
            butt.text = self.inputs[i]
        except AttributeError:
            print('js.window nefunguje')
    
    async def log_in(self): # este sa nedaju robit konta
        if self.score:
            handler = RequestHandler()
            try:
                response = await handler.post(
                    r'https://krabica.pythonanywhere.com/new_run',
                    data={'score':self.score, 'name':self.name}
                )
                if response:
                    response_data = json.loads(response)
                    return 2
                else:
                    print("POST Failed")
            except Exception as e:
                print("Failed to post data:", e)
            print('data fetched')
        else:
            print('score is None')


class Game:
    def __init__(self):
        pygame.init()
        self.state = 2 #1 for playinf, 2 for end screen, 3 for leaderboard, 4 for log in
        self.menu = None

        info = pygame.display.Info()
        screen_width = info.current_w  # Get the current width
        screen_height = info.current_h  # Get the current height
        self.s_f = min(screen_height/SCREEN_HEIGHT, screen_width/SCREEN_WIDTH) * 0.90 #only in rendering

        self.screen = pygame.display.set_mode((SCREEN_WIDTH*self.s_f, SCREEN_HEIGHT*self.s_f), pygame.RESIZABLE)
        pygame.display.set_caption("Scaled Game Window")
        self.internal_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.menu = EndScreen(self.internal_surface, self.s_f)

        self.clock = pygame.time.Clock()
        self.timer = 0

        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.objects = pygame.sprite.Group()
        self.objects.add(self.player)

        self.platforms = Platforms(s_width=SCREEN_WIDTH)
        self.platforms.add(Platform(719, 0, 1260, 1))

        self.power_ups = PowerUps()

        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.name = ''

    async def run(self):
        while True:
            await asyncio.sleep(0)

            match self.state:
                case 1:
                    await self.handle_events()
                    await self.update()
                    self.draw()

                case 2 if self.menu != None:
                    match await self.menu.update():
                        case (1, name):
                            self.re_init(name=name)
                            continue
                        case 3:
                            self.menu.leaderboard_menu = LeaderboardScreen(self.internal_surface, self.s_f, self.name, self.menu.buttons[2].color)
                            self.state = 3
                            self.menu.leaderboard_menu.draw()
                            continue
                        case 4:
                            self.menu.log_in_menu = LogInScreen(self.internal_surface, self.s_f, name=self.menu.name)
                            self.state = 4
                            self.menu.log_in_menu.draw()
                    self.menu.draw()
                    
                case 3:
                    match await self.menu.leaderboard_menu.update():
                        case 2:
                            self.menu.leaderboard_menu = None
                            self.state = 2
                            continue
                    self.menu.leaderboard_menu.draw()
                
                case 4:
                    match await self.menu.log_in_menu.update():
                        case 2:
                            self.menu.log_in_menu = None
                            self.state = 2
                            continue
                    self.menu.log_in_menu.draw()

                case _:
                    Exception('game state not valid')
            scaled_surface = pygame.transform.scale(self.internal_surface, (SCREEN_WIDTH*self.s_f, SCREEN_HEIGHT*self.s_f))
            self.screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)

    async def handle_events(self):
        for event in pygame.event.get():        
            if self.timer==0:
                self.timer = pygame.time.get_ticks()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    async def update(self):
        scroll, bonus = self.player.update(platforms=self.platforms, power_ups=self.power_ups, s_f=self.s_f)
        self.score += bonus
        self.platforms.update(scroll_lenght=scroll, s_height=SCREEN_HEIGHT)
        self.power_ups.update(scroll_lenght=scroll, s_height=SCREEN_HEIGHT)
        self.score += scroll
        if self.player.rect.y > SCREEN_HEIGHT:
            await self.end()

    def draw(self):
        self.internal_surface.fill(BACKGROUND_COLOR)  # Fill the background

        self.platforms.draw(self.internal_surface)
        self.objects.draw(self.internal_surface)
        self.power_ups.draw(self.internal_surface)

        self.internal_surface.blit(self.font.render(f"Score: {self.score-(pygame.time.get_ticks()-self.timer)//200}", True, (255, 255, 255)), (10, 10))
    
    def re_init(self, name):
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.objects = pygame.sprite.Group()
        self.objects.add(self.player)

        self.platforms = Platforms(s_width=SCREEN_WIDTH)
        self.platforms.add(Platform(719, 0, 1260, 1))

        self.power_ups = PowerUps()

        self.score = 0
        self.timer = 0
        self.state = 1
        self.name = name
        del self.menu

    async def end(self):
        self.score -= (pygame.time.get_ticks()-self.timer)//200

        self.player.kill()
        for platform in self.platforms:
            platform.kill()

        

        self.state = 2
        self.menu = EndScreen(self.internal_surface, self.s_f, score=self.score, name=self.name)
