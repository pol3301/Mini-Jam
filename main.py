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
        self.og_rect = pygame.Rect((0, 0), size)
        self.display_rect = pygame.Rect((0, 0), size)

    def update_size(self, new_size):
        self.display_rect = self.og_rect.fit(pygame.Rect((0, 0), new_size))

    def render(self, screen: pygame.Surface):
        screen.blit(
            pygame.transform.scale(self.surface, self.display_rect.size),
            self.display_rect,
        )


dscreen = DisplayScreen(constants.SCREEN_SIZE)
game_state = "title_screen"
sysfont_10 = pygame.freetype.SysFont("arial", 10)
sysfont_20 = pygame.freetype.SysFont("arial", 20)
budget_30 = pygame.freetype.Font("assets/BUDGETSTEN-BLED.ttf", 30)
mont_30 = pygame.freetype.Font("assets/Mont-ExtraLightDEMO.otf", 30)
mont_bold_30 = pygame.freetype.Font("assets/Mont-HeavyDEMO.otf", 30)
mont_15 = pygame.freetype.Font("assets/Mont-ExtraLightDEMO.otf", 15)
mont_bold_15 = pygame.freetype.Font("assets/Mont-HeavyDEMO.otf", 15)

# current run data
dinos = []
money = 1000
reputation = 100
current_day = 1
party_contracts = []


# game state change
EVENT_GAME_STATE_CHANGE = pygame.event.custom_type()


class BasicSprite:
    def __init__(self, image, size, pos, is_centered=True):
        self.image = pygame.transform.scale(
            pygame.image.load(image).convert_alpha(), size
        )
        if is_centered:
            self.rect = self.image.get_rect(center=pos)
        else:
            self.rect = self.image.get_rect(topleft=pos)

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


# general dino structure
class DinoCharacter:
    def __init__(self, name, image, size, tier, traits, recruit_cost, duration):
        self.name = name
        self.image = pygame.transform.scale(
            pygame.image.load(image).convert_alpha(), (size, size)
        )
        self.tier = tier
        self.traits = traits
        self.recruit_cost = recruit_cost
        self.inital_duration = duration
        self.days_remaining = duration


class DinoInfoBox:
    def __init__(
        self,
        dino_character: DinoCharacter,
        rect_pos,
        rect_size,
        font: pygame.freetype.Font,
        bg_color,
        text_color,
    ):
        self.rect = pygame.rect.Rect((0, 0), rect_size)
        self.rect.center = rect_pos
        self.image = pygame.Surface(self.rect.size).convert_alpha()
        self.image.fill(bg_color)
        self.font = font
        self.text_color = text_color
        self.dino_c = dino_character
        self.visible = False

    def set_dino_character(self, dino_character: DinoCharacter):
        self.dino_c = dino_character

    def tick(self):
        pass

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        surface.blit(self.image, self.rect)
        x = self.rect.x + 10
        y = self.rect.y + 10
        spacing = 40

        self.font.render_to(
            surface, (x, y + 0 * spacing), f"Name: {self.dino_c.name}", self.text_color
        )
        self.font.render_to(
            surface, (x, y + 1 * spacing), f"Tier: {self.dino_c.tier}", self.text_color
        )
        self.font.render_to(
            surface,
            (x, y + 2 * spacing),
            f"Recruit Cost: {self.dino_c.recruit_cost}",
            self.text_color,
        )
        self.font.render_to(
            surface,
            (x, y + 3 * spacing),
            f"Contract Duration: {self.dino_c.days_remaining}",
            self.text_color,
        )
        self.font.render_to(
            surface, (x, y + 4 * spacing), f"Traits:  ", self.text_color
        )
        ix = x
        for i in self.dino_c.traits:
            ix += self.font.get_rect(None).right
            if ix >= self.rect.x + self.rect.w / 2:
                ix = x
                y += spacing
            # iy = y + 80 + self.font.get_rect(None).y
            self.font.render_to(
                surface, (ix, y + 4 * spacing), f"{i} ", self.text_color
            )
            ix += 10


example_dino = DinoCharacter(
    "Placeholder",
    "assets/dino_placeholder1.png",
    200,
    "Real",
    ["Dumb", "Stupid", "Jurassic"],
    50,
    3,
)


