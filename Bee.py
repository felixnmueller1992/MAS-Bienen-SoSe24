import pygame
import random
import math

from Config import *
from Color import *
from Util import *

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
        self.action = None
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
        self.foodsource = None

        # Onlooker Attribute
        self.watchfloor = None

        # Tänzer Attribute
        self.dance_counter = 0  # Counter wie lange die Biene tanzen darf
        self.foodsource_pos = (0, 0)
        self.foodsource_sugar = 0
        self.foodsource_units = 0
        self.dance_probability = 0  # Tanzwahrscheinlichkeit
        self.dancefloor = None
        self.start_point = None
        self.end_point = None
        self.return_angle = 0
        self.dance_direction = True

    # Util Methoden - ab hier folgen Methoden die Berechnung vereinfachen etc.
    def check_for_dance(self):
        if self.foodsource_units < 0:
            return False
        if len(self.hive.dance_bees) >= MAX_BEES_DANCER:
            return False

        # Berechnung der Tanzwahrscheinlichkeit anhand des Zuckergehaltes
        dance_prob = interpolate(self.foodsource_sugar, MIN_SUGAR, MAX_SUGAR, MIN_DANCE_PROBABILITY)

        if dance_prob >= random.random():
            return True

        # if self.success == 1:  # Biene war an Futterquelle erstes Mal erfolgreich
        #     self.dance_probability = 0.4
        # elif self.success == 2:  # Biene war an Futterquelle zweites Mal erfolgreich
        #     self.dance_probability = 0.6
        # elif self.success == 3:
        #     self.dance_probability = 0.8  # Biene war an Futterquelle drittes Mal
        #
        # if self.dance_probability >= random.random():
        #     return True

        return False

    def check_for_return(self):
        if self.occupation is Occupation.SCOUT and self.foodsource is not None:
            return True
        return False

    def check_for_scout(self):
        if len(self.hive.bees) > 0:
            # Anzahl der maximalen Scouts wird in Abhängigkeit der Anzahl Dancer angepasst (je weniger Dancer,
            # desto mehr Scouts)
            # Formel aus linearer Interpolation von Lit. Daten abgeleitet
            temp_bee_scouts = len(self.hive.bees) * ((-2.046 * (len(self.hive.dance_bees) / len(
                self.hive.bees) * 100) + 46.074) / 100)
            if len(self.hive.scout_bees) < temp_bee_scouts:
                return True
        return False

    def reset_dance_information(self):
        self.dance_counter = 0
        if self.dancefloor is not None:
            self.dancefloor.clear_bees()
            self.hive.remove_dancefloor(self.dancefloor)
            self.dancefloor = None
            self.start_point = None
            self.end_point = None

    def reset_foodsource_information(self):
        self.foodsource_pos = None
        self.foodsource_sugar = 0
        self.foodsource_units = 0
        self.foodsource = None

    # Methode zur Prüfung, ob ein Objekt im Sichtfeld der Biene liegt
    def bee_vision_collide(self, circle):
        distance = math.hypot(self.x - circle.x, self.y - circle.y)
        return distance < (self.radius + circle.radius) + BEE_VISION

    def orientate_towards(self, sprite):
        self.orientation = math.atan2(sprite.y - self.y, sprite.x - self.x)

    def is_in_hive(self):
        distance = math.hypot(self.x - self.hive.x, self.y - self.hive.y)
        return distance <= self.hive.radius

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
                self.action = Action.SCOUTING
            case Occupation.EMPLOYED:
                self.hive.employed_bees.add(self)
                self.action = Action.FORAGING
            case Occupation.ONLOOKER:
                self.hive.onlooker_bees.add(self)
                self.action = Action.WANDERING
            case Occupation.DANCER:
                self.hive.dance_bees.add(self)
                self.action = Action.WAITING

    def dance_orientation(self):
        current_pos = pygame.math.Vector2(self.x, self.y)

        if self.action is Action.DANCE_WAGGLE:
            self.orientate_towards(self.end_point)
            if current_pos.distance_to(self.end_point) < 1:
                self.action = Action.DANCE_RETURN
                self.return_angle = 0
        else:
            if self.dance_direction:
                self.return_angle -= 5
            else:
                self.return_angle += 5

            circle_center = (self.start_point + self.end_point) / 2
            radius_vector = (self.end_point - self.start_point) / 2

            target = circle_center + radius_vector.rotate(self.return_angle)

            if self.return_angle <= -180 or self.return_angle >= 180:
                self.action = Action.DANCE_WAGGLE
                self.dance_direction = not self.dance_direction
                self.orientate_towards(self.end_point)
            else:
                direction = target - current_pos
                if direction.length() > 0:
                    self.orientation = math.atan2(direction.y, direction.x)

    # Aktionen - ab hier folgen Methoden die Aktionen der Biene beschreiben
    def harvest(self, food_harvested, food):  # Futter ernten
        self.capacity = self.capacity + food_harvested  # Anzahl Futter erhöhen
        self.foodsource_pos = (food.x, food.y)
        self.foodsource_sugar = food.sugar
        self.foodsource_units = food.units
        self.foodsource = food
        if self.capacity >= BEE_MAX_CAPACITY:
            self.capacity = BEE_MAX_CAPACITY  # Futtermenge begrenzen
        if self.capacity > 0:    
            self.action = Action.RETURNING
            self.speed = self.speed - REDUCE_SPEED_WHEN_CARRY  # Geschwindigkeit reduzieren, wenn Biene Futter trägt

    def deliver(self):
        # Futter abgeben
        if self.capacity != 0:
            self.hive.deposit(self.capacity, self.foodsource_sugar)
            self.speed = self.speed + REDUCE_SPEED_WHEN_CARRY
        self.capacity = 0

        # Tanz checken
        if self.check_for_dance():
            self.change_occupation(Occupation.DANCER)
            self.dancefloor = self.hive.create_dancefloor(self)
            if self.dancefloor:
                self.dance()
            else:
                print(f'Konnte keine freie Tanzfläche finden.')
                self.change_occupation(Occupation.EMPLOYED)
        # Prüfen ob Biene zur gleichen Futterquelle zurückfliegt
        elif self.check_for_return():
            if self.occupation is Occupation.SCOUT:
                self.change_occupation(Occupation.EMPLOYED)
        # Prüfen ob Biene Scout werden kann
        elif self.check_for_scout():
            self.change_occupation(Occupation.SCOUT)
            self.reset_foodsource_information()
        else:
            self.change_occupation(Occupation.ONLOOKER)
            self.reset_foodsource_information()

    def dance(self):
        self.action = Action.DANCE_WAGGLE
        distance = math.hypot(self.dancefloor.x - self.foodsource_pos[0], self.dancefloor.y - self.foodsource_pos[1])
        self.dance_counter = distance * DANCETIME_PER_UNIT
        # Positionen für Tanz bestimmen
        dancefloor_vec = pygame.math.Vector2(self.dancefloor.rect.center)
        foodsource_vec = pygame.math.Vector2(self.foodsource.x, self.foodsource.y)
        distance_vec = foodsource_vec - dancefloor_vec
        self.start_point = dancefloor_vec - distance_vec.normalize() * self.dancefloor.radius
        self.end_point = dancefloor_vec + distance_vec.normalize() * self.dancefloor.radius
        self.x = self.start_point.x
        self.y = self.start_point.y

    def evaluate_dance(self):
        if random.random() > 0.99:
            self.employ()

    def employ(self):
        dancer = self.watchfloor.dancer
        self.foodsource_pos = dancer.foodsource_pos
        self.foodsource_sugar = dancer.foodsource_sugar
        self.foodsource_units = dancer.foodsource_units
        self.foodsource = dancer.foodsource
        self.watchfloor.remove_onlooker(self)
        self.change_occupation(Occupation.EMPLOYED)

    # Update Methoden - ab hier folgen alle Methoden, die mit dem Update zutun haben
    def update(self, foodsources):
        self.check_foodsources(foodsources)
        self.update_occupation()
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

    def update_occupation(self):
        # Maximale Futterkapazität prüfen, begrenzen und zurück zum Bienenstock schicken
        if not self.occupation == Occupation.ONLOOKER and self.capacity >= BEE_MAX_CAPACITY:
            self.action = Action.RETURNING
            self.capacity = BEE_MAX_CAPACITY

        # Zustände (Occupation) der Biene
        match self.occupation:
            case Occupation.SCOUT:
                match self.action:
                    case Action.SCOUTING:
                        self.update_occupation_scouting()
                    case Action.RETURNING:
                        self.update_occupation_returning()
                    case _:
                        print(f'O:Unbekannte Aktion {self.action} bei Occupation {self.occupation}.')
            case Occupation.EMPLOYED:
                match self.action:
                    case Action.FORAGING:
                        if not self.foodsource.alive() and pygame.sprite.collide_circle(self, self.foodsource):
                            # Biene fliegt zurück zum Bienenstock, weil Futterquelle leer ist // oder Scout?
                            # self.change_occupation(Occupation.SCOUT)
                            self.action = Action.SCOUTING
                            self.success = 0
                            self.steps = MAX_STEP_COUNTER_BEES - 150
                            self.reset_foodsource_information()
                    case Action.SCOUTING:
                        self.update_occupation_scouting()
                    case Action.RETURNING:
                        self.update_occupation_returning()
                    case _:
                        print(f'O:Unbekannte Aktion {self.action} bei Occupation {self.occupation}.')
            case Occupation.ONLOOKER:
                match self.action:
                    case Action.LOOKING:
                        if self.watchfloor.dancer is not None:
                            # TODO Onlooker muss hier noch Infos sammeln
                            self.evaluate_dance()
                        else:
                            self.action = Action.WANDERING
                    case Action.WANDERING:
                        for dancefloor in self.hive.dancefloor_list:
                            if pygame.sprite.collide_circle(self, dancefloor):
                                if dancefloor.add_onlooker(self):
                                    self.action = Action.LOOKING
                                    self.orientate_towards(self.watchfloor)
                    case _:
                        print(f'O:Unbekannte Aktion {self.action} bei Occupation {self.occupation}.')
            case Occupation.RETURNING:
                if pygame.sprite.collide_circle(self, self.hive):
                    self.x = self.hive.x
                    self.y = self.hive.y
                    self.steps = 0  # Schritt Counter zurücksetzen
                    self.deliver()  # Biene ist im Stock
            case Occupation.DANCER:
                match self.action:
                    case Action.DANCE_WAGGLE | Action.DANCE_RETURN:
                        self.dance_counter = self.dance_counter - 1
                        if self.dance_counter <= 0:
                            self.change_occupation(Occupation.EMPLOYED)
                            self.reset_dance_information()
                    case Action.WAITING:
                        pass
                    case _:
                        print(f'O:Unbekannte Aktion {self.action} bei Occupation {self.occupation}.')

    def update_occupation_scouting(self):
        # Maximale Fluglänge begrenzen und zum Bienenstock zurückschicken
        if self.steps >= MAX_STEP_COUNTER_BEES:
            self.action = Action.RETURNING

    def update_occupation_returning(self):
        if pygame.sprite.collide_circle(self, self.hive):
            self.x = self.hive.x
            self.y = self.hive.y
            self.steps = 0  # Schritt Counter zurücksetzen
            self.deliver()  # Biene ist im Stock

    def update_orientation(self):
        match self.occupation:
            case Occupation.SCOUT:
                match self.action:
                    case Action.SCOUTING:
                        # Zufällige Richtungsänderungen
                        self.orientation = self.orientation + random.uniform(-0.2, 0.2)
                    case Action.RETURNING:
                        self.orientate_towards(self.hive)
                    case _:
                        print(f'D:Unbekannte Aktion {self.action} bei Occupation {self.occupation}.')
            case Occupation.EMPLOYED:
                match self.action:
                    case Action.FORAGING:
                        self.orientate_towards(self.foodsource)
                    case Action.SCOUTING:
                        self.orientation = self.orientation + random.uniform(-0.2, 0.2)
                    case Action.RETURNING:
                        self.orientate_towards(self.hive)
                    case _:
                        print(f'D:Unbekannte Aktion {self.action} bei Occupation {self.occupation}.')
            case Occupation.ONLOOKER:
                match self.action:
                    case Action.WANDERING:
                        if not self.is_in_hive():
                            # Lässt die Biene umdrehen
                            self.orientation = self.orientation + 180
                            self.orientation = self.orientation % (2 * math.pi)
                        else:
                            self.orientation = self.orientation + random.uniform(-0.2, 0.2)
                    case Action.LOOKING:
                        pass
                    case _:
                        print(f'D:Unbekannte Aktion {self.action} bei Occupation {self.occupation}.')
            case Occupation.RETURNING:
                self.orientate_towards(self.hive)
            case Occupation.DANCER:
                match self.action:
                    case Action.DANCE_WAGGLE | Action.DANCE_RETURN:
                        self.dance_orientation()
                    case Action.WAITING:
                        pass
                    case _:
                        print(f'D:Unbekannte Aktion {self.action} bei Occupation {self.occupation}.')

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

    def update_movement(self):
        # Fortbewegung: Position der Biene aktualisieren in Blickrichtung
        if self.action is not Action.LOOKING and self.action is not Action.WAITING:
            if self.occupation is Occupation.ONLOOKER or self.occupation is Occupation.DANCER:
                self.x += math.cos(self.orientation) * WALKING_SPEED
                self.y += math.sin(self.orientation) * WALKING_SPEED
            else:
                self.x += math.cos(self.orientation) * self.speed / 100
                self.y += math.sin(self.orientation) * self.speed / 100

        if self.action is Action.SCOUTING:
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
        elif self.occupation == Occupation.DANCER and self.action is not Action.WAITING:  # Biene tanzt
            pygame.draw.circle(self.image, COLOR_BEE_DANCER, (self.radius, self.radius), 2)


class Occupation(Enum):
    SCOUT = 0
    EMPLOYED = 1
    ONLOOKER = 2
    RETURNING = 3
    DANCER = 4


class Action(Enum):
    SCOUTING = 0
    WANDERING = 1
    LOOKING = 2
    FORAGING = 3
    RETURNING = 4
    DANCE_WAGGLE = 5
    DANCE_RETURN = 6
    WAITING = 7
