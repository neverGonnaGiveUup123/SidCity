import pygame, time
from settings import *
import game_functions
from game_functions import houseCoords,numHouses,roadCoords

pygame.init()

pygame.display.set_caption("City Builder")

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

game_functions.check_save()

menuButtonSelected = [None]

pause = [None]

print("E")
constructButton = game_functions.Button(
    pygame.Rect(720, 80, 80, 80),
    pygame.Rect(720, 80, 80, 80),
    FONTTYPE.render("Backspace to exit", True, BLACK),
    FONTTYPE.render("Construct", True, BLACK)
    )
print("Eeeee")
checkConstructionButton = [None]
CB_unselectedTextRect = constructButton.unselectedText.get_rect()
CB_unselectedTextRect.center = constructButton.unselectedRect.center
CB_selectedTextRect = constructButton.selectedText.get_rect()
CB_selectedTextRect.center = constructButton.selectedRect.center

economyButton = game_functions.Button(
    pygame.Rect(720,160,80,80),
    pygame.Rect(720,160,80,80),
    FONTTYPE.render("Backspace to exit", True, BLACK),
    FONTTYPE.render("Economy",True,BLACK)
)
checkEconomyButton = [None]
EB_unselectedTextRect = economyButton.unselectedText.get_rect()
EB_unselectedTextRect.center = economyButton.unselectedRect.center
EB_selectedTextRect = economyButton.selectedText.get_rect()
EB_selectedTextRect.center = economyButton.selectedRect.center

menuButton = pygame.image.load("pause_button.png")
menuButtonRect = menuButton.get_rect()
SCREEN.blit(menuButton, (720, 0))
menuButtonRect.topleft = (720, 0)

running = True
while running:

    KEYS = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    if KEYS[pygame.K_q]:
        running = False

    game_functions.create_grid()

    [SCREEN.blit(HOUSEMODELONE, i) for i in houseCoords]
    [SCREEN.blit(ROADMODELONE, i) for i in roadCoords]

    if constructButton.unselectedRect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed() == (1, 0, 0):
        checkConstructionButton[0] = True
        time.sleep(0.25)
    if KEYS[pygame.K_BACKSPACE]:
        checkConstructionButton[0] = None
    if checkConstructionButton[0] == True:
        pygame.draw.rect(SCREEN,BLUE,constructButton.selectedRect)
        SCREEN.blit(constructButton.selectedText,CB_selectedTextRect)
        game_functions.cycle_buildings()
        game_functions.mouse_square()
        game_functions.construction_func()
    elif checkConstructionButton[0] != True:
        pygame.draw.rect(SCREEN,RED,constructButton.unselectedRect)
        SCREEN.blit(constructButton.unselectedText,CB_unselectedTextRect)

    if economyButton.unselectedRect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed() == (1, 0, 0):
        checkEconomyButton[0] = True
        time.sleep(0.25)
    if KEYS[pygame.K_BACKSPACE]:
        checkEconomyButton[0] = None
    if checkEconomyButton[0] == True:
        pygame.draw.rect(SCREEN,BLUE,economyButton.selectedRect)
        SCREEN.blit(economyButton.selectedText,EB_selectedTextRect)
        game_functions.create_economy_page()
    elif checkEconomyButton[0] != True:
        pygame.draw.rect(SCREEN,GREEN,economyButton.unselectedRect)
        SCREEN.blit(economyButton.unselectedText,EB_unselectedTextRect)
    
    if menuButtonRect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed() == (1, 0, 0):
        time.sleep(0.25)
        pause[0] = True
    
    if pause[0] == True:
        game_functions.pause_screen()
    pause[0] = None

    game_functions.count_sec()

    pygame.display.update()
    pygame.time.Clock().tick(60)

print("Number of houses:", numHouses)
print("INCOME:", INCOME)
print("Bank:", TREASURY)


# while True:
#     save_input = input("Do you want to save? Y/N ")
#     if save_input.upper() == "Y":
#         try:
#             filename = input("Enter save name: ")
#             file = open(f"{filename}.json", "x")
#         except FileExistsError:
#             raw_input = input(
#                 "This file already exists! Are you sure you want to overwrite it? Y/N "
#             )
#             if raw_input.upper() == "Y":
#                 if os.path.exists(f"{filename}.json"):
#                     os.remove(f"{filename}.json")
#                     with open(f"{filename}.json", "w") as save:
#                         json.dump(SAVEVARIABLES, save)
#                 break
#             elif raw_input.upper() == "N":
#                 continue
#             else:
#                 print("Invalid")
#                 continue
#         else:
#             json.dump(SAVEVARIABLES, file)
#             file.close()
#             break
#     elif save_input.upper() == "N":
#         break
#     else:
#         print("Invalid")
#         continue

pygame.quit()