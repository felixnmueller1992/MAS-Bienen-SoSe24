import pygame
import random

# Parameter
BEES_SCOUT = 10 #Anzahl Bienen im System
BEES_ONLOOKER = 1 #Anzahl Bienen im System
FOOD_COUNT = 8 #Anzahl Futterquellen im System
MAX_SUGAR = 10 #Maximale Anzahl Zuckereinheiten pro Futterquelle
MIN_SUGAR = 1 #Minimale Anzahl an Zuckereinheiten pro Futterquelle
MAX_UNITS = 100 #Maximale Futterkapazität einer Futterquelle
MIN_UNITS = 1 #Minimale Futterkapazität einer Futterquelle
MAX_TIME = 120000   #86.400 #Anzahl Zeit der Simulation
BEE_VISION = 5

# Farben
WHITE = (230, 230, 230)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Bildschirmgröße
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

# Bienenklasse
class Bee:
    def __init__(self,status):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2
        self.status = status
        self.speed_x = random.randint(-1, 1)
        self.speed_y = random.randint(-2, 1)

    def update(self):
        if self.status == 1:  # Biene ist Scout
             self.x += self.speed_x
             self.y += self.speed_y
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), 5)

# Klasse Bienenstock
class Hive:
    def __init__(self):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 25)

# Klasse Futterquelle
class Foodsource:
    def __init__(self, units, sugar):
        self.x = random.randint(50, SCREEN_WIDTH -50)
        self.y = random.randint(50, SCREEN_HEIGHT- 50)
        self.units = units #Anzahl Futtereinheiten für diese Futterquelle
        self.sugar = sugar #Anzahl Zucker für diese Futterquelle
        self.label_font = pygame.font.SysFont("Arial", 12)  # Schriftart für das Label
        self.label_text_food = "Food value: " + str(units).encode("utf-8").decode("utf-8")   # Text für das Label Futtereinheiten
        self.label_text_sugar = "Sugar value: " + str(sugar).encode("utf-8").decode("utf-8") # Text für das Label Zuckergehalt

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.units) #Radius = Anzahl Futtereinheiten
        label_surface = self.label_font.render(self.label_text_food, True, BLACK)  # Label rendern
        screen.blit(label_surface, (self.x, self.y))  # Label auf den Bildschirm zeichnen
        label_surface = self.label_font.render(self.label_text_sugar, True, BLACK)  # Label rendern
        screen.blit(label_surface, (self.x, self.y+10))  # Label auf den Bildschirm zeichnen

    def remove(self,x):
        self.units = self.units - x

# Hauptfunktion
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bienenstock Simulation")
    clock = pygame.time.Clock()


    hive = Hive()  # Erzeugt Biennestock
    bees_scouts = [Bee(1) for _ in range(BEES_SCOUT)]  # Erzeugt Scout Bienen (Status = 1)
    bees_onlooker = [Bee(0) for _ in range(BEES_ONLOOKER)]  # Erzeugt Onlooker Bienen (Status = 0)
    foods = [Foodsource(random.randint(MIN_UNITS, MAX_UNITS),random.randint(MIN_SUGAR, MAX_SUGAR)) for _ in range(FOOD_COUNT)]

    # Hauptschleife
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.time.get_ticks() > MAX_TIME: #Simulation nach abgelaufener Zeit beenden
            running = False
        screen.fill(WHITE)

        # Schriftart für das Label in der Ecke vergangene Tage
        label_font = pygame.font.SysFont("Arial", 18)
        label_text = "Anzahl Sekunden vergangen: " + str(pygame.time.get_ticks()/1000).encode("utf-8").decode("utf-8")
        # Zeichne Label für die vergangene Zeit
        label_surface = label_font.render(label_text, True, BLACK)
        screen.blit(label_surface, (10, 10))

        hive.draw(screen)

        for bee in bees_onlooker and bees_scouts: #Alle Bienen updaten
            bee.update()
            bee.draw(screen)

        for foodsource in foods: # Alle Futterquellen updaten
            foodsource.remove(0)
            foodsource.draw(screen)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()