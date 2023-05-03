print("enter the size of board")
n=int(input())
class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.board = [[' ' for j in range(n)] for i in range(n)]
        self.current_player = '1'
    
    def print_board(self):
        for i in range(self.n):
            print('|', end='')
            for j in range(self.n):
                print(self.board[i][j], end='|')
            print()
    
    def make_move(self, i, j):
        if self.board[i][j] == ' ':
            self.board[i][j] = self.current_player
            self.current_player = '1' if self.current_player == '2' else '2'
            return True
        return False
    
    def get_winner(self):
        for i in range(self.n):
            if self.board[i][0] != ' ' and all(self.board[i][j] == self.board[i][0] for j in range(1, self.n)):
                return self.board[i][0]
            if self.board[0][i] != ' ' and all(self.board[j][i] == self.board[0][i] for j in range(1, self.n)):
                return self.board[0][i]
        if self.board[0][0] != ' ' and all(self.board[i][i] == self.board[0][0] for i in range(1, self.n)):
            return self.board[0][0]
        if self.board[0][self.n - 1] != ' ' and all(self.board[i][self.n - 1 - i] == self.board[0][self.n - 1] for i in range(1, self.n)):
            return self.board[0][self.n - 1]
        if all(self.board[i][j] != ' ' for i in range(self.n) for j in range(self.n)):
            return 'Tie'
        return None
    
    def is_game_over(self):
        return self.get_winner() is not None
    
    def get_valid_moves(self):
        moves = []
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
 import random

class MonteCarloPlayer:
    def __init__(self, n, num_simulations=1000):
        self.n = n
        self.num_simulations = num_simulations
        self.current_player = 1
    
    def get_move(self, game):
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None
        if len(valid_moves) == 1:
            return valid_moves[0]
        best_move = None
        best_score = -1
        for move in valid_moves:
            score_sum = 0
            for i in range(self.num_simulations):
                game_copy = TicTacToe(self.n)
                game_copy.board = [row[:] for row in game.board]
                game_copy.current_player = game.current_player
                game_copy.make_move(*move)
                while not game_copy.is_game_over():
                    random_move = random.choice(game_copy.get_valid_moves())
                    game_copy.make_move(*random_move)
                winner = game_copy.get_winner()
                if winner == self.current_player:
                    score_sum += 2
                elif winner is None:
                    score_sum += 1
            if score_sum > best_score:
                best_move = move
                best_score = score_sum
        return best_move
class MinimaxPlayer:
    def __init__(self, n):
        self.n = n
    
    def get_move(self, game):
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None
        if len(valid_moves) == 1:
            return valid_moves[0]
        best_move = None
        best_score = -1
        for move in valid_moves:
            game_copy = TicTacToe(self.n)
            game_copy.board = [row[:] for row in game.board]
            game_copy.current_player = game.current_player
            game_copy.make_move(*move)
            score = self.minimax(game_copy, False)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move
    
    def minimax(self, game, maximizing):
        if game.is_game_over():
            winner = game.get_winner()
            if winner == game.current_player: # changed from self.current_player to game.current_player
                return 2
            elif winner is None:
                return 1
            else:
                return 0
        if maximizing:
            return self.maximize(game)
        else:
            return self.minimize(game)
    
    def maximize(self, game):
        best_score = -1
        for move in game.get_valid_moves():
            game_copy = TicTacToe(self.n)
            game_copy.board = [row[:] for row in game.board]
            game_copy.current_player = game.current_player
            game_copy.make_move(*move)
            score = self.minimax(game_copy, False)
            best_score = max(best_score, score)
        return best_score
    
    def minimize(self, game):
        best_score = 2
        for move in game.get_valid_moves():
            game_copy = TicTacToe(self.n)
            game_copy.board = [row[:] for row in game.board]
            game_copy.current_player = game.current_player
            game_copy.make_move(*move)
            score = self.minimax(game_copy, True)
            best_score = min(best_score, score)
        return best_score
def play_game(n, player1_type="minimax", player2_type="montecarlo", num_simulations=10000, first_player=1):
    game = TicTacToe(n)
    game.current_player = first_player
    if player1_type == "minimax":
        player1 = MinimaxPlayer(n)
    else:
        player1 = MonteCarloPlayer(n, num_simulations)
    if player2_type == "minimax":
        player2 = MinimaxPlayer(n)
    else:
        player2 = MonteCarloPlayer(n, num_simulations)
    while not game.is_game_over():
        if game.current_player == 1:
            move = player1.get_move(game)
            print(f"Player 1 ({player1_type}):")
        else:
            move = player2.get_move(game)
            if player2_type != "montecarlo":
                print(f"Player 2 ({player2_type}):")
        if move is None:
            print(f"Player {game.current_player} Move: PASS")
        else:
            print(f"Player {game.current_player} Move: {move}")
            game.make_move(*move)
        game.print_board()
    winner = game.get_winner()
    if winner is None:
        print("It's a tie!")
    else:
        print(f"Player {winner} wins!")
if __name__ == '__main__':
    play_game(n, player1_type="montecarlo", player2_type="minimax", num_simulations=1000)
