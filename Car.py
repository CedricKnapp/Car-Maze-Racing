#Car
import pygame, math

pygame.init()

white = (255,255,255)

car_width = 67
display_width = 1200
display_height = 800

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Car Game')

clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def carDirection():
    pass

def game_loop():

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    y_change = 0

    gameExit = False

    while not gameExit:

        upAndDown = ((pygame.key.get_pressed()[pygame.K_DOWN]) and (pygame.key.get_pressed()[pygame.K_UP]))
        noYPress = ((pygame.key.get_pressed()[pygame.K_DOWN]) == False and (pygame.key.get_pressed()[pygame.K_UP]) == False)
        noXPress = ((pygame.key.get_pressed()[pygame.K_LEFT]) == False and (pygame.key.get_pressed()[pygame.K_RIGHT]) == False)
        lAndR = ((pygame.key.get_pressed()[pygame.K_LEFT]) and (pygame.key.get_pressed()[pygame.K_RIGHT]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: gameExit = True
            #if pygame.event.key == pygame.K_ESCAPE:
                #pygame.quit()
        #print(pygame.key.get_pressed()[pygame.K_DOWN] and pygame.key.get_pressed()[pygame.K_UP])
        
        if not upAndDown:
            if pygame.key.get_pressed()[pygame.K_DOWN] == True:
                y_change = 5
            if pygame.key.get_pressed()[pygame.K_UP] == True:
                y_change = -5
        elif upAndDown:
            y_change = 0
            
        if not lAndR:
            if pygame.key.get_pressed()[pygame.K_LEFT] == True:
                x_change = -15
            if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
                x_change = 15
        elif lAndR:
            x_change = 0
            
        if noYPress:
            y_change = 0
        if noXPress:
            x_change = 0
        
            '''
            if y_change < 0:
                y_change += -0.01
            elif y_change > 0:
                y_change = 0
                elif y_change < 0:
                    y_change += 0.5
                else:
                    y_change = 0
                    break
            '''
        rad = x_change * math.pi / 180

        x += y_change * math.sin(rad)
        y += y_change * math.cos(rad)

        #x += x_change
        #y += y_change

        gameDisplay.fill(white)
        car(x,y)

        '''
        if x > display_width - car_width or x < 0:
            gameExit = True
        '''
            #print(event)

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
