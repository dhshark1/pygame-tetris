#########################################
# Programmer: Mrs.G, Daniel Haber
# Date: 24/05/18
# File Name: tetris_template3.py
# Description: This program is the third game template for our Tetris game.
#########################################
from tetris_classes3 import *
from random import randint
import pygame
pygame.init()

HEIGHT = 600                                        #
WIDTH  = 800                                        #
GRIDSIZE = HEIGHT//24                               #
screen=pygame.display.set_mode((WIDTH,HEIGHT))      #Dimensions for the game

GREY = (192,192,192)
PURPLE = (153, 29, 60)
BLACK = (0,0,0)
WHITE = (255,255,255)                               #Colours used for fonts and game

#---------------------------------------#
COLUMNS = 12                            #
ROWS = 22                               # 
LEFT = 9                                # 
RIGHT = LEFT + COLUMNS                  # 
MIDDLE = LEFT + COLUMNS//2              #
TOP = 1                                 #
FLOOR = TOP + ROWS                      #
#---------------------------------------#

#----------------------------------------#
#           Picture Loading              #
#----------------------------------------#
background = pygame.image.load("background.jpg") #loading background image
background = background.convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
gamepic = pygame.image.load("game background.jpg")
gamepic = gamepic.convert_alpha()
gamepic = pygame.transform.scale(gamepic, (WIDTH, HEIGHT))
over = pygame.image.load("game_over.jpg")
over = over.convert_alpha()
over = pygame.transform.scale(over, (WIDTH, HEIGHT)) #loading game over image

#----------------------------------------#
#             Music and Sound            #
#----------------------------------------#

music = pygame.mixer.music.load("theme music.wav")    #loading background music
pygame.mixer.music.play(-1, 0)                        #repeats music infinitely
land = pygame.mixer.Sound("smash.wav")                #loading landing sound effect
clear = pygame.mixer.Sound("clear.wav")               #loading clear sound effect
levelup = pygame.mixer.Sound("level up.wav")          #loading level up sound effect

#------------------------------------------#
#           Variable names                 #
#------------------------------------------#
score = 0                                               #score variable
timer = 0                                               #time played variable
delay = 200                                            #speed of the game
level = 1                                               #starting level of game
lvl = 500                                               #required score to level up
font = pygame.font.SysFont("tetris.ttf", 60)      
font1 = pygame.font.SysFont("tetris.ttf", 22)            #loading fonts


#---------------------------------------#
#   functions                           #
#---------------------------------------#
def intro_screen():
    screen.blit(background, (0,0))                       #blit background image 
    introText = font.render("Click the space bar to begin!", 1, WHITE)
    introText2 = font1.render("100 point for clearing a single line. 800 point for clearing 4 lines! 1200 points for back-to-back four lines!!", 1,WHITE)
    screen.blit(introText, (100,0))
    screen.blit(introText2, (20,500))              #texts being printed, applied to game
    pygame.display.update()

def redraw_screen():               
    screen.blit(gamepic, (0,0))                                   #filling the screen background in grey 
    shape.draw(screen, GRIDSIZE)                        #drawing shape 
    floor.draw(screen, GRIDSIZE)                        #drawing floor
    leftwall.draw(screen, GRIDSIZE)                     #drawing leftwall
    rightwall.draw(screen, GRIDSIZE)                    #drawing rightwall
    obstacle.draw(screen, GRIDSIZE)                     #drawing the obstacle
    newShape.draw(screen, GRIDSIZE)                     #drawing the next shape
    shadow.draw(screen, GRIDSIZE)                       #drawing the shadow

    scoreText = font.render("Score: "+ str(score), 1, BLACK)
    levelText = font.render("Level: "+ str(level), 1, BLACK)
    timerText = font.render("Time: "+ str(int(round(timer, 0))), 1, BLACK)
    nextText = font.render("Next:", 1, BLACK)

    screen.blit(scoreText, (10,0))                      ##
    screen.blit(levelText, (620, 0))                    ##
    screen.blit(timerText, (10, 500))                   ##
    screen.blit(nextText, (650,200))                    ##printing and applying texts for game screen
    pygame.display.update()

def game_over():
    screen.blit(over, (0,0))                                   #game over screen filled out in grey
    over_text = font.render("Game Over!", 1, BLACK)
    over_text2 = font.render("Final Score: {}".format(score), 1, BLACK)
    screen.blit(over_text, (250, 200))
    screen.blit(over_text2, [250, 400])                 #printing and applying text for game over screen
    pygame.display.update()
#---------------------------------------#
#   main program                        #
#---------------------------------------#    
shapeNo = randint(1,7)                              #chooses a random shape for the first shape
newShapeNo = randint(1,7)                           #chooses a random shape for the next new one
shape = Shape(MIDDLE, TOP, shapeNo)                 #where the shape is placed
floor = Floor(LEFT,FLOOR,COLUMNS)                   #coordinates of floor
leftwall = Wall(LEFT-1, TOP, ROWS)                  #coordinates of the leftwall
rightwall = Wall(RIGHT, TOP, ROWS)                  #coordinates of the rightwall
obstacle = Obstacles(LEFT, FLOOR)                   #coordinates of the obstacle
top = Floor(LEFT, TOP, COLUMNS)                     #coordinates of the ceiling
shadow = Shape(MIDDLE, TOP, shapeNo)
newShape = Shape(MIDDLE+11, TOP +12, newShapeNo)    #coordinates of next shape
lastTetris = False                                  #determines double teris
inPlay = 1                                          #inPlay at 1 means its at intro screen

