class Board(object):
    def __init__(self):
        self.board = ['-','-','-','-','-','-',
                      '-','-','-','-','-','-',
                      '-','-','-','-','-','-',
                      '-','-','-','-','-','-',
                      '-','-','-','-','-','-',
                      '-','-','-','-','-','-']

    def move(self, action, take):
        """
        action: which column to drop the number
        take: X or O
        """
        i = 30 + action
        while i >= action:
            if self.board[i] == "-":
                self.board[i] = take
                break
            i -= 6

    def restore(self, action):
        i = action
        while i <= 30+ action:
            if self.board[i] != "-":
                self.board[i] = "-"
                break
            i+= 6 

    def check_legal_actions(self, action):
        check = self.board[action:30+action+1:6]
        if "-" in check:
            return True
        return False

    def legal_moves(self):
        moves = []
        for i in range(0,6):
            if self.board[i] == "-":
                moves.append(i)
        return moves
                
    def check_rows(self, take):
        i = 0
        while i <= 30:
            check = self.board[i:i+6]
            for j in range(len(check)-3):
                if check[j] == check[j+1] == check[j+2] == check[j+3] == take:
                    return True
            i += 6
        return False
                
    def check_columns(self, take):
        i = 0
        for i in range(6):
            check = self.board[i:30+i+1:6]
            for j in range(len(check)-3):
                if check[j] == check[j+1] == check[j+2] == check[j+3] == take:
                    return True
        return False

    def check_diagonal(self, take):
        board = self.board
        checks = [board[3:19:5], board[4:25:5], board[5:31:5], board[11:32:5],
                  board[17:33:5], board[12:34:5], board[6:35:5], board[0:36:5],
                  board[1:30:5], board[2:24:5]]
        for item in checks:
            for j in range(len(item)-3):
                if item[j] == item[j+1] == item[j+2] == item[j+3] == take:
                    return True
        return False

    def has_won(self, take):
        if self.check_rows(take) or self.check_columns(take) or self.check_diagonal(take):
            return True
        return False

    def gameover(self):
        if self.has_won('X') or self.has_won('O') or '-' not in self.board:
            return True
        return False

    def get_winner(self):
        if self.gameover():
            if self.has_won('X'):
                return 0
            elif self.has_won('O'):
                return 1
            else:
                return 2

    def print_board(self):
        board = self.board
        print(board[0:6])
        print(board[6:12])
        print(board[12:18])
        print(board[18:24])
        print(board[24:30])
        print(board[30:36])

    def evaluate_board(self):
        if self.has_won('X'):
            return float("Inf")
        elif self.has_won('O'):
            return -float("Inf")
        else:
            num_top_x = 0
            num_top_o = 0

            i = 0
            for i in range(6):
                check = self.board[i:30+i+1:6]
                for j in check:
                    if j == "X":
                        num_top_x += 1
                        break
                    elif j == "O":
                        num_top_o += 1
                        break
            return num_top_x - num_top_o
        

class Player(object):
    def __init__(self, take='X'):
        self.take = take

    def think(self, board):
        pass

    def move(self, board, action):
        board.move(action, self.take)

class HumanPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        while True:
            action = input('Please input a column number in 0-5:')
            if len(action) == 1 and action in '012345' and board.check_legal_actions(int(action)):
                return int(action)

class AIPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        print('AI is thinking ...')
        take = ['X', 'O'][self.take == 'X']
        player = AIPlayer(take) 
        action = self.minimax(board, player)[1]
        return action

    def minimax(self, board, player,depth = 9, alpha =-float("Inf"), beta= float("Inf")):
        if board.gameover() or depth == 0:
            return [board.evaluate_board(), -1, alpha, beta]
        if self.take == "0":
            bestVal = -float("Inf")
        else:
            bestVal = float("Inf")
        for action in board.legal_moves():
            board.move(action, self.take)
            val = self.minimax(board,player,depth-1, alpha, beta)[0]
            board.restore(action)
            if self.take == "O" and val > bestVal:
                bestVal, bestAction = val, action
                alpha = max(alpha, bestVal)
            if self.take == "X" and val < bestVal:
                bestVal, bestAction = val, action
                beta = min(beta, bestVal)
            if alpha > beta:
                break
        return [bestVal, bestAction]
                        
        

class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None

    def mk_player(self, p, take='X'):
        return [HumanPlayer(take),AIPlayer(take)][p]

    def run(self):
        ps = input("Please select two player's type:\n\t0.Human\n\t1.AI\nSuch as:0 0\n")
        p1, p2 = [int(p) for p in ps.split(' ')]
        player1, player2 = self.mk_player(p1, 'X'), self.mk_player(p2, 'O') 

        print('\nGame start!\n')
        self.board.print_board()
        while not self.board.gameover():
            # the players would take turns to play
            if self.current_player == player1:
                self.current_player = player2
            else:
                self.current_player = player1
            action = self.current_player.think(self.board)
            self.current_player.move(self.board, action)
            self.board.print_board()
        winner = self.board.get_winner()
        print(['Winner is player1', 'Winner is player2', 'Draw'][winner])
        print('Game over!')


if __name__ == '__main__':
    Game().run()
