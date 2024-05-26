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
        bee_group.update(foodsource_group)

        # Futterquellen auf Karte zeichnen
        foodsource_group.draw(screen)
        foodsource_group.update()

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
