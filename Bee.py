import pygame
import random
import math

from Config import *
from Color import *

from enum import Enum


# Bienenklasse
class Bee(pygame.sprite.Sprite):
    def __init__(self, occupation, hive):
        super().__init__()
        self.x = hive.x  # Startposition X im Bienenstock
        self.y = hive.y  # Startposition Y im Bienenstock
        self.hive = hive
        self.occupation = None  # Occupation muss initialisiert werden
        self.change_occupation(occupation)  # Status der Biene: 0 = Scout , 1 = employed , 2 = onlooker , 3 = to_home ,
        # 4 = Biene ist im Stock
        self.speed = random.randint(MIN_VELOCITY_BEE, MAX_VELOCITY_BEE)  # Zufällige Geschwindigkeit
        self.orientation = random.uniform(0.0, 360.0)  # Zufällige Start-Orientierung
        self.capacity = 0  # Aktuelle tragende Nahrungsanzahl der Biene
        self.destination = 0, 0, 0  # Koordinaten und Zuckergehalt des Ziels
        self.foodsource = None  # Futterquelle an der die Biene employed ist oder die sie gefunden hat
        self.dance_information = 0.0, 0.0, 0, 0  # Koordinaten X/Y, Zuckergehalt und übrige Menge der gefunden
        # Nahrungsquelle
        self.steps = 0  # Anzahl Schritte bevor die Biene zum Bienenstock zurückkehren muss (auch ohne Futter)
        self.dance_counter = 0  # Counter wie lange die Biene tanzen darf
        self.amount_employed = 0  # Wie viele Bienen hat diese Biene rekrutiert

        # Image
        self.size = 6
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.radius = self.size / 2

        # Rect
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.update_image()

    def update(self, foodsources):
        self.check_foodsources(foodsources)
        self.update_movement()
        self.update_image()

    def check_foodsources(self, foodsources):
        for food in foodsources:
            if (food.units >= 1
                    and food.x - (food.units + BEE_VISION) < self.x < food.x + (food.units + BEE_VISION)
                    and food.y - (food.units + BEE_VISION) < self.y < food.y + (food.units + BEE_VISION)
                    and self.capacity < BEE_MAX_CAPACITY
                    and self.occupation is not Occupation.EMPLOYED):
                # Gefundene Futterquelle anfliegen
                self.orientation = math.atan((food.y - self.y) / (food.x - self.x)) * 180 / math.pi

            if (food.x - (food.units + 3) < self.x < food.x + (food.units + 3)
                    and food.y - (food.units + 3) < self.y < food.y + (food.units + 3)
                    and self.capacity < BEE_MAX_CAPACITY):
                # Futter entnehmen aus Futterquelle
                food_harvested = food.harvest(BEE_MAX_CAPACITY - self.capacity)
                # Futter und Tanzinformation an Biene übergeben
                self.harvest(food_harvested, food.x, food.y, food.sugar, food.units, food)

    def update_movement(self):
        # Fortbewegung: Position der Biene aktualisieren in Blickrichtung
        self.x += math.cos(self.orientation) * self.speed / 100
        self.y += math.sin(self.orientation) * self.speed / 100

        # Maximale Futterkapazität prüfen, begrenzen und zurück zum Bienenstock schicken
        if not self.occupation == Occupation.IN_HIVE and self.capacity >= BEE_MAX_CAPACITY:
            self.change_occupation(Occupation.RETURNING)  # Biene muss zurückfliegen
            self.capacity = BEE_MAX_CAPACITY

        # Maximale Fluglänge begrenzen und zum Bienenstock zurückschicken
        if not self.occupation == Occupation.IN_HIVE and self.steps >= MAX_STEP_COUNTER_BEES:
            self.change_occupation(Occupation.RETURNING)  # Biene muss zurückfliegen

        # Kontrollieren ob Biene über Simulationsgrenzen fliegt und umkehren lassen
        if self.x <= 0:
            self.orientation = self.orientation * random.randint(2, 5)  # Zufällige neue Orientierung
            self.x = 1
        if self.x >= SCREEN_WIDTH:
            self.orientation = self.orientation * random.randint(2, 5)  # Zufällige neue Orientierung
            self.x = SCREEN_WIDTH - 1
        if self.y <= 0:
            self.orientation = self.orientation * random.randint(2, 5)  # Zufällige neue Orientierung
            self.y = 1
        if self.y >= SCREEN_HEIGHT:
            self.orientation = self.orientation * random.randint(2, 5)  # Zufällige neue Orientierung
            self.y = SCREEN_HEIGHT - 1

        # Zustände (Occupation) der Biene
        match self.occupation:
            case Occupation.SCOUT:
                self.orientation = self.orientation + random.uniform(-0.2, 0.2)  # Zufällige Richtungsänderungen
                self.steps = self.steps + 1  # Schrittcounter um 1 addieren

            case Occupation.EMPLOYED:  # Biene ist Employed
                self.orientation = math.atan((self.dance_information[1] - self.y) / (
                        self.dance_information[0] - (self.x))) * 180 / math.pi  # Winkel zur Futterquelle berechnen

            case Occupation.ONLOOKER:  # Biene ist Onlooker
                self.orientation = math.atan(
                    (self.hive.y - self.y) / (
                            self.hive.x - (self.x))) * 180 / math.pi  # Winkel zum Bienenstock berechnen

            case Occupation.RETURNING:  # Biene fliegt zurück zum Bienenstock
                # Winkel zum Bienenstock berechnen
                self.orientation = math.atan((self.hive.y - self.y) / (self.hive.x - self.x)) * 180 / math.pi
                if pygame.sprite.collide_circle(self, self.hive):
                    self.x = self.hive.x
                    self.y = self.hive.y
                    self.change_occupation(Occupation.IN_HIVE)  # Biene ist im Stock
                    self.steps = 0  # Schritt Counter zurücksetzen

            case Occupation.IN_HIVE:  # Biene befindet sich im Bienenstock
                # Winkel zum Bienenstock berechnen
                self.orientation = math.atan((self.hive.y - self.y) / (self.hive.x - (self.x))) * 180 / math.pi
                # Nahrungsübergabe an Bienenstock und Zuckergehalt übergabe
                self.hive.deposit(self.capacity, self.dance_information[2])
                self.deliver()  # Nahrung von Biene entfernen

            case Occupation.DANCER:  # Biene tanzt
                self.orientation = math.atan(
                    (self.hive.y - self.y) / (
                            self.hive.x - (self.x))) * 180 / math.pi  # Winkel zum Bienenstock berechnen
                for onlooker in self.hive.onlooker_bees:  # Schleife um Bienen in der Nähe der tanzen Biene zu finden
                    if self.amount_employed < min(
                            self.dance_information[2],
                            self.dance_information[
                                3]):  # Biene ist Onlooker und es
                        # dürfen so viele Bienen rekrutiert werden, wie der Zuckergehalt der
                        onlooker.dance_information = self.dance_information  # Übergabe Tanz Informationen von
                        # tanzende Biene zu Onlooker Biene
                        onlooker.foodsource = self.foodsource
                        onlooker.change_occupation(Occupation.EMPLOYED)  # Biene wird employed
                        self.amount_employed = self.amount_employed + 1  # Zähler für maximale Anzahl Bienen rekrutierbar
                self.dance_counter = self.dance_counter + 1  # Schritt counter um 1 addieren
                if self.dance_counter == MAX_DANCE_COUNTER:  # Ende des Schwänzeltanz
                    self.change_occupation(Occupation.ONLOOKER)  # Biene wird nach dem Tanzen zur Onlooker Biene
                    self.amount_employed = 0  # Rücksetzen Zähler max Anzahl Bienen zu rekrutieren

    def update_image(self):
        self.image.fill((0, 0, 0, 0))
        self.rect.center = (self.x, self.y)
        if self.occupation == Occupation.SCOUT:  # Biene ist Scout
            pygame.draw.circle(self.image, COLOR_BEE_SCOUT, (self.radius, self.radius), self.radius)
        elif self.occupation == Occupation.EMPLOYED:  # Biene ist Employed
            pygame.draw.circle(self.image, COLOR_BEE_EMPLOYED, (self.radius, self.radius), self.radius)
        elif self.occupation == Occupation.ONLOOKER:  # Biene ist Onlooker
            pygame.draw.circle(self.image, COLOR_BEE_ONLOOKER, (self.radius, self.radius), 2)
        elif self.occupation == Occupation.RETURNING:  # Biene fliegt zurück zum Bienenstock
            pygame.draw.circle(self.image, YELLOW, (self.radius, self.radius), 4)
        elif self.occupation == Occupation.DANCER:  # Biene tanzt
            pygame.draw.circle(self.image, COLOR_BEE_DANCER, (self.radius, self.radius), 6)

    def change_occupation(self, occupation):
        match self.occupation:
            case Occupation.SCOUT:
                self.hive.scout_bees.remove(self)
            case Occupation.EMPLOYED:
                self.hive.employed_bees.remove(self)
            case Occupation.ONLOOKER:
                self.hive.onlooker_bees.remove(self)
            case Occupation.DANCER:
                self.hive.dance_bees.remove(self)
        self.occupation = occupation
        match self.occupation:
            case Occupation.SCOUT:
                self.hive.scout_bees.add(self)
            case Occupation.EMPLOYED:
                self.hive.employed_bees.add(self)
            case Occupation.ONLOOKER:
                self.hive.onlooker_bees.add(self)
            case Occupation.DANCER:
                self.hive.dance_bees.add(self)

    def harvest(self, food_harvested, food_x, food_y, food_sugar, food_units_remaining, food):  # Futter ernten
        self.capacity = self.capacity + food_harvested  # Anzahl Futter erhöhen
        self.dance_information = food_x, food_y, food_sugar, food_units_remaining  # Tanz Informationen von der
        # Futterquelle an die Biene übergeben
        self.foodsource = food
        if not self.foodsource.alive() or food_harvested < 1:
            self.change_occupation(
                Occupation.SCOUT)  # Biene fliegt zurück zum Bienenstock, weil Futterquelle leer ist // oder Scout?
            self.steps = MAX_STEP_COUNTER_BEES - 150  # Schrittzähler wird erhöht, sodass Scout Biene nur kurz die
            # Umgebung absucht
        elif self.capacity >= BEE_MAX_CAPACITY:
            self.capacity = BEE_MAX_CAPACITY  # Futtermenge begrenzen
            self.change_occupation(Occupation.RETURNING)  # Biene ist voll und muss in den Bienenstock fliegen
            self.speed = self.speed - REDUCE_SPEED_WHEN_CARRY  # Geschwindigkeit reduzieren, wenn Biene Futter trägt

    def deliver(self):  # Futter abgeben
        if self.capacity != 0:  # Biene hat Futter dabei
            self.speed = self.speed + REDUCE_SPEED_WHEN_CARRY  # Geschwindigkeit erhöhen wenn Biene kein Futter mehr
            # trägt
        self.capacity = 0  # Nahrung wird von Biene entfernt

        # TODO Hier Formel zur Auswertung der Güte der Futterquelle -> Soll Biene Tanzen oder nicht? #####
        if len(self.hive.dance_bees) < MAX_BEES_DANCER:  # noch keine Biene tanzt und Zuckergehalt hoch genug
            # self.dance_information[2] <- Zuckergehalt , self.dance_information[3] = restliche Nahrungsmenge
            self.change_occupation(Occupation.DANCER)  # Biene wird Tänzer
            self.dance_counter = 0  # Tanz beginnt von vorne
            self.orientation = random.uniform(0.0, 360.0)  # Zufällige Orientierung
        else:  # Biene tanzt nicht, dann
            if len(self.hive.scout_bees) >= MAX_BEES_SCOUT:  # Wenn maximale Anzal an Scout Bienen erreicht, wird die Biene zur
                # Onlooker Biene
                self.change_occupation(Occupation.ONLOOKER)  # Biene wird Biene Onlooker
            else:
                self.change_occupation(Occupation.SCOUT)  # Ansonsten wird Biene wird Scout Biene
                self.orientation = random.uniform(0.0, 360.0)  # Zufällige Orientierung


class Occupation(Enum):
    SCOUT = 0
    EMPLOYED = 1
    ONLOOKER = 2
    RETURNING = 3
    IN_HIVE = 4
    DANCER = 5
