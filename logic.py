import config
import json
import random

player_stats = {"hp":30 , "lvl":0,"inventary":[] , "viewSize":config.START_VIEW}



class Player:
    def __init__(self , name ="empty", hp = 3, lvl = 0, inventary = [], playerSpeed = 10 , viewSize = config.START_VIEW):
        self.__playerStats = {"name":name,"hp":hp , "lvl":lvl,"inventary":inventary,"viewSize":viewSize}
        

        self.speed = playerSpeed
        # self.playerX = config.TILE_SIZE + (config.TILE_SIZE // 2)
        # self.playerY = config.TILE_SIZE + (config.TILE_SIZE // 2)
        self.playerY = config.MINI_MAP_SIZE_Y // 2 * config.TILE_SIZE
        self.playerX = config.MINI_MAP_SIZE_X // 2 * config.TILE_SIZE
        self.angle = 0
        self.viewSize = viewSize
        self.invisible = 0
        
    def getName(self):return self.__playerStats["name"]
    def getLvl(self):return self.__playerStats["lvl"]
    def getHp(self):return self.__playerStats["hp"]
    def getInventary(self): return self.__playerStats["inventary"]
    def getSpeed(self):return self.speed
    def getAngle(self): return self.angle
    def setSpeed(self ,speed):self.speed = speed
    def isInvisible(self): return self.invisible > 0
    def setLvl(self, lvl): self.__playerStats["lvl"] = lvl
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
                return 1
            if map.getMapXY(tileX , tileY) == config.WALL:
                return 1
            if map.getMapXY(tileX , tileY) == config.THORNS:
                return 2
            if map.getMapXY(tileX , tileY) == config.TIMERS_THORNS:
                return 3
            if map.getMapXY(tileX , tileY) == config.PORTAL:
                return config.PORTAL
        return 0
    
    def updateTimer(self , tmr):
        if self.invisible > 0: self.invisible -= tmr
    def checkDamage(self):
        if self.isInvisible(): return
        if self.checkColision(self.playerX , self.playerY) == 2:
            self.__playerStats["hp"] = self.__playerStats["hp"] - 1
            # if config.IS_RETURN_HOME:
            #     self.playerY = config.MINI_MAP_SIZE_Y // 2 * config.TILE_SIZE
            #     self.playerX = config.MINI_MAP_SIZE_X // 2 * config.TILE_SIZE
            self.invisible = 5
            return True
        return False
    def checkDamageTmr(self):
        if self.isInvisible(): return
        if self.checkColision(self.playerX , self.playerY) == 3:
            self.__playerStats["hp"] = self.__playerStats["hp"] - 1
            # if config.IS_RETURN_HOME:
            #     self.playerY = config.MINI_MAP_SIZE_Y // 2 * config.TILE_SIZE
            #     self.playerX = config.MINI_MAP_SIZE_X // 2 * config.TILE_SIZE
            self.invisible = 5
            return True
        return False
    def checkLevelChange(self):
        if self.checkColision(self.playerX , self.playerY) == config.PORTAL:
            map.generateMap()
            self.playerY = config.MINI_MAP_SIZE_Y // 2 * config.TILE_SIZE
            self.playerX = config.MINI_MAP_SIZE_X // 2 * config.TILE_SIZE
            return True
        return False        
    def moveRight(self):
        newX = self.playerX + self.speed
        if not self.checkColision(newX  , self.playerY) == 1:
            self.playerX = newX
            self.angle = 90 
    def moveLeft(self):
        newX = self.playerX - self.speed 
        if not  self.checkColision(newX  , self.playerY) == 1:
            self.playerX = newX 
            self.angle = 270 
    def moveForward(self):
        newY = self.playerY - self.speed 
        if not self.checkColision(self.playerX ,newY) == 1:
            self.playerY = newY
            self.angle = 180 
    def moveBackward(self):
        newY = self.playerY + self.speed
        if not self.checkColision(self.playerX ,newY) == 1:
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
        self.boolInvisible = False
        self.invisible = 0
    def updateTimer(self , tmr):
        if self.invisible > 0: self.invisible -= tmr
        else:
            self.invisible = (random.randint(5,30) / 10)
            self.boolInvisible = not self.boolInvisible
    def isShow(self ):return self.boolInvisible

            
    def generateMap(self):
        self.__grid = [[1 for _ in range(self.mapSizeX)] for _ in range(self.mapSizeY)]
        for y in range(1 , self.mapSizeY , 2):
            for x in range(1 , self.mapSizeX , 2):
                self.__grid[y][x] = config.FLOOR
                directions = []
                if y > 1 :
                    directions.append("UP")
                if x < self.mapSizeX - 1:
                    directions.append("RIGHT")
                
                if directions:
                    dir = random.choice(directions)
                    if dir == "UP":self.__grid[y - 1][x] = config.FLOOR
                    if dir == "RIGHT":self.__grid[y][x + 1] = config.FLOOR
        
        for y in range(1 , self.mapSizeY):
            self.__grid[y][self.mapSizeX - 1] = config.WALL
            if y >= self.mapSizeY - 3 and y != self.mapSizeY - 1: 
                for x in range(1, self.mapSizeX - 1): 
                    self.__grid[y][x] = config.FLOOR
        self.__grid[self.mapSizeY - 2][random.randint(1 , self.mapSizeX - 2)] = config.PORTAL
        self.__grid[1][random.randint(1 , self.mapSizeX - 2)] = config.PORTAL
        for y in range(1 , self.mapSizeY - 1):
            for x in range(1 , self.mapSizeX - 1):
                if self.__grid[y][x] == config.WALL:
                    if random.random() < config.thornsChance: self.__grid[y][x] = config.THORNS
                    elif random.random() < config.timerThornsChance:self.__grid[y][x] = config.TIMERS_THORNS
        startY = config.MINI_MAP_SIZE_Y // 2
        startX = config.MINI_MAP_SIZE_X // 2
        for y in range(startY - 2 , startY + 3):
            for x in range(startX - 2 , startX + 3):
                self.__grid[y][x] = config.FLOOR
                if y == startY:
                    if x == startX - 1:
                        self.__grid[y][x] = config.FLOOR_PORTAL_DOWN
                    if x == startX + 1:
                        self.__grid[y][x] = config.FLOOR_PORTAL_UP
                

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