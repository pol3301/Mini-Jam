import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

class DisplayScreen:
    def __init__(self, width, height):
        self.surface = pygame.Surface((width, height))
        self.og_rect = pygame.Rect((0,0), (width, height))
        self.display_rect = pygame.Rect((0,0), (width, height))
    
    def update_size(self, new_size):
        self.display_rect = self.og_rect.fit(pygame.Rect((0,0), new_size))

    def render(self, screen: pygame.Surface):
        screen.blit(pygame.transform.scale(self.surface, self.display_rect.size), self.display_rect)

dscreen = DisplayScreen(1280, 720)
game_state = "title_screen"

#game state change
EVENT_GAME_STATE_CHANGE = pygame.event.custom_type()

#shop code
class ShopDino:

    def __init__(self, image, size, pos):
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), size)
        self.rect = self.image.get_rect(center=pos)
        self.state = "roaming"
        self.next_roam = 0
        self.stop_roam = 0
        self.start_roam = 0
        self.direction = [0, 0]
    
    def grab(self):
        self.state = "grabbed"

    def tick(self):
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

    def draw(self, surface):
        if self.state == "idle":
            surface.blit(self.image, self.rect)
        elif self.state == "roaming":
            tick_progress = pygame.time.get_ticks() - self.start_roam
            total = self.stop_roam - self.start_roam
            surface.blit(self.image, (self.rect.x, self.rect.y + 5*math.sin((tick_progress/total)*math.pi*6)))
        elif self.state == "grabbed":
            surface.blit(pygame.transform.rotate(self.image, 45), self.rect)


objects = []

mouse_just_pressed = False
mouse_down = False

while running:
    mouse_pos = pygame.mouse.get_pos()
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
                    objects.append(ShopDino("assets/dino_placeholder1.png", (100, 100), (500, 500)))
    
    if game_state == "title_screen":
        pygame.event.post(pygame.event.Event(EVENT_GAME_STATE_CHANGE, new_state="phase_shop"))

    elif game_state == "phase_shop":
        for i in objects:
            if i.rect.collidepoint(mouse_pos) and mouse_just_pressed:
                i.grab()
                break
            i.tick()

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