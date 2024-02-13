import math
from Game import ConnectFour
import pygame
from score import calculateScore
from Player import Player
from minmax import minmax
import sys

HEIGHT = 800
WIDTH = 800
COLOR = {
    'X': (204, 0, 0),
    'O': (255, 213, 0)}
PLAYING = True
GAMEOVER = False


def drawBoard(screen) :
    screen.fill((0,0,140))
    
    for i in range(8):
         for j in range(7):
              addToken(screen, i,j,'black')


def addToken(screen, x, y, player):
    color = COLOR.get(player, 'black')
    coordx = (x * (WIDTH / 7)) - (WIDTH / (7 * 2))
    coordy = (y * (HEIGHT / 6)) - (HEIGHT / (6 * 2))

    pygame.draw.circle(screen, color, (coordx, coordy), WIDTH / 16)
  

def makeMove(screen, game, column):
    row = game.makeMove(column)
    addToken(screen, column+1,row+1,game.currentPlayer)


def clickToPos(mouse_x):
     return int(mouse_x/(WIDTH/7))


def handleMouseDown(event, screen, game):
    if event.button == 1 :
        mouse_x, _ = event.pos
                    
        column = clickToPos(mouse_x)
                    
        if(not game.isAPossibleMove(column)) :
            print("Invalid move")
            return PLAYING
        
        makeMove(screen, game, column)
        game.printBoard()
    
        if game.isWin(column):
            print(f"Player {game.currentPlayer} wins!")
            game.printBoard()
            return GAMEOVER

    return PLAYING


def gameLoop(screen, game):
    clock = pygame.time.Clock()
    state = PLAYING
    drawBoard(screen)

    while state :
        clock.tick(60) # limits FPS to 60
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                state = GAMEOVER

            elif event.type == pygame.MOUSEBUTTONDOWN :
                state = handleMouseDown(event, screen, game)

        pygame.display.flip()







def playMinMax(game,screen):
    """ This function is an example of how to use the ConnectFour class with the minmax algorithm.

    Args:
        game (ConnectFour): The game state.
    """
    clock = pygame.time.Clock()
    IA1 = Player('X')
    IA2 = Player('O')
    game.printBoard()

    while True:
        
        clock.tick(60) 
        
        #drawBoard(screen)

        if game.currentPlayer == IA1.symbol:
            chosenMove = minmax(game, 5, IA1)
            print(f"Player {IA1.symbol} played column {chosenMove}")
        else:
            chosenMove = minmax(game, 5, IA2)
            print(f"Player {IA2.symbol} played column {chosenMove}")
        
        if (not game.isAPossibleMove(chosenMove)):
            print("Invalid move")
            continue

        game.makeMove(chosenMove)

        if game.isWin(chosenMove):
            game.switchPlayer()
            print(f"Player {game.currentPlayer} wins!")
            game.printBoard()
            break

        if game.isBoardFull():
            print("Draw!")
            game.printBoard()
            break
        pygame.display.flip()





def optionMenu(screen,game):
        pygame.font.init()
        font_size = 36 #taille du text des boutons
        font_size2 = 100 #taille du texte en haut 


        font = pygame.font.Font(None, font_size)
        font2 = pygame.font.Font(None, font_size2)

        clock = pygame.time.Clock()
        running = True
        nbr = 0

        button1_rect = pygame.Rect(300, 200, 200, 80)  #bouton1 pour jouer en 1v1
        button1_text = "Play 1v1"

        button2_rect = pygame.Rect(500, 500, 200, 80)
        button2_text = "MinMax"

        while running:
            #--------------------------affichage du titre-----------------------
            text = "Connect Four"
            text_surface = font2.render(text, True,(255, 255, 255)) 
            text_rect = text_surface.get_rect()
            text_rect.center = (WIDTH/2, HEIGHT/12)  
            screen.blit(text_surface, text_rect)
            #--------------------------affichage du titre-----------------------

            pygame.draw.rect(screen, 'red', button1_rect)
            text_surface = font.render(button1_text, True, 'white')
            text_rect = text_surface.get_rect(center=button1_rect.center) #bouton1
            screen.blit(text_surface, text_rect)

            pygame.draw.rect(screen, 'blue', button2_rect)
            text_surface = font.render(button2_text, True, 'white') #bouton2
            text_rect = text_surface.get_rect(center=button2_rect.center)
            screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(60)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1_rect.collidepoint(event.pos):
                        gameLoop(screen, game)
                        running = False
                        print("Button Clicked!")
                    if button2_rect.collidepoint(event.pos):
                        playMinMax(game,screen)
                        running = False
                        print("Button Clicked!")                

        pygame.quit()







def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = ConnectFour()
    optionMenu(screen,game)
    
    
   # gameLoop(screen, game)

    pygame.quit()

if __name__ == "__main__":
    main()