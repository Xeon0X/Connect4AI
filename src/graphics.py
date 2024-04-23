from time import sleep

import pygame
from src.Game import ConnectFour
from src.Player import Player
from src.AIs.minmax import minmax
from src.AIs.alphaBeta import alphaBeta
from src.AIs.mcts import mcts
from src.AIs.Q_learning import QLearning

PLAYING = True
GAMEOVER = False
COLOR = {'X': (204, 0, 0),
         'O': (255, 213, 0)}

HEIGHT = 800
WIDTH = 800
DEPTH_MINMAX = 3
DEPTH_ALPHABETA = 7
TIME_MCTS = 3


def drawBoard(screen: pygame.Surface) :
    """Draws the game board on the screen.

    Args:
        screen (pygame.Surface): screen of the game
    """
    screen.fill((0,0,140))
    
    for i in range(8):
         for j in range(7):
              addToken(screen, i, j, 'black')


def addToken(screen: pygame.Surface, x: int, y: int, player: str):
    """Draws a token on the screen.

    Args:
        screen (pygame.Surface): screen of the game
        x (int): x position of the token
        y (int): y position of the token
        player (str): the current player
    """
    color = COLOR.get(player, 'black')
    coordx = (x * (WIDTH / 7)) - (WIDTH / (7 * 2))
    coordy = (y * (HEIGHT / 6)) - (HEIGHT / (6 * 2))

    pygame.draw.circle(screen, color, (coordx, coordy), WIDTH / 16)
  

def makeMove(screen: pygame.Surface, game: ConnectFour, column: int):
    """Makes the move in the given column

    Args:
        screen (pygame.Surface): screen of the game
        game (ConnectFour): the game itself
        column (int): column to play the move

    Returns:
        bool: False if the game is over, True otherwise 
    """
    row = game.makeMove(column)
    addToken(screen, column+1, row+1, game.currentPlayer)
    
    if game.isWin(column):
        print(f"Player {game.currentPlayer} wins!")
        game.printBoard()
        return GAMEOVER
    
    return PLAYING


def clickToPos(mouse_x: int):
    """Converts the mouse click to a column position.

    Args:
        mouse_x (int): x position of the mouse

    Returns:
        int: the column position 
    """
    return int(mouse_x/(WIDTH/7))


def handleMouseDown(event: pygame.event, screen: pygame.Surface, game: ConnectFour):
    """Handles the mouse down event.

    Args:
        event (pygame.event): event of the mouse
        screen (pygame.Surface): screen of the game
        game (ConnectFour): the game itself

    Returns:
        bool: False if the game is over, True otherwise
    """
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
            return GAMEOVER
        
    return PLAYING


def gameLoop(screen: pygame.Surface, game: ConnectFour, mode: int):
    """Main loop of the game.

    Args:
        screen (pygame.Surface): screen of the game
        game (ConnectFour): the game itself
        mode (int): mode of the game (1: 1v1 / 2: MiniMax / 3: AlphaBeta / 4: MCTS)
    """
    state = PLAYING
    drawBoard(screen)
    IA1 = Player('O')

    if(mode == 5):
        Q_learning = QLearning()

    while state:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                state = GAMEOVER

            elif event.type == pygame.MOUSEBUTTONDOWN :
                state = handleMouseDown(event, screen, game)
                pygame.display.flip()
                
                sleep(0.05)
                # Make the IA play the game if the player based on the mode selected by the player
                if(state and mode != 1):
                    match(mode):
                        case 2:
                            chosenMove = minmax(game, DEPTH_MINMAX, IA1)
                        case 3:
                            chosenMove = alphaBeta(game, DEPTH_ALPHABETA, IA1)
                        case 4:
                            chosenMove = mcts(game, TIME_MCTS)
                        case 5:
                            chosenMove = Q_learning.get_move(game)
                    state = makeMove(screen, game, chosenMove)
                    pygame.display.flip()
                    
        pygame.display.flip()


