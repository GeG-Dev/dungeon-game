import config
import logic
import pygame
import time
import random



screen = pygame.display.set_mode((config.screenW , config.screenH ), pygame.NOFRAME | pygame.SCALED )
# screen = pygame.display.set_mode((config.SCREEN_HEIGHT , config.SCREEN_WIDTH))
# screen = pygame.display.set_mode(py)

FLOOR_IMG = pygame.transform.scale(pygame.image.load("pictures/woodFloor.jpg") , (config.TILE_SIZE , config.TILE_SIZE))
WALL_IMG = pygame.transform.scale(pygame.image.load("pictures/woodWall.png") , (config.TILE_SIZE , config.TILE_SIZE))



logic.map.generateMap()
running = True
while running:
    playerPos = logic.player.getXY()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:running = False
    keys = pygame.key.get_pressed()
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
        
    for y in range(config.MINI_MAP_SIZE_Y):
        for x in range(config.MINI_MAP_SIZE_X):
            screen.blit(FLOOR_IMG , (playerPos[0] + x * config.TILE_SIZE , playerPos[1] + y * config.TILE_SIZE))
            if logic.map.getMapXY(x , y) == 1:
                screen.blit(WALL_IMG , (playerPos[0] + x * config.TILE_SIZE , playerPos[1] +y * config.TILE_SIZE))

    # pygame.draw.rect(screen , (10,10,10) , ())
    pygame.display.flip()
pygame.quit()


