class Board(object):
    def __init__(self):
        self.board = ['-' for _ in range(9)]
        self.history = []  

    def move(self, action, take):
        if self.board[action] == '-':
            self.board[action] = take
            self.history.append((action, take))

    def restore(self, action):
        self.board[action] = '-'
        self.history.pop()

    def get_legal_actions(self):
        actions = []
        for i in range(9):
            if self.board[i] == '-':
                actions.append(i)
        return actions

    def is_legal_action(self, action):
        return self.board[action] == '-'

    def has_won(self, take):
        board = self.board
        lines = [board[0:3], board[3:6], board[6:9], board[0::3],
                 board[1::3], board[2::3], board[0::4], board[2:7:2]]
        if [take]*3 in lines:
            return True
        else:
            return False

    def gameover(self):
        if self.has_won('X') or self.has_won('O') or '-' not in self.board:
            return True
        else:
            return False

    def get_winner(self):
        if self.gameover():
            if self.has_won('X'):
                return 0
            elif self.has_won('O'):
                return 1
            else:
                return 2

    def print_b(self):
        board = self.board
        for i in range(len(board)):
            print(board[i], end='')
            if (i+1) % 3 == 0:
                print()

    def print_history(self):
        print(self.history)


class Player(object):
    def __init__(self, take='X'):  # 默认执的棋子为 take = 'X'
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
            action = input('Please input a num in 0-8:')
            if len(action) == 1 and action in '012345678' and board.is_legal_action(int(action)):
                return int(action)

class AIPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        print('AI is thinking ...')
        take = ['X', 'O'][self.take == 'X']
        player = AIPlayer(take)     # 假想敌！！！
        action = self.minimax(board, player)[1]
        return action
    
    def minimax(self, board, player,depth =0):
        if board.gameover():
            if board.get_winner() == 0:
                return -10 + depth, None
            elif board.get_winner() == 1:
                return 10 - depth, None
            elif board.get_winner() == 2:
                return 0, None
        if self.take == "O":
            bestVal = -float("Inf")
        else:
            bestVal = float("Inf")
        # exploring all the possible moves
        for action in board.get_legal_actions():
            board.move(action, self.take)
            val = player.minimax(board,self,depth-1)[0]
            board.restore(action)
            if self.take == "O" and val > bestVal:
                bestVal, bestAction = val, action
            if self.take == "X" and val < bestVal:
                bestVal, bestAction = val, action
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
        player1, player2 = self.mk_player(p1, 'X'), self.mk_player(p2, 'O')  # 先手执X，后手执O

        print('\nGame start!\n')
        self.board.print_b()
        while not self.board.gameover():
            # the players would take turns to play
            if self.current_player == player1:
                self.current_player = player2
            else:
                self.current_player = player1
            action = self.current_player.think(self.board)
            self.current_player.move(self.board, action)
            self.board.print_b()
        winner = self.board.get_winner()
        print(['Winner is player1', 'Winner is player2', 'Draw'][winner])
        print('Game over!')

        self.board.print_history()


if __name__ == '__main__':
    Game().run()
