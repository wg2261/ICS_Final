#was unable to properly integrate into chat system without errors
import pygame
import sys
import math
 
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

SQUARESIZE = 75
RADIUS = int(SQUARESIZE/2 - 5)

games = []

class Board:
    def __init__(self, to, sender):
        self.players = [to, sender]
        self.row = 6
        self.column = 7
        self.board = [["-" for c in range(self.column)] for r in range(self.row)]
        self.turn = 0
        self.winner = ""
        self.width = self.column * SQUARESIZE
        self.height = (self.row + 1) * SQUARESIZE
        self.size = (self.width, self.height)
        games.append(self)

    def get_board(self):
        return self.board
    
    def get_columnlength(self):
        return self.column

    def get_row(self, r):
        return self.board[r]
    
    def get_nextrow(self, c):
        for r in range(self.row - 1, -1, -1):
            if self.board[r][c] == "-":
                return r
        return -1

    def get_column(self, c):
        return [self.board[r][c] for r in range(self.row)]
    
    def get_posdia(self, r, c):
        pieces = []
        while r < self.row - 1 and c > 0:
            r += 1
            c -= 1
        while r >= 0 and c < self.column: 
            pieces.append(self.board[r][c])
            r -= 1
            c += 1
        return pieces

    def get_negdia(self, r, c):
        pieces = []
        while r > 0 and c > 0: 
            r -= 1
            c -= 1
        while r < self.row and c < self.column:
            pieces.append(self.board[r][c])
            r += 1
            c += 1
        return pieces
    
    def my_turn(self, player):
        return player == self.players[self.turn]
    
    def placeable(self, column):
        return column >= 0 and column < self.column
    
    def place(self, c): 
        r = self.get_nextrow(c)
        if r == -1:
            return False
        self.turn += 1
        self.turn %= 2
        self.board[r][c] = str(self.turn)
        self.win(str(self.turn), r, c)
        return True
    
    def check(self, pieces, p):
        count = 0
        if len(pieces) > 3:
            for i in pieces:
                if i == p:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def finished(self):
        if "-" not in self.get_row(0) and self.winner == "":
            self.winner = "Tie"
    
    def win(self, p, r, c):
        column = self.get_column(c)
        row = self.get_row(r)
        pos = self.get_posdia(r, c)
        neg = self.get_negdia(r, c)
        if self.check(column, p) or self.check(row, p) or self.check(pos, p) or self.check(neg, p):
            self.winner = self.players[self.turn]
    
    def get_winner(self):
        return self.winner
    
    def get_update(self):
        text = str(self)
        if self.winner == "Tie":
            text += "Tie!"
        elif self.winner != "":
            text += self.winner + " won~\n" 
        return text
        
    def __str__(self):
        display = "\n".join([" ".join(row) for row in self.board]) + "\n"
        display += " ".join([str(i + 1) for i in range(self.column)]) + "\n"
        display += "~" * self.column * 2 + "\n"
        return display

    def draw_board(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        for c in range(self.column):
            for r in range(self.row):
                pygame.draw.rect(self.screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        
        for c in range(self.column):
            for r in range(self.row):      
                if self.board[r][c] == "1":
                    pygame.draw.circle(self.screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2) + SQUARESIZE), RADIUS)
                elif self.board[r][c] == "0": 
                    pygame.draw.circle(self.screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2) + SQUARESIZE), RADIUS)
        pygame.display.update()
        print(self.get_update())
        myfont = pygame.font.SysFont("monospace", 50)

    def show_board(self, me):
        while self.winner == "":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
        
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.turn == 0:
                        pygame.draw.circle(self.screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                    else: 
                        pygame.draw.circle(self.screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
                    column = int(math.floor(posx/SQUARESIZE))
                    comment = ""
                    if self.my_turn(self.players[self.turn]):
                        if self.placeable(column):
                            if self.place(column):
                                comment = "~~Placed~~"
                            else:
                                comment = "~~This column is full~~"
                        else:
                            comment = "~~Out of bounds. \nGive a number between 1 and " + str(self.column) + '~~\n'
                    else:
                        comment = "~~It is not your turn.~~\n"

                    self.draw_board()
        pygame.time.wait(3000)
        


# b = Board("one", "two")
# b.draw_board()
# b.show_board("one")