import random

from Config import *
from Foodsource import Foodsource
from Hive import Hive
from Legende import *


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

        # Futterquellen auf Karte zeichnen
        foodsource_group.draw(screen)
        foodsource_group.update()

        # Bienen auf Karte zeichnen
        bee_group.draw(screen)
        bee_group.update(foodsource_group)

        legende_zeichnen(screen, hive, total_food_amount)  # Legende auf die Map zeichnen

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
