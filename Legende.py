import pygame
from Color import *

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
