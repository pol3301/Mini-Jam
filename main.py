import pygame
import pygame.freetype
import random
import math

import party
import constants


pygame.init()
pygame.freetype.init()
screen = pygame.display.set_mode(constants.SCREEN_SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

class DisplayScreen:
    def __init__(self, size):
        self.surface = pygame.Surface(size)
        self.og_rect = pygame.Rect((0,0), size)
        self.display_rect = pygame.Rect((0,0), size)
    
    def update_size(self, new_size):
        self.display_rect = self.og_rect.fit(pygame.Rect((0,0), new_size))

    def render(self, screen: pygame.Surface):
        screen.blit(pygame.transform.scale(self.surface, self.display_rect.size), self.display_rect)

dscreen = DisplayScreen(constants.SCREEN_SIZE)
game_state = "title_screen"
sysfont_10 = pygame.freetype.SysFont("arial", 10)
sysfont_20 = pygame.freetype.SysFont("arial", 20)

#current run data
dinos = []
money = 1000
reputation = 100
current_day = 1



#game state change
EVENT_GAME_STATE_CHANGE = pygame.event.custom_type()

class BasicSprite:
    def __init__(self, image, size, pos):
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), size)
        self.rect = self.image.get_rect(center=pos)
    def tick(self):
        pass
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class BasicText:
    def __init__(self, font: pygame.freetype.Font, pos, text, color="black"):
        self.font = font
        self.pos = pos
        self.text = text
        self.color = color
    def tick(self):
        pass
    def draw(self, surface):
        self.font.render_to(surface, self.pos, self.text, fgcolor=self.color)

#general dino structure
class DinoCharacter:
    def __init__(self, name, image, size, tier, traits, recruit_cost, duration):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (size, size))
        self.tier = tier
        self.traits = traits
        self.recruit_cost = recruit_cost
        self.inital_duration = duration
        self.days_remaining = duration

class DinoInfoBox:
    def __init__(self, dino_character: DinoCharacter, rect_pos, rect_size, font: pygame.freetype.Font, bg_color, text_color):
        self.rect = pygame.rect.Rect(rect_pos, rect_size)
        self.font = font
        self.rect_color = bg_color
        self.text_color = text_color
        self.dino_c = dino_character
    
    def set_dino_character(self, dino_character: DinoCharacter):
        self.dino_c = dino_character
    
    def tick(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.rect_color, self.rect)
        x = self.rect.x
        y = self.rect.y

        self.font.render_to(surface, (x, y+0), f"Name: {self.dino_c.name}", self.text_color)
        self.font.render_to(surface, (x, y+20), f"Tier: {self.dino_c.tier}", self.text_color)
        self.font.render_to(surface, (x, y+40), f"Recruit Cost: {self.dino_c.recruit_cost}", self.text_color)
        self.font.render_to(surface, (x, y+60), f"Contract Duration: {self.dino_c.days_remaining}", self.text_color)
        self.font.render_to(surface, (x, y+80), f"Traits:  ", self.text_color)
        ix = x
        for i in self.dino_c.traits:
            ix += self.font.get_rect(None).right
            #iy = y + 80 + self.font.get_rect(None).y
            self.font.render_to(surface, (ix, y+80), i, self.text_color)
            ix += 10

example_dino = DinoCharacter("Placeholder", "assets/dino_placeholder1.png", 200, "Real", ["Dumb", "Stupid", "Jurassic"], 50, 3)