while inPlay == 1:
    intro_screen()                                  #calling intro screen function
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
                if keys[pygame.K_SPACE]:            #if space is entered, game proceeds from intro screen
                    inPlay = 2
    pygame.display.update() 

while inPlay==2:

    shadow.shdw()
    shape.move_down()

    if shape.collides(floor) or shape.collides(obstacle):
        fullRows = obstacle.findFullRows(TOP, FLOOR, COLUMNS) 
        obstacle.removeFullRows(fullRows)               #finding and removing full rows
        shape.move_up()                                 #prevents shape from continuously moving down
        obstacle.append(shape)
        shapeNo = newShapeNo
        shape = Shape(MIDDLE, TOP, shapeNo)
        shadow = Shape(MIDDLE,TOP,shapeNo)
        newShapeNo = randint(1,7)
        newShape = Shape(MIDDLE+11,TOP+12,newShapeNo)   #generating a new shape and a new next shape
        land.play()
            
        if len(fullRows)==1:                                    
            score+=100
            clear.play()
        elif len(fullRows)==2:                                  
            score+=200
            clear.play()
        elif len(fullRows)==3:                                  
            score+=300
            clear.play()
        elif len(fullRows)==4 and lastTetris == False:      
            score+=800
            clear.play()
            lastTetris=True
        elif len(fullRows)==4 and lastTetris == True:      
            score+=1200
            clear.play()
            lastTetris=False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = 4
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                shape.rotateClkwise()                   #if UP is pressed, the shape rotates clockwise
                shadow.shadowRotate(shape)
                if shape.collides(leftwall) or shape.collides(rightwall) or shape.collides(floor) or shape.collides(obstacle):
                    shape.rotateCntclkwise()            #solves conflict between rotating shape and colliding border
            elif event.key == pygame.K_LEFT:
                shape.move_left()
                shadow.move_left()
                shadow.col = shape.col
                shadow.row = shape.row
                if shape.collides(leftwall) or shape.collides(floor) or shape.collides(obstacle):
                    shape.move_right()
                    shadow.move_right()
            elif event.key == pygame.K_RIGHT:
                shape.move_right()
                shadow.move_right()
                shadow.col = shape.col
                shadow.row = shape.row
                if shape.collides(rightwall) or shape.collides(floor) or shape.collides(obstacle): 
                    shape.move_left()
                    shadow.move_left()
            elif event.key == pygame.K_DOWN:
                shape.move_down()
                if shape.collides(floor):
                    shape.move_up()
            elif event.key == pygame.K_SPACE:
                while not (shape.collides(floor) or shape.collides(obstacle)):
                    shape.move_down()
                shape.move_up()
                obstacle.append(shape)
                shapeNo = randint(1,7)
                shape = Shape(MIDDLE, TOP, shapeNo)
                newShapeNo = randint(1,7)
                newShape = Shape(MIDDLE+11,TOP+12,newShapeNo)
                shadow= Shape(MIDDLE, TOP, shapeNo)
                fullRows = obstacle.findFullRows(TOP, FLOOR, COLUMNS) 
                obstacle.removeFullRows(fullRows)
                land.play()
            
                if len(fullRows)==1:                                    
                    score+=100                              #score increases by 100 if a line is cleared
                elif len(fullRows)==2:                                  
                    score+=200                              #score increases by 200 if 2 lines are cleared
                elif len(fullRows)==3:                                  
                    score+=300                              #score increases by 300 if 3 lines are cleared
                elif len(fullRows)==4 and lastTetris == False:      
                    score+=800                              #tetris- score increases by 800 if 4 lines are cleared
                    lastTetris=True
                elif len(fullRows)==4 and lastTetris == True:      
                    score+=1200                             #double tetris- score increases by 1200 if 4 lines are cleared twice in a row
                    lastTetris=False

        while not(shadow.collides(floor) or shadow.collides(obstacle)):    ## shadow moves down when not colliding
            shadow.move_down()
        if shadow.collides(floor) or shadow.collides(obstacle):         #shadow moves up once when collides with obstacle
            shadow.move_up()
            
        if score >= lvl:
            level += 1                                      #level increases once the amount of points meets 500
            lvl += 500                                 #sets the new level goal
            levelup.play()
            delay -= 50                                      #increases game speed
            
    if obstacle.collides(top):
        inPlay = 3                                      #game end when obstacles reach the ceiling
            
    redraw_screen()
    pygame.time.delay(delay)
    timer += 0.001*delay                                    #timer

if inPlay == 3:
    game_over()
    pygame.mixer.music.pause()                          #pausing music
    pygame.display.update()
    
#pygame.quit()
    #DOESNT SHOW GAME OVER SCREEN
