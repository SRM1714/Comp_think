import numpy as np
from copy import deepcopy

def get_valid_row(board, col):
    #Find the lowest available row in the given column
    for row in range(5, -1, -1):
        if board[row][col] == ' ':
            return row
    return None  # Column is full

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or check_win(board, 'X') or check_win(board, 'O') or not generate_moves(board):  
        return evaluate(board)  # Base case: return board evaluation
    
    moves = generate_moves(board)
    moves.sort(key=lambda x: abs(x - len(board[0]) // 2))  # Prioritize center moves
    
    if maximizing_player:  
        max_eval = float('-inf') 
        for move in moves:
            new_board = deepcopy(board)
            row = get_valid_row(new_board, move)
            if row is not None:
                new_board[row][move] = 'X'
                eval = minimax(new_board, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:  # Alpha-Beta Pruning
                    break
        return max_eval

    else:  # Minimizing player (Human)
        min_eval = float('inf')
        for move in moves:
            new_board = deepcopy(board)
            row = get_valid_row(new_board, move)
            if row is not None:
                new_board[row][move] = 'O'
                eval = minimax(new_board, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:  # Alpha-Beta Pruning
                    break
        return min_eval


def check_win(board, player):
    for row in range(6):
        for col in range(7):
            if col <= 3 and board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                return True  # Check horizontal
            if row <= 2 and board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                return True  # Check vertical
            if col <= 3 and row <= 2 and board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True  # Check positive diagonal
            if col >= 3 and row <= 2 and board[row][col] == player and board[row+1][col-1] == player and board[row+2][col-2] == player and board[row+3][col-3] == player:
                return True  # Check negative diagonal
    return False

def check_center(board, player):
    """Count the player's pieces in the center column."""
    return sum(1 for row in range(6) if board[row][3] == player)

def check_corners(board, player):
    return sum(1 for row, col in [(0, 0), (0, 6), (5, 0), (5, 6)] if board[row][col] == player)

def evaluate(board):
    if check_win(board, 'X'):
        return 100
    if check_win(board, 'O'):
        return -100
    return check_center(board, 'X') - check_center(board, 'O') + check_corners(board, 'X') - check_corners(board, 'O')

def print_board(board):
    """Print the board with a more visually appealing format."""
    print("\n  0   1   2   3   4   5   6 ")
    print("___________________________")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("_________________________________")

def generate_moves(board):
    return [col for col in range(7) if board[0][col] == ' ']

def make_computer_move(board):
    best_score, best_move = float('-inf'), None
    for move in generate_moves(board):
        new_board = np.copy(board)
        for row in range(5, -1, -1):
            if new_board[row][move] == ' ':
                new_board[row][move] = 'X'
                break
        score = minimax(new_board, 4, float('-inf'), float('inf'), False)
        if score > best_score:
            best_score, best_move = score, move
    for row in range(5, -1, -1):
        if board[row][best_move] == ' ':
            board[row][best_move] = 'X'
            break

def play_game():
    """Main game loop with improved interface."""
    board = np.full((6, 7), ' ')
    print_board(board)
    while True:
        # Player's move
        while True:
            try:
                col = int(input("Select your move (0-6): "))
                if col < 0 or col > 6 or board[0][col] != ' ':
                    raise ValueError
                break
            except ValueError:
                print("Invalid move. Try again.")
        for row in range(5, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                break
        print_board(board)
        if check_win(board, 'O'):
            print("\nYou win!")
            break
        if ' ' not in board.flatten():
            print("\nDraw!")
            break
        print("\nThinking...")
        make_computer_move(board)
        print_board(board)
        if check_win(board, 'X'):
            print("\nComputer wins!")
            break
        if ' ' not in board.flatten():
            print("\nDraw!")
            break

# Start the game
play_game()
