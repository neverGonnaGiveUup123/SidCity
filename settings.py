import pygame

pygame.init()

RED = (255, 100, 100)
GREEN = (0, 255, 0)
GRASS = (50, 150, 50)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
DARKWHITE = (200, 200, 200)
YELLOW = (255,100,0)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

HOUSEMODELONE = pygame.image.load("test_house1.png")
ROADMODELONE = pygame.image.load("small_road.png")

GRIDSQUARESIZE = 40

INCOME = 0

BUILDINGOPTIONS = ["ROADMODELONE", "HOUSEMODELONE"]

TREASURY = 100

FONTTYPE = pygame.font.Font("freesansbold.ttf", 9)

MOUSESQUAREVAR = pygame.Rect(0, 40, GRIDSQUARESIZE, GRIDSQUARESIZE)

INSTRUCTIONTEXT = FONTTYPE.render("WASD to move. Spacebar to build. Right and left arrows to cycle buildings.",True,BLACK,)