# shop code
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
            if self.dino_character.tier == "Real":
                self.rect.x += self.direction[0] * 2
                self.rect.y += self.direction[1] * 2
            elif self.dino_character.tier == "Costume":
                self.rect.x += self.direction[0] * 1
                self.rect.y += self.direction[1] * 1
            if current_tick >= self.stop_roam:
                self.state = "idle"
                self.next_roam = current_tick + random.randint(1000, 3000)

        if self.state == "idle":
            if current_tick >= self.next_roam:
                self.state = "roaming"
                self.stop_roam = current_tick + 250 * random.randint(1, 4)
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
        mont_bold_15.render_to(
            surface,
            (self.rect.left + 20, self.rect.bottom + 10),
            f"Cost: {self.dino_character.recruit_cost}",
            "white",
        )
        mont_bold_15.render_to(
            surface,
            (self.rect.left + 10, self.rect.bottom + 25),
            f"For: {self.dino_character.inital_duration} day(s)",
            "white",
        )
        if self.state == "idle" or self.dino_character.tier == "Cutout":
            surface.blit(self.image, self.rect)
        elif self.state == "roaming":
            tick_progress = pygame.time.get_ticks() - self.start_roam
            total = self.stop_roam - self.start_roam
            surface.blit(
                self.image,
                (
                    self.rect.x,
                    self.rect.y + 5 * math.sin((tick_progress / total) * math.pi * 6),
                ),
            )
        elif self.state == "grabbed":
            surface.blit(pygame.transform.rotate(self.image, 45), self.rect)


# admin phase code
class DinoInfoBlock:
    def __init__(self, pos, dino_character: DinoCharacter):
        self.rect = pygame.Rect(pos, (200, 100))
        self.dino_image = dino_character.image
        self.dino_character = dino_character
        self.name_text = BasicText(
            mont_15, (self.rect.x, self.rect.y), str(dino_character.name)
        )
        self.tier_text = BasicText(
            mont_15, (self.rect.x, self.rect.y + 20), str(dino_character.tier)
        )
        traits_text = ""
        for i in dino_character.traits:
            traits_text += f"{i}  "
        self.traits_text = BasicText(
            mont_15, (self.rect.x, self.rect.y + 40), str(traits_text)
        )
        self.days_text = BasicText(
            mont_15, (self.rect.x, self.rect.y + 60), str(dino_character.days_remaining)
        )
        self.selected = False

    def tick(self):
        pass

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, "white", self.rect)
        surface.blit(self.dino_image, self.rect)
        self.name_text.draw(surface)
        self.tier_text.draw(surface)
        self.traits_text.draw(surface)
        self.days_text.draw(surface)


class DinoList:
    def __init__(self, dino_character_list):
        self.dino_list = []
        for i in range(len(dino_character_list)):
            self.dino_list.append(DinoInfoBlock((0, i * 100), dino_character_list[i]))

    def tick(self):
        pass

    def draw(self, surface: pygame.Surface):
        for i in self.dino_list:
            i.draw(surface)


def adjust_pos_to_display(pos):
    ratio_x = dscreen.og_rect.w / dscreen.display_rect.w
    ratio_y = dscreen.og_rect.h / dscreen.display_rect.h
    adjusted_x = pos[0] - ((screen.get_width() - dscreen.display_rect.w) / 2)
    adjusted_y = pos[1] - ((screen.get_height() - dscreen.display_rect.h) / 2)
    adjusted_x = adjusted_x * ratio_x
    adjusted_y = adjusted_y * ratio_y
    return int(adjusted_x), int(adjusted_y)


# shop things
next_button = BasicSprite("assets/end_shop_button.png", (150, 120), (10, 550), False)
buy_basket = BasicSprite("assets/basket.png", (200, 200), (1100, 400))
money_count_text = BasicText(mont_bold_30, (10, 10), "0", "white")
shop_dinos = []
dino_info_box = DinoInfoBox(
    None, (640, 360), (450, 300), mont_bold_30, (0, 0, 0, 125), "white"
)
shop_floor = BasicSprite("assets/stone_floor.png", (1280, 720), (0, 0), False)

# admin phase things
dino_list = DinoList([])
gray_backdrop = BasicSprite("assets/backdrop.png", (1280, 720), (0, 0), False)


