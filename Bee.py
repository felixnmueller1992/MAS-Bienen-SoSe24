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

        # Generelle Attribute
        self.x = hive.x  # Startposition X im Bienenstock
        self.y = hive.y  # Startposition Y im Bienenstock
        self.hive = hive
        self.occupation = None  # Occupation muss initialisiert werden
        self.change_occupation(occupation)
        self.speed = random.randint(MIN_VELOCITY_BEE, MAX_VELOCITY_BEE)  # Zufällige Geschwindigkeit
        self.orientation = random.uniform(0.0, 360.0)  # Zufällige Start-Orientierung

        # Sprite Attribute
        self.size = 6
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.radius = self.size / 2
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.update_image()

        # Scout Attribute
        self.steps = 0  # Anzahl Schritte bevor die Biene zum Bienenstock zurückkehren muss (auch ohne Futter)
        self.success = 0  # Counter wie oft Biene erfolgreich Futter gesammelt hat

        # Sammler-/Employed Bee Attribute
        self.capacity = 0  # Aktuelle tragende Nahrungsanzahl der Biene
        self.foodsource = None  # Futterquelle an der die Biene employed ist oder die sie gefunden hat

        # Tänzer Attribute
        self.dance_counter = 0  # Counter wie lange die Biene tanzen darf
        self.dance_information = 0.0, 0.0, 0, 0  # Koordinaten X/Y, Zuckergehalt und übrige Menge der gefundenen Nahrung
        self.amount_employed = 0  # Wie viele Bienen hat diese Biene rekrutiert
        self.dance_probability = 0  # Tanzwahrscheinlichkeit
        self.dancefloor = None

    def reset_dance_information(self):
        self.amount_employed = 0
        self.dance_counter = 0
        self.dance_information = 0, 0, 0, 0
        self.foodsource = None

    def update(self, foodsources):
        self.check_foodsources(foodsources)
        self.update_occupations()
        self.update_movement()
        self.update_orientation()
        self.update_image()

    def check_foodsources(self, foodsources):
        if ((self.occupation is Occupation.SCOUT or self.occupation is Occupation.EMPLOYED)
                and self.capacity < BEE_MAX_CAPACITY):
            for food in foodsources:
                if (food.units >= 1
                        and self.occupation is not Occupation.EMPLOYED
                        and self.bee_vision_collide(food)):
                    # Gefundene Futterquelle anfliegen
                    self.orientate_towards(food)

                # Kollision Biene mit Futterquelle erkennen
                if pygame.sprite.collide_circle(self, food):
                    # Futter und Tanzinformation an Biene übergeben
                    self.harvest(food.harvest(BEE_MAX_CAPACITY - self.capacity), food)
                    # Da Futter an der Location gefunden wurde, wird Sammelerfolg um 1 erhöht
                    self.success = self.success + 1

    # Methode zur Prüfung, ob ein Objekt im Sichtfeld der Biene liegt
    def bee_vision_collide(self, circle):
        distance = math.hypot(self.x - circle.x, self.y - circle.y)
        return distance < (self.radius + circle.radius) + BEE_VISION

    def orientate_towards(self, sprite):
        self.orientation = math.atan2(sprite.y - self.y, sprite.x - self.x)

    def update_occupations(self):
        # Maximale Futterkapazität prüfen, begrenzen und zurück zum Bienenstock schicken
        if not self.occupation == Occupation.ONLOOKER and self.capacity >= BEE_MAX_CAPACITY:
            self.change_occupation(Occupation.RETURNING)  # Biene muss zurückfliegen
            self.capacity = BEE_MAX_CAPACITY

        # Maximale Fluglänge begrenzen und zum Bienenstock zurückschicken
        if not self.occupation == Occupation.ONLOOKER and self.steps >= MAX_STEP_COUNTER_BEES:
            self.change_occupation(Occupation.RETURNING)  # Biene muss zurückfliegen

        # Zustände (Occupation) der Biene
        match self.occupation:
            case Occupation.SCOUT:
                pass
            case Occupation.EMPLOYED:
                if not self.foodsource.alive() and pygame.sprite.collide_circle(self, self.foodsource):
                    # Biene fliegt zurück zum Bienenstock, weil Futterquelle leer ist // oder Scout?
                    self.change_occupation(Occupation.SCOUT)
                    # Sammelerfolg wird zurück auf 0 gesetzt
                    self.success = 0
                    # Schrittzähler wird erhöht, sodass Scout Biene nur kurz die Umgebung absucht
                    self.steps = MAX_STEP_COUNTER_BEES - 150
                    self.reset_dance_information()
            case Occupation.ONLOOKER:
                for dancefloor in self.hive.dancefloor_list:
                    if pygame.sprite.collide_circle(self, dancefloor):
                        pass
            case Occupation.RETURNING:
                if pygame.sprite.collide_circle(self, self.hive):
                    self.x = self.hive.x
                    self.y = self.hive.y
                    self.steps = 0  # Schritt Counter zurücksetzen
                    self.deliver()  # Biene ist im Stock
            case Occupation.DANCER:
                for onlooker in self.hive.onlooker_bees:  # Schleife um Bienen in der Nähe der tanzen Biene zu finden
                    if self.amount_employed < min(self.dance_information[2], self.dance_information[3]):
                        # Biene ist Onlooker und es dürfen so viele Bienen rekrutiert werden, wie der Zuckergehalt der
                        onlooker.dance_information = self.dance_information
                        onlooker.foodsource = self.foodsource
                        onlooker.change_occupation(Occupation.EMPLOYED)
                        self.amount_employed = self.amount_employed + 1
                self.dance_counter = self.dance_counter + 1
                # Ende des Schwänzeltanz
                if self.dance_counter == MAX_DANCE_COUNTER:
                    self.change_occupation(Occupation.ONLOOKER)
                    self.reset_dance_information()

    def update_orientation(self):
        match self.occupation:
            case Occupation.SCOUT:
                self.orientation = self.orientation + random.uniform(-0.2, 0.2)  # Zufällige Richtungsänderungen
            case Occupation.EMPLOYED:
                # Winkel zur Futterquelle berechnen
                self.orientate_towards(self.foodsource)
            case Occupation.ONLOOKER:
                # Winkel zum Bienenstock berechnen
                if not self.is_in_hive():
                    # Lässt die Biene umdrehen
                    self.orientation = self.orientation + 180
                    self.orientation = self.orientation % (2 * math.pi)
                else:
                    self.orientation = self.orientation + random.uniform(-0.2, 0.2)
            case Occupation.RETURNING:
                # Winkel zum Bienenstock berechnen
                self.orientate_towards(self.hive)
            case Occupation.DANCER:
                # Winkel zum Bienenstock berechnen
                self.orientate_towards(self.dancefloor)

        # Kontrollieren ob Biene über Simulationsgrenzen fliegt und umkehren lassen
        if self.x <= 0:
            self.orientation = self.orientation * random.randint(2, 5)  # Zufällige neue Orientierung
            self.x = 1
        if self.x >= SIMULATION_WIDTH:
            self.orientation = self.orientation * random.randint(2, 5)  # Zufällige neue Orientierung
            self.x = SIMULATION_WIDTH - 1
        if self.y <= 0:
            self.orientation = self.orientation * random.randint(2, 5)  # Zufällige neue Orientierung
            self.y = 1
        if self.y >= SCREEN_HEIGHT:
            self.orientation = self.orientation * random.randint(2, 5)  # Zufällige neue Orientierung
            self.y = SCREEN_HEIGHT - 1

    def is_in_hive(self):
        distance = math.hypot(self.x - self.hive.x, self.y - self.hive.y)
        return distance <= self.hive.radius

    def update_movement(self):
        # Fortbewegung: Position der Biene aktualisieren in Blickrichtung
        if self.occupation == Occupation.ONLOOKER:
            self.x += math.cos(self.orientation) * WALKING_SPEED
            self.y += math.sin(self.orientation) * WALKING_SPEED
        else:
            self.x += math.cos(self.orientation) * self.speed / 100
            self.y += math.sin(self.orientation) * self.speed / 100

        if self.occupation is Occupation.SCOUT:
            self.steps = self.steps + 1  # Schritt counter um 1 addieren

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
            pygame.draw.circle(self.image, DARK_GREEN, (self.radius, self.radius), 4)
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

    def harvest(self, food_harvested, food):  # Futter ernten
        self.capacity = self.capacity + food_harvested  # Anzahl Futter erhöhen
        self.dance_information = food.x, food.y, food.sugar, food.units
        self.foodsource = food
        if self.capacity >= BEE_MAX_CAPACITY:
            self.capacity = BEE_MAX_CAPACITY  # Futtermenge begrenzen
            self.change_occupation(Occupation.RETURNING)  # Biene ist voll und muss in den Bienenstock fliegen
            self.speed = self.speed - REDUCE_SPEED_WHEN_CARRY  # Geschwindigkeit reduzieren, wenn Biene Futter trägt

    def deliver(self):  # Futter abgeben
        if self.capacity != 0:  # Biene hat Futter dabei
            self.hive.deposit(self.capacity, self.dance_information[2])
            self.speed = self.speed + REDUCE_SPEED_WHEN_CARRY  # Geschwindigkeit erhöhen wenn Biene kein Futter mehr
            # trägt
        self.capacity = 0  # Nahrung wird von Biene entfernt

        # TODO Hier Formel zur Auswertung der Güte der Futterquelle -> Soll Biene Tanzen oder nicht? #####
        if self.success == 1:  # Biene war an Futterquelle erstes Mal erfolgreich
            self.dance_probability = 0.4
        elif self.success == 2:  # Biene war an Futterquelle zweites Mal erfolgreich
            self.dance_probability = 0.6
        elif self.success == 3:
            self.dance_probability = 0.8  # Biene war an Futterquelle drittes Mal erfolgreich

        if self.dance_information[3] > 0:
            if len(self.hive.dance_bees) < MAX_BEES_DANCER and self.dance_probability >= random.random():
                self.dance()
            else:  # Biene tanzt nicht, dann
                # Anzahl der maximalen Scouts wird in Abhängigkeit der Anzahl Dancer angepasst (je weniger Dancer,
                # desto mehr Scouts)
                if len(self.hive.bees) > 0:
                    # Formel aus linearer Interpolation von Lit. Daten abgeleitet
                    temp_bee_scouts = len(self.hive.bees) * ((-2.046 * (len(self.hive.dance_bees) / len(
                        self.hive.bees) * 100) + 46.074) / 100)
                    if len(self.hive.scout_bees) >= temp_bee_scouts:
                        self.change_occupation(Occupation.ONLOOKER)
                else:
                    self.change_occupation(Occupation.EMPLOYED)  # Ansonsten wird Biene wird Scout Biene
                    # self.orientation = random.uniform(0.0, 360.0)  # Zufällige Orientierung
        else:
            self.reset_dance_information()
            # Anzahl der maximalen Scouts wird in Abhängigkeit der Anzahl Dancer angepasst (je weniger Dancer,
            # desto mehr Scouts)
            # Formel aus linearer Interpolation von Lit. Daten abgeleitet
            temp_bee_scouts = len(self.hive.bees) * ((-2.046 * (len(self.hive.dance_bees) / len(
                self.hive.bees) * 100) + 46.074) / 100)
            if len(self.hive.scout_bees) >= temp_bee_scouts:
                self.change_occupation(Occupation.ONLOOKER)
            else:
                self.change_occupation(Occupation.SCOUT)  # Ansonsten wird Biene wird Scout Biene
                self.orientation = random.uniform(0.0, 360.0)  # Zufällige Orientierung

    def dance(self):
        self.change_occupation(Occupation.DANCER)  # Biene wird Tänzer
        self.dance_counter = 0  # Tanz beginnt von vorne
        self.dancefloor = self.hive.create_dancefloor()
        self.x = self.dancefloor.x
        self.y = self.dancefloor.y



class Occupation(Enum):
    SCOUT = 0
    EMPLOYED = 1
    ONLOOKER = 2
    RETURNING = 3
    DANCER = 4
