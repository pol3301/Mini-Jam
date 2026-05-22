import pygame
import random

import constants

# SCREEN_SIZE = (1280, 720)

dinosaur_characteristics = [
    "Tall", "Fast", "Flying", "Strong", "Herbivore", "Horns", "Water", "Armoured" 
]

class Kid:
    def __init__(self, favourite_ranking, is_host):
        self.favourite_characteristics = random.sample(dinosaur_characteristics, 2)
            
        self.favourite_ranking = favourite_ranking 
        self.is_host = is_host

class Dino:
    def __init__(self):
        self.base_earn = random.randint(2,9)
        
        self.characteristics = random.sample(dinosaur_characteristics, 2)

class Party:
    stage_path = "assets/stage.png"
    
    def __init__(self, kid_count, dino_count):
        self.party_kids = [Kid(1, True)]
        for i in range(kid_count - 1):
            self.party_kids.append(Kid(i + 2, False))
        self.party_dinos:list[Dino] = []

        for i in range(dino_count):
            self.party_dinos.append(Dino())
            
        self.stage = pygame.transform.scale(pygame.image.load(self.stage_path).convert_alpha(), constants.SCREEN_SIZE)

    def calculate_earn(self):
        party_earn = 0
        for kid in self.party_kids:
            personal_earn = 5
            
            for dino in self.party_dinos:
                dino_earn = dino.base_earn
                
                for characteristic in dino.characteristics:
                    for kid_fav_char in kid.favourite_characteristics:
                        if (characteristic == kid_fav_char):
                            dino_earn *= 2

                personal_earn += dino_earn
            
            personal_earn *= ((len(self.party_kids) - kid.favourite_ranking) / len(self.party_kids)) + 0.8
            party_earn += personal_earn

        return party_earn

    def draw_party(self, surface):
        self.draw_stage(surface)
        pass
        
    def draw_stage(self, surface):
        surface.blit(self.stage, self.stage.get_rect(topleft=(0,0)))
        pass
        
    def draw_audience(self):
        pass



#
# party_size = random.randint(3,8)
# party = Party(party_size, 3)
# for i in range(party_size):
#     print(party.party_kids[i].favourite_characteristics, party.party_kids[i].favourite_ranking, party.party_kids[i].is_host)
#
# print(party.calculate_earn())
