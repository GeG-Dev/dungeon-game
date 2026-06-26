import pygame
#настройки карты
MINI_MAP_SIZE_X = 41 #размер карты
MINI_MAP_SIZE_Y = 101 #размер карты
TILE_SIZE = 100
PLAYER_SIZE = 75
BOX_CHANCE = 0.3
SCREEN_STEP = 50
START_VIEW = 5000

FLOOR = 0
WALL = 1
FLOOR_PORTAL_DOWN = 2
FLOOR_PORTAL_UP = 3
PORTAL = 9
THORNS = 4
TIMERS_THORNS = 5
IS_RETURN_HOME = 1

thornsChance = 0.1
timerThornsChance = 0.3
STARTED_THORNS_CHANCE = 0.1
STARTED_TIMER_THORNS_CHANCE = 0.3
THORNS_CHANGE_STEP = 0.1

MAX_LEVEL = 7

pygame.init()

monitorInfo = pygame.display.Info()
screenW = monitorInfo.current_w
screenH = monitorInfo.current_h

PLAYER_SPEED = 12
VOLUME_STEP = 0.05
SAVE_FILE_DIR = "save.json"

#параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
