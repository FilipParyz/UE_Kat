import tkinter as tk
import random
from tkinter import messagebox

def check_winner(board):
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != "":
            return True
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return True
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return True
    return False

def button_click(row, col):
    global current_player
    if buttons[row][col]["text"] == "" and not winner:
        buttons[row][col]["text"] = "X"  # Cz³owiek wykonuje ruch
        game_board[row][col] = "X"
        if check_winner(game_board):
            messagebox.showinfo("Tic Tac Toe", "Player X wins!")
            reset_board()
        elif all(button["text"] != "" for row in buttons for button in row):
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            reset_board()
        else:
            computer_move()

def computer_move():
    available_moves = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]["text"] == ""]
    if available_moves:
        row, col = random.choice(available_moves)
        buttons[row][col]["text"] = "O"  # Ruch komputera
        game_board[row][col] = "O"
        if check_winner(game_board):
            messagebox.showinfo("Tic Tac Toe", "Player O wins!")
            reset_board()
        elif all(button["text"] != "" for row in buttons for button in row):
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            reset_board()

def reset_board():
    global winner, game_board
    winner = False
    game_board = [["" for _ in range(3)] for _ in range(3)]
    for row in buttons:
        for button in row:
            button["text"] = ""

# Utworzenie okna g³ównego
root = tk.Tk()
root.title("Tic Tac Toe")

game_board = [["" for _ in range(3)] for _ in range(3)]
buttons = []

for i in range(3):
    button_row = []
    for j in range(3):
        button = tk.Button(root, text="", font=("Arial", 20), width=5, height=2,
                           command=lambda row=i, col=j: button_click(row, col))
        button.grid(row=i, column=j)
        button_row.append(button)
    buttons.append(button_row)

current_player = random.choice(["X", "O"])  # Losowe wybranie gracza rozpoczynaj¹cego
winner = False

if current_player == "O":
    computer_move()

root.mainloop()
