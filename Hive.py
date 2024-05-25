import pygame

from Color import *


# Klasse Bienenstock
class Hive(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.food_count = 0  # Anzahl Nahrung im Bienenstock
        self.scout_bees = 0  # Anzahl Scout Bienen dem Bienenstock zugewiesen
        self.dance_bees = 0  # Anzahl tanzende Bienen

        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Macht das Rectangle im Hintergrund unsichtbar
        pygame.draw.circle(self.image, BLACK, (25, 25), 25)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    # def draw(self, screen):  # Zeichne den Bienenstock
    #     pygame.draw.circle(screen, BLACK, (self.x, self.y), 25)

    def deposit(self, food_amount, sugar_amount):  # Nahrung wird an Bienenstock übergeben
        self.food_count = self.food_count + (food_amount * sugar_amount)

    def update(self):
        pass