class RadioButton():
    """A class to create radio buttons."""
    def __init__(self, x: int, y: int, text: str, screen: pygame.Surface, font: pygame.font, game: ConnectFour):
        """Initialize the radio button.

        Args:
            x (int): position x of the radio button
            y (int): position y of the radio button
            text (str): the text next to the radio button
            screen (pygame.Surface): screen of the game
            font (pygame.font): font of the text
            game (ConnectFour): the game itself
        """
        self.x = x
        self.y = y
        self.text = text
        self.selected = False
        self.screen = screen
        self.font = font
        self.col = 'red'
        self.game: ConnectFour = game
        pygame.draw.circle(self.screen, 'yellow', (self.x + 10, self.y + 10), 20)
       

    def draw(self):
        """Draw the radio button in the screen."""
        pygame.draw.circle(self.screen, 'white', (self.x + 10, self.y + 10), 20, 2)
        if self.selected:
            pygame.draw.circle(self.screen, self.col, (self.x + 10, self.y + 10), 20)
            pygame.draw.circle(self.screen, 'white', (self.x + 10, self.y + 10), 20, 2)
     
        # Draw radio button text
        text_surface = self.font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(midleft=(self.x + 50, self.y + 10))
        self.screen.blit(text_surface, text_rect)
        

    def check_click(self, pos: tuple):
        """Check if the radio button is clicked.

        Args:
            pos (tuple): Position of the mouse click
        """
        if pygame.Rect(self.x, self.y, 40, 40).collidepoint(pos):
            self.selected = not self.selected  #True
            pygame.draw.circle(self.screen, 'yellow', (self.x + 10, self.y + 10), 20)
            self.game.switchPlayer()
                
      #  else:
          #  self.selected = False

# Create radio buttons





def optionMenu(screen: pygame.Surface, game: ConnectFour):
    """Main menu of the game.

    Args:
        screen (pygame.Surface): screen of the game
        game (ConnectFour): the game itself

    Returns:
        int: game mode selected by the player
    """
    pygame.font.init()
    clock = pygame.time.Clock()
    clock.tick(60)
    
    font_size = 36 #Taille du text des boutons
    font_size2 = 100 #Taille du texte en haut 
    font = pygame.font.Font(None, font_size)
    font2 = pygame.font.Font(None, font_size2)

    button1_rect = pygame.Rect(300, 200, 200, 80) #bouton1 pour jouer en 1v1
    button1_text = "Play 1v1"

    button2_rect = pygame.Rect(300, 300, 200, 80) #bouton1 pour jouer avec minMax
    button2_text = "Mini Max"

    button3_rect = pygame.Rect(300, 400, 200, 80) #bouton3 pour jouer avec alphabeta
    button3_text = "Alpha Beta"
    
    button4_rect = pygame.Rect(300, 500, 200, 80) #bouton4 pour jouer avec MCTS
    button4_text = "MCTS"

    button4_rect = pygame.Rect(300, 500, 200, 80) #bouton4 pour jouer avec MCTS
    button4_text = "Q Learning"
    
    button_array = [{'rect': button1_rect, 'text': button1_text, 'color': 'red', 'value': 1}, 
                {'rect': button2_rect, 'text': button2_text, 'color': 'blue', 'value': 2}, 
                {'rect': button3_rect, 'text': button3_text, 'color': 'yellow', 'value': 3}, 
                {'rect': button4_rect, 'text': button4_text, 'color': 'green', 'value': 4},
                {'rect': button4_rect, 'text': button4_text, 'color': 'purple', 'value': 5}]
    
    color_choice_button = RadioButton (550, 230, "Color Choice", screen, font, game)
    
    while True:
        #Affichage du titre
        text_title = "Connect4IA"
        text_surface = font2.render(text_title, True,(255, 255, 255)) 
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH/2, HEIGHT/12)  
        screen.blit(text_surface, text_rect)
        
        #Affichage des boutons
        for button in button_array:
            pygame.draw.rect(screen, button['color'], button['rect'])
            text_surface = font.render(button['text'], True, 'black')
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)

        color_choice_button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_array:
                    if button['rect'].collidepoint(event.pos):
                        return button['value']
                        
                if event.button == 1:
                    color_choice_button.check_click(event.pos)
                    color_choice_button.draw()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = ConnectFour()
    mode = optionMenu(screen,game)
    if(mode != 0):
        gameLoop(screen, game, mode)
    pygame.quit()

if __name__ == "__main__":
    main()