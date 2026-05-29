import config
import json
import random

player_stats = {"hp":100 , "lvl":0,"inventary":[]}

class Player:
    def __init__(self , name ="empty", hp = 100, lvl = 0, inventary = [], playerSpeed = 10):
        self.__playerStats = {"name":name,"hp":hp , "lvl":lvl,"inventary":inventary}
        
        self.speed = playerSpeed
        self.playerX = 0
        self.playerY = 0
        
    def getName(self):
        return self.__playerStats["name"]
    def getLvl(self):
        return self.__playerStats["lvl"]
    def getHp(self):
        return self.__playerStats["hp"]
    def getInventary(self):
        return self.__playerStats["inventary"]
    def getSpeed(self):
        return self.speed
    def setSpeed(self ,speed):
        self.speed = speed
    def moveRight(self):
        if self.playerX > -(config.TILE_SIZE * config.MINI_MAP_SIZE_X - config.screenW):
            self.playerX -= self.speed 
    def moveLeft(self):
        if self.playerX < 0:
            self.playerX += self.speed 
    def moveForward(self):
        if self.playerY < 0:
            self.playerY += self.speed 
    def moveBackward(self):
        if self.playerY > -(config.TILE_SIZE * config.MINI_MAP_SIZE_Y - config.screenH):
            self.playerY -= self.speed
    def getXY(self):
        return [self.playerX , self.playerY]
    
    
    
class Map:
    def __init__(self , size_x , size_y ):
        self.mapSizeX = size_x
        self.mapSizeY = size_y
        self.__grid = []
    
    def generateMap(self):
        self.__grid.clear()
        for y in range(self.mapSizeY):
            row = []
            for x in range(self.mapSizeX):
                if x == 0 or x == self.mapSizeX - 1 or y == 0 or y == self.mapSizeY - 1:
                    row.append(1)
                else:
                    row.append(0 if random.random() > config.BOX_CHANCE else 1)
            self.__grid.append(row)
        # print(self.__grid)
    def getMapXY(self , x , y):return self.__grid[y][x]
        
    
map = Map(config.MINI_MAP_SIZE_X , config.MINI_MAP_SIZE_Y)
map.generateMap()

player = Player("bob",  100, 0, [], config.PLAYER_SPEED)