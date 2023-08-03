import pygame

# infinite
INF = 9999

# initializing font
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Futura Medium', 50)


class MiniMax:
    def __init__(self, GameBoard):
        self.GameBoard = GameBoard

    # decides who won the game
    def evaluate(self):
        # 1 = x won, 0 = tie, -1 = o won
        
        # check rows
        for row in range(3):
            if (self.GameBoard[row][0] == self.GameBoard[row][1] 
                and self.GameBoard[row][1] == self.GameBoard[row][2]):
                if self.GameBoard[row][0] == 'x':
                    return 1
                elif self.GameBoard[row][0] == 'o':
                    return -1

        # check columns
        for col in range(3):
            if (self.GameBoard[0][col] == self.GameBoard[1][col] 
                and self.GameBoard[1][col] == self.GameBoard[2][col]):
                if self.GameBoard[0][col] == 'x':
                    return 1
                elif self.GameBoard[0][col] == 'o':
                    return -1

        # check diagonals
        if (self.GameBoard[0][0] == self.GameBoard[1][1] 
            and self.GameBoard[2][2] == self.GameBoard[1][1]):
            if self.GameBoard[1][1] == 'x':
                return 1
            elif self.GameBoard[1][1] == 'o':
                return -1
        if (self.GameBoard[0][2] == self.GameBoard[1][1] 
            and self.GameBoard[2][0] == self.GameBoard[1][1]):
            if self.GameBoard[1][1] == 'x':
                return 1
            elif self.GameBoard[1][1] == 'o':
                return -1

        # check if game is empty
        for i in range(3):
            for j in range(3):
                if self.GameBoard[i][j] == '-':
                    return 2
        
        return 0

    # max player
    def max(self):
        x = None
        y = None
        max_val = -INF
        val = self.evaluate()
        
        # if not starting position
        if val != 2:
            return (val, 0, 0)

        for row in range(0, 3):
            for col in range(0, 3):
                if self.GameBoard[row][col] == '-':
                    self.GameBoard[row][col] = 'x'
                    min_val = self.min()[0]
                    if max_val < min_val:
                        max_val = min_val
                        x = col
                        y = row
                    self.GameBoard[row][col] = '-'
        return(max_val, x, y)

    # min player
    def min(self):
        x = None
        y = None
        min_val = INF
        val = self.evaluate()
        if val != 2:
            return (val, 0, 0)
        for row in range(0, 3):
            for col in range(0, 3):
                if self.GameBoard[row][col] == '-':
                    self.GameBoard[row][col] = 'o'
                    max_val = self.max()[0]
                    if min_val > max_val:
                        min_val = max_val
                        x = col
                        y = row
                    self.GameBoard[row][col] = '-'
        return(min_val, x, y)


class GameLoop:
    # initialising display
    def __init__(self):
        self.GameState = 2
        background_color = (0, 0, 0)
        self.foreground_color = (255, 255, 255)
        (width, height) = (600, 600)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Tik Tak Toe AI')
        self.screen.fill(background_color)
        pygame.display.flip()

    def RenderUI(self, gameboard):
        self.gameboard = gameboard

        while True:
            # checks for events
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Mouse_x, Mouse_y = pygame.mouse.get_pos()
                    x = round(Mouse_x/200 - 0.49)
                    y = round(Mouse_y/200 - 0.49)
                    self.GameOver()
                    if self.GameState == 2:
                        ValidMove = self.MakeMove(x, y, 'o')
                        if ValidMove:
                            return self.gameboard
                if event.type == pygame.QUIT:
                    pygame.quit()

            # draws the board lines
            self.DrawBoard()
            
            # draws the x's and o's
            for row in range(3):
                for col in range(3):
                    if self.gameboard[row][col] == 'x':
                        self.DrawX(col, row)
                    if self.gameboard[row][col] == 'o':
                        self.DrawO(col, row)

            # checks if the game is over
            self.GameOver()

            pygame.display.update()

    def DrawBoard(self):
        '''Draws the lines of the GameBoard'''
        for xy in range(200, 401, 200):
            pygame.draw.line(self.screen, self.foreground_color,
                             (0, xy), (600, xy), 3)
            pygame.draw.line(self.screen, self.foreground_color,
                             (xy, 0), (xy, 600), 3)

    def DrawX(self, x, y):
        x += 1
        y += 1
        pygame.draw.line(self.screen, self.foreground_color, (200 * x -
                                                              200 + 10, 200 * y - 200 + 10), ((x * 200) - 10, (y * 200) - 10), 3)
        pygame.draw.line(self.screen, self.foreground_color, (200 * x - 200 + 10,
                                                              (y * 200) - 10), ((x * 200) - 10, 200 * y - 200 + 10), 3)

    def DrawO(self, x, y):
        x += 1
        y += 1
        pygame.draw.circle(self.screen, self.foreground_color,
                           (x * 200 - 100, y * 200 - 100), 90, 3)

    def MakeMove(self, x, y, player):

        if self.gameboard[y][x] == '-':
            self.gameboard[y][x] = player
            return True
        return False

    # on each call checks if the game is over, if yes prints winner on
    def GameOver(self):
        self.GameState = MiniMax(self.gameboard).evaluate()
        if self.GameState == 1:
            textsurface = myfont.render('X Won this Game', False, (255, 0, 0))
            GL.screen.blit(textsurface, (200,250))
        elif self.GameState == 0:
            textsurface = myfont.render('Tie', False, (255, 0, 0))
            GL.screen.blit(textsurface, (280,300))
        elif self.GameState == -1:
            textsurface = myfont.render('O Won this Game', False, (255, 0, 0))
            GL.screen.blit(textsurface, (200,250))


if __name__ == "__main__":
    Board = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]
    
    # creating object of class game loop
    GL = GameLoop()

    # game loop
    while True:
        GL.RenderUI(Board)

        # creating object of class minimax
        MM = MiniMax(Board)
        
        # our AI is always the max player, so we ask for max
        bestmove = MM.max()

        # returns best evaluation , x and y coordinates
        GL.MakeMove(bestmove[1], bestmove[2], 'x')
