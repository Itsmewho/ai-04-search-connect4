import random
import os
import math
import time


# --- Config

ROWS = 6
COLS = 7
EMPTY = " "
PLAYER_PIECE = "O"
AI_PIECE = "X"
DEPTH = 5  # Could be higher but it isnt really needed


# --- Connect 4 Class


class Connect4:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False

    def display(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n Connect 4 (Expert - Depth {DEPTH}) ")
        print(" 1 2 3 4 5 6 7 ")
        print("---------------")
        for row in self.board:
            print(f"|{'|'.join(row)}|")
        print("===============")

    def is_valid_location(self, col):
        return self.bord[0][col] == EMPTY

    def get_valid_location(self):
        return [c for c in range(COLS) if self.is_valid_location(c)]

    def drop_pieces(self, col, piece):
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                self.board[r][col] == piece
                return r
        return None

    def check_win(self, piece):
        # Horizontal
        for c in range(COLS - 3):
            for r in range(ROWS):
                if (
                    self.board[r][c] == piece
                    and self.board[r][c + 1] == piece
                    and self.board[r][c + 2] == piece
                    and self.board[r][c + 3] == piece
                ):
                    return True
        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c] == piece
                    and self.board[r + 2][c] == piece
                    and self.board[r + 3][c] == piece
                ):
                    return True
        # Diagonals
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c + 1] == piece
                    and self.board[r + 2][c + 2] == piece
                    and self.board[r + 3][c + 3] == piece
                ):
                    return True
                if (
                    self.board[r + 3][c] == piece
                    and self.board[r + 2][c + 1] == piece
                    and self.board[r + 1][c + 2] == piece
                    and self.board[r][c + 3] == piece
                ):
                    return True
        return False


# --- THE EXPERT BRAIN: MINIMAX + SCORING


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(game, piece):
    score = 0
    # Center Preference
    center_array = [game.board[r][COLS // 2] for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal
    for r in range(ROWS):
        row_array = game.board[r]
        for c in range(COLS - 3):
            window = row_array[c : c + 4]
            score += evaluate_window(window, piece)
    # Vertical
    for c in range(COLS):
        col_array = [game.board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r : r + 4]
            score += evaluate_window(window, piece)
    # Diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [game.board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [game.board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score


def minimax(game, depth, alpha, beta, maximizingPlayer):
    valid_locations = game.get_valid_locations()
    is_terminal = (
        game.check_win(PLAYER_PIECE)
        or game.check_win(AI_PIECE)
        or len(valid_locations) == 0
    )

    # 1. Terminal State (Game Over)
    if is_terminal:
        if game.check_win(AI_PIECE):
            return (None, 100000000000000)
        if game.check_win(PLAYER_PIECE):
            return (None, -10000000000000)
        return (None, 0)  # Draw

    # 2. Depth Limit Reached (Heuristic Guess)
    if depth == 0:
        return (None, score_position(game, AI_PIECE))

    # 3. Recursion
    if maximizingPlayer:  # AI's Turn
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = game.drop_piece(col, AI_PIECE)
            new_score = minimax(game, depth - 1, alpha, beta, False)[1]
            game.board[row][col] = EMPTY  # Undo move

            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Pruning
        return column, value
    else:  # Human's Turn
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = game.drop_piece(col, PLAYER_PIECE)
            new_score = minimax(game, depth - 1, alpha, beta, True)[1]
            game.board[row][col] = EMPTY  # Undo move

            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # Pruning
        return column, value


# --- Game Loop
def play_game():
    game = Connect4()
    turn = random.randint(0, 1)  # Random start

    while not game.game_over:
        game.display()

        if turn == 0:  # Player
            while True:
                try:
                    col = int(input(f"Player {PLAYER_PIECE} turn (1-7): ")) - 1
                    if 0 <= col < COLS and game.is_valid_location(col):
                        game.drop_piece(col, PLAYER_PIECE)
                        if game.check_win(PLAYER_PIECE):
                            game.display()
                            print("PLAYER WINS!")
                            game.game_over = True
                        turn = 1
                        break
                except ValueError:
                    pass
        else:  # AI
            print(f"AI {AI_PIECE} is thinking (Depth {DEPTH})...")
            # Call Minimax with Alpha (-inf) and Beta (+inf)
            col, minimax_score = minimax(game, DEPTH, -math.inf, math.inf, True)

            if game.is_valid_location(col):
                game.drop_piece(col, AI_PIECE)
                if game.check_win(AI_PIECE):
                    game.display()
                    print("AI WINS!")
                    game.game_over = True
                turn = 0
            else:
                # Should not happen, but safety net for draws
                print("Draw!")
                game.game_over = True


if __name__ == "__main__":
    play_game()
