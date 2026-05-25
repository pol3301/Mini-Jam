import pygame
import pygame.freetype
import math
import random


import constants

# SCREEN_SIZE = (1280, 720)

box_blue = pygame.Color(31, 221, 255)


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

    def __init__(self, base_pay, budget: int, kid_count):
        self.budget = budget

        self.party_kids = [Kid(1, True)]
        for i in range(kid_count - 1):
            self.party_kids.append(Kid(i + 2, False))
        #self.party_dinos: list[Dino] = [Dino(), Dino(), Dino()]
        self.party_dinos: list[Dino] = [None, None, None]
        self.base_pay = base_pay
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
        if len(self.party_dinos) == 0:
            return 0

        for kid in self.party_kids:
            personal_earn = 5

            for dino in self.party_dinos:
                if dino.tier == "Cutout":
                    dino_earn = 2
                elif dino.tier == "Costume":
                    dino_earn = 4
                elif dino.tier == "Real":
                    dino_earn = 6
                else:
                    print("FUCK")
                    dino_earn = 0

                for characteristic in dino.traits:
                    for kid_fav_char in kid.favourite_characteristics:
                        if characteristic == kid_fav_char:
                            dino_earn *= 2

                personal_earn += dino_earn

            personal_earn *= (
                (len(self.party_kids) - kid.favourite_ranking) / len(self.party_kids)
            ) + 0.8
            party_earn += personal_earn

        return party_earn

    def calculate_total(self):
        if len(self.party_dinos) == 0:
            return 0
        return self.base_pay + self.calculate_tip()

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
        self.party_box_list = []
        self.is_owned = is_owned
        self.pos = pos
        if is_owned:
            box_size = (630, 200)
        else:
            box_size = (1180, 200)
        for i in range(len(parties)):
            self.party_box_list.append(PartyBox(parties[i], i, box_size))
    
    def scroll(self, d_index):
        num_boxes = len(self.party_box_list)
        for i in self.party_box_list:
            i.index += d_index
            if i.index == num_boxes:
                i.index = 0
            elif i.index == -1:
                i.index = num_boxes - 1
            i.reassign_dino_pos()
    
    def set_party_dinos(self):
        for i in self.party_box_list:
            i.set_party_dinos()

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
        self.dino_blocks = [None, None, None]

    def draw(self, surface, x, starting_y):
        y = starting_y + 210 * self.index

        # rect = pygame.Rect(50, y, 1180, 200)
        pygame.draw.rect(surface, pygame.Color(31, 221, 255), ((x, y), self.size))
        self.draw_mugshot(surface, x + 30, starting_y + 10)
        self.draw_stats(surface, x + 230, starting_y + 10)
        self.draw_dinos(surface, x + 500, y + 10)
    
    def get_rect(self, list_x, list_y):
        y = list_y + 210 * self.index
        return ((list_x, y), self.size)

    def draw_mugshot(self, surface, x, starting_y):
        x, y = x, starting_y + 210 * self.index
        for kid in self.party.party_kids:
            if kid.is_host:
                kid.draw(surface, x, y)
    
    def assign_dino(self, dino_block_list, dino_info_block, dino_character):
        assignment = dino_info_block.assignment
        if assignment != None:
            dino_info_block.assignment[0].party.party_dinos[assignment[1]] = None

        index = -1
        if self.party.party_dinos[0] == None:
            self.party.party_dinos[0] = dino_character
            index = 0
        elif self.party.party_dinos[1] == None:
            self.party.party_dinos[1] = dino_character
            index = 1
        elif self.party.party_dinos[2] == None:
            self.party.party_dinos[2] = dino_character
            index = 2
        else:
            self.party.party_dinos = [None, None, None]
            dino_info_block.assignment = None
            for i in dino_block_list.dino_list:
                if i.assignment != None:
                    if i.assignment[0] == self:
                        i.assignment = None
            return
        
        topleft = self.get_rect(640, 10)[0]
        self.dino_blocks[index] = dino_info_block
        
        pos = (topleft[0] + 560 + 10, topleft[1] + 20 + index*30)
        dino_info_block.assignment = (self, index, pos)
    
    def reassign_dino_pos(self):
        topleft = self.get_rect(640, 10)[0]
        for i in range(len(self.party.party_dinos)):
            if self.party.party_dinos[i] != None:
                pos = (topleft[0] + 560 + 10, topleft[1] + 20 + i*30)
                self.dino_blocks[i].assignment = (self, i, pos)
    
    def set_party_dinos(self):
        self.party.party_dinos = []
        for i in self.dino_blocks:
            if i != None:
                self.party.party_dinos.append(i.dino_character)
    
    def draw_dinos(self, surface, starting_x, starting_y):
        sysfont_20 = pygame.freetype.SysFont("arial", 20)
        sysfont_20.render_to(surface, (starting_x, starting_y), "Dino 1: ")
        sysfont_20.render_to(surface, (starting_x, starting_y + 30), "Dino 2: ")
        sysfont_20.render_to(surface, (starting_x, starting_y + 60), "Dino 3: ")
        pygame.draw.rect(surface, "grey", ((starting_x + 60, starting_y), (20, 20)))
        pygame.draw.rect(surface, "grey", ((starting_x + 60, starting_y + 30), (20, 20)))
        pygame.draw.rect(surface, "grey", ((starting_x + 60, starting_y + 60), (20, 20)))

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
            sysfont_10, (x, y), f"Pay (before tip): {self.party.base_pay}"
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


