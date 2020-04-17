import pygame
import time
import numpy as np
import random as rd

# We initiate pygame
pygame.init()
win = pygame.display.set_mode((440,545)) 
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

# We load the number images
Numbers_Images = [pygame.image.load('images/2.png'), pygame.image.load('images/4.png'), pygame.image.load('images/8.png'),
           pygame.image.load('images/16.png'), pygame.image.load('images/32.png'), pygame.image.load('images/64.png'),
           pygame.image.load('images/128.png'), pygame.image.load('images/256.png'), pygame.image.load('images/512.png'),
           pygame.image.load('images/1024.png'), pygame.image.load('images/2048.png'), pygame.image.load('images/4096.png')]

# We load the configuration images
Bg = pygame.image.load("images/fondo.png")
Restart = pygame.image.load("images/restart.png")
Restart_2 = pygame.image.load("images/restart_2.png")
GameOver = pygame.image.load("images/gameOver.png")
GameRestart = pygame.image.load("images/gameOver_Restart.png")


# We create the classes that we are going to use afterward 
# 1. We create the mesh that defines the limits of the number squares
class Mesh(object):
    def __init__(self): # Initial parameters
        self.x = 20
        self.y = 125
        self.vel = 100
            
    def draw(self,win): 
        '''
        We draw the mesh in the window
        '''
        while self.x < 450:
            pygame.draw.line(win,(255,228,195),(self.x,125),(self.x,525),2)
            pygame.draw.line(win,(255,228,195),(20,self.y),(420,self.y),2)
            self.x += self.vel
            self.y += self.vel
        self.x = 20
        self.y = 125

# We create the mess object
mesh = Mesh()


