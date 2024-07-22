import random
import pandas as pd

from Config import *
from Foodsource import Foodsource
from Hive import Hive
from Legende import *
from Szenario import *
from DataExport import *
from Util import *
from Button import Button

file_date = time.strftime("%Y%m%d_%H%M%S")


# Hauptfunktion
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    simulation_screen = pygame.surface.Surface((SIMULATION_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Bienenstock Simulation")
    clock = pygame.time.Clock()

    Minus_img = pygame.image.load('resources/images/Minus_Button.png').convert_alpha()
    Plus_img = pygame.image.load('resources/images/Plus_Button.png').convert_alpha()

    Minus_button = Button(50, 750, Minus_img, 0.4)
    Plus_button = Button(150, 750, Plus_img, 0.4)
    FRAMES_PER_SECOND_var = FRAMES_PER_SECOND

    # Initialisiere alle Objekte für Simulation

    if len(IMPORT_ENVIRONMENT_FILE) > 0:  # Falls file import gewünscht
        hive_group = pygame.sprite.Group()
        foodsource_group = pygame.sprite.Group()

        df_import = pd.read_csv(IMPORT_ENVIRONMENT_FILE, names=['Object', 'Units', 'Sugar', 'X_cord', 'Y_cord', 'Algorithm'])
        for index, row in df_import.iterrows():
            if row['Object'] == "Hive":
                hive = Hive(row['X_cord'], row['Y_cord'], row['Algorithm'])
                hive_group.add(hive)

            if row['Object'] == "Foodsource":
                food = Foodsource(row['Units'], row['Sugar'], row['X_cord'], row['Y_cord'])
                foodsource_group.add(food)

    else:  # Zufällige initialisierung, falls kein file import gewünscht

        hivePosX = SIMULATION_WIDTH / random.randint(2, 4)
        hivePosY = SCREEN_HEIGHT / random.randint(2, 4)

        # Erzeuge Bienenstock
        hive = Hive(hivePosX, hivePosY)
        hive_group = pygame.sprite.Group()
        hive_group.add(hive)

        # Erzeuge Futterquellen
        foodsource_group = pygame.sprite.Group()
        foods = [
            Foodsource(random.randint(MIN_UNITS, MAX_UNITS), random.randint(MIN_SUGAR, MAX_SUGAR),
                       MIN_RANGE_FOOD_TO_HIVE,
                       hivePosX, hivePosY) for _ in range(FOOD_COUNT)]
        foodsource_group.add(foods)

    # Verwalte Dancefloors
    dancefloor_group = pygame.sprite.Group()


    # Erzeuge Bienen
    bee_group = pygame.sprite.Group()
    for hive in hive_group:
        bee_group.add(hive.create_bees())

    total_food_amount = 0

    # Alle Units der Futterquellen zusammenzählen
    for foodsource in foodsource_group:
        total_food_amount = total_food_amount + (foodsource.units * foodsource.sugar)

    if EXPORT_ENVIRONMENT:

        for hive in hive_group:
            environment_data = ["Hive", "N/A", "N/A", hive.x, hive.y, str(hive.algorithm).split('.')[1]]
            export_szenario(environment_data, file_date)

        for foodsource in foodsource_group:
            environment_data = ["Foodsource", foodsource.units, foodsource.sugar, foodsource.x, foodsource.y]
            export_szenario(environment_data, file_date)

    # Erstelle DF für Config-Werte für den Simulatioins Export
    if EXPORT_SIMULATION:
        config_df = collect_config_data()
        config_df.to_excel(file_date + "_Simulationsdaten.xlsx", sheet_name="Config-Daten", index=False)
        
    # Timer-Setup für Dateiexport/Plot
    export_data_event = pygame.USEREVENT + 1
    pygame.time.set_timer(export_data_event, EXPORT_DATA_INTERVALL)
    telemetry_df = pd.DataFrame()

    # Hauptschleife
    running = True
    while running:
        # telemetry_df_temp = pd.DataFrame()
        for event in pygame.event.get():
            # Abtasten von Daten für Datenexport und Analysen
            if event.type == export_data_event:
                telemetry_df_temp = daten_exportieren(hive_group, bee_group, total_food_amount)
                telemetry_df = pd.concat([telemetry_df, telemetry_df_temp])

            if event.type == pygame.QUIT:
                if EXPORT_SIMULATION:
                    with pd.ExcelWriter(file_date + "_Simulationsdaten.xlsx", engine='openpyxl') as writer:
                        telemetry_df.to_excel(writer, sheet_name="Simulationsdaten", index=False)
                        config_df.to_excel(writer, sheet_name="Config-Daten", index=False, header=False)
                running = False

        if pygame.time.get_ticks() > MAX_TIME:  # Simulation nach abgelaufener Zeit beenden
            if EXPORT_SIMULATION:
                with pd.ExcelWriter(file_date + "_Simulationsdaten.xlsx", engine='openpyxl') as writer:
                        telemetry_df.to_excel(writer, sheet_name="Simulationsdaten", index=False)
                        config_df.to_excel(writer, sheet_name="Config-Daten", index=False, header=False)
            running = False

        #if total_food_amount == sum([hive.food_count for hive in hive_group]):  # Simulation beenden wenn das komplette Futter gesammelt
        #    if EXPORT_SIMULATION:
        #        telemetry_df.to_excel(file_date + "_Simulationsdaten.xlsx", index=False)
        #    running = False    

        
        # Hintergrund zeichnen
        screen.fill(WHITE)
        simulation_screen.fill(GREY)

        # Bienenstock auf Karte zeichnen
        hive_group.draw(simulation_screen)
        hive_group.update()

        # Update Tanzflächen
        dancefloor_group.empty()
        for hive in hive_group:
            dancefloor_group.add(hive.dancefloor_list)

        # Tanzflächen auf Karte zeichnen
        dancefloor_group.draw(simulation_screen)
        dancefloor_group.update()

        # Futterquellen auf Karte zeichnen
        foodsource_group.draw(simulation_screen)
        foodsource_group.update()

        # Bienen auf Karte zeichnen
        bee_group.draw(simulation_screen)
        bee_group.update(foodsource_group)

        # Legende auf die Map zeichnen
        dance_algorithm = hive.algorithm
        legende_zeichnen(screen, hive_group, bee_group, total_food_amount, dance_algorithm, FRAMES_PER_SECOND_var)

        # Simulation auf den darunterliegenden Screen zeichnen
        screen.blit(simulation_screen, (SCREEN_WIDTH - SIMULATION_WIDTH, 0))

        # Buttons zeichnen
        if Minus_button.draw(screen):
            FRAMES_PER_SECOND_var = FRAMES_PER_SECOND_var - 10
            
        if Plus_button.draw(screen):
            FRAMES_PER_SECOND_var = FRAMES_PER_SECOND_var + 10  

        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND_var)

    pygame.quit()


if __name__ == "__main__":
    main()
