from settings import *
import time,pygame,json,os

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

KEYS = pygame.key.get_pressed()

gridSquareList = []

class Button:
    def __init__(self,unselectedRect,selectedRect,selectedText,unselectedText):
        self.unselectedRect = unselectedRect
        self.selectedRect = selectedRect
        self.selectedText = selectedText
        self.unselectedText = unselectedText
    
    # def get_text_rect(self):
    #     return self.selectedText.get_rect()

    

def create_grid():
    for x in range(0, WINDOW_WIDTH - 80, GRIDSQUARESIZE):
        for y in range(0, WINDOW_HEIGHT, GRIDSQUARESIZE):
            global gridSquare
            gridSquare = pygame.Rect(x, y, GRIDSQUARESIZE, GRIDSQUARESIZE)
            gridSquareList.append(gridSquare)
            pygame.draw.rect(SCREEN, GRASS, gridSquare)

def mouse_square():
    global MOUSESQUAREVAR
    KEYS = pygame.key.get_pressed()

    if KEYS[pygame.K_d] and MOUSESQUAREVAR.right < 720:
        time.sleep(0.25)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(40, 0)

    elif KEYS[pygame.K_s] and MOUSESQUAREVAR.bottom < 800:
        time.sleep(0.25)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(0, 40)
    elif KEYS[pygame.K_a] and MOUSESQUAREVAR.left > 0:
        time.sleep(0.25)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(-40, 0)

    elif KEYS[pygame.K_w] and MOUSESQUAREVAR.top > 40:
        time.sleep(0.25)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(0, -40)
    pygame.draw.rect(SCREEN, RED, MOUSESQUAREVAR)

buildingOptions = ["Road", "House"]
selectedBuilding = buildingOptions[0]
cycleCounter = 0

def cycle_buildings():
    global selectedBuilding, cycleCounter, buildingOptions, moneyNeeded, incomeGenerated
    KEYS = pygame.key.get_pressed()

    if KEYS[pygame.K_RIGHT]:
        time.sleep(0.25)
        try:
            selectedBuilding = buildingOptions[cycleCounter + 1]
            cycleCounter += 1
        except IndexError:
            selectedBuilding = buildingOptions[0]
            cycleCounter = 0
    if KEYS[pygame.K_LEFT]:
        time.sleep(0.25)
        try:
            selectedBuilding = buildingOptions[cycleCounter - 1]
            cycleCounter -= 1
        except IndexError:
            selectedBuilding = buildingOptions[-1]
            cycleCounter = buildingOptions.index(buildingOptions[-1])
    if selectedBuilding == "House":
        moneyNeeded = 30
        incomeGenerated = 10
    elif selectedBuilding == "Road":
        moneyNeeded = 10
        incomeGenerated = 0
    else:
        moneyNeeded = 0
        incomeGenerated = 0

houseCoords = []
roadCoords = []

instructionTextRect = INSTRUCTIONTEXT.get_rect()

def check_double_build():
    global houseCoords,roadCoords,MOUSESQUAREVAR,doubleBuildAttempt
    doubleBuildAttempt = False
    for i in houseCoords:
        if MOUSESQUAREVAR.topleft == i:
            print("You cant build here!")
            doubleBuildAttempt = True
    for i in roadCoords:
        if MOUSESQUAREVAR.topleft == i:
            print("You cant build there!")
            doubleBuildAttempt = True

def construction_func():
    global houseCoords, CONSTRUCTBUTTON, TREASURY, doubleBuildAttempt, roadCoords, INCOME
    KEYS = pygame.key.get_pressed()
    instructionTextRect.center = (400, 600)

    if KEYS[pygame.K_SPACE]:
        time.sleep(0.25)
        
        check_double_build()

        if TREASURY < moneyNeeded:
            print("Not enough money!")

        elif TREASURY >= moneyNeeded and doubleBuildAttempt == False:
            if selectedBuilding == "House":
                houseCoords.append(MOUSESQUAREVAR.topleft)
                TREASURY -= moneyNeeded
                INCOME += incomeGenerated
            elif selectedBuilding == "Road":
                roadCoords.append(MOUSESQUAREVAR.topleft)
                TREASURY -= moneyNeeded
        else:
            print("skill issue")

    buildingInfoText = FONTTYPE.render(f"Selected building: {selectedBuilding}, cost: ${moneyNeeded}, generates: ${incomeGenerated}",True,BLACK)
    buildingInfoTextRect = buildingInfoText.get_rect()
    buildingInfoTextRect.center = (400, 620)

    [SCREEN.blit(HOUSEMODELONE, i) for i in houseCoords]
    [SCREEN.blit(ROADMODELONE, i) for i in roadCoords]

    SCREEN.blit(INSTRUCTIONTEXT, instructionTextRect)
    SCREEN.blit(buildingInfoText, buildingInfoTextRect)


