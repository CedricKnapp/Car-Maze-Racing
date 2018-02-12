#Pygame Car Game

import pygame, math, os
from random import shuffle, randrange
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1' #Center The window created on the users screen
global rectList
rectList = []

white = (255,255,255)
grey = (100,100,100)
red = (160,0,0)
bright_red = (255,0,0)
green = (0,150,0)
bright_green = (0,255,0)
blue = (0,0,120)
bright_blue = (0,0,230)
black = (0,0,0)

display_width = 1183
display_height = 793
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

def make_maze(w = 6, h = 6): #This function is modified from the original source which can be found at https://rosettacode.org/wiki/Maze_generation#Python
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["---"] * w + ['-'] for _ in range(h + 1)]
 
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)
 
    walk(randrange(w), randrange(h))
 
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ["n\\"] + ['\n'] + b + ["n\\"] + ['\n'])
    return s

def draw_maze(mazeIN):
    maze = mazeIN
    del rectList[:] #clear the list of Rect objects from walls
    WALL_LENGTH = 65
    x=y=x2=y2=START=5
    #screen.fill(0,0,0)
    linecount = 1
    
    for i in maze:
        if i == "-" or i == "+":
            x2+=WALL_LENGTH
            draw_line(screen,black,(x,y),(x2,y2),5)
            rectList.append(pygame.Rect((x,y),(x2-x,y2-y)))
            x+=WALL_LENGTH
        elif i == "n":
            linecount+=1
            if(linecount % 2 == 0):
                draw_line(screen,grey,(x-WALL_LENGTH,y),(x2,y2),5)
                y+=WALL_LENGTH*2
                y2=y
            x=START
            x2=START
        elif i == "|":
            y2-=WALL_LENGTH*2
            draw_line(screen,black,(x,y),(x2,y2),5)
            rectList.append(pygame.Rect((x2,y2),(x-x2,y-y2)))
            x+=WALL_LENGTH
            x2=x
            y2=y
        elif i == " ":
            x+=WALL_LENGTH
            x2=x

def draw_line(surface,color,start_pos,end_pos,width): #used for drawing maze
    pygame.draw.line(surface,color,start_pos,end_pos,width)


def new_level(ball,car1,car2):
    ball.generateObject(display_width,display_height)
    currentMaze = make_maze()
    car1.position = car1.spawn
    car2.position = car2.spawn
    return currentMaze


class SpawnObject(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = [0,0]

    def generateObject(self, objX, objY):
        #create the spawn location inside of the maze for the ball
        self.position[0] = randrange(int(objX - (objX * 0.7)),int(objX * 0.7))
        self.position[1] = randrange(int(objY - (objY * 0.7)),int(objY * 0.7))

        self.image = pygame.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect()
        self.rect.center = self.position
        
        

class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = -(MAX_FORWARD_SPEED *.6)
    ACCELERATION = 1
    F_TURN_SPEED = MAX_FORWARD_SPEED * 0.70
    R_TURN_SPEED = MAX_REVERSE_SPEED * 0.70
    
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self) #Call the parent class (Sprite) constructor
        self.src_image = pygame.image.load(image)
        self.position = position
        self.spawn = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        
    def update(self, deltat):

        #Handles Turning Speed
        if (self.k_right or self.k_left) and (not(self.k_right and self.k_left)):
            if self.speed > self.F_TURN_SPEED:
                self.speed -= self.ACCELERATION
            elif self.speed < self.R_TURN_SPEED:
                self.speed -= -self.ACCELERATION
            else:
                self.speed += (self.k_up + self.k_down)  
        else:
            self.speed += (self.k_up + self.k_down)

        #Handles Max/Min Speed
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        elif self.speed < self.MAX_REVERSE_SPEED:
            self.speed = self.MAX_REVERSE_SPEED

        #Handles no input -> Slowdown, and turning direction, based on + or - motion
        if self.speed > 0:
            self.direction += (self.k_right + self.k_left)
            if self.k_up == 0:
                self.speed -= self.ACCELERATION
        elif self.speed < 0:
            self.direction -= (self.k_right + self.k_left)
            if self.k_down == 0:
                self.speed += self.ACCELERATION
                
        print(self.speed) #Shows speed of the car(s)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x -= self.speed*math.sin(rad)
        y -= self.speed*math.cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotozoom(self.src_image, self.direction, 0.55) #scales the cars to approprate size, and applies rotation
        #self.image = pygame.transform.rotate(self.src_image, self.direction)
        #self.image = pygame.transform.scale(self.src_image, (30, 30))
        self.rect = self.image.get_rect()
        #self.rect.inflate_ip(x*1.1,y*1.1)
        self.rect.center = self.position

