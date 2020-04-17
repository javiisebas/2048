import pygame
import time
import numpy as np
import random as rd

pygame.init()
win = pygame.display.set_mode((440,545)) 
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

Numbers_Images = [pygame.image.load('images/2.png'), pygame.image.load('images/4.png'), pygame.image.load('images/8.png'),
           pygame.image.load('images/16.png'), pygame.image.load('images/32.png'), pygame.image.load('images/64.png'),
           pygame.image.load('images/128.png'), pygame.image.load('images/256.png'), pygame.image.load('images/512.png'),
           pygame.image.load('images/1024.png'), pygame.image.load('images/2048.png'), pygame.image.load('images/4096.png')]

Bg = pygame.image.load("images/fondo.png")
Restart = pygame.image.load("images/restart.png")
Restart_2 = pygame.image.load("images/restart_2.png")
GameOver = pygame.image.load("images/gameOver.png")
GameRestart = pygame.image.load("images/gameOver_Restart.png")


class Mesh(object):
    def __init__(self):
        self.x = 20
        self.y = 125
        self.vel = 100
            
    def draw(self,win):
        while self.x < 450:
            pygame.draw.line(win,(255,228,195),(self.x,125),(self.x,525),2)
            pygame.draw.line(win,(255,228,195),(20,self.y),(420,self.y),2)
            self.x += self.vel
            self.y += self.vel
        self.x = 20
        self.y = 125

mesh = Mesh()

class Matrix(object):
    def __init__(self):
        self.numMatrix = np.zeros([4,4],float)
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
        self.pos_x = int(rd.randint(0,3))
        self.pos_y = int(rd.randint(0,3))
        while self.numMatrix[self.pos_x,self.pos_y] != 0:
            self.pos_x = int(rd.randint(0,3))
            self.pos_y = int(rd.randint(0,3))
        self.numMatrix[self.pos_x,self.pos_y] = 1
        
    def start(self):
        if not(self.moves):
            self.appear()
            self.moves = True
    
    def direction(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.left = True
            self.move()
            
        if keys[pygame.K_RIGHT]:
            self.right = True
            self.move()
            
        if keys[pygame.K_UP]:
            self.up = True
            self.move()
            
        if keys[pygame.K_DOWN]:
            self.down = True
            self.move()
            
    def move_left(self):
        for j in range(len(self.numMatrix)):  
            self.c = []
            for i in list(self.numMatrix[j,:]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],float)),axis = 0)
            self.numMatrix[j,:] = np.array(self.c)

    def move_right(self):
        for j in range(len(self.numMatrix)):  
            self.c = []
            for i in list(self.numMatrix[j,:]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],float),self.c),axis = 0)
            self.numMatrix[j,:] = np.array(self.c)

    def move_up(self):
        for j in range(len(self.numMatrix)):  
            self.c = []
            for i in list(self.numMatrix[:,j]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],float)),axis = 0)
            self.numMatrix[:,j] = np.array(self.c)

    def move_down(self):
        for j in range(len(self.numMatrix)):  
            self.c = []
            for i in list(self.numMatrix[:,j]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],float),self.c),axis = 0)
            self.numMatrix[:,j] = np.array(self.c)

    def sum_left(self):
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

    def sum_up(self):
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

    def sum_right(self):
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
    
    def move(self):    
        self.numMatrizBefore = np.empty(np.shape(self.numMatrix))
        for i in range(np.shape(self.numMatrizBefore)[0]):
            for j in range(np.shape(self.numMatrizBefore)[1]):
                self.numMatrizBefore[i,j] = self.numMatrix[i,j]
        
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
            
        for i in range(len(self.numMatrix)):
            for j in range(len(self.numMatrix)):
                if int(self.numMatrix[i,j]) != int(self.numMatrizBefore[i,j]) and self.counter == 0:
                    self.appear()
                    self.counter += 1
        
        self.left = False
        self.up = False
        self.right = False
        self.down = False
        time.sleep(0.3)
        self.counter = 0
        
    def die(self):
        self.deathCounter = 0
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
            
        if self.deathCounter == 0:
            self.death = True
        
    def draw(self,win):
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
                
matrix = Matrix()

class NewGame(object):
    def draw(self,win):
        if matrix.death:
            win.blit(GameOver,(-25,0))
        else:
            win.blit(Restart,(-25,0))
        self.mouseX = pygame.mouse.get_pos()[0]
        self.mouseY = pygame.mouse.get_pos()[1]
        if self.mouseX > 100 and self.mouseX < 350:
            if self.mouseY > 25 and self.mouseY < 100:
                if matrix.death:
                    win.blit(GameRestart,(-25,0))
                else:
                    win.blit(Restart_2,(-25,0))
                if pygame.mouse.get_pressed()[0]:
                    matrix.moves = False
                    matrix.death = False
                    matrix.numMatrix = np.zeros([4,4],float)
                    time.sleep(0.3)
                    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            matrix.moves = False
            matrix.numMatrix = np.zeros([4,4],float)
            time.sleep(0.3)
            
newGame = NewGame()

def redrawWinGame():
    win.blit(Bg,(0,0))
    newGame.draw(win)
    mesh.draw(win)
    matrix.draw(win)
    pygame.display.update()

run = True
while run:
    clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    redrawWinGame()
            
pygame.quit()