import pygame
import random
import math

from Config import *

# Farben
WHITE = (180, 180, 180)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
COLOR_BEE_SCOUT = (255, 0, 0)
COLOR_BEE_EMPLOYED= (30, 144, 255)
COLOR_BEE_ONLOOKER = (255, 100, 0)
COLOR_BEE_DANCER = (128 , 0 , 128)

# Bienenklasse
class Bee:
    def __init__(self,occupation,hive_x,hive_y):
        self.x = hive_x #Startposition X im Bienestock
        self.y = hive_y#Startposition Y im Bienenstock
        self.occupation = occupation #Status der Biene: 0 = Scout , 1 = employed , 2 = onlooker , 3 = to_home , 4 = Biene ist im Stock
        self.speed = random.randint(MIN_VELOCITY_BEE, MAX_VELOCITY_BEE) #Zufällige Geschwindigkeit
        self.orientation = random.uniform(0.0,360.0) #Zufällige Start-Orientierung
        self.capacity = 0 #Aktuelle tragende Nahrungsanzahl der Biene
        self.destination = 0,0,0 #Koordinaten und Zuckergehalt des Ziels
        self.dance_information = 0.0,0.0,0,0 #Koordinaten X/Y,Zuckergehalt und übrige Menge der gefunden Nahrungsquelle
        self.hive_x = self.x #x Koordinate des zugeordneten Bienenstocks
        self.hive_y = self.y #y Koordinate des zugeordneten Bienenstocks
        self.steps = 0 #Anzalh Schritte bevor die Biene zum Bienenstock zurückkehren muss (auch ohne Futter)
        self.dance_counter = 0 #Counter wie lange die Biene tanzen darf
        self.amount_employed = 0 #Wieviele Bienen hat diese Biene rekrutiert

    def update(self):
        #Fortbewegung: Position der Biene aktualisieren in Blickrichtung
        self.x += math.cos(self.orientation) * self.speed / 100
        self.y += math.sin(self.orientation) * self.speed / 100

        #Maxiale Futterkapazität prüfen, begrenzen und zurück zum Bienenstock schicken
        if self.capacity >= BEE_MAX_CAPACITY:
            self.occupation = 3 #Biene muss zurückfliegen
            self.capacity = BEE_MAX_CAPACITY

        #Maximale Fluglänge begrenzen und zum Bienenstock zurückschicken
        if self.steps >= MAX_STEP_COUNTER_BEES:
            self.occupation = 3  # Biene muss zurückfliegen

        #Kontrollieren ob Biene über Simulationsgrenzen fliegt und umkehren lassen
        if self.x <= 0:
            self.orientation = self.orientation * random.randint(2,5) #Zufällige neue Orientierung
            self.x = 1
        if self.x >= SCREEN_WIDTH:
            self.orientation = self.orientation * random.randint(2, 5) #Zufällige neue Orientierung
            self.x = SCREEN_WIDTH-1
        if self.y <= 0:
            self.orientation = self.orientation * random.randint(2,5) #Zufällige neue Orientierung
            self.y = 1
        if self.y >= SCREEN_HEIGHT:
            self.orientation = self.orientation * random.randint(2, 5) #Zufällige neue Orientierung
            self.y = SCREEN_HEIGHT-1

        #Zustände (Occupation) der Biene
        if self.occupation == 0: #Biene ist Scout
            self.orientation = self.orientation + random.uniform(-0.2,0.2) #Zufällige Richtungsänderungen
            self.steps = self.steps + 1  # Schrittcounter um 1 addieren

        if self.occupation == 1:  # Biene ist Employed
            self.orientation = math.atan((self.dance_information[1] - self.y) / (self.dance_information[0] - (self.x))) * 180 / math.pi  # Winkel zur Futterquelle berechnen

        if self.occupation == 2:  # Biene ist Onlooker
            self.orientation = math.atan((self.hive_y - self.y) / (self.hive_x - (self.x))) * 180 / math.pi  # Winkel zum Bienenstock berechnen
            #self.x = self.hive_x
            #self.y = self.hive_y

        if self.occupation == 3:  # Biene fliegt zurück zum Bienenstock
            self.orientation = math.atan((self.hive_y - self.y) / (self.hive_x - (self.x))) *180 / math.pi  # Winkel zum Bienenstock berechnen

        if self.occupation == 4:  # Biene befindet sich im Bienenstock
            self.orientation = math.atan((self.hive_y - self.y) / (self.hive_x - (self.x))) *180 / math.pi  # Winkel zum Bienenstock berechnen

        if self.occupation == 5: #Biene tanzt
            self.orientation = math.atan((self.hive_y - self.y) / (self.hive_x - (self.x))) * 180 / math.pi  # Winkel zum Bienenstock berechnen
            self.dance_counter = self.dance_counter + 1  # Schrittcounter um 1 addieren
            if self.dance_counter == MAX_DANCE_COUNTER: #Ende des Schwänzeltanz
                self.occupation = 2 #Biene wird nach dem Tanzen zur Onlooker Biene
                self.amount_employed = 0 #Rücksetzen Zähler max Anzahl Bienen zu rekrutieren

        #Biene im Bienenstock einfangen
        if self.x > self.hive_x - 5 and self.x < self.hive_x + 5 and self.y > self.hive_y - 5 and self.y < self.hive_y + 5 and self.occupation == 3:
            self.x = self.hive_x
            self.y = self.hive_y
            self.occupation = 4 #Biene ist im Stock
            self.steps = 0 #Schritt Counter zurücksetzen


    def draw(self, screen):
        if self.occupation == 0: #Biene ist Scout
            pygame.draw.circle(screen, COLOR_BEE_SCOUT, (self.x, self.y), 3)
        if self.occupation == 1: #Biene ist Employed
            pygame.draw.circle(screen, COLOR_BEE_EMPLOYED, (self.x, self.y), 3)
        if self.occupation == 2: #Biene ist Onlooker
            pygame.draw.circle(screen, COLOR_BEE_ONLOOKER, (self.x, self.y), 2)
        if self.occupation == 3: #Biene fliegt zurück zum Bienenstock
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), 4)
        if self.occupation == 5: #Biene tanzt
            pygame.draw.circle(screen, COLOR_BEE_DANCER, (self.x, self.y), 6)
    def change_occupation(self,occupation):
        self.occupation = occupation #Status der Biene: 0 = Scout , 1 = employed , 2 = onlooker , 3 = fliegt zurück

    def harvest(self,food_harvested, food_x, food_y, food_sugar, food_units_remaining): #Futter ernten
        self.capacity = self.capacity + food_harvested #Anzahl Futter erhöhen
        self.dance_information = food_x, food_y,food_sugar,food_units_remaining #Tanz Informationen von der Futterquelle an die Biene übergeben
        if self.capacity >= BEE_MAX_CAPACITY:
            self.capacity = BEE_MAX_CAPACITY #Futtermenge begrenzen
            self.occupation = 3 #Biene ist voll und muss in den Bienenstock fliegen
            self.speed = self.speed - REDUCE_SPEED_WHEN_CARRY #Geschwindigkeit reduzieren wenn Biene Futter trägt
        if food_harvested < 1: #Futterquelle war leer, es konnte nichts entnommen werden
            self.occupation = 0  # Biene fliegt zurück zum Bienenstock weil Futterquelle leer ist // oder Scout?
            self.steps = MAX_STEP_COUNTER_BEES - 150  #Schrittzähler wird erhöht, sodass Scout Biene nur kurz die Umgebung absucht


    def deliver(self,scout_bees,dancing_bees): #Futter abgeben
        if self.capacity != 0: #Biene hat Futter dabei
            self.speed = self.speed + REDUCE_SPEED_WHEN_CARRY  # Geschwindigkeit erhöhen wenn Biene kein Futter mehr trägt
        self.capacity = 0  #Nahrung wird von Biene entfernt

        ##### Hier Formel zur Auswertung der Güte der Futterquelle -> Soll Biene Tanzen oder nicht? #####
        if dancing_bees < MAX_BEES_DANCER: #noch keine Biene tanzt und Zuckergehalt hoch genug
            #self.dance_information[2] <- Zuckergehalt , self.dance_information[3] = restliche Nahrungsmenge
            self.occupation = 5 #Biene wird Tänzer
            self.dance_counter = 0 #Tanz beginnt von vorne
            self.orientation = random.uniform(0.0, 360.0)  # Zufällige Orientierung
        else: #Biene tanzt nicht, dann
            if scout_bees >= MAX_BEES_SCOUT: #Wenn maximale Anzal an Scout Bienen erreicht, wird die Biene zur Onlooker Biene
                self.occupation = 2 #Biene wird Biene Onlooker
            else:
                self.occupation = 0  # Ansonsten wird Biene wird Scout Biene
                self.orientation = random.uniform(0.0, 360.0)  # Zufällige Orientierung


