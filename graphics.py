from Game import ConnectFour
import pygame

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

    while state :
        clock.tick(60) # limits FPS to 60
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                state = GAMEOVER

            elif event.type == pygame.MOUSEBUTTONDOWN :
                state = handleMouseDown(event, screen, game)

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = ConnectFour()
    
    drawBoard(screen)
    gameLoop(screen, game)
    
    pygame.quit()

if __name__ == "__main__":
    main()