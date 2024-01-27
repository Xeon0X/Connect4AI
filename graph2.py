from Game import *

import pygame


pygame.init()

height = 800
width = 800

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True




def drawboard() :
        pygame.draw.line(screen, 'blue', (2,0), (2,height), width=5)
        for i in range(1, 7):
            x_position = i * width / 7
            pygame.draw.line(screen, 'blue', (x_position, 0), (x_position, height), width=5)

        pygame.draw.line(screen, 'blue', (width-2,0), (width-2,height), width=5)


        pygame.draw.line(screen, 'blue', (0,2), (width,2), width=5)
        for i in range(1, 7):
            y_position = i * height / 6
            pygame.draw.line(screen, 'blue', (0, y_position), (width, y_position), width=5)
        
    



def addToken(x,y,player):

        if player == 'X':
            color = 'red'
        else :
            color = 'yellow'


        
        coordx = (x*(width/7))-(width/(7*2))
        coordy = (y*(height/6))-(height/(6*2))


        pygame.draw.circle(screen, color, (coordx,coordy), width/20) 
  


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

                
                
                


    drawboard()
   
    pygame.display.flip()
 
    clock.tick(60)  # limits FPS to 60

pygame.quit()