def button(msg,x,y,width,height,incol,accol,action=None): #Create buttons for Title Screen
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(screen, accol, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "Play":
                game_loop()
            elif action == "Quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, incol, (x,y,width,height))

    smallText = pygame.font.Font(None,32)

    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(width/2), y+(height/2)))
    screen.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_intro():

    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        largeText = pygame.font.Font(None,115)
        TextSurf, TextRect = text_objects("Maze Racing Game", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        screen.blit(TextSurf, TextRect) 

        button("Continue Game",100,550,200,50,blue,bright_blue,"Play")
        button("New Game",500,550,200,50,green,bright_green,"Play")
        button("Exit Game",900,550,200,50,red,bright_red,"Quit")
   
        pygame.display.flip()
        clock.tick(30)

        
# CREATE A CAR AND RUN
def game_loop():
    gameExit = False
    turnMultiple = 7
    points = {"car1": 0, "car2": 0}
    press = True
    rect = screen.get_rect()
    keyBindings = [[pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN],[pygame.K_d,pygame.K_a,pygame.K_w,pygame.K_s]]
    
    car1 = CarSprite('racecar.png', (1110,725))
    car2 = CarSprite('racecar2.png', (75,70)) 

    ball = SpawnObject('carball.png')
    ball_group = pygame.sprite.Group(ball)
    
    ball.generateObject(display_width,display_height)
        
    currentMaze = make_maze()
    
    car_group = pygame.sprite.Group(car1) #Adds car to the car_group (.RenderPlain() & .renderClear() are an alias for .Group)
    car_group.add(car2)

    
    
    while not gameExit:
        # USER INPUT
        deltat = clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: gameExit = True
            if not hasattr(event, 'key'): continue
            down = event.type == pygame.KEYDOWN
            #Car1: Player 1
            if event.key == keyBindings[0][0]: car1.k_right = down * -turnMultiple
            elif event.key == keyBindings[0][1]: car1.k_left = down * +turnMultiple
            elif event.key == keyBindings[0][2]: car1.k_up = down * press
            elif event.key == keyBindings[0][3]: car1.k_down = down * -press
            #Car2: Player 2
            if event.key == keyBindings[1][0]: car2.k_right = down * -turnMultiple
            elif event.key == keyBindings[1][1]: car2.k_left = down * +turnMultiple
            elif event.key == keyBindings[1][2]: car2.k_up = down * press
            elif event.key == keyBindings[1][3]: car2.k_down = down * -press

            if event.type == pygame.QUIT:
                break
            if event.key == pygame.K_ESCAPE: pygame.quit()
            
        # RENDERING
        screen.fill(grey)
        car_group.update(deltat)
        draw_maze(currentMaze)
                                                                                        
        while ball.rect.collidelist(rectList) > 0:                                   #
            ball.generateObject(display_width,display_height)                        #
                                                                                     #
        if ball.rect.colliderect(car1.rect):                                         #
            points["car1"] += 1                                                      #
            currentMaze = new_level(ball,car1,car2)                                  #
                                                                                     #
        if ball.rect.colliderect(car2.rect):                                         # COLLISION
            points["car2"] += 1                                                      # DETECTION
            currentMaze = new_level(ball,car1,car2)                                  #
                                                                                     #
        if car2.rect.colliderect(car1.rect):                                         # 
            car1.speed = 0                                                           # 
            car2.speed = 0                                                           #
        if car1.rect.collidelist(rectList) > 0: #collision with one of the walls     #
            car1.position = car1.spawn #respawn the car                              #
        if car2.rect.collidelist(rectList) > 0: #collision with one of the walls     #
            car2.position = car2.spawn #respawn the car                              #
        car_group.draw(screen)
        ball_group.draw(screen)
        print(points)

        pygame.display.flip()

game_intro()
game_loop()
pygame.quit()
quit()

