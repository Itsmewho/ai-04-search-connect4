import random
import os
import time

# --- Config ---
ROWS = 6
COLS = 7
EMPTY = " "
PLAYER_PIECE = "O"
AI_PIECE = "X"


# --- Connect 4 Class (Reused) ---
class Connect4:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False

    def display(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n Connect 4 (Intermediate) ")
        print(" 1 2 3 4 5 6 7 ")
        print("---------------")
        for row in self.board:
            print(f"|{'|'.join(row)}|")
        print("===============")

    def is_valid_location(self, col):
        return self.board[0][col] == EMPTY

    def get_valid_locations(self):
        return [c for c in range(COLS) if self.is_valid_location(c)]

    def drop_piece(self, col, piece):
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                self.board[r][col] = piece
                return r
        return None

    def check_win(self, piece):
        # (Same win check logic as before - abbreviated for clarity)
        # Check Horizontal
        for c in range(COLS - 3):
            for r in range(ROWS):
                if (
                    self.board[r][c] == piece
                    and self.board[r][c + 1] == piece
                    and self.board[r][c + 2] == piece
                    and self.board[r][c + 3] == piece
                ):
                    return True
        # Check Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c] == piece
                    and self.board[r + 2][c] == piece
                    and self.board[r + 3][c] == piece
                ):
                    return True
        # Check Diagonals
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
                ):  # Neg Diag
                    return True
        return False


# --- THE INTERMEDIATE BRAIN ---


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # Block Opponent (Heavy Penalty)
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(game, piece):
    score = 0

    # 1. Center Column Preference
    center_array = [game.board[r][COLS // 2] for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # 2. Horizontal Scoring
    for r in range(ROWS):
        row_array = game.board[r]
        for c in range(COLS - 3):
            window = row_array[c : c + 4]
            score += evaluate_window(window, piece)

    # 3. Vertical Scoring
    for c in range(COLS):
        col_array = [game.board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r : r + 4]
            score += evaluate_window(window, piece)

    # 4. Diagonal Scoring
    # Positive Slope
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [game.board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)
    # Negative Slope
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [game.board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def get_best_move(game, piece):
    valid_locations = game.get_valid_locations()
    best_score = -10000
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        # Simulate the move
        row = game.drop_piece(col, piece)

        # Calculate score of the board AFTER the move
        score = score_position(game, piece)

        # Undo the move (Manually reset the slot)
        game.board[row][col] = EMPTY

        if score > best_score:
            best_score = score
            best_col = col

    return best_col


# --- Game Loop ---
def play_game():
    game = Connect4()
    turn = 0

    while not game.game_over:
        game.display()

        if turn == 0:
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
        else:
            print(f"AI {AI_PIECE} is calculating (Scoring)...")
            time.sleep(0.5)
            col = get_best_move(game, AI_PIECE)  # <-- Uses Scoring Logic
            game.drop_piece(col, AI_PIECE)

            if game.check_win(AI_PIECE):
                game.display()
                print("AI WINS!")
                game.game_over = True
            turn = 0


if __name__ == "__main__":
    play_game()
