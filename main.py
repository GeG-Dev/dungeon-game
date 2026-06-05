import config
import logic
import pygame
import time
import random
import btn


clock = pygame.time.Clock()
screen = pygame.display.set_mode((config.screenW , config.screenH ), pygame.NOFRAME | pygame.SCALED )
font = pygame.font.SysFont("Arial" , 22)

# screen = pygame.display.set_mode((config.SCREEN_HEIGHT , config.SCREEN_WIDTH))
# screen = pygame.display.set_mode(py)

FLOOR_IMG = pygame.transform.scale(pygame.image.load("pictures/woodFloor.jpg") , (config.TILE_SIZE , config.TILE_SIZE))
WALL_IMG = pygame.transform.scale(pygame.image.load("pictures/woodWall.png") , (config.TILE_SIZE , config.TILE_SIZE))
GHOST_PNG = pygame.transform.scale(pygame.image.load("pictures/ghost.png") , (config.PLAYER_SIZE , config.PLAYER_SIZE))
GAME_TITLE = pygame.transform.scale(pygame.image.load("pictures/gameName.png") , (config.screenW // 3 , config.screenH // 3))
pygame.mixer.music.load("music/bgMusic.mp3")

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
# print(f"{5:04d}")
# while True:pass


btnX = 200
btnY = 60
startBtn = btn.button(config.screenW // 2 - 100 , config.screenH // 2 , btnX, btnY , (150,100,0) , (250,200,0) , "play")
settingsBtn = btn.button(config.screenW // 2 - 100  , config.screenH // 2 + btnY*1.5 , btnX , btnY , (150,100,0) , (250,200,0) , "settings")
exitBtn = btn.button(config.screenW // 2 - 100  , config.screenH // 2 + btnY*3 , btnX , btnY , (150,100,0) , (250,200,0) , "exit")


resumeBtn = btn.button(config.screenW // 2 - 100 , config.screenH // 2 , btnX, btnY , (150,100,0) , (250,200,0) , "resume")
exitMainMenuBtn = btn.button(config.screenW // 2 - 100  , config.screenH // 2 + btnY*1.5 , btnX , btnY , (150,100,0) , (250,200,0) , "exit")
gameMenu = 1

frame = 0
def mainMenu():
    global gameMenu , frame
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
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        if exitBtn.click(event , mousePos):
            gameMenu = 0
            pygame.quit()
            quit()
            
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



logic.map.generateMap()
running = True
def game():
    global gameMenu
    clock.tick(60)
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
            for event in pygame.event.get():
                if resumeBtn.click(event , mousePos):run = False
                if exitMainMenuBtn.click(event , mousePos):
                    pygame.mixer.music.load("music/bgMusic.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    gameMenu = 1
                    run = False
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
        
    camPosX = config.screenW // 2 - playerPos[0]
    camPosY = config.screenH  // 2- playerPos[1]
        
    for y in range(config.MINI_MAP_SIZE_Y):
        for x in range(config.MINI_MAP_SIZE_X):
            xTilePos = camPosX + x * config.TILE_SIZE
            yTilePos =  camPosY + y * config.TILE_SIZE
            screen.blit(FLOOR_IMG , (xTilePos ,yTilePos))
            if logic.map.getMapXY(x , y) == 1:
                screen.blit(WALL_IMG , (xTilePos ,yTilePos))

    playerImg = pygame.transform.rotate(GHOST_PNG , logic.player.getAngle())
    imgRect = playerImg.get_rect()
    imgRect.center = (config.screenW // 2 , config.screenH // 2)
    screen.blit(playerImg , imgRect)
    
    pygame.display.flip()

while gameMenu:
    mousePos = pygame.mouse.get_pos()
    
    match gameMenu:
        case 1:
            mainMenu()
        case 2:
            game()




pygame.quit()


