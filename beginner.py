import random
import os
import time

# --- Config

ROWS = 6
COLS = 7
EMPTY = " "
PLAYER_PIECE = "O"
AI_PIECE = "X"


class Connect4:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False
        self.winner = None

    def display(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n Connect 4 (Beginner) ")
        print(" 1 2 3 4 5 6 7 ")  # Column numbers
        print("---------------")
        for row in self.board:
            print(f"|{'|'.join(row)}|")
        print("===============")

    def is_valid_location(self, col):
        # Check if the top row of the column is empty
        return self.board[0][col] == EMPTY

    def get_valid_locations(self):
        return [c for c in range(COLS) if self.is_valid_location(c)]

    def drop_piece(self, col, piece):
        # Find the next open row (Gravity logic)
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                self.board[r][col] = piece
                return r, col
        return None

    def check_win(self, piece):
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

        # Check Positive Diagonal (/)
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if (
                    self.board[r][c] == piece
                    and self.board[r - 1][c + 1] == piece
                    and self.board[r - 2][c + 2] == piece
                    and self.board[r - 3][c + 3] == piece
                ):
                    return True

        # Check Negative Diagonal (\)
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c + 1] == piece
                    and self.board[r + 2][c + 2] == piece
                    and self.board[r + 3][c + 3] == piece
                ):
                    return True
        return False


# ---- Game Loop
def play_game():
    game = Connect4()
    turn = 0  # 0 = Player, 1 = AI

    while not game.game_over:
        game.display()

        if turn == 0:
            # Player Turn
            while True:
                try:
                    col = int(input(f"Player {PLAYER_PIECE} turn (1-7): ")) - 1
                    if 0 <= col < COLS and game.is_valid_location(col):
                        game.drop_piece(col, PLAYER_PIECE)
                        if game.check_win(PLAYER_PIECE):
                            game.display()
                            print(f"PLAYER {PLAYER_PIECE} WINS!")
                            game.game_over = True
                        turn = 1
                        break
                    else:
                        print("Column full or invalid.")
                except ValueError:
                    print("Numbers only.")
        else:
            # AI Turn (Random)
            print(f"AI {AI_PIECE} is thinking...")
            time.sleep(0.5)
            valid_cols = game.get_valid_locations()
            col = random.choice(valid_cols)
            game.drop_piece(col, AI_PIECE)

            if game.check_win(AI_PIECE):
                game.display()
                print(f"AI {AI_PIECE} WINS!")
                game.game_over = True

            turn = 0


if __name__ == "__main__":
    play_game()
