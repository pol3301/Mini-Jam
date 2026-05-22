import pygame

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
EVENT_GAME_STATE_CHANGED = pygame.event.custom_type()

#shop code
class ShopDino:

    def __init__(self, image, pos):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def tick(self):
        pass

    def draw(self, surface):
        self.image.blit(surface, self.rect)

objects = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWSIZECHANGED:
            dscreen.update_size([event.x, event.y])
        if event.type == EVENT_GAME_STATE_CHANGED:
            game_state = event.new_state
            if event.new_state == "phase_shop":
                objects = []
                for i in range(5):
                    pass
                    #objects.append(ShopDino())
    
    if game_state == "title_screen":
        pygame.event.post(EVENT_GAME_STATE_CHANGED, new_state="phase_shop")
    elif game_state == "phase_shop":
        pass
    elif game_state == "phase_contracts":
        pass
    elif game_state == "phase_admin":
        pass
    elif game_state == "phase_results":
        pass

    screen.fill("black")
    dscreen.surface.fill("purple")

    dscreen.render(screen)
    pygame.display.flip()

    clock.tick(60)
    
pygame.quit()