# 2. We create the matrix with the one we will interact
class Matrix(object):
    def __init__(self): # Initial parameters
        self.numMatrix = np.zeros([4,4],float) # We start with a 4x4 matrix full of zeros
        self.length = len(self.numMatrix)
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.moves = False
        self.death = False
        self.counter = 0
        self.numMatrizBefore = np.empty(np.shape(self.numMatrix))
    
    def appear(self): 
        '''
        The function will makes appear a new number in the matrix with a random position
        '''
        # Initial position
        self.pos_x = int(rd.randint(0,3))
        self.pos_y = int(rd.randint(0,3))
        # We will lock for a postion till we find one that is not already being used
        while self.numMatrix[self.pos_x,self.pos_y] != 0:
            self.pos_x = int(rd.randint(0,3))
            self.pos_y = int(rd.randint(0,3))
        # Finally we introduce the number in the matrix
        self.numMatrix[self.pos_x,self.pos_y] = 1
        
    def start(self):
        if not(self.moves):
            self.appear()
            self.moves = True
    
    def direction(self):
        '''
        The function interact with the keyboard and gets the moves that the user has done
        '''
        keys = pygame.key.get_pressed() # Gets the pressed keys
        
        if keys[pygame.K_LEFT]: # Left key pressed
            self.left = True
            self.move()
            
        if keys[pygame.K_RIGHT]: # Right key pressed
            self.right = True
            self.move()
            
        if keys[pygame.K_UP]: # Up key pressed
            self.up = True
            self.move()
            
        if keys[pygame.K_DOWN]: # Down key pressed
            self.down = True
            self.move()
            
    def move_left(self):
        '''
        The function moves all the numbers in the matrix to the left
        '''
        for j in range(len(self.numMatrix)):  
            self.c = []
            for i in list(self.numMatrix[j,:]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],float)),axis = 0)
            self.numMatrix[j,:] = np.array(self.c)

    def move_right(self):
        '''
        The function moves all the numbers in the matrix to the right
        '''
        for j in range(len(self.numMatrix)):  
            self.c = []
            for i in list(self.numMatrix[j,:]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],float),self.c),axis = 0)
            self.numMatrix[j,:] = np.array(self.c)

    def move_up(self):
        '''
        The function moves all the numbers in the matrix to the upper part
        '''
        for j in range(len(self.numMatrix)):  
            self.c = []
            for i in list(self.numMatrix[:,j]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],float)),axis = 0)
            self.numMatrix[:,j] = np.array(self.c)

    def move_down(self):
        '''
        The function moves all the numbers in the matrix to the bottom
        '''
        for j in range(len(self.numMatrix)):  
            self.c = []
            for i in list(self.numMatrix[:,j]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],float),self.c),axis = 0)
            self.numMatrix[:,j] = np.array(self.c)

    def sum_left(self):
        '''
        The function sums every two consecutive number from left to right
        '''
        for i in range(len(self.numMatrix)):  
            self.c = []
            for j in range(len(self.numMatrix)-1):
                if self.numMatrix[i,j] == self.numMatrix[i,j+1] and self.numMatrix[i,j] != 0:
                    self.numMatrix[i,j] += 1
                    self.numMatrix[i,j+1] = 0
            for k in self.numMatrix[i,:]:
                if k != 0:
                    self.c.append(k)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],int)),axis = 0)
            self.numMatrix[i,:] = np.array(self.c)

    def sum_right(self):
        '''
        The function sums every two consecutive number from right to left
        '''
        for i in range(len(self.numMatrix)):  
            self.c = []
            for j in range(len(self.numMatrix)-1):
                if self.numMatrix[i,j] == self.numMatrix[i,j+1] and self.numMatrix[i,j] != 0:
                    self.numMatrix[i,j] += 1
                    self.numMatrix[i,j+1] = 0
            for k in self.numMatrix[i,:]:
                if k != 0:
                    self.c.append(k)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],int),self.c),axis = 0)
            self.numMatrix[i,:] = np.array(self.c)

    def sum_up(self):
        '''
        The function sums every two consecutive number from upper part to bottom
        '''
        for i in range(len(self.numMatrix)):  
            self.c = []
            for j in range(len(self.numMatrix)-1):
                if self.numMatrix[j,i] == self.numMatrix[j+1,i] and self.numMatrix[j,i] != 0:
                    self.numMatrix[j,i] += 1
                    self.numMatrix[j+1,i] = 0
            for k in self.numMatrix[:,i]:
                if k != 0:
                    self.c.append(k)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],int)),axis = 0)
            self.numMatrix[:,i] = np.array(self.c)

    def sum_down(self):
        '''
        The function sums every two consecutive number from bottom to upper part
        '''
        for i in range(len(self.numMatrix)):  
            self.c = []
            for j in range(self.length-1):
                if self.numMatrix[self.length - (j+1),i] == self.numMatrix[self.length -(j+2),i] and self.numMatrix[self.length - (j+1),i] != 0:
                    self.numMatrix[self.length - (j+1),i] += 1
                    self.numMatrix[self.length - (j+2),i] = 0
            for k in self.numMatrix[:,i]:
                if k != 0:
                    self.c.append(k)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],int),self.c),axis = 0)
            self.numMatrix[:,i] = np.array(self.c)
    
    def move(self):    
        # We create a copy of the original matrix to help us with the calculations
        self.numMatrizBefore = np.empty(np.shape(self.numMatrix))
        for i in range(np.shape(self.numMatrizBefore)[0]):
            for j in range(np.shape(self.numMatrizBefore)[1]):
                self.numMatrizBefore[i,j] = self.numMatrix[i,j]
        
        # For each key pressed we will call its correspondant function
        if self.left:
            self.move_left()
            self.sum_left()
            self.move_left()
            
        if self.up:
            self.move_up()
            self.sum_up()
            self.move_up()
        
        if self.right:
            self.move_right()
            self.sum_right()
            self.move_right()
            
        if self.down:
            self.move_down()
            self.sum_down()
            self.move_down()
            
        # In case the user makes presses a key and it does not generate any finally move in the matriz
        for i in range(len(self.numMatrix)):
            for j in range(len(self.numMatrix)):
                if int(self.numMatrix[i,j]) != int(self.numMatrizBefore[i,j]) and self.counter == 0:
                    # In the case its generates a move in the matrix, we will make appear a new number square
                    self.appear()
                    self.counter += 1
        
        # We reset or parameters
        self.left = False
        self.up = False
        self.right = False
        self.down = False
        time.sleep(0.3)
        self.counter = 0
        
    def die(self):
        '''
        The function studies if the user can do one more move
        '''
        self.deathCounter = 0 # If the user can not do a move at the end it will be still zero
        for i in range(4):
            for j in range(4):
                if self.numMatrix[i,j] == 0:
                    self.deathCounter += 1
        for i in range(3):
            if self.numMatrix[i,3] == self.numMatrix[i+1,3]:
                self.deathCounter += 1
            if self.numMatrix[3,i] == self.numMatrix[3,i+1]:
                self.deathCounter += 1
            for j in range(3): 
                if self.numMatrix[i,j] == self.numMatrix[i,j+1]:
                    self.deathCounter += 1
                if self.numMatrix[i,j] == self.numMatrix[i+1,j]:
                    self.deathCounter += 1
        
        # If it is zero at the end it means the game has finished
        if self.deathCounter == 0:
            self.death = True
        
    def draw(self,win):
        '''
        The functions introduces the number images in the window
        '''
        self.start()
        self.direction()
        self.die()
        self.posx = 23
        for i in range(len(self.numMatrix)):
            self.posy = 128
            for j in range(len(self.numMatrix)):
                if self.numMatrix[j,i] != 0:
                    win.blit(Numbers_Images[int(round(self.numMatrix[j,i]))-1],(self.posx,self.posy))
                self.posy += 100
            self.posx += 100
        
# We create the matrix object
matrix = Matrix()


# 3. We create the new game option
class NewGame(object):
    def draw(self,win):
        if matrix.death: # In case the user has died
            win.blit(GameOver,(-25,0))
        else: # In case the user wants to restart the game
            win.blit(Restart,(-25,0))

        self.mouseX = pygame.mouse.get_pos()[0]
        self.mouseY = pygame.mouse.get_pos()[1]

        if self.mouseX > 100 and self.mouseX < 350:
            if self.mouseY > 25 and self.mouseY < 100:
                if matrix.death:
                    win.blit(GameRestart,(-25,0))
                else:
                    win.blit(Restart_2,(-25,0))

                # If the user presses over the option it will restart the game
                if pygame.mouse.get_pressed()[0]:
                    matrix.moves = False
                    matrix.death = False
                    matrix.numMatrix = np.zeros([4,4],float)
                    time.sleep(0.3)
                  
        # We create a shortcut to restart the game with the space key    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            matrix.moves = False
            matrix.numMatrix = np.zeros([4,4],float)
            time.sleep(0.3)
        
# We create the new game object    
newGame = NewGame()


# We define the function that we will call to interact with the functions of the classes
def redrawWinGame():
    win.blit(Bg,(0,0))
    newGame.draw(win)
    mesh.draw(win)
    matrix.draw(win)
    pygame.display.update()

# Finally we define the loop that will run the game and call the function that we have defined before
run = True
while run:
    clock.tick(25)
    # In case the user presses the exit button of the window it will end the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # In each step of the loop it will call the function that prints the images in the windows
    redrawWinGame()
            
pygame.quit()