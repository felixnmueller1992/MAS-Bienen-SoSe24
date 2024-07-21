import math
import random

import pygame

from Algorithm import Algorithm
from Bee import Bee, Occupation
from Color import *
from Config import *


# Klasse Bienenstock
class Hive(pygame.sprite.Sprite):

    def __init__(self, x, y, algorithm='SUGAR'):
        super().__init__()
        self.x = x
        self.y = y
        self.food_count = 0

        self.algorithm = Algorithm[algorithm]

        self.size = 100
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
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

        # Dancefloor-Liste
        self.dancefloor_list = []

    # Bienen werden nach Ratio erzeugt mit jeweiliger Occupation
    def create_bees(self):
        match self.algorithm:
            case Algorithm.SUGAR:
                self.bees.add([Bee(Occupation.SCOUT, self) for _ in range(BEES_SCOUT)])
                self.bees.add([Bee(Occupation.ONLOOKER, self) for _ in range(BEES_ONLOOKER)])
                return self.bees
            case Algorithm.REPETITION:
                self.bees.add([Bee(Occupation.SCOUT, self) for _ in range(BEES_SCOUT)])
                self.bees.add([Bee(Occupation.ONLOOKER, self) for _ in range(BEES_ONLOOKER)])
                return self.bees
            case Algorithm.NONE:
                self.bees.add([Bee(Occupation.SCOUT, self) for _ in range(BEES_SCOUT)])
                self.bees.add([Bee(Occupation.SCOUT, self) for _ in range(BEES_ONLOOKER)])
                return self.bees

    # Nahrung wird an Bienenstock übergeben
    def deposit(self, food_amount, sugar_amount):
        self.food_count = self.food_count + (food_amount * sugar_amount)

    def find_dancefloor_position(self):
        # Wenn nach hundert Versuchen kein geeigneter Platz gefunden wurde, dann geben wir None als Dancefloor zurück
        # und die Biene tanzt nicht. Verhindert Endlosschleife beim Finden eines geeigneten Platzes im Hive.
        for i in range(100):
            pos_x = random.uniform(self.rect.left + DANCEFLOOR_RADIUS,
                                   self.rect.right - DANCEFLOOR_RADIUS)
            pos_y = random.uniform(self.rect.top + DANCEFLOOR_RADIUS,
                                   self.rect.bottom - DANCEFLOOR_RADIUS)

            if math.hypot(pos_x - self.rect.centerx, pos_y - self.rect.centery) <= self.radius - DANCEFLOOR_RADIUS:
                if not self.overlaps_with_existing_dancefloor(pos_x, pos_y):
                    return pos_x, pos_y

    def overlaps_with_existing_dancefloor(self, x, y):
        for dancefloor in self.dancefloor_list:
            distance = math.hypot(x - dancefloor.rect.centerx, y - dancefloor.rect.centery)
            # Wenn der Abstand geringer ist als die beiden Radien, dann überlappen sich die Tanzflächen.
            if distance < (DANCEFLOOR_RADIUS + dancefloor.radius):
                return True
        return False

    def create_dancefloor(self, dancer):
        position = self.find_dancefloor_position()
        if position:
            x, y = position
            new_dancefloor = Dancefloor(x, y, dancer)
            self.dancefloor_list.append(new_dancefloor)
            return new_dancefloor
        return None

    def remove_dancefloor(self, dancefloor):
        self.dancefloor_list.remove(dancefloor)

    def update(self):
        pass


# Klasse für Tanzflächen im Hive
class Dancefloor(pygame.sprite.Sprite):
    def __init__(self, x, y, dancer):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Macht das Rectangle im Hintergrund unsichtbar
        pygame.draw.circle(self.image, YELLOW, (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.dancer = dancer
        self.onlookers = []

    def add_onlooker(self, bee):
        if len(self.onlookers) < DANCEFLOOR_CAPACITY:
            for onlooker in self.onlookers:
                if pygame.sprite.collide_circle(bee, onlooker):
                    return False
            self.onlookers.append(bee)
            bee.watchfloor = self
            return True

    def clear_bees(self):
        for onlooker in self.onlookers:
            onlooker.evaluate_dance()
        self.onlookers.clear()
        self.dancer = None

    def update(self):
        pass