# Klasse Bienenstock
class Hive:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.food_count = 0 #Anzahl Nahrung im Bienenstock
        self.scout_bees = 0 #Anzahl Scout Bienen dem Bienenstock zugewiesen
        self.dance_bees = 0 #Anzahl tanzende Bienen

    def draw(self, screen): #Zeichne den Bienenstock
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 25)

    def deliver(self,food_amount,sugar_amount): #Nahrung wird an Bienenstock übergeben
        self.food_count = self.food_count + (food_amount * sugar_amount)

# Klasse Futterquelle
class Foodsource:
    def __init__(self, units, sugar,distance_to_hive,hive_x,hive_y):
        self.x = random.randint(50, SCREEN_WIDTH -50) #Zufällige Position X
        if self.x > hive_x - distance_to_hive and self.x < hive_x + distance_to_hive: #Futterquelle ist zu nah am Bienenstock
            self.x = self.x + 2 * distance_to_hive #Futterquelle vom Bienenstock wegschieben
        self.y = random.randint(50, SCREEN_HEIGHT- 50) #Zufällige Posiition Y
        self.units = units #Anzahl Futtereinheiten für diese Futterquelle
        self.sugar = sugar #Anzahl Zucker für diese Futterquelle
        self.label_font = pygame.font.SysFont("Arial", 12)  # Schriftart für das Label
        self.label_text_food = "Food value: " + str(units).encode("utf-8").decode("utf-8")   # Text für das Label Futtereinheiten
        self.label_text_sugar = "Sugar value: " + str(sugar).encode("utf-8").decode("utf-8") # Text für das Label Zuckergehalt

    def draw(self, screen): #Futterquelle und Labels zeichnen
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.units) #Radius = Anzahl Futtereinheiten
        self.label_text_food = "Food value: " + str(self.units).encode("utf-8").decode("utf-8")  # Text für das Label Futtereinheiten
        label_surface = self.label_font.render(self.label_text_food, True, BLACK)  # Label rendern
        screen.blit(label_surface, (self.x, self.y))  # Label auf den Bildschirm zeichnen
        self.label_text_sugar = "Sugar value: " + str(self.sugar).encode("utf-8").decode("utf-8")  # Text für das Label Zuckergehalt
        label_surface = self.label_font.render(self.label_text_sugar, True, BLACK)  # Label rendern
        screen.blit(label_surface, (self.x, self.y+10))  # Label auf den Bildschirm zeichnen

    def harvest(self,x): #Biene erntet Futter von Futterquelle
        if x > self.units: #Verbleidendes Futter ist kleine als Bienenkapazität
            retval = self.units #Es wird nur das verbleibende Futter entnommen
        else:
            retval = x #Maximales Futter wird entnommen
        self.units = self.units - x #Futtermenge von Futterquelle abziehen
        if self.units < 0: #Negative Zahlen begrenzen
            self.units = 0
        return retval #Tasächlich gesammelte Futtermenge als Rückgabewert


