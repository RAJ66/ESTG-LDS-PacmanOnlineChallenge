import pygame , sys
from settings import *
from pacman import *

pygame.init()

vec = pygame.math.Vector2

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock  = pygame.time.Clock()
        self.gameLoop = True
        self.state = 'menu'
        self.cell_width = MAP_WIDTH//28
        self.cell_height = MAP_HEIGHT//30
        self.pacman = Pacman(self,START_POS)
        self.walls = []
        self.coins = []

        self.load()



    #### GAME LOOP ####
    def run(self):
        while self.gameLoop:
            if self.state == 'menu':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playsingle':
                self.playsingle_events()
                self.playsingle_update()
                self.playsingle_draw()
            else:
                self.gameLoop = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


    def draw_text(self, message, screen, position, size, font_type, color):
        font = pygame.font.SysFont(font_type , size)
        text = font.render(message, False, color)
        text_size = text.get_size()
        position[0] = position[0]-text_size[0]//2
        screen.blit(text, position)

    #### EVENTS KEYS ####
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameLoop = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playsingle'

    def start_update(self):
        pass

    #### MENU ####
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PACMAM ONLINE', self.screen, [WIDTH // 2, HEIGHT // 2-140], TITLE_SIZE, FONT_MENU, YELLOW)
        self.draw_text('CHALLENGE', self.screen, [WIDTH // 2, HEIGHT // 2 - 100], TITLE_SIZE, FONT_MENU, YELLOW)
        self.draw_text('SINGLE PLAYER', self.screen, [WIDTH // 2, HEIGHT // 2+50], TEXT_SIZE_MENU, FONT_MENU, BLUE)
        self.draw_text('MULTIPLAYER', self.screen, [WIDTH // 2, HEIGHT // 2 + 100], TEXT_SIZE_MENU, FONT_MENU, RED)
        self.draw_text('INSTRUCTIONS', self.screen, [WIDTH // 2, HEIGHT // 2 + 150], TEXT_SIZE_MENU, FONT_MENU, GREEN)
        pygame.display.update()

    def playsingle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameLoop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pacman.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.pacman.move(vec(1, 0))
                if event.key == pygame.K_DOWN:
                    self.pacman.move(vec(0, 1))
                if event.key == pygame.K_UP:
                    self.pacman.move(vec(0, -1))

    def playsingle_update(self):
        self.pacman.update()

    def playsingle_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background,(TOP_BOTTOM_SPACE//2,TOP_BOTTOM_SPACE//2))
        self.draw_coins()
        #self.draw_grid() #REDE
        self.draw_text('CURRENT SCORE : {}'.format(self.pacman.score), self.screen, [100,0], TEXT_SIZE_GAME, FONT_GAME, WHITE)
        self.draw_text('TIME : 0', self.screen, [550, 0], TEXT_SIZE_GAME, FONT_GAME, WHITE)
        self.draw_text('PACMAN ONLINE CHALLENGE', self.screen, [WIDTH//2, 650], TEXT_SIZE_GAME, FONT_GAME, YELLOW)
        self.pacman.draw()
        pygame.display.update()
        #self.coins.pop()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen,LIGHT_YELLOW , (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_SPACE//2,int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_SPACE//2),4)

    def draw_grid(self):
        for x in range (WIDTH//self.cell_width):
            pygame.draw.line(self.background, WHITE , (x*self.cell_width,0), (x*self.cell_width, HEIGHT))
        for x in range (HEIGHT//self.cell_height):
            pygame.draw.line(self.background, WHITE , (0 , x*self.cell_height), (WIDTH, x*self.cell_height))
        for coin in self.coins:
            pygame.draw.rect(self.background, GREEN, (coin.x*self.cell_width,coin.y*self.cell_height,self.cell_width,self.cell_height))


    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAP_WIDTH, MAP_HEIGHT))
        #settings wall while opening
        with open("walls.txt",'r') as fp:
            for yindex,line in enumerate(fp):
                for xindex,char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xindex,yindex))
                    elif char == "C":
                        self.coins.append(vec(xindex,yindex))

