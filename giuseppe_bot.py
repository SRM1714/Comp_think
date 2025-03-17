# i do not htink the algoritmh is the best, but is able to match the battle code 
# it is able to win against gemin bot
#it can bet the chatgpt bot if it starts
#it is not made to play against it, but can be implemented

import random
import time

ROWS = 6  # Standard Connect 4 dimensions
COLS = 7

HUMAN = -1
COMP = +1

class Connect4Bot:
    def __init__(self, player_id):
        self.player_id = player_id  # MM's player number
        self.opponent_id = HUMAN if player_id == COMP else COMP

    def evaluate(self, board):
        """
        Evaluates the board state based on the difference between MM and opponent advantages.
        """
        return self.count_patterns(board, self.player_id) - self.count_patterns(board, self.opponent_id)

    def count_patterns(self, board, player):
        """Counts the number of two-in-a-row, three-in-a-row, and four-in-a-row for a player."""
        score = 0
        for row in range(ROWS):
            for col in range(COLS - 3):
                score += self.pattern_score([board[row][col + i] for i in range(4)], player)
        
        for row in range(ROWS - 3):
            for col in range(COLS):
                score += self.pattern_score([board[row + i][col] for i in range(4)], player)
        
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                score += self.pattern_score([board[row + i][col + i] for i in range(4)], player)
        
        for row in range(ROWS - 3):
            for col in range(3, COLS):
                score += self.pattern_score([board[row + i][col - i] for i in range(4)], player)
        return score

    def pattern_score(self, window, player):
        """Determines the score of a 4-slot window based on occurrences of the player's pieces."""
        player_count = window.count(player)
        opponent_count = window.count(self.opponent_id)
        empty_count = window.count(0)
        
        if player_count == 4:
            return 10000  # Winning move
        elif player_count == 3 and empty_count == 1:
            return 100   # Strong threat
        elif player_count == 2 and empty_count == 2:
            return 10    # Potential future move
        elif opponent_count == 3 and empty_count == 1:
            return -100  # Blocking opponent's strong move
        return 0

    def get_valid_moves(self, board):
        """Returns a list of columns that are not full."""
        return [c for c in range(COLS) if board[0][c] == 0]

    def drop_piece(self, board, col, player):
        """Simulates dropping a piece into the board."""
        for row in reversed(range(ROWS)):
            if board[row][col] == 0:
                board[row][col] = player
                return

    def is_terminal(self, board):
        """Checks if the game has ended."""
        return self.winning_move(board, self.player_id) or self.winning_move(board, self.opponent_id) or all(board[0][c] != 0 for c in range(COLS))

    def winning_move(self, board, player):
        """Checks if the given player has won."""
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(board[row][col + i] == player for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(COLS):
                if all(board[row + i][col] == player for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(board[row + i][col + i] == player for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(3, COLS):
                if all(board[row + i][col - i] == player for i in range(4)):
                    return True
        return False

    def minimax(self, board, depth, alpha, beta, maximizing, start_time, time_limit):
        """Minimax algorithm with Alpha-Beta Pruning, considering time limits."""
        if time.time() - start_time > time_limit:
            print("TIMEOUT: Random action taken.")
            return None, self.evaluate(board)  # Return best evaluation found before timeout
        
        valid_moves = self.get_valid_moves(board)
        if depth == 0 or self.is_terminal(board):
            return None, self.evaluate(board)
        
        best_col = None
        if maximizing:
            max_eval = -float("inf")
            for col in valid_moves:
                temp_board = [row[:] for row in board]
                self.drop_piece(temp_board, col, self.player_id)
                _, score = self.minimax(temp_board, depth - 1, alpha, beta, False, start_time, time_limit)
                if score > max_eval:
                    max_eval = score
                    best_col = col
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break
            return best_col, max_eval
        else:
            min_eval = float("inf")
            for col in valid_moves:
                temp_board = [row[:] for row in board]
                self.drop_piece(temp_board, col, self.opponent_id)
                _, score = self.minimax(temp_board, depth - 1, alpha, beta, True, start_time, time_limit)
                if score < min_eval:
                    min_eval = score
                    best_col = col
                beta = min(beta, min_eval)
                if alpha >= beta:
                    break
            return best_col, min_eval

    def get_move(self, board, first_move):
        """Determines the best move using Minimax with Alpha-Beta Pruning."""
        start_time = time.time()
        time_limit = 2 if first_move else 5  # 2s for first call, 5s for second
        depth = 6  # Increased depth for stronger play
        best_move, _ = self.minimax(board, depth, -float("inf"), float("inf"), True, start_time, time_limit)
        
        decision = [False] * COLS
        if best_move is not None:
            decision[best_move] = True
        return decision

# Expose get_move at the module level to ensure compatibility with the game script
def get_move(board, first_move, player_id):
    """Module-level function that creates a bot instance and gets the move."""
    bot = Connect4Bot(player_id)
    return bot.get_move(board, first_move)

