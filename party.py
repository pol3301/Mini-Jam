# import pygame
import random

dinosaur_characteristics = [
    "Tall", "Fast", "Flying", "Strong", "Herbivore", "Horns", "Water", "Armoured" 
]

class Kid:
    def __init__(self, favourite_ranking, is_host):
        characteristic1 = dinosaur_characteristics[random.randint(0,len(dinosaur_characteristics)-1)]
        characteristic2 = dinosaur_characteristics[random.randint(0,len(dinosaur_characteristics)-1)]
        while (characteristic1 == characteristic2):
            characteristic2 = dinosaur_characteristics[random.randint(0,len(dinosaur_characteristics)-1)]
        self.favourite_characteristics = [characteristic1, characteristic2]
            
        self.favourite_ranking = favourite_ranking 
        self.is_host = is_host
        pass

class Dino:
    def __init__(self):
        self.base_earn = random.randint(2,9)
        
        characteristic1 = dinosaur_characteristics[random.randint(0,len(dinosaur_characteristics)-1)]
        characteristic2 = dinosaur_characteristics[random.randint(0,len(dinosaur_characteristics)-1)]
        while (characteristic1 == characteristic2):
            characteristic2 = dinosaur_characteristics[random.randint(0,len(dinosaur_characteristics)-1)]
        self.characteristics = [characteristic1, characteristic2]
        
        pass

class Party:
    def __init__(self, kid_count):
        self.party_kids = [Kid(1, True)]
        for i in range(kid_count - 1):
            self.party_kids.append(Kid(i + 1, False))
        self.party_dinos:list[Dino] = []

        for i in range(4):
            self.party_dinos.append(Dino())

    def calculate_win(self):
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
            
            personal_earn *= (kid.favourite_ranking / len(self.party_kids)) + 0.8
            party_earn += personal_earn

        return party_earn



party_size = 5
party = Party(party_size)
# for i in range(party_size):
#     print(party.party_kids[i].favourite_characteristics, party.party_kids[i].favourite_ranking, party.party_kids[i].is_host)

print(party.calculate_win())
