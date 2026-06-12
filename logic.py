import config
import json
import random

player_stats = {"hp":3 , "lvl":0,"inventary":[] , "viewSize":config.START_VIEW}



class Player:
    def __init__(self , name ="empty", hp = 3, lvl = 0, inventary = [], playerSpeed = 10 , viewSize = config.START_VIEW):
        self.__playerStats = {"name":name,"hp":hp , "lvl":lvl,"inventary":inventary,"viewSize":viewSize}
        
        self.lvl = lvl
        self.speed = playerSpeed
        self.playerX = config.TILE_SIZE + (config.TILE_SIZE // 2)
        self.playerY = config.TILE_SIZE + (config.TILE_SIZE // 2)
        self.angle = 0
        self.viewSize = viewSize
        
    def getName(self):return self.__playerStats["name"]
    def getLvl(self):return self.__playerStats["lvl"]
    def getHp(self):return self.__playerStats["hp"]
    def getInventary(self): return self.__playerStats["inventary"]
    def getSpeed(self):return self.speed
    def getAngle(self): return self.angle
    def setSpeed(self ,speed):self.speed = speed
    def checkColision(self , newX , newY):
        offset = config.PLAYER_SIZE // 2
        
        pointForCheck = [
            (newX - offset , newY - offset), # left / up
            (newX - offset , newY + offset), # left / down
            (newX + offset , newY - offset), #right / up
            (newX + offset , newY + offset) #right / down
        ]
        
        for cx , cy in pointForCheck:
            tileX = int(cx // config.TILE_SIZE)
            tileY = int(cy // config.TILE_SIZE)
            
            if tileX < 0 or tileX >= config.MINI_MAP_SIZE_X or tileY < 0 or tileY >= config.MINI_MAP_SIZE_Y:
                return False
            if map.getMapXY(tileX , tileY) == 1:
                return False
        return True
    
    
    def moveRight(self):
        newX = self.playerX + self.speed
        if self.checkColision(newX  , self.playerY):
            self.playerX = newX
            self.angle = 90 
    def moveLeft(self):
        newX = self.playerX - self.speed 
        if self.checkColision(newX  , self.playerY):
            self.playerX = newX 
            self.angle = 270 
    def moveForward(self):
        newY = self.playerY - self.speed 
        if self.checkColision(self.playerX ,newY):
            self.playerY = newY
            self.angle = 180 
    def moveBackward(self):
        newY = self.playerY + self.speed
        if self.checkColision(self.playerX , self.playerY):
            self.playerY = newY
            self.angle = 0 
    
    def getXY(self):return [self.playerX , self.playerY]

    def getViewSize(self):return self.viewSize
    def nextLevel(self):
        self.lvl += 1
        self.viewSize = (max(self.viewSize , 100))
    
    
    
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
                if y == 1 and x != 0 and x != self.mapSizeX - 1:
                    row.append(0)
                elif y == self.mapSizeY - 2 and x != 0 and x != self.mapSizeX - 1:
                    row.append(0)
                elif x == 0 or x == self.mapSizeX - 1 or y == 0 or y == self.mapSizeY - 1:
                    row.append(1)
                else:
                    row.append(0 if random.random() > config.BOX_CHANCE else 3)
                
            self.__grid.append(row)
        # print(self.__grid)
    def getMapXY(self , x , y):return self.__grid[y][x]
        
def saveData(txt):
    with open(config.SAVE_FILE_DIR , "w" ) as f:
        json.dump( txt , f)
def readData():
    with open(config.SAVE_FILE_DIR , "r") as f:
        return json.load(f)


map = Map(config.MINI_MAP_SIZE_X , config.MINI_MAP_SIZE_Y)
map.generateMap()

player = Player("bob",  3, 0, [], config.PLAYER_SPEED)