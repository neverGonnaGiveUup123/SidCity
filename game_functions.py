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
    playButton = Button(
        pygame.Rect(200,400,400,100),
        pygame.Rect(205,405,390,90),
        HEADINGFONT.render("Play",True,BLACK),
        None
        )
    pbTextRect = playButton.selectedText.get_rect()
    pbTextRect.center = (400,450)

    yesButton = Button(
        pygame.Rect(100,450,300,50),
        pygame.Rect(105,455,290,40),
        HEADINGFONT.render("Yes",True,BLACK),
        None
    )
    yBTextRect = yesButton.selectedText.get_rect()
    yBTextRect.center = (250,475)

    loaded = False
    while True:
        pygame.event.get()
        KEYS = pygame.key.get_pressed()
        SCREEN.fill(GRASS)
        pygame.draw.rect(SCREEN,RED,playButton.unselectedRect)
        SCREEN.blit(playButton.selectedText,pbTextRect)
        if KEYS[pygame.K_0]:
            break

        if pygame.mouse.get_pos()[0] >= 200 and pygame.mouse.get_pos()[0] <= 600:
            if pygame.mouse.get_pos()[1] >= 400 and pygame.mouse.get_pos()[1] <= 500:
                pygame.draw.rect(SCREEN,DARKRED,playButton.selectedRect)
                SCREEN.blit(playButton.selectedText,pbTextRect)
                pygame.display.update()
                if pygame.mouse.get_pressed() == (1,0,0):
                    while True:
                        pygame.event.get()
                        SCREEN.fill(GRASS)
                        SCREEN.blit(HEADINGFONT.render("Do you want to load a saved game?",True,BLACK),(100,400))
                        pygame.draw.rect(SCREEN,RED,yesButton.unselectedRect)
                        SCREEN.blit(yesButton.selectedText,yBTextRect)
                        if pygame.mouse.get_pos()[0] >= 100 and pygame.mouse.get_pos()[0] <= 300:
                            if pygame.mouse.get_pos()[1] >= 450 and pygame.mouse.get_pos()[1] <= 500:
                                pygame.draw.rect(SCREEN,DARKRED,yesButton.selectedRect)
                                SCREEN.blit(yesButton.selectedText,yBTextRect)
                                if pygame.mouse.get_pressed() == (1,0,0):
                                    try:
                                        with open("saveFile.json", "r") as file:
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
                                    except json.decoder.JSONDecodeError:
                                        print("Corrupted file. You probably did something stupid.")
                                    finally:
                                        loaded = True
                                        break
                                        
                        pygame.display.update()
        if loaded == True:
            break

        pygame.display.update()
        # user_input = input("Do you want to open a saved game? Y/N ")
        # if user_input.upper() == "Y":
        #     try:
        #         user_input = input("Enter name of save game: ")
        #         with open(f"{user_input}.json", "r") as file:
        #             save_game = json.load(file)
        #             TREASURY = save_game["savedTreasury"]
        #             for coords in save_game["savedHouses"]:
        #                 houseCoords.append(tuple(coords))
        #             for coords in save_game["savedRoads"]:
        #                 roadCoords.append(tuple(coords))
        #             for houses in houseCoords:
        #                 INCOME += 10
        #             break
        #     except FileNotFoundError:
        #         print(
        #             "Sorry, this file could not be found. Make sure you spelled it correctly!"
        #         )
        #         continue
        #     except json.decoder.JSONDecodeError:
        #         print("Corrupted file. You probably did something stupid.")
        #         continue

        # elif user_input.upper() == "N":
        #     break
        # else:
        #     print("Invalid")
        #     continue

ecoTextRect = HEADINGFONT.render("Financial Report",True,BLACK).get_rect()
ecoTextRect.center = (360,120)
def create_economy_page():
    pygame.draw.rect(SCREEN,DARKWHITE,pygame.Rect(80,80,560,640))
    SCREEN.blit(HEADINGFONT.render("Financial Report",True,BLACK),ecoTextRect)
    SCREEN.blit(HEADINGFONT.render(f"Treasury: {TREASURY}",True,BLACK),(80,160))
    SCREEN.blit(HEADINGFONT.render(f"Income: {INCOME}",True,BLACK),(80,240))

def pause_screen():
    counter = 0
    while True:
        pygame.event.get()
        SCREEN.fill(GREY)

        quitButton = Button(pygame.Rect(200,400,400,50),pygame.Rect(205,405,390,40),HEADINGFONT.render("Quit",True,BLACK),None)
        pygame.draw.rect(SCREEN,WHITE,quitButton.unselectedRect)
        qbTextRect = quitButton.selectedText.get_rect()
        qbTextRect.center = (400,425)

        saveButton = Button(pygame.Rect(200,350,400,50),pygame.Rect(205,355,390,40),HEADINGFONT.render("Save",True,BLACK),HEADINGFONT.render("Saved successfully!",True,BLACK))
        pygame.draw.rect(SCREEN,WHITE,saveButton.unselectedRect)
        sbTextRect = saveButton.selectedText.get_rect()
        sbUnTextRect = saveButton.unselectedText.get_rect()
        sbTextRect.center = (400,375)
        sbUnTextRect.center = (400,375)

        SCREEN.blit(quitButton.selectedText,qbTextRect)
        if counter != 0:
            pygame.draw.rect(SCREEN,WHITE,saveButton.unselectedRect)
            SCREEN.blit(saveButton.unselectedText,sbUnTextRect)
            counter += 1
        else:
            SCREEN.blit(saveButton.selectedText,sbTextRect)

        if pygame.mouse.get_pos()[0] >= 200 and pygame.mouse.get_pos()[0] <= 600:
            if pygame.mouse.get_pos()[1] >= 400 and pygame.mouse.get_pos()[1] <= 450:
                pygame.draw.rect(SCREEN,DARKWHITE,quitButton.selectedRect)
                SCREEN.blit(quitButton.selectedText,qbTextRect)
                if pygame.mouse.get_pressed() == (1,0,0):
                    pygame.quit()

        if pygame.mouse.get_pos()[0] >= 200 and pygame.mouse.get_pos()[0] <= 600:
            if pygame.mouse.get_pos()[1] >= 350 and pygame.mouse.get_pos()[1] <= 400:
                pygame.draw.rect(SCREEN,DARKWHITE,saveButton.selectedRect)
                if counter != 0:
                    SCREEN.blit(saveButton.unselectedText,sbUnTextRect)
                else:
                    SCREEN.blit(saveButton.selectedText,sbTextRect)
                SAVEVARIABLES = dict(savedIncome=INCOME,savedTreasury=TREASURY,savedHouses=houseCoords,savedRoads=roadCoords)
                if pygame.mouse.get_pressed() == (1,0,0):
                    with open("saveFile.json", 'w') as file:
                        json.dump(SAVEVARIABLES,file)
                    counter += 1
        if counter >= 1000:
            counter = 0
        pygame.display.update()