#shop code
class ShopDino:

    def __init__(self, dino_character: DinoCharacter, pos):
        self.image = pygame.transform.scale(dino_character.image, (100, 100))
        self.dino_character = dino_character
        self.rect = self.image.get_rect(center=pos)
        self.state = "roaming"
        self.next_roam = 0
        self.stop_roam = 0
        self.start_roam = 0
        self.direction = [0, 0]
    
    def grab(self):
        self.state = "grabbed"

    def tick(self, mouse_pos):
        current_tick = pygame.time.get_ticks()

        if self.state == "roaming":
            self.rect.x += self.direction[0] * 2
            self.rect.y += self.direction[1] * 2
            if current_tick >= self.stop_roam:
                self.state = "idle"
                self.next_roam = current_tick + random.randint(1000, 3000)

        if self.state == "idle":
            if current_tick >= self.next_roam:
                self.state = "roaming"
                self.stop_roam = current_tick + 250*random.randint(1,4)
                self.start_roam = current_tick
                self.direction = [random.randint(-1, 1), random.randint(-1, 1)]
        
        if self.state == "grabbed":
            self.rect.center = mouse_pos
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1280:
            self.rect.right = 1280
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 720:
            self.rect.bottom = 720

    def draw(self, surface):
        sysfont_20.render_to(surface, (self.rect.centerx, self.rect.bottom + 20), f"Cost: {self.dino_character.recruit_cost}")
        sysfont_20.render_to(surface, (self.rect.centerx, self.rect.bottom + 50), f"Contract for: {self.dino_character.inital_duration} day(s)")
        if self.state == "idle":
            surface.blit(self.image, self.rect)
        elif self.state == "roaming":
            tick_progress = pygame.time.get_ticks() - self.start_roam
            total = self.stop_roam - self.start_roam
            surface.blit(self.image, (self.rect.x, self.rect.y + 5*math.sin((tick_progress/total)*math.pi*6)))
        elif self.state == "grabbed":
            surface.blit(pygame.transform.rotate(self.image, 45), self.rect)

def adjust_pos_to_display(pos):
    ratio_x = dscreen.og_rect.w / dscreen.display_rect.w
    ratio_y = dscreen.og_rect.h / dscreen.display_rect.h
    adjusted_x = pos[0] - ((screen.get_width() - dscreen.display_rect.w) / 2)
    adjusted_y = pos[1] - ((screen.get_height() - dscreen.display_rect.h) / 2)
    adjusted_x = adjusted_x * ratio_x
    adjusted_y = adjusted_y * ratio_y
    return int(adjusted_x), int(adjusted_y)

#shop things
next_button = BasicSprite("assets/end_shop_button.png", (250, 150), (500, 500))
buy_basket = BasicSprite("assets/basket.png", (200, 200), (1000, 500))
money_count_text = BasicText(sysfont_20, (10, 10), "0")
shop_dinos = []
dino_info_box = DinoInfoBox(None, (500, 500), (750, 500), sysfont_20, (0,0,0,125), "white")

objects = []

mouse_just_pressed = False
mouse_down = False

while running:
    mouse_pos = adjust_pos_to_display(pygame.mouse.get_pos())
    mouse_just_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWSIZECHANGED:
            dscreen.update_size([event.x, event.y])
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_just_pressed = True
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        if event.type == EVENT_GAME_STATE_CHANGE:
            game_state = event.new_state
            if event.new_state == "phase_shop":
                for i in range(5):
                    shop_dinos.append(ShopDino(example_dino, (random.randint(100, 1180), random.randint(50, 670))))
                for i in shop_dinos:
                    objects.append(i)
                objects.append(next_button)
                objects.append(buy_basket)
                objects.append(money_count_text)
                objects.append(dino_info_box)
                dino_info_box.set_dino_character(shop_dinos[0].dino_character)
    
    if game_state == "title_screen":
        pygame.event.post(pygame.event.Event(EVENT_GAME_STATE_CHANGE, new_state="phase_shop"))

    elif game_state == "phase_shop":
        money_count_text.text = str(money)
        for i in shop_dinos:
            if i.rect.collidepoint(mouse_pos) and mouse_just_pressed:
                i.grab()
                break

            if not mouse_down and i.state == "grabbed":
                if buy_basket.rect.collidepoint(mouse_pos) and i.dino_character.recruit_cost <= money:
                    money -= i.dino_character.recruit_cost
                    dinos.append(i.dino_character)
                    shop_dinos.remove(i)
                    objects.remove(i)
                else:
                    i.state = "roaming"
            elif i.rect.collidepoint(mouse_pos):
                dino_info_box.set_dino_character(i.dino_character)

            i.tick(mouse_pos)
        if mouse_just_pressed and next_button.rect.collidepoint(mouse_pos):
            pygame.event.post(pygame.event.Event(EVENT_GAME_STATE_CHANGE, new_state="phase_admin"))

    elif game_state == "phase_contracts":
        pass

    elif game_state == "phase_admin":
        pass

    elif game_state == "phase_results":
        pass

    screen.fill("black")
    dscreen.surface.fill("white")
    
    for i in objects:
        i.draw(dscreen.surface)

    dscreen.render(screen)
    pygame.display.flip()

    clock.tick(60)
    
pygame.quit()