def generate_dinos(amount, day, reputation):
    cutouts = 0
    costumes = 0
    reals = 0

    quality = 0
    generated_dinos = []

    strong_traits = constants.dinosaur_characteristics
    weak_traits = constants.dinosaur_characteristics

    for i in range(amount):
        for i in range(day * int(reputation / 50)):
            quality += random.randint(3, 6)
        if random.randint(1, 10) == 10:
            reals += 1
        elif quality <= 70:
            cutouts += 1
        elif quality <= 140:
            costumes += 1
        elif quality > 140:
            reals += 1

    for i in range(cutouts):
        name = "Placeholder"
        image = "assets/dino_placeholder1.png"
        size = 150
        cost = random.randint(1, 3) * 5
        duration = random.randint(4, 8)
        traits = []
        for i in range(random.randint(3, 5)):
            if random.randint(1, 5) == 5:
                traits.append(random.choice(strong_traits))
                luck = random.randint(0, 3)
                if luck == 0:
                    cost = int(cost * 1.5)
                elif luck == 1:
                    duration -= 1
            else:
                traits.append(random.choice(weak_traits))
                luck = random.randint(0, 2)
                if luck == 0:
                    cost = int(cost * 0.8)
                elif luck == 1:
                    duration += 1
        if duration <= 0:
            duration = 1
        generated_dinos.append(
            DinoCharacter(name, image, size, "Cutout", traits, cost, duration)
        )

    for i in range(costumes):
        name = "Placeholder"
        image = "assets/dino_placeholder1.png"
        size = 175
        cost = random.randint(3, 6) * 10
        duration = random.randint(4, 6)
        traits = []
        for i in range(random.randint(3, 5)):
            if random.randint(1, 3) == 3:
                traits.append(random.choice(strong_traits))
                luck = random.randint(0, 2)
                if luck == 0:
                    cost = int(cost * 1.25)
                elif luck == 1:
                    duration -= 1
            else:
                traits.append(random.choice(weak_traits))
                luck = random.randint(0, 2)
                if luck == 0:
                    cost = int(cost * 0.7)
                elif luck == 1:
                    duration += 1
        if duration <= 0:
            duration = 1
        generated_dinos.append(
            DinoCharacter(name, image, size, "Costume", traits, cost, duration)
        )

    for i in range(reals):
        name = "Placeholder"
        image = "assets/dino_placeholder1.png"
        size = 200
        cost = random.randint(7, 15) * 10
        duration = random.randint(1, 3)
        traits = []
        for i in range(random.randint(4, 6)):
            if random.randint(1, 5) >= 3:
                traits.append(random.choice(strong_traits))
                luck = random.randint(0, 5)
                if luck == 0:
                    cost = int(cost * 1.2)
                elif luck == 1:
                    duration -= 1
            else:
                traits.append(random.choice(weak_traits))
                luck = random.randint(0, 1)
                if luck == 0:
                    cost = int(cost * 0.8)
                elif luck == 1:
                    duration += 1
        if duration <= 0:
            duration = 1
        generated_dinos.append(
            DinoCharacter(name, image, size, "Real", traits, cost, duration)
        )

    return generated_dinos


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
            for i in range(len(objects)):
                objects.pop(0)
            game_state = event.new_state
            if event.new_state == "phase_shop":
                objects.append(shop_floor)
                objects.append(buy_basket)
                for i in generate_dinos(random.randint(5, 10), current_day, reputation):
                    shop_dinos.append(
                        ShopDino(i, (random.randint(50, 900), random.randint(100, 620)))
                    )
                for i in shop_dinos:
                    objects.append(i)
                objects.append(next_button)
                objects.append(money_count_text)
                objects.append(dino_info_box)
                dino_info_box.set_dino_character(shop_dinos[0].dino_character)
            elif event.new_state == "phase_admin":
                dino_list = DinoList(dinos)
                objects.append(gray_backdrop)
                objects.append(dino_list)
                party_contracts = [party.Party(3), party.Party(5)]
                objects.append(party.PartyContractsList(party_contracts))

            elif event.new_state == "phase_results":
                test_party1 = party.Party(8)
                test_party2 = party.Party(8)
                test_party3 = party.Party(8)

                results = party.Results([test_party1, test_party2, test_party3])
                objects.append(results)

    if game_state == "title_screen":
        pygame.event.post(
            pygame.event.Event(EVENT_GAME_STATE_CHANGE, new_state="phase_shop")
        )

    elif game_state == "phase_shop":
        money_count_text.text = f"Money: {str(money)}"
        dino_info_box.visible = False
        for i in shop_dinos:
            if i.rect.collidepoint(mouse_pos) and mouse_just_pressed:
                i.grab()
                break
            elif not mouse_down and i.state == "grabbed":
                if (
                    buy_basket.rect.collidepoint(mouse_pos)
                    and i.dino_character.recruit_cost <= money
                ):
                    money -= i.dino_character.recruit_cost
                    dinos.append(i.dino_character)
                    shop_dinos.remove(i)
                    objects.remove(i)
                else:
                    i.state = "roaming"
            elif i.rect.collidepoint(mouse_pos):
                dino_info_box.set_dino_character(i.dino_character)
                dino_info_box.visible = True
            elif i.state == "grabbed" and mouse_down:
                dino_info_box.set_dino_character(i.dino_character)
                dino_info_box.visible = True

            i.tick(mouse_pos)
        if mouse_just_pressed and next_button.rect.collidepoint(mouse_pos):
            pygame.event.post(
                pygame.event.Event(EVENT_GAME_STATE_CHANGE, new_state="phase_admin")
            )

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
