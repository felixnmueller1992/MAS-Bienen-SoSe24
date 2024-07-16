# Technische Parameter
FRAMES_PER_SECOND = 60
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1650

SIMULATION_WIDTH = 1400

# Parameter Simulation
BEES_SCOUT = 60  # Anzahl Scout Bienen im System zum Start
BEES_ONLOOKER = 160  # Anzahl Onlooker Bienen im System zum Start
MAX_BEES_SCOUT = (BEES_SCOUT + BEES_ONLOOKER) * 0.4  # Anzahl maximale Scout Bienen im System
MAX_BEES_DANCER = 15  # Anzahl maximale tanzende Bienen
FOOD_COUNT = 15  # Anzahl Futterquellen im System
MAX_SUGAR = 7  # Maximale Anzahl Zuckereinheiten pro Futterquelle
MIN_SUGAR = 1  # Minimale Anzahl an Zuckereinheiten pro Futterquelle
MAX_UNITS = 75  # Maximale Futterkapazität einer Futterquelle
MIN_UNITS = 20  # Minimale Futterkapazität einer Futterquelle
MAX_TIME = 1800000  # 86.400 # Anzahl Zeit der Simulation
MIN_RANGE_FOOD_TO_HIVE = 150  # Wie weit müssen Futterquellen mindestens vom Bienenstock entfernt sein

# Parameter Biene
MAX_VELOCITY_BEE = 200  # Maximale Geschwindigkeit einer Biene
MIN_VELOCITY_BEE = 160  # Minimale Geschwindigkeit einer Biene
WALKING_SPEED = 0.4  # Faktor für die Gehgeschwindigkeit einer Biene
BEE_VISION = 30  # Sichtradius einer Biene
BEE_MAX_CAPACITY = 2  # Maximale Anzahl Futter das eine Biene tragen kann
REDUCE_SPEED_WHEN_CARRY = 15  # Reduktion der Geschwindigkeit, wenn die Biene Nahrung trägt
MAX_STEP_COUNTER_BEES = 1000  # Anzahl Schritte bevor die Biene zurückkehren muss

# Parameter Schwänzeltanz
DANCETIME_PER_UNIT = FRAMES_PER_SECOND / 100  # Anzahl der
DANCEFLOOR_RADIUS = 8  # Radius einer einzelnen Tanzfläche
DANCEFLOOR_CAPACITY = 5  # Maximale Anzahl von Bienen die gleichzeitig zuschauen kann
MIN_DANCE_PROBABILITY = 0.05  # Minimale Wahrscheinlichkeit mit der eine Biene für eine Quelle tanzt

# Parameter Onlooker
MAX_DANCES_WATCHED = 8  # Anzahl der Tänze die ein Onlooker maximal schaut
MIN_DANCES_WATCHED = 5  # Anzahl der Tänze die ein Onlooker mindestens schaut

# Testing
EXPORT_ENVIRONMENT = False
IMPORT_ENVIRONMENT_FILE = ""

EXPORT_SIMULATION = False
EXPORT_COMPLETE_BEE_GROUP = False
EXPORT_DATA_INTERVALL = 1000  # Intervall [ms]
