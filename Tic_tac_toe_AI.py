import tkinter as tk
from tkinter import messagebox

# Define constants
PLAYER_X = "X"
PLAYER_O = "O"


class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.board = [""] * 9  # 3x3 board initialized with empty strings
        self.current_player = PLAYER_X

        self.buttons = [tk.Button(master, text="", font=('Arial', 20), width=5, height=2,
                                  command=lambda i=i: self.player_move(i)) for i in range(9)]

        for i, button in enumerate(self.buttons):
            button.grid(row=i // 3, column=i % 3)

    def player_move(self, i):
        if self.board[i] == "" and self.current_player == PLAYER_X:
            self.board[i] = PLAYER_X
            self.buttons[i].config(text=PLAYER_X)
            if self.check_winner(PLAYER_X):
                messagebox.showinfo("Game Over", "Player X wins!")
                self.reset_game()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = PLAYER_O
                self.ai_move()

    def ai_move(self):
        best_score = float("-inf")
        best_move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = PLAYER_O
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.board[best_move] = PLAYER_O
            self.buttons[best_move].config(text=PLAYER_O)
            if self.check_winner(PLAYER_O):
                messagebox.showinfo("Game Over", "Player O wins!")
                self.reset_game()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = PLAYER_X

    def minimax(self, board, depth, is_maximizing):
        scores = {PLAYER_X: -1, PLAYER_O: 1, "draw": 0}

        winner = self.check_winner(PLAYER_O)
        if winner:
            return scores[PLAYER_O]
        winner = self.check_winner(PLAYER_X)
        if winner:
            return scores[PLAYER_X]
        if "" not in board:
            return scores["draw"]

        if is_maximizing:
            best_score = float("-inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = PLAYER_O
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = PLAYER_X
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]

        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def reset_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="")
        self.current_player = PLAYER_X


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
