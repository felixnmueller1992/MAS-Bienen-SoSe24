import pygame
from Color import *


def legende_zeichnen(screen, hive_group, total_food_amount):
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
    legend_items = [
        ("Scout Biene", COLOR_BEE_SCOUT),
        ("Employed Biene", COLOR_BEE_EMPLOYED),
        ("Onlooker Biene", COLOR_BEE_ONLOOKER),
        ("Biene kehrt zurück", YELLOW),
        ("Biene Schwänzeltanz", COLOR_BEE_DANCER)
    ]

    y_offset = 150
    for text, color in legend_items:
        color_surface = label_font.render(text, True, color)
        screen.blit(color_surface, (10, y_offset))
        y_offset += 30


