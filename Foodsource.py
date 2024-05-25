import pygame
import random

from Config import *
from Color import *


# Klasse Futterquelle
class Foodsource(pygame.sprite.Sprite):
    def __init__(self, units, sugar, distance_to_hive, hive_x, hive_y):
        super().__init__()
        self.x = random.randint(50, SCREEN_WIDTH - 50)  # Zufällige Position X
        if self.x > hive_x - distance_to_hive and self.x < hive_x + distance_to_hive:  # Futterquelle ist zu nah am Bienenstock
            self.x = self.x + 2 * distance_to_hive  # Futterquelle vom Bienenstock wegschieben
        self.y = random.randint(50, SCREEN_HEIGHT - 50)  # Zufällige Posiition Y
        self.units = units  # Anzahl Futtereinheiten für diese Futterquelle
        self.sugar = sugar  # Anzahl Zucker für diese Futterquelle
        self.label_font = pygame.font.SysFont("Arial", 12)

        size = self.units * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Macht das Rectangle im Hintergrund unsichtbar
        pygame.draw.circle(self.image, GREEN, (size // 2, size // 2), self.units)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.update_labels()

    # Futterquelle und Labels zeichnen
    def update_labels(self):
        size = self.image.get_width()
        self.image.fill((0, 0, 0, 0))  # Macht das Rectangle im Hintergrund unsichtbar
        pygame.draw.circle(self.image, GREEN, (size // 2, size // 2), self.units)

        label_text_food = "Food value: " + str(self.units)
        label_surface_food = self.label_font.render(label_text_food, True, BLACK)
        food_rect = label_surface_food.get_rect(center=(size // 2, size // 2 - 10))  # Zentriert Label
        self.image.blit(label_surface_food, food_rect)

        label_text_sugar = "Sugar value: " + str(self.sugar)
        label_surface_sugar = self.label_font.render(label_text_sugar, True, BLACK)
        sugar_rect = label_surface_sugar.get_rect(center=(size // 2, size // 2 + 10))  # Zentriert Label
        self.image.blit(label_surface_sugar, sugar_rect)

    def update(self):
        self.update_labels()
        if self.units == 0:
            self.kill()

    def harvest(self, x):  # Biene erntet Futter von Futterquelle
        print(self.units)
        if x > self.units:  # Verbleibendes Futter ist kleiner als Bienenkapazität
            retval = self.units  # Es wird nur das verbleibende Futter entnommen
        else:
            retval = x  # Maximales Futter wird entnommen
        self.units = self.units - x  # Futtermenge von Futterquelle abziehen
        if self.units < 0:  # Negative Zahlen begrenzen
            self.units = 0
        return retval  # Tatsächlich gesammelte Futtermenge als Rückgabewert
