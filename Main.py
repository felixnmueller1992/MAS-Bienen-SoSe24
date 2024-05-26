import pygame
import random
import math

from Config import *
from Color import *

from Hive import Hive
from Bee import Bee, Occupation
from Foodsource import Foodsource


# Hauptfunktion
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bienenstock Simulation")
    clock = pygame.time.Clock()

    # Initialisiere alle Objekte für Simulation
    hivePosX = SCREEN_WIDTH / random.randint(2, 4)
    hivePosY = SCREEN_HEIGHT / random.randint(2, 4)

    # Erzeuge Bienenstock
    hive = Hive(hivePosX, hivePosY)
    hive_group = pygame.sprite.Group()
    hive_group.add(hive)

    # Erzeuge Bienen
    bees = hive.create_bees()
    bee_group = pygame.sprite.Group()
    bee_group.add(bees)

    # Erzeuge Futterquellen
    foodsource_group = pygame.sprite.Group()
    foods = [
        Foodsource(random.randint(MIN_UNITS, MAX_UNITS), random.randint(MIN_SUGAR, MAX_SUGAR), MIN_RANGE_FOOD_TO_HIVE,
                   hivePosX, hivePosY) for _ in range(FOOD_COUNT)]
    foodsource_group.add(foods)
    total_food_amount = 0

    # Alle Units der Futterquellen zusammenzählen
    for foodsource in foodsource_group:
        total_food_amount = total_food_amount + (
                foodsource.units * foodsource.sugar)

    # Hauptschleife
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.time.get_ticks() > MAX_TIME:  # Simulation nach abgelaufener Zeit beenden
            running = False

        # Hintergrund zeichnen
        screen.fill(WHITE)

        # Bienenstock auf Karte zeichnen
        hive_group.draw(screen)
        hive_group.update()

        # Bienen auf Karte zeichnen
        bee_group.draw(screen)
        bee_group.update()

        # Futterquellen auf Karte zeichnen
        foodsource_group.draw(screen)
        foodsource_group.update()

        for bee in bee_group:  # Alle Bienen updaten
            # bee.update()
            # bee.draw(screen)
            if bee.occupation == Occupation.DANCER:  # Biene ist tanzende Biene
                for onlooker in bees:  # Schleife um Bienen in der Nähe der tanzen Biene zu finden
                    if onlooker.occupation == Occupation.ONLOOKER and bee.amount_employed < min(
                            bee.dance_information[2],
                            bee.dance_information[
                                3]):  # Biene ist Onlooker und es
                        # dürfen so viele Bienen rekrutiert werden, wie der Zuckergehalt der
                        onlooker.dance_information = bee.dance_information  # Übergabe Tanz Informationen von
                        # tanzende Biene zu Onlooker Biene
                        onlooker.foodsource = bee.foodsource
                        onlooker.change_occupation(Occupation.EMPLOYED)  # Biene wird employed
                        bee.amount_employed = bee.amount_employed + 1  # Zähler für maximale Anzahl Bienen rekrutierbar
            if bee.occupation == Occupation.IN_HIVE:  # Wenn Biene im Stock ist
                hive.deposit(bee.capacity,
                             bee.dance_information[2])  # Nahrungsübergabe an Bienenstock und Zuckergehalt übergabe
                bee.deliver(hive.scout_bees, hive.dance_bees)  # Nahrung von Biene entfernen

            # Abfrage, ob eine Futterquelle im Sichtbereich der Biene liegt
            for food in foods:
                if food.units >= 1 and bee.x > food.x - (food.units + BEE_VISION) and bee.x < food.x + (
                        food.units + BEE_VISION) and bee.y > food.y - (food.units + BEE_VISION) and bee.y < food.y + (
                        food.units + BEE_VISION) and bee.capacity < BEE_MAX_CAPACITY and bee.occupation != 1:
                    bee.orientation = math.atan(
                        (food.y - bee.y) / (food.x - (bee.x))) * 180 / math.pi  # Gefundene Futterquelle anfliegen
                if bee.x > food.x - (food.units + 3) and bee.x < food.x + (food.units + 3) and bee.y > food.y - (
                        food.units + 3) and bee.y < food.y + (food.units + 3) and bee.capacity < BEE_MAX_CAPACITY:
                    food_harvested = food.harvest(BEE_MAX_CAPACITY - bee.capacity)  # Futter entnehmen aus Futterquelle
                    bee.harvest(food_harvested, food.x, food.y, food.sugar,
                                food.units, food)  # Futter und Tanzinformation an Biene übergeben

        legende_zeichnen(screen, hive, total_food_amount)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def legende_zeichnen(screen, hive, total_food_amount):
    # Schriftart für Labels
    label_font = pygame.font.SysFont("Arial", 18)
    label_text = "Anzahl Sekunden vergangen: " + str(pygame.time.get_ticks() / 1000).encode("utf-8").decode("utf-8")
    # Zeichne Label für die vergangene Zeit
    label_surface = label_font.render(label_text, True, BLACK)
    screen.blit(label_surface, (10, 10))

    # Zeichen Label für Information Futterquelle
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


if __name__ == "__main__":
    main()
