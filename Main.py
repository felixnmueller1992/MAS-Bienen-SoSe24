import pygame
import random
import math

from Config import *
from Color import *

from Hive import Hive
from Bee import Bee
from Foodsource import Foodsource

# Hauptfunktion
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bienenstock Simulation")
    clock = pygame.time.Clock()

    hive = Hive(SCREEN_WIDTH / random.randint(2, 4),
                SCREEN_HEIGHT / random.randint(2, 4))  # Erzeugt Biennestock und Bienen
    bees = [Bee(0, hive.x, hive.y) for _ in range(BEES_SCOUT)]  # Erzeugt Scout Bienen (Status = 0)
    bees = bees + [Bee(1, hive.x, hive.y) for _ in range(BEES_EMPLOYED)]  # Erzeugt employed Bienen (Status = 1)
    bees = bees + [Bee(2, hive.x, hive.y) for _ in range(BEES_ONLOOKER)]  # Erzeugt Onlooker Bienen (Status = 2)
    foods = [
        Foodsource(random.randint(MIN_UNITS, MAX_UNITS), random.randint(MIN_SUGAR, MAX_SUGAR), MIN_RANGE_FOOD_TO_HIVE,
                   hive.x, hive.y) for _ in range(FOOD_COUNT)]
    total_food_amount = 0  #Gesamte verfügbare Futter Einheiten

    #Alle Futterquellen zusammenzählen
    for foodsource in foods:
        total_food_amount = total_food_amount + (
                foodsource.units * foodsource.sugar)  # Gesamte Futtereinheiten zusammenzählen

    # Hauptschleife
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.time.get_ticks() > MAX_TIME:  #Simulation nach abgelaufener Zeit beenden
            running = False

        screen.fill(WHITE)  #Hintergrund zeichnen
        hive.draw(screen)  #Bienenstock auf Karte zeichnen

        #Alle Futterquellen updaten
        for foodsource in foods:
            foodsource.draw(screen)

        hive.scout_bees = 0  # Anzahl Scout Bienen intialisieren
        hive.dance_bees = 0  #Anzahl Tanzende Bienen initialisieren
        for bee in bees:  # Alle Bienen zählen
            if bee.occupation == 0:  #Biene ist Scout Biene
                hive.scout_bees += 1  #Anzahl Scout Bienen im Bienenstock
            if bee.occupation == 5:  #Biene ist tanzende Biene
                hive.dance_bees += 1  #Anzahl Tanzende Bienen im Bienenstock

        for bee in bees:  #Alle Bienen updaten
            bee.update()
            bee.draw(screen)
            if bee.occupation == 5:  # Biene ist tanzende Biene
                for onlooker in bees:  #Schleife um Bienen in der nähe der tanzen Biene zu finden
                    if onlooker.occupation == 2 and bee.amount_employed < min(bee.dance_information[2],
                                                                              bee.dance_information[
                                                                                  3]):  #Biene ist Onlooker und Es dürfen so viele Bienen rekuriert werden, wie der Zuckergehalt der
                        onlooker.dance_information = bee.dance_information  #Übergabe Tanz Informationen von tanzende Biene zu Onlooker Biene
                        onlooker.change_occupation(1)  #Biene wird employed
                        bee.amount_employed = bee.amount_employed + 1  #Zähler für maximale Anzahl Bienen rekrutierbar
            if bee.occupation == 4:  #Wenn Biene im Stock ist
                hive.deliver(bee.capacity,
                             bee.dance_information[2])  #Nahrungsübergabe an Bienenstock und Zuckergehalt übergabe
                bee.deliver(hive.scout_bees, hive.dance_bees)  #Nahrung von Biene entfernen
            #Abfrage ob eine Futterquelle im Sichtbereich der Biene liegt
            for food in foods:
                if food.units > 1 and bee.x > food.x - (food.units + BEE_VISION) and bee.x < food.x + (
                        food.units + BEE_VISION) and bee.y > food.y - (food.units + BEE_VISION) and bee.y < food.y + (
                        food.units + BEE_VISION) and bee.capacity < BEE_MAX_CAPACITY and bee.occupation != 1:
                    bee.orientation = math.atan(
                        (food.y - bee.y) / (food.x - (bee.x))) * 180 / math.pi  #Gefundene Futterquelle anfliegen
                if bee.x > food.x - (food.units + 3) and bee.x < food.x + (food.units + 3) and bee.y > food.y - (
                        food.units + 3) and bee.y < food.y + (food.units + 3) and bee.capacity < BEE_MAX_CAPACITY:
                    food_harvested = food.harvest(BEE_MAX_CAPACITY - bee.capacity)  # Futter entnehmen aus Futterquelle
                    bee.harvest(food_harvested, food.x, food.y, food.sugar,
                                food.units)  # Futter und Tanzinformation an Biene übergeben

        # Schriftart für Labels
        label_font = pygame.font.SysFont("Arial", 18)
        label_text = "Anzahl Sekunden vergangen: " + str(pygame.time.get_ticks() / 1000).encode("utf-8").decode("utf-8")
        # Zeichne Label für die vergangene Zeit
        label_surface = label_font.render(label_text, True, BLACK)
        screen.blit(label_surface, (10, 10))

        #Zeichen Label für Information Futterquelle
        label_text = "Anzahl Futter gesammelt: " + str(hive.food_count).encode("utf-8").decode("utf-8") + " / " + str(
            total_food_amount).encode("utf-8").decode("utf-8")
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
