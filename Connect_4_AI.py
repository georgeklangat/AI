import tkinter as tk
import numpy as np
from tkinter import messagebox

ROWS = 6
COLS = 7
PLAYER = 1  # Human player
AI = 2  # AI player
EMPTY = 0


class Connect4:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect 4 with AI")
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.buttons = [tk.Button(master, text="", width=10, height=3, command=lambda c=c: self.player_move(c))
                        for c in range(COLS)]
        self.labels = [
            [tk.Label(master, text="", font=("Arial", 24), width=4, height=2, bg="white") for _ in range(COLS)]
            for _ in range(ROWS)]

        for c in range(COLS):
            self.buttons[c].grid(row=0, column=c)
        for r in range(ROWS):
            for c in range(COLS):
                self.labels[r][c].grid(row=r + 1, column=c)

        self.current_player = PLAYER

    def player_move(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.board[row][col] = PLAYER
            self.update_ui()
            if self.check_winner(PLAYER):
                messagebox.showinfo("Game Over", "You win!")
                self.reset_game()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = AI
                self.ai_move()

    def ai_move(self):
        best_score = float("-inf")
        best_col = None
        for col in range(COLS):
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                self.board[row][col] = AI
                score = self.minimax(self.board, 5, False, float("-inf"), float("inf"))
                self.board[row][col] = EMPTY
                if score > best_score:
                    best_score = score
                    best_col = col

        row = self.get_next_open_row(best_col)
        self.board[row][best_col] = AI
        self.update_ui()

        if self.check_winner(AI):
            messagebox.showinfo("Game Over", "AI wins!")
            self.reset_game()
        elif self.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
        else:
            self.current_player = PLAYER

    def minimax(self, board, depth, maximizingPlayer, alpha, beta):
        if self.check_winner(AI):
            return 1000
        elif self.check_winner(PLAYER):
            return -1000
        elif self.is_board_full() or depth == 0:
            return 0

        if maximizingPlayer:
            best_score = float("-inf")
            for col in range(COLS):
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    board[row][col] = AI
                    score = self.minimax(board, depth - 1, False, alpha, beta)
                    board[row][col] = EMPTY
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break
            return best_score
        else:
            best_score = float("inf")
            for col in range(COLS):
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    board[row][col] = PLAYER
                    score = self.minimax(board, depth - 1, True, alpha, beta)
                    board[row][col] = EMPTY
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if alpha >= beta:
                        break
            return best_score

    def update_ui(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] == PLAYER:
                    self.labels[r][c].config(bg="red", text="X")
                elif self.board[r][c] == AI:
                    self.labels[r][c].config(bg="yellow", text="O")
                else:
                    self.labels[r][c].config(bg="white", text="")

    def is_valid_location(self, col):
        return self.board[0][col] == EMPTY

    def get_next_open_row(self, col):
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                return r

    def check_winner(self, piece):
        # Check horizontal locations
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Check vertical locations
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Check positively sloped diagonals
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        # Check negatively sloped diagonals
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True

        return False

    def is_board_full(self):
        return all(self.board[0][c] != EMPTY for c in range(COLS))

    def reset_game(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.update_ui()
        self.current_player = PLAYER


if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4(root)
    root.mainloop()
