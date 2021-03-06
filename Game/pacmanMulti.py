import pygame , sys , socket , time
vec = pygame.math.Vector2
from settings import *
import MenuPrincipal
import requests
import json

HOST = '127.0.0.1'
PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


pygame.init()

class pacmanMulti:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.gameLoop = True
        self.state = 'playing'
        self.cell_width = MAP_WIDTH // NUMBER_CELLS_WIDTH
        self.cell_height = MAP_HEIGHT // NUMBER_CELLS_HEIGHT
        #self.pixel_pos = self.get_pix_pos()
        self.direction = vec(1,0)
        self.buffer_direction = None
        self.can_move = True
        self.score = 0
        self.speed = 2
        self.walls = []
        self.player_position = None
        self.load()
        self.grid_pos = vec(self.player_position)
        self.pixel_pos = self.get_pix_pos()
        self.enemy_x = None
        self.enemy_y = None
        self.start_time = time.time()
        self.current_time = None
        self.username = ''
        self.score = 0

    def run(self, user):
        self.username = user
        while self.gameLoop:
            if self.state == 'playing':
                try:
                    myCoord = bytes(str(self.pixel_pos[0]) + "/" + str(self.pixel_pos[1]) + "/" + str(self.current_time), 'utf-8')
                    s.sendall(myCoord)
                    otherPlayerCoord = s.recv(1024)
                    decode = otherPlayerCoord.decode('utf-8').split("/")
                    self.enemy_x, self.enemy_y = float(decode[0]), float(decode[1])
                except:
                    if int(self.current_time) < 60:
                        self.score = 500
                    elif int(self.current_time) > 60:
                        self.score = 1000
                    self.gameover_draw()
                    time.sleep(5)
                    self.updateUser()
                    MenuPrincipal.menuPrincipal(self.username)

                self.multiplayer_events()
                self.multiplayer_update()
                self.multiplayer_draw()

            else:
                self.gameLoop = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def updateUser(self):
        url = "https://localhost:5001/api/game/multiplayerchallenge"
        data = {'Username': str(self.username), 'Score': str(self.score)}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers, verify= False)
        print(r.status_code)

    def draw_enemy(self,x,y):
        self.screen.blit(self.redGhost, (int(x)-8, int(y)-8))

    def update(self):
        if self.can_move:
            self.pixel_pos += self.direction*self.speed

        if self.time_to_move_x():
            if self.buffer_direction != None:
                self.direction = self.buffer_direction
            self.can_move = self.let_move()
        if self.time_to_move_y():
            if self.buffer_direction != None:
                self.direction = self.buffer_direction
            self.can_move = self.let_move()

        self.grid_pos[0] = (self.pixel_pos[0]-TOP_BOTTOM_SPACE+self.cell_width//2)//self.cell_width + 1
        self.grid_pos[1] = (self.pixel_pos[1] - TOP_BOTTOM_SPACE+self.cell_height//2) // self.cell_height + 1



    def multiplayer_update(self):
        self.update()

        #inimigos



    def draw(self):
        if(self.direction == vec(1,0)):
            self.screen.blit(self.yellowPacman, (int(self.pixel_pos.x - 8), int(self.pixel_pos.y - 8)))
        elif (self.direction == vec(-1,0)):
            self.screen.blit(pygame.transform.flip(self.yellowPacman,True, False), (int(self.pixel_pos.x - 8), int(self.pixel_pos.y - 8)))
        elif (self.direction == vec(0,1)):
            self.screen.blit(pygame.transform.rotate(self.yellowPacman, 270), (int(self.pixel_pos.x - 8), int(self.pixel_pos.y - 8)))
        elif (self.direction == vec(0,-1)):
            self.screen.blit(pygame.transform.rotate(self.yellowPacman, 90), (int(self.pixel_pos.x - 8), int(self.pixel_pos.y - 8)))


    def move(self,direction):
        self.buffer_direction = direction

    def get_pix_pos(self):
        return  vec((self.grid_pos.x*self.cell_width)+TOP_BOTTOM_SPACE//2+self.cell_width//2,
                             (self.grid_pos.y*self.cell_height)+TOP_BOTTOM_SPACE//2+self.cell_height//2)

    def time_to_move_x(self):
        if int(self.pixel_pos.x+TOP_BOTTOM_SPACE//2)%self.cell_width==0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0) or self.direction == vec(0,0):
                return True

    def time_to_move_y(self):
        if int(self.pixel_pos.y+TOP_BOTTOM_SPACE//2)%self.cell_height==0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1) or self.direction == vec(0,0):
                return True

    def let_move(self):
        for wall in self.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True


    def load(self):
        self.background = pygame.image.load('img/maze.png')
        self.redGhost = pygame.image.load('img/vermelho.png')
        self.redGhost = pygame.transform.scale(self.redGhost,(14,14))
        self.yellowPacman = pygame.image.load('img/pacman.png')
        self.yellowPacman = pygame.transform.scale(self.yellowPacman,(20,20))
        #self.coin_sound = pygame.mixer.Sound('music/coin.wav')
        #self.gameover_sound = pygame.mixer.Sound('music/gameover.wav')

        #HA FALTA DE MELHOR VAI TER QUE SER ASSIM com a string
        self.background = pygame.transform.scale(self.background, (MAP_WIDTH, MAP_HEIGHT))
        #settings wall while opening and characters / coins
        with open("walls_pacman_multi.txt",'r') as fp:
            for yindex,line in enumerate(fp):
                for xindex,char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xindex,yindex))
                    elif char == "P":
                        self.player_position = [xindex, yindex]
                    elif char == "B":
                        pygame.draw.rect(self.background,BLACK, (xindex*self.cell_width,yindex*self.cell_height,self.cell_width,self.cell_height))

                    ##por char == 'E' para inimigo

    def draw_text(self, message, screen, position, size, font_type, color):
        font = pygame.font.SysFont(font_type , size)
        text = font.render(message, False, color)
        text_size = text.get_size()
        position[0] = position[0]-text_size[0]//2
        screen.blit(text, position)


    def multiplayer_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_SPACE // 2, TOP_BOTTOM_SPACE // 2))
        time_difference = time.time() - self.start_time
        time_difference = str(time_difference)
        time_difference = time_difference.split(".")
        self.current_time = time_difference[0]
        self.draw_text('TIME : {}'.format(time_difference[0]), self.screen, [550, 0], TEXT_SIZE_GAME, FONT_GAME, WHITE)
        self.draw_text('PACMAN ONLINE CHALLENGE', self.screen, [WIDTH // 2, 650], TEXT_SIZE_GAME, FONT_GAME, YELLOW)
        self.draw()
        self.draw_enemy(self.enemy_x,self.enemy_y)
        pygame.display.update()


    def draw_coins(self):
        for coin in self.coins:
            self.screen.blit(self.coin, ((int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_SPACE//2)-8,
                                         (int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_SPACE//2)-8))

    def multiplayer_events(self):

        try:
            j = pygame.joystick.Joystick(0)
            j.init()

            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if j.get_axis(0) > 0.2:
                        self.move(vec(1,0))
                    elif j.get_axis(0) < -0.2:
                        self.move(vec(-1,0))
                    elif j.get_axis(1) > 0.2:
                        self.move(vec(0,1))
                    elif j.get_axis(1) < -0.2:
                        self.move(vec(0,-1))
                    elif j.get_hat(0) == (0 , 1):
                        self.move(vec(0,-1))
                    elif j.get_hat(0) == (0 , -1):
                        self.move(vec(0,1))
                    elif j.get_hat(0) == (1 , 0):
                        self.move(vec(1,0))
                    elif j.get_hat(0) == (-1 , 0):
                        self.move(vec(-1,0))

        except:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameLoop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(vec(-1,0))
                    elif event.key == pygame.K_RIGHT:
                        self.move(vec(1, 0))
                    elif event.key == pygame.K_DOWN:
                        self.move(vec(0, 1))
                    elif event.key == pygame.K_UP:
                        self.move(vec(0, -1))

    def gameover_draw(self):
        enemyscore = 0
        if self.score == 1000:
            enemyscore = 500
        else:
            enemyscore = 1000
        self.screen.fill(BLACK)
        self.draw_text("YOUR SCORE: " + str(self.score), self.screen, [WIDTH//2,500],36, FONT_MENU, (0, 128, 0))
        self.draw_text("ENEMY SCORE: " + str(enemyscore), self.screen, [WIDTH//2,550],36, FONT_MENU, (0, 128, 0))
        self.draw_text("TIME PLAYED: " + str(self.current_time), self.screen, [WIDTH//2,600],36, FONT_MENU, (0, 128, 0))
        img = pygame.image.load('img/go.jpeg')
        self.screen.blit(pygame.transform.scale(img, (400, 500)), (100, 0))
        pygame.display.update()
