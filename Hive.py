import pygame

from enum import Enum
from Color import *
from Config import *

from Bee import Bee, Occupation


# Klasse Bienenstock
class Hive(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.food_count = 0  # Anzahl Nahrung im Bienenstock

        self.algorithm = Algorithm.ABC

        self.size = 75
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Macht das Rectangle im Hintergrund unsichtbar
        self.radius = self.size / 2
        pygame.draw.circle(self.image, BLACK, (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Gruppen der Bienen
        self.bees = pygame.sprite.Group()
        self.scout_bees = pygame.sprite.Group()
        self.employed_bees = pygame.sprite.Group()
        self.onlooker_bees = pygame.sprite.Group()
        self.dance_bees = pygame.sprite.Group()

    # Bienen werden nach Ratio erzeugt mit jeweiliger Occupation
    def create_bees(self):
        match self.algorithm:
            case Algorithm.ABC:
                self.bees.add([Bee(Occupation.SCOUT, self) for _ in range(BEES_SCOUT)])
                self.bees.add([Bee(Occupation.EMPLOYED, self) for _ in range(BEES_EMPLOYED)])
                self.bees.add([Bee(Occupation.ONLOOKER, self) for _ in range(BEES_ONLOOKER)])
                return self.bees
            case Algorithm.BEE:
                pass
            case Algorithm.NONE:
                pass

    def deposit(self, food_amount, sugar_amount):  # Nahrung wird an Bienenstock übergeben
        self.food_count = self.food_count + (food_amount * sugar_amount)
      

    def update(self):
        pass
        # print(f'Bees:{len(self.bees)}, SCOUT:{len(self.scout_bees)}, EMPLOYED:{len(self.employed_bees)}'
        #       f', ONLOOKER:{len(self.onlooker_bees)}, DANCERS:{len(self.dance_bees)}')

# Enum für Algorithmus
class Algorithm(Enum):
    ABC = 1
    BEE = 2
    NONE = 3

