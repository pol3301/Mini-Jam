import pygame
import pygame.freetype
import math
import random


import constants

# SCREEN_SIZE = (1280, 720)


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


class Kid:
    def __init__(self, favourite_ranking, is_host):
        self.favourite_characteristics = random.sample(
            constants.dinosaur_characteristics, 2
        )

        self.favourite_ranking = favourite_ranking
        self.is_host = is_host
        self.audience_image = pygame.transform.scale(
            pygame.image.load("assets/kid1.png").convert_alpha(), (180, 180)
        )

    def draw(self, surface, x, y):
        surface.blit(self.audience_image, self.audience_image.get_rect(topleft=(x, y)))


class Dino:
    def __init__(self):
        self.base_earn = random.randint(2, 9)

        self.characteristics = random.sample(constants.dinosaur_characteristics, 2)


class Party:
    stage_path = "assets/stage.png"
    audience_path = "assets/audience.png"

    def __init__(self, price, budget: int, kid_count):
        self.price = price
        self.budget = budget

        self.party_kids = [Kid(1, True)]
        for i in range(kid_count - 1):
            self.party_kids.append(Kid(i + 2, False))
        self.party_dinos: list[Dino] = [Dino(), Dino(), Dino()]
        self.base_pay = 0
        self.host_name = "Henry"

        self.stage_image = pygame.transform.scale(
            pygame.image.load(self.stage_path).convert_alpha(), constants.SCREEN_SIZE
        )
        self.audience_image = pygame.transform.scale(
            pygame.image.load(self.audience_path).convert_alpha(),
            (1280 / 1.5, 720 / 1.5),
        )

    def set_dino(self, index, dino_character):
        self.party_dinos[index] = dino_character

    def calculate_tip(self):
        party_earn = 0
        for kid in self.party_kids:
            personal_earn = 5

            for dino in self.party_dinos:
                dino_earn = dino.base_earn

                for characteristic in dino.characteristics:
                    for kid_fav_char in kid.favourite_characteristics:
                        if characteristic == kid_fav_char:
                            dino_earn *= 2

                personal_earn += dino_earn

            personal_earn *= (
                (len(self.party_kids) - kid.favourite_ranking) / len(self.party_kids)
            ) + 0.8
            party_earn += personal_earn

        return party_earn

    def draw(self, surface):
        self.draw_stage(surface)
        self.draw_audience(surface)

    def draw_stage(self, surface):
        surface.blit(self.stage_image, self.stage_image.get_rect(topleft=(0, 0)))

    def draw_audience(self, surface):
        surface.blit(
            self.audience_image, self.audience_image.get_rect(topleft=(90, 420))
        )


class PartyContractsList:
    def __init__(self, parties, pos, is_owned=False):
        print("party contract list")
        self.party_box_list = []
        self.is_owned = is_owned
        self.pos = pos
        if is_owned:
            box_size = (630, 200)
        else:
            box_size = (1180, 200)
        for i in range(len(parties)):
            self.party_box_list.append(PartyBox(parties[i], i, box_size))

    def tick(self):
        pass

    def draw(self, surface: pygame.Surface):
        for i in self.party_box_list:
            i.draw(surface, self.pos[0], self.pos[1])


class PartyBox:
    def __init__(self, party: Party, index, size):
        self.party = party
        self.index = index
        self.size = size

    def draw(self, surface, x, starting_y):
        y = starting_y + 210 * self.index

        # rect = pygame.Rect(50, y, 1180, 200)
        pygame.draw.rect(surface, pygame.Color(31, 221, 255), ((x, y), self.size))
        self.draw_mugshot(surface, x + 30, starting_y + 10)
        self.draw_stats(surface, x + 230, starting_y + 10)

    def draw_mugshot(self, surface, x, starting_y):
        x, y = x, starting_y + 210 * self.index
        for kid in self.party.party_kids:
            if kid.is_host:
                kid.draw(surface, x, y)

    def draw_stats(self, surface, x, starting_y):
        sysfont_10 = pygame.freetype.SysFont("arial", 10)
        sysfont_20 = pygame.freetype.SysFont("arial", 20)

        y = starting_y + 210 * self.index
        name = BasicText(sysfont_20, (x, y), "Henry's party")
        y += 30
        budget = ""
        if self.party.budget == 0:
            budget = "Low"
        elif self.party.budget == 1:
            budget == "Average"
        elif self.party.budget == 2:
            budget == "High"
        elif self.party.budget >= 3:
            budget == "Endless"
        econ_stat = BasicText(sysfont_10, (x, y), f"Budget: {budget}")
        y += 20
        kid_count = BasicText(
            sysfont_10, (x, y), f"Number of Guests: {len(self.party.party_kids)}"
        )
        y += 20
        minimum_pay = BasicText(
            sysfont_10, (x, y), f"Pay (before tip): {self.party.price}"
        )
        y += 20

        host_favs = ""
        guest_favs_list = []
        guest_favs = ""
        for i in self.party.party_kids:
            if i.is_host:
                for j in i.favourite_characteristics:
                    host_favs += f"{j}  "
            else:
                for j in i.favourite_characteristics:
                    if not j in guest_favs_list:
                        guest_favs_list.append(j)
        for i in guest_favs_list:
            guest_favs += f"{i}  "

        host_fav_characteristics = BasicText(
            sysfont_10, (x, y), f"Henry likes dinos that are: {host_favs}"
        )
        y += 20
        guest_fav_characteristics = BasicText(
            sysfont_10, (x, y), f"The guests like dinos that are: {guest_favs}"
        )

        name.draw(surface)
        econ_stat.draw(surface)
        kid_count.draw(surface)
        minimum_pay.draw(surface)
        host_fav_characteristics.draw(surface)
        guest_fav_characteristics.draw(surface)


class Results:
    def __init__(self, parties: list[Party]):
        self.parties = parties

    def draw(self, surface: pygame.surface.Surface):

        for i, party in enumerate(self.parties):
            self.draw_mugshots(surface, i, party)
            self.draw_stats(surface, i, party)

    def draw_mugshots(self, surface: pygame.surface.Surface, i, party: Party):
        x, y = 70, 30 + 210 * i
        for kid in party.party_kids:
            if kid.is_host:
                kid.draw(surface, x, y)
                return
        pass

    def draw_stats(self, surface: pygame.surface.Surface, i, party: Party):
        font_10 = pygame.freetype.SysFont("arial", 10)
        font_20 = pygame.freetype.SysFont("arial", 20)

        tip = math.trunc(party.calculate_tip())

        y = 30 + 210 * i
        name_text = BasicText(font_20, (270, y), f"{party.host_name}'s party")
        y += 60
        base_pay_text = BasicText(font_10, (270, y), f"Base pay: {party.base_pay}")
        y += 20
        tip_pay_text = BasicText(font_10, (270, y), f"Tip pay: {tip}")
        y += 20
        total_pay_text = BasicText(
            font_10, (270, y), f"Total pay: {tip + party.base_pay}"
        )

        name_text.draw(surface)
        base_pay_text.draw(surface)
        total_pay_text.draw(surface)
        tip_pay_text.draw(surface)


#
# party_size = random.randint(3,8)
# party = Party(party_size, 3)
# for i in range(party_size):
#     print(party.party_kids[i].favourite_characteristics, party.party_kids[i].favourite_ranking, party.party_kids[i].is_host)
#
# print(party.calculate_earn())
