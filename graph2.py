from Game import *

import pygame


pygame.init()
game = ConnectFour()

height = 800
width = 800

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True




    
def drawboard() :
    screen.fill((0,0,140))
    
    for i in range(8):
         for j in range(7):
              addToken(i,j,'black')






def addToken(x,y,player):

        if player == 'X':
            color = (204,0,0)
        elif player == 'O':
            color = (255,213,0)
        else : color = 'black'
             


        
        coordx = (x*(width/7))-(width/(7*2))
        coordy = (y*(height/6))-(height/(6*2))


        pygame.draw.circle(screen, color, (coordx,coordy), width/16) 
  


def makeMove(column):
        for row in range(5, -1, -1) :
            if game.board[row][column] == ' ' :
                addToken(column+1,row+1,game.currentPlayer)
                game.board[row][column] = game.currentPlayer
                print("row:",row)
                print("column:",column)
                break




def clickToPos():
     
     return int(mouse_x/(width/7))
     
    
drawboard()

while running:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:
               
                
                mouse_x, mouse_y = event.pos
                              
                column = clickToPos()
                
                               
                if(not game.isAPossibleMove(column)) :
                    print("Invalid move")
                    continue
                
                                           
         
                makeMove(column)
                game.printBoard()
            
                
                
               
                if game.isWin(column):
                    print(f"Player {game.currentPlayer} wins!")
                    game.printBoard()
                    running = False
                    break
                game.switchPlayer()

                
                

   
    pygame.display.flip()
 
    clock.tick(60)  # limits FPS to 60

pygame.quit()