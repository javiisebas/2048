import pygame
import random
import time
import numpy as np
import random as rd

pygame.init()
win = pygame.display.set_mode((440,545)) 
pygame.display.set_caption("JAVIER SEBASTIÁN FERNÁNDEZ")
clock = pygame.time.Clock()

Numeros = [pygame.image.load('images/2.png'), pygame.image.load('images/4.png'), pygame.image.load('images/8.png'),
           pygame.image.load('images/16.png'), pygame.image.load('images/32.png'), pygame.image.load('images/64.png'),
           pygame.image.load('images/128.png'), pygame.image.load('images/256.png'), pygame.image.load('images/512.png'),
           pygame.image.load('images/1024.png'), pygame.image.load('images/2048.png'), pygame.image.load('images/4096.png')]

Bg = pygame.image.load("images/fondo.png")
Restart = pygame.image.load("images/restart.png")
Restart_2 = pygame.image.load("images/restart_2.png")
GameOver = pygame.image.load("images/gameOver.png")
GameRestart = pygame.image.load("images/gameOver_Restart.png")


class malla(object):
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

mallas = malla()

class matriz(object):
    def __init__(self):
        self.numMatriz = np.zeros([4,4],float)
        self.tam = len(self.numMatriz)
        self.arriba = False
        self.abajo = False
        self.izquierda = False
        self.derecha = False
        self.moves = False
        self.muerto = False
        self.cont = 0
        self.numMatrizAntes = np.empty(np.shape(self.numMatriz))
    
    def aparece(self):
        self.pos_x = int(rd.randint(0,3))
        self.pos_y = int(rd.randint(0,3))
        while self.numMatriz[self.pos_x,self.pos_y] != 0:
            self.pos_x = int(rd.randint(0,3))
            self.pos_y = int(rd.randint(0,3))
        self.numMatriz[self.pos_x,self.pos_y] = 1
        
    def inicio(self):
        if not(self.moves):
            self.aparece()
            self.moves = True
    
    def direccion(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.izquierda = True
            self.move()
            
        if keys[pygame.K_RIGHT]:
            self.derecha = True
            self.move()
            
        if keys[pygame.K_UP]:
            self.arriba = True
            self.move()
            
        if keys[pygame.K_DOWN]:
            self.abajo = True
            self.move()
            
    def move_izquierda(self):
        for j in range(len(self.numMatriz)):  
            self.c = []
            for i in list(self.numMatriz[j,:]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],float)),axis = 0)
            self.numMatriz[j,:] = np.array(self.c)

    def move_derecha(self):
        for j in range(len(self.numMatriz)):  
            self.c = []
            for i in list(self.numMatriz[j,:]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],float),self.c),axis = 0)
            self.numMatriz[j,:] = np.array(self.c)

    def move_arriba(self):
        for j in range(len(self.numMatriz)):  
            self.c = []
            for i in list(self.numMatriz[:,j]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],float)),axis = 0)
            self.numMatriz[:,j] = np.array(self.c)

    def move_abajo(self):
        for j in range(len(self.numMatriz)):  
            self.c = []
            for i in list(self.numMatriz[:,j]):
                if i != 0:
                    self.c.append(i)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],float),self.c),axis = 0)
            self.numMatriz[:,j] = np.array(self.c)

    def suma_izquierda(self):
        for i in range(len(self.numMatriz)):  
            self.c = []
            for j in range(len(self.numMatriz)-1):
                if self.numMatriz[i,j] == self.numMatriz[i,j+1] and self.numMatriz[i,j] != 0:
                    self.numMatriz[i,j] += 1
                    self.numMatriz[i,j+1] = 0
            for k in self.numMatriz[i,:]:
                if k != 0:
                    self.c.append(k)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],int)),axis = 0)
            self.numMatriz[i,:] = np.array(self.c)

    def suma_arriba(self):
        for i in range(len(self.numMatriz)):  
            self.c = []
            for j in range(len(self.numMatriz)-1):
                if self.numMatriz[j,i] == self.numMatriz[j+1,i] and self.numMatriz[j,i] != 0:
                    self.numMatriz[j,i] += 1
                    self.numMatriz[j+1,i] = 0
            for k in self.numMatriz[:,i]:
                if k != 0:
                    self.c.append(k)
            if len(self.c) != 4:
                self.c = np.concatenate((self.c,np.zeros([4-len(self.c)],int)),axis = 0)
            self.numMatriz[:,i] = np.array(self.c)

    def suma_abajo(self):
        for i in range(len(self.numMatriz)):  
            self.c = []
            for j in range(self.tam-1):
                if self.numMatriz[self.tam - (j+1),i] == self.numMatriz[self.tam -(j+2),i] and self.numMatriz[self.tam - (j+1),i] != 0:
                    self.numMatriz[self.tam - (j+1),i] += 1
                    self.numMatriz[self.tam - (j+2),i] = 0
            for k in self.numMatriz[:,i]:
                if k != 0:
                    self.c.append(k)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],int),self.c),axis = 0)
            self.numMatriz[:,i] = np.array(self.c)

    def suma_derecha(self):
        for i in range(len(self.numMatriz)):  
            self.c = []
            for j in range(len(self.numMatriz)-1):
                if self.numMatriz[i,j] == self.numMatriz[i,j+1] and self.numMatriz[i,j] != 0:
                    self.numMatriz[i,j] += 1
                    self.numMatriz[i,j+1] = 0
            for k in self.numMatriz[i,:]:
                if k != 0:
                    self.c.append(k)
            if len(self.c) != 4:
                self.c = np.concatenate((np.zeros([4-len(self.c)],int),self.c),axis = 0)
            self.numMatriz[i,:] = np.array(self.c)
    
    def move(self):    
        self.numMatrizAntes = np.empty(np.shape(self.numMatriz))
        for i in range(np.shape(self.numMatrizAntes)[0]):
            for j in range(np.shape(self.numMatrizAntes)[1]):
                self.numMatrizAntes[i,j] = self.numMatriz[i,j]
        
        if self.izquierda:
            self.move_izquierda()
            self.suma_izquierda()
            self.move_izquierda()
            
        if self.arriba:
            self.move_arriba()
            self.suma_arriba()
            self.move_arriba()
        
        if self.derecha:
            self.move_derecha()
            self.suma_derecha()
            self.move_derecha()
            
        if self.abajo:
            self.move_abajo()
            self.suma_abajo()
            self.move_abajo()
            
        for i in range(len(self.numMatriz)):
            for j in range(len(self.numMatriz)):
                if int(self.numMatriz[i,j]) != int(self.numMatrizAntes[i,j]) and self.cont == 0:
                    self.aparece()
                    self.cont += 1
        
        self.izquierda = False
        self.arriba = False
        self.derecha = False
        self.abajo = False
        time.sleep(0.3)
        self.cont = 0
        
    def muerte(self):
        self.contMuerte = 0
        for i in range(4):
            for j in range(4):
                if self.numMatriz[i,j] == 0:
                    self.contMuerte += 1
        for i in range(3):
            if self.numMatriz[i,3] == self.numMatriz[i+1,3]:
                self.contMuerte += 1
            if self.numMatriz[3,i] == self.numMatriz[3,i+1]:
                self.contMuerte += 1
            for j in range(3): 
                if self.numMatriz[i,j] == self.numMatriz[i,j+1]:
                    self.contMuerte += 1
                if self.numMatriz[i,j] == self.numMatriz[i+1,j]:
                    self.contMuerte += 1
            
        if self.contMuerte == 0:
            #time.sleep(1)
            self.muerto = True
        
    def draw(self,win):
        self.inicio()
        self.direccion()
        self.muerte()
        self.posx = 23
        for i in range(len(self.numMatriz)):
            self.posy = 128
            for j in range(len(self.numMatriz)):
                if self.numMatriz[j,i] != 0:
                    win.blit(Numeros[int(round(self.numMatriz[j,i]))-1],(self.posx,self.posy))
                self.posy += 100
            self.posx += 100
                
matrix = matriz()

class restart(object):
    def draw(self,win):
        if matrix.muerto:
            win.blit(GameOver,(-25,0))
        else:
            win.blit(Restart,(-25,0))
        self.ratonX = pygame.mouse.get_pos()[0]
        self.ratonY = pygame.mouse.get_pos()[1]
        if self.ratonX > 100 and self.ratonX < 350:
            if self.ratonY > 25 and self.ratonY < 100:
                if matrix.muerto:
                    win.blit(GameRestart,(-25,0))
                else:
                    win.blit(Restart_2,(-25,0))
                if pygame.mouse.get_pressed()[0]:
                    matrix.moves = False
                    matrix.muerto = False
                    matrix.numMatriz = np.zeros([4,4],float)
                    time.sleep(0.3)
                    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            matrix.moves = False
            matrix.numMatriz = np.zeros([4,4],float)
            time.sleep(0.3)
            
nuevaPartida = restart()

def redrawWinGame():
    win.blit(Bg,(0,0))
    nuevaPartida.draw(win)
    mallas.draw(win)
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