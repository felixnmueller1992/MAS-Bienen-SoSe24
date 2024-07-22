import pygame
from Color import *
from Config import *

from Bee import Occupation


def legende_zeichnen(screen, hive_group, bee_group, total_food_amount, dance_algorithm, FRAMES_PER_SECOND_var):
    # Schriftart für Labels
    label_font = pygame.font.SysFont("Arial", 16)
    header_font = pygame.font.SysFont("Arial", 20, bold=True)

    # Titel
    title_text = "Bienen Simulation"
    title_surface = header_font.render(title_text, True, BLACK)
    screen.blit(title_surface, (10, 20))

    # Zeichne Label für die vergangene Zeit
    time_text = "Sekunden vergangen: " + str(int(pygame.time.get_ticks() / 1000))
    time_surface = label_font.render(time_text, True, BLACK)
    screen.blit(time_surface, (10, 60))

    # Zeichen Label für Information Futterquelle
    food_text_1 = "Futter gesammelt:"
    gathered_food = sum([hive.food_count for hive in hive_group])
    food_text_2 = f"{gathered_food} / {total_food_amount}"
    food_surface_1 = label_font.render(food_text_1, True, BLACK)
    food_surface_2 = label_font.render(food_text_2, True, BLACK)
    screen.blit(food_surface_1, (10, 90))
    screen.blit(food_surface_2, (10, 110))


    # Zeichne Labels für Legende
    total_scouts = 0
    total_employed = 0
    total_onlooker = 0
    total_returner = 0
    total_dancer = 0

    for bee in bee_group:
        match bee.occupation:
            case Occupation.SCOUT:
                total_scouts += 1
            case Occupation.EMPLOYED:
                total_employed += 1
            case Occupation.ONLOOKER:
                total_onlooker += 1
            case Occupation.DANCER:
                total_dancer += 1

    total_bees = BEES_SCOUT + BEES_ONLOOKER  # Aus Config Datei
    legend_items = [
        ("Bienen Tanzverhalten:", str(dance_algorithm).split('.')[1], "", BLACK),
        ("Bienen gesamt:", str(total_bees), "", BLACK),
        ("Scout Biene:", str(total_scouts), str(round(total_scouts / total_bees * 100, 1)) + "%", COLOR_BEE_SCOUT),
        ("Employed Biene: ", str(total_employed), str(round(total_employed / total_bees * 100, 1)) + "%",
         COLOR_BEE_EMPLOYED),
        ("Onlooker Biene:", str(total_onlooker), str(round(total_onlooker / total_bees * 100, 1)) + "%",
         COLOR_BEE_ONLOOKER),
        ("Biene tanzt:", str(total_dancer), str(round(total_dancer / total_bees * 100, 1)) + "%", COLOR_BEE_DANCER)
    ]

    y_offset = 150
    for occupation, total, percentage, color in legend_items:
        color_surface = label_font.render(occupation, True, color)
        screen.blit(color_surface, (10, y_offset))
        color_surface = label_font.render(total, True, color)
        screen.blit(color_surface, (150, y_offset))
        color_surface = label_font.render(percentage, True, color)
        screen.blit(color_surface, (190, y_offset))

        y_offset += 30

    color_surface = label_font.render("FPS", True, BLACK)
    screen.blit(color_surface, (110, 725))
    color_surface = label_font.render(str(FRAMES_PER_SECOND_var), True, BLACK)
    screen.blit(color_surface, (110, 760))