class Star:
    def __init__(self):
        self.image = pygame.transform.scale(
            pygame.image.load("assets/star.png").convert_alpha(), (100, 100)
        )

    def draw(
        self,
        surface: pygame.Surface,
        x,
        y,
    ):
        surface.blit(self.image, self.image.get_rect(topleft=(x, y)))


class Results:
    def __init__(self, parties: list[Party]):
        self.parties = parties

    def draw(self, surface: pygame.surface.Surface):

        for i, party in enumerate(self.parties):
            y = 20 + 210 * i
            rect = pygame.Rect(50, y, 1180, 200)
            pygame.draw.rect(surface, box_blue, rect)

            self.draw_mugshots(surface, i, party)
            self.draw_stats(surface, i, party)
            self.draw_populartiy(surface, 5, i)

    def draw_mugshots(self, surface: pygame.Surface, i, party: Party):
        x, y = 70, 30 + 210 * i
        for kid in party.party_kids:
            if kid.is_host:
                kid.draw(surface, x, y)
                return
        pass

    def draw_stats(self, surface: pygame.Surface, i, party: Party):
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

        # TODO:

    def draw_populartiy(self, surface: pygame.Surface, popularity_rating: int, i):
        y = 80 + 210 * i
        for star in range(popularity_rating):
            x = 600 + 120 * star
            Star().draw(surface, x, y)



class Star:
    def __init__(self):
        self.image = pygame.transform.scale(
            pygame.image.load("assets/star.png").convert_alpha(), (100, 100)
        )

    def draw(
        self,
        surface: pygame.Surface,
        x,
        y,
    ):
        surface.blit(self.image, self.image.get_rect(topleft=(x, y)))


class Results:
    def __init__(self, parties: list[Party]):
        self.parties = parties

    def draw(self, surface: pygame.surface.Surface):

        for i, party in enumerate(self.parties):
            y = 20 + 210 * i
            rect = pygame.Rect(50, y, 1180, 200)
            pygame.draw.rect(surface, box_blue, rect)

            self.draw_mugshots(surface, i, party)
            self.draw_stats(surface, i, party)
            self.draw_populartiy(surface, 5, i)

    def draw_mugshots(self, surface: pygame.Surface, i, party: Party):
        x, y = 70, 30 + 210 * i
        for kid in party.party_kids:
            if kid.is_host:
                kid.draw(surface, x, y)
                return

    def draw_stats(self, surface: pygame.Surface, i, party: Party):
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
            font_10, (270, y), f"Total pay: {party.calculate_total()}"
        )
        y += 20
        if party.calculate_total() == 0:
            fail_text = BasicText(font_10, (270, y), "CONTRACT FAILED", "red")
            fail_text.draw(surface)


        name_text.draw(surface)
        base_pay_text.draw(surface)
        total_pay_text.draw(surface)
        tip_pay_text.draw(surface)

        # TODO:

    def draw_populartiy(self, surface: pygame.Surface, popularity_rating: int, i):
        y = 80 + 210 * i
        for star in range(popularity_rating):
            x = 600 + 120 * star
            Star().draw(surface, x, y)


#
# party_size = random.randint(3,8)
# party = Party(party_size, 3)
# for i in range(party_size):
#     print(party.party_kids[i].favourite_characteristics, party.party_kids[i].favourite_ranking, party.party_kids[i].is_host)
#
# print(party.calculate_earn())
