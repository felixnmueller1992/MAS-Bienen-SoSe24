import pygame
import random
import math

from Config import *
from Color import *


# Klasse Bienenstock
class Hive:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_count = 0  # Anzahl Nahrung im Bienenstock
        self.scout_bees = 0  # Anzahl Scout Bienen dem Bienenstock zugewiesen
        self.dance_bees = 0  # Anzahl tanzende Bienen

    def draw(self, screen):  # Zeichne den Bienenstock
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 25)

    def deliver(self, food_amount, sugar_amount):  # Nahrung wird an Bienenstock übergeben
        self.food_count = self.food_count + (food_amount * sugar_amount)
