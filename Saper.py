import tkinter as tk
import random

#dodaæ flagi do saperka
class SaperGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Saper")
        self.rows = 10
        self.columns = 10
        self.mines = 10
        self.is_game_over = False
        self.total_cells = self.rows * self.columns
        self.cells_uncovered = 0
        self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.buttons = [[None for _ in range(self.columns)] for _ in range(self.rows)]

        self.create_widgets()
        self.place_mines()
        self.calculate_numbers()

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.uncovered_label = tk.Label(self.master, text="Odkryte pola: 0", pady=10)
        self.uncovered_label.pack()

        for i in range(self.rows):
            for j in range(self.columns):
                self.buttons[i][j] = tk.Button(self.frame, width=2, command=lambda i=i, j=j: self.click(i, j), fg="white")
                self.buttons[i][j].grid(row=i, column=j)
                self.buttons[i][j].config(disabledforeground="white")
                
        self.status_label = tk.Label(self.master, text="", pady=10)
        self.status_label.pack()
        
        self.restart_button = tk.Button(self.master, text="Zagraj ponownie", command=self.restart_game)
        self.restart_button.pack()
        
        self.quit_button = tk.Button(self.master, text="Zakoncz gre", command=self.master.quit)
        self.quit_button.pack()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.columns - 1)
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1

    def calculate_numbers(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != -1:
                    self.board[i][j] = self.count_adjacent_mines(i, j)

    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.columns, col + 2)):
                if self.board[i][j] == -1:
                    count += 1
        return count

    def click(self, row, col):
        if self.is_game_over or self.buttons[row][col]["state"] == "disabled":
            return

        if self.board[row][col] == -1:
            self.game_over()
            self.reveal_all_mines()
        else:
            self.reveal(row, col)

        self.uncovered_label.config(text=f"Odkryte pola: {self.cells_uncovered}")

    def reveal(self, row, col):
        if self.buttons[row][col]["state"] == "disabled":
            return

        self.buttons[row][col].config(state="disabled", bg="gray", fg="white", font=('Arial', 10, 'bold'))
        if self.board[row][col] > 0:
            self.buttons[row][col].config(text=str(self.board[row][col]))
        else:
            for i in range(max(0, row - 1), min(self.rows, row + 2)):
                for j in range(max(0, col - 1), min(self.columns, col + 2)):
                    self.reveal(i, j)
        
        self.cells_uncovered += 1
        self.check_game_status()

    def check_game_status(self):
        if self.cells_uncovered == self.total_cells - self.mines:
            self.is_game_over = True
            self.status_label.config(text=f"Wygrales! {self.cells_uncovered}/{self.total_cells} pol odkrytych.")
            self.disable_all_buttons()

    def game_over(self):
        self.is_game_over = True
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == -1:
                    self.buttons[i][j].config(text="*", relief=tk.SUNKEN, state="disabled", bg="red")
                else:
                    self.buttons[i][j].config(state="disabled")

    def reveal_all_mines(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == -1:
                    self.buttons[i][j].config(text="*", relief=tk.SUNKEN, state="disabled")

    def disable_all_buttons(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.buttons[i][j].config(state="disabled")

    def restart_game(self):
        self.frame.destroy()
        self.status_label.destroy()
        self.restart_button.destroy()
        self.quit_button.destroy()
        self.is_game_over = False
        self.cells_uncovered = 0
        self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.buttons = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.create_widgets()
        self.place_mines()
        self.calculate_numbers()

def main():
    root = tk.Tk()
    game = SaperGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()