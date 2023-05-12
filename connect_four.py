class Board:
    def __init__(self, to, sender):
        self.players = {0:["X", sender], 1:["O", to]}
        self.row = 6
        self.column = 7
        self.board = [["-" for c in range(self.column)] for r in range(self.row)]
        self.turn = 1
        self.winner = ""

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
        return player == self.players[self.turn][1]
    
    def placeable(self, column):
        return column > 0 and column <= self.column
    
    def place(self, c):
        c -= 1
        r = self.get_nextrow(c)
        if r == -1:
            return False
        piece = self.players[self.turn][0]
        self.board[r][c] = piece
        self.turn += 1
        self.turn %= 2
        self.win(piece, r, c)
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
            self.winner = self.players[self.turn][1]
    
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
        return  display
