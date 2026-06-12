import config
import logic
import pygame
import time
import random
import btn



clock = pygame.time.Clock()
screen = pygame.display.set_mode((config.screenW , config.screenH ), pygame.NOFRAME | pygame.SCALED )
viewPlace = pygame.Surface((config.screenW , config.screenH) , pygame.SRCALPHA)
font = pygame.font.SysFont("Arial" , 22)

FLOOR_IMG = pygame.transform.scale(pygame.image.load("pictures/woodFloor.jpg") , (config.TILE_SIZE , config.TILE_SIZE))
WALL_IMG = pygame.transform.scale(pygame.image.load("pictures/woodWall.png") , (config.TILE_SIZE , config.TILE_SIZE))
DOOR_IMG = pygame.transform.scale(pygame.image.load("pictures/door.png") , (config.TILE_SIZE , config.TILE_SIZE))
THORNS_IMG = pygame.transform.scale(pygame.image.load("pictures/thorns.png") , (config.TILE_SIZE , config.TILE_SIZE))
GHOST_PNG = pygame.transform.scale(pygame.image.load("pictures/ghost.png") , (config.PLAYER_SIZE , config.PLAYER_SIZE))
HEART_IMG = pygame.transform.scale(pygame.image.load("pictures/heart.png") , (config.PLAYER_SIZE // 1.5 , config.PLAYER_SIZE // 1.5))
# HEART_IMG = pygame.transform.scale(pygame.image.load("pictures/heart.png") , (config.TILE_SIZE // 2 , config.TILE_SIZE // 2))
GAME_TITLE = pygame.transform.scale(pygame.image.load("pictures/gameName.png") , (config.screenW // 3 , config.screenH // 3))
pygame.mixer.music.load("music/bgMusic.mp3")

try:
    data = logic.readData()
    volume = data["bob"]["volume"]

except Exception as e:
    volume = 0.1
    print(e)

pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

btnX = 200
btnY = 60
startBtn = btn.button(config.screenW // 2 - 100 , config.screenH // 2 , btnX, btnY , (150,100,0) , (250,200,0) , "play")
settingsBtn = btn.button(config.screenW // 2 - 100  , config.screenH // 2 + btnY*1.5 , btnX , btnY , (150,100,0) , (250,200,0) , "settings")
exitBtn = btn.button(config.screenW // 2 - 100  , config.screenH // 2 + btnY*3 , btnX , btnY , (150,100,0) , (250,200,0) , "exit")


resumeBtn = btn.button(config.screenW // 2 - 100 , config.screenH // 2  + btnY*1.5, btnX, btnY  , (150,100,0) , (250,200,0) , "resume")
exitMainMenuBtn = btn.button(config.screenW // 2 - 100  , config.screenH // 2 + btnY*3 , btnX , btnY , (150,100,0) , (250,200,0) , "exit")
gameMenu = 1

minus = btn.button(config.screenW // 2 - 300 , config.screenH // 2 , btnX, btnY , (150,100,0) , (250,200,0) , "-")
plus = btn.button(config.screenW // 2 + 100 , config.screenH // 2 , btnX, btnY , (150,100,0) , (250,200,0) , "+")

logic.map.generateMap()
running = True
frame = 0

def mainMenu():
    global gameMenu , frame , volume
    clock.tick(60)
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameMenu = False
            pygame.quit()
            quit()
        if startBtn.click(event , mousePos): 
            gameMenu = 2
            pygame.mixer.music.load("music/gameMusic.mp3")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        if exitBtn.click(event , mousePos):
            gameMenu = 0
            pygame.quit()
            quit()
        if settingsBtn.click(event , mousePos):
            gameMenu = 3
            
    frame += 1
    img = pygame.transform.scale(pygame.image.load(f"gameVideo/{frame:04d}.png") , (config.screenW , config.screenH))
    if frame >= 101:frame = 0
    
    screen.blit(img , (0,0))
    screen.blit(GAME_TITLE , (config.screenW // 3,config.screenH // 6))
    startBtn.checkHover(mousePos)
    startBtn.draw(screen)
    settingsBtn.checkHover(mousePos)
    settingsBtn.draw(screen)
    exitBtn.checkHover(mousePos)
    exitBtn.draw(screen)
    pygame.display.flip()


def settingsMenu():
    global gameMenu
    global volume
    clock.tick(60)
    screen.fill((150,150,150))
    plus.checkHover(mousePos)
    minus.checkHover(mousePos)
    exitBtn.checkHover(mousePos)
    plus.draw(screen)
    minus.draw(screen)
    exitBtn.draw(screen)
    pygame.mixer.music.set_volume(volume)
    
    textVolume = btn.button(config.screenW // 2 - 100 , config.screenH // 2 , btnX, btnY , (150,100,0) , (150,100,0) , f"{volume*100:1f}")
    textVolume.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameMenu = False
        if exitBtn.click(event , mousePos): gameMenu = 1
        if plus.click(event , mousePos):volume += config.VOLUME_STEP
        if minus.click(event , mousePos): volume -= config.VOLUME_STEP
    volume = min(max(0 , volume) , 1)
    pygame.display.flip()


def game():
    global gameMenu , volume
    tmr = clock.tick(60) / 1000.0
    screen.fill((0,0,0))
    playerPos = logic.player.getXY()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:gameMenu = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = True
        while run:
            mousePos = pygame.mouse.get_pos()
            screen.fill((150,150,150))
            resumeBtn.checkHover(mousePos)    
            exitMainMenuBtn.checkHover(mousePos)    
            resumeBtn.draw(screen)    
            exitMainMenuBtn.draw(screen)
            plus.checkHover(mousePos)
            minus.checkHover(mousePos)
            plus.draw(screen)
            minus.draw(screen)
            pygame.mixer.music.set_volume(volume)
            
            textVolume = btn.button(config.screenW // 2 - 100 , config.screenH // 2 , btnX, btnY , (150,100,0) , (150,100,0) , f"{volume*100:1f}")
            textVolume.draw(screen)
            for event in pygame.event.get():
                if resumeBtn.click(event , mousePos):run = False
                if exitMainMenuBtn.click(event , mousePos):
                    pygame.mixer.music.load("music/bgMusic.mp3")
                    pygame.mixer.music.set_volume(volume)
                    pygame.mixer.music.play(-1)
                    gameMenu = 1
                    run = False
                
                if plus.click(event , mousePos):volume += config.VOLUME_STEP
                if minus.click(event , mousePos): volume -= config.VOLUME_STEP
            volume = min(max(0 , volume) , 1)
                
            pygame.display.flip()
    if keys[pygame.K_SPACE]:
        logic.map.generateMap()
    if keys[pygame.K_d]:
        logic.player.moveRight()
    if keys[pygame.K_a]:
        logic.player.moveLeft()
    if keys[pygame.K_w]:
        logic.player.moveForward()
    if keys[pygame.K_s]:
        logic.player.moveBackward()
    logic.player.updateTimer(tmr)
    logic.player.checkDamage()
    logic.player.checkLevelChange()
        
    camPosX = config.screenW // 2 - playerPos[0]
    camPosY = config.screenH  // 2- playerPos[1]
        
    for y in range(config.MINI_MAP_SIZE_Y):
        for x in range(config.MINI_MAP_SIZE_X):
            xTilePos = camPosX + x * config.TILE_SIZE
            yTilePos =  camPosY + y * config.TILE_SIZE
            coordinate = logic.map.getMapXY(x , y)
            screen.blit(FLOOR_IMG , (xTilePos ,yTilePos))
            if coordinate == config.WALL:
                screen.blit(WALL_IMG , (xTilePos ,yTilePos))
            if coordinate == config.PORTAL:
                screen.blit(DOOR_IMG , (xTilePos , yTilePos))
            if coordinate == config.THORNS:
                screen.blit(THORNS_IMG , (xTilePos , yTilePos))

    playerImg = pygame.transform.rotate(GHOST_PNG , logic.player.getAngle())
    if logic.player.isInvisible():playerImg.set_alpha(120)
    else:playerImg.set_alpha(255)
    imgRect = playerImg.get_rect()
    imgRect.center = (config.screenW // 2 , config.screenH // 2)
    screen.blit(playerImg , imgRect)
    
    # рисую круг для ограничения вида
    viewPlace.fill((0,0,0,255))
    pygame.draw.circle(viewPlace , (0,0,0,0) , (config.screenW // 2, config.screenH // 2) , logic.player.getViewSize())
    screen.blit(viewPlace , (0,0))
    
    #рисую хп
    for i in range(logic.player.getHp()):
        screen.blit(HEART_IMG , (5 + i * config.TILE_SIZE // 2 , 5))
    
    pygame.display.flip()

while gameMenu:
    mousePos = pygame.mouse.get_pos()
    
    match gameMenu:
        case 1:
            mainMenu()
        case 2:
            game()
        case 3:
            settingsMenu()
    
    data = {logic.player.getName():{"hp":logic.player.getHp(),"lvl":logic.player.getLvl(),"inventory":logic.player.getInventary(),"volume":volume,"viewSize":logic.player.getViewSize()}}
    logic.saveData(data)
    
pygame.quit()