timer = 0
def count_sec():
    global timer, INCOME, TREASURY
    if timer < 1000:
        timer += 1

    else:
        timer = 0
        TREASURY += INCOME

numHouses = 0

def check_save():
    global TREASURY, INCOME
    while True:
        user_input = input("Do you want to open a saved game? Y/N ")
        if user_input.upper() == "Y":
            try:
                user_input = input("Enter name of save game: ")
                with open(f"{user_input}.json", "r") as file:
                    save_game = json.load(file)
                    TREASURY = save_game["savedTreasury"]
                    for coords in save_game["savedHouses"]:
                        houseCoords.append(tuple(coords))
                    for coords in save_game["savedRoads"]:
                        roadCoords.append(tuple(coords))
                    for houses in houseCoords:
                        INCOME += 10
                    break
            except FileNotFoundError:
                print(
                    "Sorry, this file could not be found. Make sure you spelled it correctly!"
                )
                continue
            except json.decoder.JSONDecodeError:
                print("Corrupted file. You probably did something stupid.")
                continue

        elif user_input.upper() == "N":
            break
        else:
            print("Invalid")
            continue

ecoTextRect = HEADINGFONT.render("Financial Report",True,BLACK).get_rect()
ecoTextRect.center = (360,120)
def create_economy_page():
    pygame.draw.rect(SCREEN,DARKWHITE,pygame.Rect(80,80,560,640))
    SCREEN.blit(HEADINGFONT.render("Financial Report",True,BLACK),ecoTextRect)
    SCREEN.blit(HEADINGFONT.render(f"Treasury: {TREASURY}",True,BLACK),(80,160))
    SCREEN.blit(HEADINGFONT.render(f"Income: {INCOME}",True,BLACK),(80,240))

def pause_screen():
    while True:
        pygame.event.get()
        SCREEN.fill(GREY)

        quitButton = Button(pygame.Rect(200,400,400,50),pygame.Rect(205,405,390,40),HEADINGFONT.render("Quit",True,BLACK),None)
        pygame.draw.rect(SCREEN,WHITE,quitButton.unselectedRect)
        qbTextRect = quitButton.selectedText.get_rect()
        qbTextRect.center = (400,425)

        saveButton = Button(pygame.Rect(200,350,400,50),pygame.Rect(205,355,390,40),HEADINGFONT.render("Save",True,BLACK),None)
        pygame.draw.rect(SCREEN,WHITE,saveButton.unselectedRect)
        sbTextRect = saveButton.selectedText.get_rect()
        sbTextRect.center = (400,375)

        SCREEN.blit(quitButton.selectedText,qbTextRect)
        SCREEN.blit(saveButton.selectedText,sbTextRect)

        if pygame.mouse.get_pos()[0] >= 200 and pygame.mouse.get_pos()[0] <= 600:
            if pygame.mouse.get_pos()[1] >= 400 and pygame.mouse.get_pos()[1] <= 450:
                pygame.draw.rect(SCREEN,DARKWHITE,quitButton.selectedRect)
                SCREEN.blit(quitButton.selectedText,qbTextRect)
                if pygame.mouse.get_pressed() == (1,0,0):
                    quit()
        if pygame.mouse.get_pos()[0] >= 200 and pygame.mouse.get_pos()[0] <= 600:
            if pygame.mouse.get_pos()[1] >= 350 and pygame.mouse.get_pos()[1] <= 400:
                pygame.draw.rect(SCREEN,DARKWHITE,saveButton.selectedRect)
                SCREEN.blit(saveButton.selectedText,sbTextRect)
                SAVEVARIABLES = dict(savedIncome=INCOME,savedTreasury=TREASURY,savedHouses=houseCoords,savedRoads=roadCoords)
                if pygame.mouse.get_pressed() == (1,0,0):
                    while True:
                        save_input = input("Do you want to save? Y/N ")
                        if save_input.upper() == "Y":
                            try:
                                filename = input("Enter save name: ")
                                file = open(f"{filename}.json", "x")
                            except FileExistsError:
                                raw_input = input(
                                    "This file already exists! Are you sure you want to overwrite it? Y/N "
                                )
                                if raw_input.upper() == "Y":
                                    if os.path.exists(f"{filename}.json"):
                                        os.remove(f"{filename}.json")
                                        with open(f"{filename}.json", "w") as save:
                                            json.dump(SAVEVARIABLES, save)
                                    break
                                elif raw_input.upper() == "N":
                                    continue
                                else:
                                    print("Invalid")
                                    continue
                            else:
                                json.dump(SAVEVARIABLES, file)
                                file.close()
                                break
                        elif save_input.upper() == "N":
                            break
                        else:
                            print("Invalid")
                            continue
                    pygame.quit()
        try:
            pygame.display.update()
        except Exception:
            quit()