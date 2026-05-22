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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWSIZECHANGED:
            dscreen.update_size([event.x, event.y])

    dscreen.surface.fill("purple")

    dscreen.render(screen)
    pygame.display.flip()

    clock.tick(60)
    
pygame.quit()