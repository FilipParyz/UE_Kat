import tkinter as tk
import random

# Inicjalizacja zmiennych globalnych
root = None
rows, columns, mines = 0, 0, 0
frame = None
buttons = None
board = None
is_game_over = False
cells_uncovered = 0
total_cells = 0
uncovered_label = None
status_label = None
restart_button = None
quit_button = None
flags_placed = 0
total_flags = 40

def create_game_frame():
    global frame
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

def create_labels():
    global uncovered_label, status_label
    labels_frame = tk.Frame(root)
    labels_frame.grid(row=1, column=0)

    status_label = tk.Label(labels_frame, text="", pady=10)
    status_label.grid(row=0, column=0)

    uncovered_label = tk.Label(labels_frame, text="", pady=10)
    uncovered_label.grid(row=1, column=0)

    return uncovered_label

def place_flag(event, row, col):
    global buttons
    if buttons[row][col]["text"] == "" and buttons[row][col]["state"] != "disabled":
        buttons[row][col].config(fg="red")
        buttons[row][col].config(text="🚩")
    else:
        buttons[row][col].config(text="")
        
def create_buttons():
    global buttons
    buttons = [[None for _ in range(columns)] for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):
            create_button(i, j)

def create_button(i, j):
    global frame, buttons
    buttons[i][j] = tk.Button(frame, width=2, command=lambda i=i, j=j: click(i, j), fg="white")
    buttons[i][j].grid(row=i, column=j)
    buttons[i][j].config(disabledforeground="white")
    buttons[i][j].config(state="normal")  
    
    buttons[i][j].bind("<Button-3>", lambda event, row=i, col=j: place_flag(event, i, j))

def create_widgets():
    global uncovered_label, status_label, restart_button, quit_button
    create_labels()
    create_buttons()
    create_restart_quit_buttons()

def create_restart_quit_buttons():
    global restart_button, quit_button
    restart_button = tk.Button(root, text="Zagraj ponownie", command=restart_game)
    restart_button.grid(row=2, column=0)
    
    quit_button = tk.Button(root, text="Zakończ grę", command=root.quit)
    quit_button.grid(row=3, column=0)

def place_mines():
    global board
    board = [[0 for _ in range(columns)] for _ in range(rows)]
    mines_placed = 0
    while mines_placed < mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, columns - 1)
        if board[row][col] != -1:
            board[row][col] = -1
            mines_placed += 1

def calculate_numbers():
    global board
    for i in range(rows):
        for j in range(columns):
            if board[i][j] != -1:
                board[i][j] = count_adjacent_mines(i, j)

def count_adjacent_mines(row, col):
    count = 0
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(columns, col + 2)):
            if board[i][j] == -1:
                count += 1
    return count

def click(row, col):
    global cells_uncovered, total_cells
    if board[row][col] == -1:
        game_over()
        reveal_all_mines()
    else:
        reveal(row, col)
    uncovered_label.config(text=f"Odkryte pola: {cells_uncovered}/{total_cells}")

def reveal(row, col):
    global cells_uncovered, total_cells
    if buttons[row][col]["state"] == "disabled":
        return

    buttons[row][col].config(state="disabled", bg="gray", fg="white", font=('Arial', 10, 'bold'))
    if board[row][col] > 0:
        buttons[row][col].config(text=str(board[row][col]))
    else:
        for i in range(max(0, row - 1), min(rows, row + 2)):
            for j in range(max(0, col - 1), min(columns, col + 2)):
                reveal(i, j)
    
    cells_uncovered += 1
    check_game_status()

def check_game_status():
    global cells_uncovered, total_cells, is_game_over
    if cells_uncovered == total_cells - mines:
        is_game_over = True
        status_label.config(text=f"Wygrałeś! {cells_uncovered}/{total_cells} pól odkrytych.")
        disable_all_buttons()

def game_over():
    global is_game_over
    is_game_over = True
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == -1:
                buttons[i][j].config(text="*", relief=tk.SUNKEN, state="disabled", bg="red")
            else:
                buttons[i][j].config(state="disabled")

def reveal_all_mines():
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == -1:
                buttons[i][j].config(text="*", relief=tk.SUNKEN, state="disabled")

def disable_all_buttons():
    for i in range(rows):
        for j in range(columns):
            buttons[i][j].config(state="disabled")

def restart_game():
    global frame, status_label, restart_button, quit_button, is_game_over, cells_uncovered, board, buttons, uncovered_label, flags_placed
    
    # Usunięcie istniejących elementów interfejsu
    frame.destroy()
    status_label.destroy()
    restart_button.destroy()
    quit_button.destroy()
    if uncovered_label:
        uncovered_label.destroy()

    # Resetowanie zmiennych
    is_game_over = False
    cells_uncovered = 0
    flags_placed = 0
    board = [[0 for _ in range(columns)] for _ in range(rows)]
    
    # Usunięcie istniejących przycisków
    for i in range(rows):
        for j in range(columns):
            if buttons[i][j] is not None:
                buttons[i][j].destroy()
    
    # Utworzenie nowych przycisków i odświeżenie interfejsu
    create_game_frame()
    create_widgets()
    place_mines()
    calculate_numbers()

def main():
    global root, rows, columns, mines, total_cells
    root = tk.Tk()
    root.title("Saper")
    rows, columns, mines = 10, 10, 10
    total_cells = rows * columns

    create_game_frame()
    create_widgets()
    place_mines()
    calculate_numbers()

    root.mainloop()

if __name__ == "__main__":
    main()
