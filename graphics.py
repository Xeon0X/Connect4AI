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
            screen.fill('black')

           # return GAMEOVER


    return PLAYING


def gameLoop(screen, game,mode):
    clock = pygame.time.Clock()
    state = PLAYING
    drawBoard(screen)
    IA1 = Player('O')
    
    

    while state and mode == 1 :
        clock.tick(60) # limits FPS to 60
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                state = GAMEOVER

            elif event.type == pygame.MOUSEBUTTONDOWN :
                state = handleMouseDown(event, screen, game)
        pygame.display.flip()

    while state and mode == 2 :
        
        
        
        clock.tick(60) # limits FPS to 60
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                state = GAMEOVER

            elif event.type == pygame.MOUSEBUTTONDOWN :
                
                
                state = handleMouseDown(event, screen, game)
                pygame.display.flip()

                chosenMove = minmax(game, 3, IA1)
                makeMove(screen,game,chosenMove)
                #game.makeMove(chosenMove)
                if game.isWin(chosenMove):
                    print(f"Player {game.currentPlayer} wins!")
                    game.printBoard()
                    state = GAMEOVER
                    

                

        pygame.display.flip()







class RadioButton():
    def __init__(self, x, y, text,screen,font,game):
        self.x = x
        self.y = y
        self.text = text
        self.selected = False
        self.screen = screen
        self.font = font
        self.col = 'red'
        self.game = game
        pygame.draw.circle(self.screen, 'yellow', (self.x + 10, self.y + 10), 20)
       

    def draw(self):
        # Draw radio button circle
        
        pygame.draw.circle(self.screen, 'white', (self.x + 10, self.y + 10), 20, 2)
        if self.selected:
            pygame.draw.circle(self.screen, self.col, (self.x + 10, self.y + 10), 20)
            pygame.draw.circle(self.screen, 'white', (self.x + 10, self.y + 10), 20, 2)
     
        # Draw radio button text
        text_surface = self.font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(midleft=(self.x + 50, self.y + 10))
        self.screen.blit(text_surface, text_rect)
        

    def check_click(self, pos):
        if pygame.Rect(self.x, self.y, 40, 40).collidepoint(pos):
           
            self.selected = not self.selected  #True
            pygame.draw.circle(self.screen, 'yellow', (self.x + 10, self.y + 10), 20)
            if self.game.currentPlayer == 'O':
                self.game.currentPlayer = 'X'
                
            else :
                self.game.currentPlayer = 'O'
                
        
       


  


      #  else:
          #  self.selected = False

# Create radio buttons


















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

        button2_rect = pygame.Rect(300, 300, 200, 80) #bouton1 pour jouer avec minMax
        button2_text = "MinMax"

        button3_rect = pygame.Rect(300, 400, 200, 80) #bouton3 pour jouer avec alphabeta
        button3_text = "AlphaBeta"

        
        b1=RadioButton (550, 230, "Color Choice",screen,font,game)
 
        
        
        
        

        
        while running:
            
            




            #--------------------------affichage du titre-----------------------
            titleText = "Connect Four"
            text_surface = font2.render(titleText, True,(255, 255, 255)) 
            text_rect = text_surface.get_rect()
            text_rect.center = (WIDTH/2, HEIGHT/12)  
            screen.blit(text_surface, text_rect)
            #--------------------------affichage du titre-----------------------

            pygame.draw.rect(screen, 'red', button1_rect)
            text_surface = font.render(button1_text, True, 'black')
            text_rect = text_surface.get_rect(center=button1_rect.center) #bouton1
            screen.blit(text_surface, text_rect)

            pygame.draw.rect(screen, 'blue', button2_rect)
            text_surface = font.render(button2_text, True, 'black') #bouton2
            text_rect = text_surface.get_rect(center=button2_rect.center)
            screen.blit(text_surface, text_rect)

            pygame.draw.rect(screen, 'yellow', button3_rect)
            text_surface = font.render(button3_text, True, 'black') #bouton3
            text_rect = text_surface.get_rect(center=button3_rect.center)
            screen.blit(text_surface, text_rect)

            b1.draw()
           # b2.draw()
            #b3.draw() 
        

            pygame.display.flip()
            clock.tick(60)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

              #  if pygame.Rect(x, y, 20, 20).collidepoint(pos):
                  #  selected = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1_rect.collidepoint(event.pos):
                        gameLoop(screen, game,1)
                        running = False
                        print("Button Clicked!")
                    if button2_rect.collidepoint(event.pos):
                        gameLoop(screen, game,2)
                        running = False
                        print("Button Clicked!")
                    if button3_rect.collidepoint(event.pos):
                        gameLoop(screen, game,3)
                        running = False
                        print("Button Clicked!")    

                    if event.button == 1:
                        #screen.fill('black')
                      
                                  
                        b1.check_click(event.pos)
                       # b2.check_click(event.pos)
                       # b3.check_click(event.pos)

                            
            
                        print("eyahhhh")
                        b1.draw()
                 
                            
       

    
    # Draw radio buttons
            
               
            






def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = ConnectFour()
   
    optionMenu(screen,game)
    
    
   # gameLoop(screen, game)
    

    pygame.quit()

if __name__ == "__main__":
    main()