# Hauptfunktion
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bienenstock Simulation")
    clock = pygame.time.Clock()


    hive = Hive(SCREEN_WIDTH/random.randint(2,4),SCREEN_HEIGHT/random.randint(2,4))  # Erzeugt Biennestock und Bienen
    bees = [Bee(0,hive.x,hive.y) for _ in range(BEES_SCOUT)]  # Erzeugt Scout Bienen (Status = 0)
    bees = bees + [Bee(1,hive.x,hive.y) for _ in range(BEES_EMPLOYED)]  # Erzeugt employed Bienen (Status = 1)
    bees = bees + [Bee(2,hive.x,hive.y) for _ in range(BEES_ONLOOKER)]  # Erzeugt Onlooker Bienen (Status = 2)
    foods = [Foodsource(random.randint(MIN_UNITS, MAX_UNITS),random.randint(MIN_SUGAR, MAX_SUGAR),MIN_RANGE_FOOD_TO_HIVE,hive.x,hive.y) for _ in range(FOOD_COUNT)]
    total_food_amount = 0 #Gesamte verfügbare Futter Einheiten

    #Alle Futterquellen zusammenzählen
    for foodsource in foods:
         total_food_amount = total_food_amount + (foodsource.units * foodsource.sugar)  # Gesamte Futtereinheiten zusammenzählen

    # Hauptschleife
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.time.get_ticks() > MAX_TIME: #Simulation nach abgelaufener Zeit beenden
            running = False

        screen.fill(WHITE) #Hintergrund zeichnen
        hive.draw(screen) #Bienenstock auf Karte zeichnen

        #Alle Futterquellen updaten
        for foodsource in foods:
            foodsource.draw(screen)

        hive.scout_bees = 0  # Anzahl Scout Bienen intialisieren
        hive.dance_bees = 0 #Anzahl Tanzende Bienen initialisieren
        for bee in bees:  # Alle Bienen zählen
            if bee.occupation == 0: #Biene ist Scout Biene
                hive.scout_bees += 1 #Anzahl Scout Bienen im Bienenstock
            if bee.occupation == 5: #Biene ist tanzende Biene
                hive.dance_bees += 1 #Anzahl Tanzende Bienen im Bienenstock

        for bee in bees: #Alle Bienen updaten
            bee.update()
            bee.draw(screen)
            if bee.occupation == 5:  # Biene ist tanzende Biene
                for onlooker in bees: #Schleife um Bienen in der nähe der tanzen Biene zu finden
                    if onlooker.occupation == 2 and bee.amount_employed < min(bee.dance_information[2],bee.dance_information[3]): #Biene ist Onlooker und Es dürfen so viele Bienen rekuriert werden, wie der Zuckergehalt der
                        onlooker.dance_information = bee.dance_information #Übergabe Tanz Informationen von tanzende Biene zu Onlooker Biene
                        onlooker.change_occupation(1) #Biene wird employed
                        bee.amount_employed = bee.amount_employed + 1 #Zähler für maximale Anzahl Bienen rekrutierbar
            if bee.occupation == 4: #Wenn Biene im Stock ist
                hive.deliver(bee.capacity,bee.dance_information[2]) #Nahrungsübergabe an Bienenstock und Zuckergehalt übergabe
                bee.deliver(hive.scout_bees,hive.dance_bees) #Nahrung von Biene entfernen
            #Abfrage ob eine Futterquelle im Sichtbereich der Biene liegt
            for food in foods:
                if food.units > 1 and bee.x > food.x - (food.units+BEE_VISION) and bee.x < food.x + (food.units+BEE_VISION) and bee.y > food.y - (food.units+BEE_VISION) and bee.y < food.y + (food.units+BEE_VISION) and bee.capacity < BEE_MAX_CAPACITY and bee.occupation != 1:
                    bee.orientation = math.atan((food.y - bee.y) / (food.x - (bee.x))) * 180 / math.pi  #Gefundene Futterquelle anfliegen
                if bee.x > food.x - (food.units+3) and bee.x < food.x + (food.units+3) and bee.y > food.y - (food.units+3) and bee.y < food.y + (food.units+3) and bee.capacity < BEE_MAX_CAPACITY:
                    food_harvested = food.harvest(BEE_MAX_CAPACITY - bee.capacity)  # Futter entnehmen aus Futterquelle
                    bee.harvest(food_harvested,food.x,food.y,food.sugar, food.units) # Futter und Tanzinformation an Biene übergeben

        # Schriftart für Labels
        label_font = pygame.font.SysFont("Arial", 18)
        label_text = "Anzahl Sekunden vergangen: " + str(pygame.time.get_ticks()/1000).encode("utf-8").decode("utf-8")
        # Zeichne Label für die vergangene Zeit
        label_surface = label_font.render(label_text, True, BLACK)
        screen.blit(label_surface, (10, 10))

        #Zeichen Label für Information Futterquelle
        label_text = "Anzahl Futter gesammelt: " + str(hive.food_count).encode("utf-8").decode("utf-8") + " / " + str(total_food_amount).encode("utf-8").decode("utf-8")
        label_surface = label_font.render(label_text, True, BLACK)
        screen.blit(label_surface, (10, 30))

        # Zeichen Labels für Legende
        label_text = "Scout Biene"
        label_surface = label_font.render(label_text, True, COLOR_BEE_SCOUT)
        screen.blit(label_surface, (10, 700))
        label_text = "Employed Biene"
        label_surface = label_font.render(label_text, True, COLOR_BEE_EMPLOYED)
        screen.blit(label_surface, (10, 720))
        label_text = "Onlooker Biene"
        label_surface = label_font.render(label_text, True, COLOR_BEE_ONLOOKER)
        screen.blit(label_surface, (10, 740))
        label_text = "Biene kehrt zurück"
        label_surface = label_font.render(label_text, True, YELLOW)
        screen.blit(label_surface, (10, 760))
        label_text = "Biene Schwänzeltanz"
        label_surface = label_font.render(label_text, True, COLOR_BEE_DANCER)
        screen.blit(label_surface, (10, 780))


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()