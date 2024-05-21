import pygame
import random
import math

from Config import *
from Color import *

# Bienenklasse
class Bee:
    def __init__(self, occupation, hive_x, hive_y):
        self.x = hive_x  # Startposition X im Bienestock
        self.y = hive_y  # Startposition Y im Bienenstock
        self.occupation = occupation  # Status der Biene: 0 = Scout , 1 = employed , 2 = onlooker , 3 = to_home ,
        # 4 = Biene ist im Stock
        self.speed = random.randint(MIN_VELOCITY_BEE, MAX_VELOCITY_BEE)  #Zufällige Geschwindigkeit
        self.orientation = random.uniform(0.0, 360.0)  #Zufällige Start-Orientierung
        self.capacity = 0  #Aktuelle tragende Nahrungsanzahl der Biene
        self.destination = 0, 0, 0  #Koordinaten und Zuckergehalt des Ziels
        self.dance_information = 0.0, 0.0, 0, 0  #Koordinaten X/Y,Zuckergehalt und übrige Menge der gefunden Nahrungsquelle
        self.hive_x = self.x  #x Koordinate des zugeordneten Bienenstocks
        self.hive_y = self.y  #y Koordinate des zugeordneten Bienenstocks
        self.steps = 0  #Anzalh Schritte bevor die Biene zum Bienenstock zurückkehren muss (auch ohne Futter)
        self.dance_counter = 0  #Counter wie lange die Biene tanzen darf
        self.amount_employed = 0  #Wieviele Bienen hat diese Biene rekrutiert

    def update(self):
        #Fortbewegung: Position der Biene aktualisieren in Blickrichtung
        self.x += math.cos(self.orientation) * self.speed / 100
        self.y += math.sin(self.orientation) * self.speed / 100

        #Maxiale Futterkapazität prüfen, begrenzen und zurück zum Bienenstock schicken
        if self.capacity >= BEE_MAX_CAPACITY:
            self.occupation = 3  #Biene muss zurückfliegen
            self.capacity = BEE_MAX_CAPACITY

        #Maximale Fluglänge begrenzen und zum Bienenstock zurückschicken
        if self.steps >= MAX_STEP_COUNTER_BEES:
            self.occupation = 3  # Biene muss zurückfliegen

        #Kontrollieren ob Biene über Simulationsgrenzen fliegt und umkehren lassen
        if self.x <= 0:
            self.orientation = self.orientation * random.randint(2, 5)  #Zufällige neue Orientierung
            self.x = 1
        if self.x >= SCREEN_WIDTH:
            self.orientation = self.orientation * random.randint(2, 5)  #Zufällige neue Orientierung
            self.x = SCREEN_WIDTH - 1
        if self.y <= 0:
            self.orientation = self.orientation * random.randint(2, 5)  #Zufällige neue Orientierung
            self.y = 1
        if self.y >= SCREEN_HEIGHT:
            self.orientation = self.orientation * random.randint(2, 5)  #Zufällige neue Orientierung
            self.y = SCREEN_HEIGHT - 1

        #Zustände (Occupation) der Biene
        if self.occupation == 0:  #Biene ist Scout
            self.orientation = self.orientation + random.uniform(-0.2, 0.2)  #Zufällige Richtungsänderungen
            self.steps = self.steps + 1  # Schrittcounter um 1 addieren

        if self.occupation == 1:  # Biene ist Employed
            self.orientation = math.atan((self.dance_information[1] - self.y) / (
                    self.dance_information[0] - (self.x))) * 180 / math.pi  # Winkel zur Futterquelle berechnen

        if self.occupation == 2:  # Biene ist Onlooker
            self.orientation = math.atan(
                (self.hive_y - self.y) / (self.hive_x - (self.x))) * 180 / math.pi  # Winkel zum Bienenstock berechnen
            #self.x = self.hive_x
            #self.y = self.hive_y

        if self.occupation == 3:  # Biene fliegt zurück zum Bienenstock
            self.orientation = math.atan(
                (self.hive_y - self.y) / (self.hive_x - (self.x))) * 180 / math.pi  # Winkel zum Bienenstock berechnen

        if self.occupation == 4:  # Biene befindet sich im Bienenstock
            self.orientation = math.atan(
                (self.hive_y - self.y) / (self.hive_x - (self.x))) * 180 / math.pi  # Winkel zum Bienenstock berechnen

        if self.occupation == 5:  #Biene tanzt
            self.orientation = math.atan(
                (self.hive_y - self.y) / (self.hive_x - (self.x))) * 180 / math.pi  # Winkel zum Bienenstock berechnen
            self.dance_counter = self.dance_counter + 1  # Schrittcounter um 1 addieren
            if self.dance_counter == MAX_DANCE_COUNTER:  #Ende des Schwänzeltanz
                self.occupation = 2  #Biene wird nach dem Tanzen zur Onlooker Biene
                self.amount_employed = 0  #Rücksetzen Zähler max Anzahl Bienen zu rekrutieren

        #Biene im Bienenstock einfangen
        if self.x > self.hive_x - 5 and self.x < self.hive_x + 5 and self.y > self.hive_y - 5 and self.y < self.hive_y + 5 and self.occupation == 3:
            self.x = self.hive_x
            self.y = self.hive_y
            self.occupation = 4  #Biene ist im Stock
            self.steps = 0  #Schritt Counter zurücksetzen

    def draw(self, screen):
        if self.occupation == 0:  #Biene ist Scout
            pygame.draw.circle(screen, COLOR_BEE_SCOUT, (self.x, self.y), 3)
        if self.occupation == 1:  #Biene ist Employed
            pygame.draw.circle(screen, COLOR_BEE_EMPLOYED, (self.x, self.y), 3)
        if self.occupation == 2:  #Biene ist Onlooker
            pygame.draw.circle(screen, COLOR_BEE_ONLOOKER, (self.x, self.y), 2)
        if self.occupation == 3:  #Biene fliegt zurück zum Bienenstock
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), 4)
        if self.occupation == 5:  #Biene tanzt
            pygame.draw.circle(screen, COLOR_BEE_DANCER, (self.x, self.y), 6)

    def change_occupation(self, occupation):
        self.occupation = occupation  #Status der Biene: 0 = Scout , 1 = employed , 2 = onlooker , 3 = fliegt zurück

    def harvest(self, food_harvested, food_x, food_y, food_sugar, food_units_remaining):  #Futter ernten
        self.capacity = self.capacity + food_harvested  #Anzahl Futter erhöhen
        self.dance_information = food_x, food_y, food_sugar, food_units_remaining  #Tanz Informationen von der Futterquelle an die Biene übergeben
        if self.capacity >= BEE_MAX_CAPACITY:
            self.capacity = BEE_MAX_CAPACITY  #Futtermenge begrenzen
            self.occupation = 3  #Biene ist voll und muss in den Bienenstock fliegen
            self.speed = self.speed - REDUCE_SPEED_WHEN_CARRY  #Geschwindigkeit reduzieren wenn Biene Futter trägt
        if food_harvested < 1:  #Futterquelle war leer, es konnte nichts entnommen werden
            self.occupation = 0  # Biene fliegt zurück zum Bienenstock weil Futterquelle leer ist // oder Scout?
            self.steps = MAX_STEP_COUNTER_BEES - 150  #Schrittzähler wird erhöht, sodass Scout Biene nur kurz die Umgebung absucht

    def deliver(self, scout_bees, dancing_bees):  #Futter abgeben
        if self.capacity != 0:  #Biene hat Futter dabei
            self.speed = self.speed + REDUCE_SPEED_WHEN_CARRY  # Geschwindigkeit erhöhen wenn Biene kein Futter mehr trägt
        self.capacity = 0  #Nahrung wird von Biene entfernt

        ##### Hier Formel zur Auswertung der Güte der Futterquelle -> Soll Biene Tanzen oder nicht? #####
        if dancing_bees < MAX_BEES_DANCER:  #noch keine Biene tanzt und Zuckergehalt hoch genug
            #self.dance_information[2] <- Zuckergehalt , self.dance_information[3] = restliche Nahrungsmenge
            self.occupation = 5  #Biene wird Tänzer
            self.dance_counter = 0  #Tanz beginnt von vorne
            self.orientation = random.uniform(0.0, 360.0)  # Zufällige Orientierung
        else:  #Biene tanzt nicht, dann
            if scout_bees >= MAX_BEES_SCOUT:  #Wenn maximale Anzal an Scout Bienen erreicht, wird die Biene zur Onlooker Biene
                self.occupation = 2  #Biene wird Biene Onlooker
            else:
                self.occupation = 0  # Ansonsten wird Biene wird Scout Biene
                self.orientation = random.uniform(0.0, 360.0)  # Zufällige Orientierung