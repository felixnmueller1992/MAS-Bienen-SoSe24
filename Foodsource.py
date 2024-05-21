import pygame
import random

from Config import *
from Color import *

# Klasse Futterquelle
class Foodsource:
    def __init__(self, units, sugar, distance_to_hive, hive_x, hive_y):
        self.x = random.randint(50, SCREEN_WIDTH - 50)  #Zufällige Position X
        if self.x > hive_x - distance_to_hive and self.x < hive_x + distance_to_hive:  #Futterquelle ist zu nah am Bienenstock
            self.x = self.x + 2 * distance_to_hive  #Futterquelle vom Bienenstock wegschieben
        self.y = random.randint(50, SCREEN_HEIGHT - 50)  #Zufällige Posiition Y
        self.units = units  #Anzahl Futtereinheiten für diese Futterquelle
        self.sugar = sugar  #Anzahl Zucker für diese Futterquelle
        self.label_font = pygame.font.SysFont("Arial", 12)  # Schriftart für das Label
        self.label_text_food = "Food value: " + str(units).encode("utf-8").decode(
            "utf-8")  # Text für das Label Futtereinheiten
        self.label_text_sugar = "Sugar value: " + str(sugar).encode("utf-8").decode(
            "utf-8")  # Text für das Label Zuckergehalt

    def draw(self, screen):  #Futterquelle und Labels zeichnen
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.units)  #Radius = Anzahl Futtereinheiten
        self.label_text_food = "Food value: " + str(self.units).encode("utf-8").decode(
            "utf-8")  # Text für das Label Futtereinheiten
        label_surface = self.label_font.render(self.label_text_food, True, BLACK)  # Label rendern
        screen.blit(label_surface, (self.x, self.y))  # Label auf den Bildschirm zeichnen
        self.label_text_sugar = "Sugar value: " + str(self.sugar).encode("utf-8").decode(
            "utf-8")  # Text für das Label Zuckergehalt
        label_surface = self.label_font.render(self.label_text_sugar, True, BLACK)  # Label rendern
        screen.blit(label_surface, (self.x, self.y + 10))  # Label auf den Bildschirm zeichnen

    def harvest(self, x):  #Biene erntet Futter von Futterquelle
        if x > self.units:  #Verbleidendes Futter ist kleine als Bienenkapazität
            retval = self.units  #Es wird nur das verbleibende Futter entnommen
        else:
            retval = x  #Maximales Futter wird entnommen
        self.units = self.units - x  #Futtermenge von Futterquelle abziehen
        if self.units < 0:  #Negative Zahlen begrenzen
            self.units = 0
        return retval  #Tasächlich gesammelte Futtermenge als Rückgabewert