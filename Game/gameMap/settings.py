from pygame.math import Vector2 as vec

#screen
WIDTH , HEIGHT = 610 , 670
TOP_BOTTOM_SPACE = 50
MAP_WIDTH , MAP_HEIGHT = WIDTH-TOP_BOTTOM_SPACE , HEIGHT-TOP_BOTTOM_SPACE

#colors
BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)

#text type
TEXT_SIZE_MENU = 18
FONT_MENU = 'elephant'
TITLE_SIZE = 26
TEXT_SIZE_GAME = 13
FONT_GAME = 'arial black'

#other settings
FPS = 60
START_POS = vec(1,1)