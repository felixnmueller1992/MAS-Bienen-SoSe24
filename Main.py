import random

from Config import *
from Foodsource import Foodsource
from Hive import Hive
from Legende import *
from Szenario import *


# Hauptfunktion
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    simulation_screen = pygame.surface.Surface((SIMULATION_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Bienenstock Simulation")
    clock = pygame.time.Clock()

    # Initialisiere alle Objekte für Simulation

    if len(IMPORT_ENVIRONMENT_FILE) > 0:       # Falls file import gewünscht
        hive_group = pygame.sprite.Group()
        foodsource_group = pygame.sprite.Group()

        df_import = pd.read_csv(IMPORT_ENVIRONMENT_FILE, names=['Object', 'Units', 'Sugar', 'X_cord', 'Y_cord'])
        for index, row in df_import.iterrows():
            if row['Object'] == "Hive":
                hive = Hive(row['X_cord'], row['Y_cord'])
                hive_group.add(hive)

            if row['Object'] == "Foodsource":
                food = Foodsource(row['Units'], row['Sugar'], row['X_cord'], row['Y_cord']) 
                foodsource_group.add(food)
        
    else:                                       # Zufällige initialisierung falls kein file import gewünscht
        
        hivePosX = SIMULATION_WIDTH / random.randint(2, 4)
        hivePosY = SCREEN_HEIGHT / random.randint(2, 4)

        # Erzeuge Bienenstock
        hive = Hive(hivePosX, hivePosY)
        hive_group = pygame.sprite.Group()
        hive_group.add(hive)

        # Erzeuge Futterquellen
        foodsource_group = pygame.sprite.Group()
        foods = [
            Foodsource(random.randint(MIN_UNITS, MAX_UNITS), random.randint(MIN_SUGAR, MAX_SUGAR), MIN_RANGE_FOOD_TO_HIVE,
                    hivePosX, hivePosY) for _ in range(FOOD_COUNT)]
        foodsource_group.add(foods)


    # Erzeuge Bienen
    bees = hive.create_bees()
    bee_group = pygame.sprite.Group()
    bee_group.add(bees)

    total_food_amount = 0

        # Alle Units der Futterquellen zusammenzählen
    for foodsource in foodsource_group:
        total_food_amount = total_food_amount + (foodsource.units * foodsource.sugar)


    if EXPORT_ENVIRONMENT == True:

        for hive in hive_group:
            environment_data = ["Hive", "N/A" , "N/A", hive.x, hive.y]
            export_szenario(environment_data)

        for foodsource in foodsource_group:
            environment_data = ["Foodsource",foodsource.units, foodsource.sugar, foodsource.x, foodsource.y]
            export_szenario(environment_data)
            

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
        simulation_screen.fill(GREY)

        # Bienenstock auf Karte zeichnen
        hive_group.draw(simulation_screen)
        hive_group.update()

        # Futterquellen auf Karte zeichnen
        foodsource_group.draw(simulation_screen)
        foodsource_group.update()

        # Bienen auf Karte zeichnen
        bee_group.draw(simulation_screen)
        bee_group.update(foodsource_group)

        # Legende auf die Map zeichnen
        legende_zeichnen(screen, hive_group, total_food_amount)

        # Simulation auf den darunterliegenden Screen zeichnen
        screen.blit(simulation_screen, (SCREEN_WIDTH - SIMULATION_WIDTH, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
