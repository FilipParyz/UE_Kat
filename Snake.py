import tkinter as tk
from tkinter import messagebox
import random


class Snake:
    def __init__(self, canvas, space_size, body_parts, snake_color):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []
        self.canvas = canvas
        self.space_size = space_size
        self.snake_color = snake_color
        self.create_snake()

    def create_snake(self):
        for i in range(self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            stomach = self.canvas.create_oval(
                x, y, x + self.space_size, y + self.space_size, fill=self.snake_color, tag="snake"
            )
            self.squares.append(stomach)

class Food:
    def __init__(self, canvas, space_size, food_color):
        x = random.randint(0, (int)(GAME_WIDTH / space_size) - 1) * space_size
        y = random.randint(0, (int)(GAME_HEIGHT / space_size) - 1) * space_size

        self.coordinates = [x, y]
        self.canvas = canvas
        self.space_size = space_size
        self.food_color = food_color
        self.create_food()

    def create_food(self):
        x, y = self.coordinates
        self.canvas.create_polygon(
            x + self.space_size / 2,
            y,
            x + self.space_size,
            y + self.space_size / 3,
            x + 3 * self.space_size / 4,
            y + self.space_size,
            x + self.space_size / 4,
            y + self.space_size,
            x,
            y + self.space_size / 3,
            fill=self.food_color,
            tag="Jedzonko",
        )

class SnakeGame:
    def __init__(self, window):
        self.window = window

        # Zmienne
        self.GAME_WIDTH = 840
        self.GAME_HEIGHT = 680
        self.SPEED = 300
        self.SPACE_SIZE = 40
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = "#800080"
        self.FOOD_COLOR = "#FF0000"
        self.BACKGROUND_COLOR = "#000000"
        self.wyniczek = 0
        self.direction = "Right"
        self.paused = False

        # Canvas
        self.canvas = tk.Canvas(
            window,
            bg=self.BACKGROUND_COLOR,
            height=self.GAME_HEIGHT,
            width=self.GAME_WIDTH,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.window.update()

        # Tworzenie etykiety wyniczek
        self.label = tk.Label(
            window, text="Wyniczek: {0}".format(self.wyniczek), font=("Comic Sans", 30)
        ).pack()

        self.snake = Snake(self.canvas, Space_size, Body_Parts, Snake_Color)
        self.food = Food(self.canvas, Space_size, Food_Color)

        self.initialize_game()
        self.start_game()
        #keybinds
        self.window.bind("<space>", self.toggle_pause)
        self.window.bind("<BackSpace>", self.restart_game)
        self.window.bind("<Escape>", self.quit)
        self.window.bind("<Up>", lambda event: self.change_direction("up"))
        self.window.bind("<Down>", lambda event: self.change_direction("down"))
        self.window.bind("<Left>", lambda event: self.change_direction("left"))
        self.window.bind("<Right>", lambda event: self.change_direction("right"))
        self.window.bind("w", lambda event: self.change_direction("up"))
        self.window.bind("a", lambda event: self.change_direction("left"))
        self.window.bind("s", lambda event: self.change_direction("down"))
        self.window.bind("d", lambda event: self.change_direction("right"))

    def initialize_game(self):
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = int(screen_width / 2 - window_width / 2)
        y = int(screen_height / 2 - window_height / 2)

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    

    def start_game(self):
        self.next_turn()
        self.window.mainloop()

    def change_direction(self, new_direction):
        if new_direction == "left" and self.direction != "Right":
            self.direction = "Left"
        elif new_direction == "right" and self.direction != "Left":
            self.direction = "Right"
        elif new_direction == "up" and self.direction != "Down":
            self.direction = "Up"
        elif new_direction == "down" and self.direction != "Up":
            self.direction = "Down"

    def restart_game(self):
        self.wyniczek = 0
        self.label.config(text="Wyniczek: {0}".format(self.wyniczek))
        self.canvas.delete(tk.ALL)

        self.direction = "Right"

        self.snake.coordinates = []
        self.snake.squares = []
        for i in range(Body_Parts):
            self.snake.coordinates.append([0, 0])

        for x, y in self.snake.coordinates:
            stomach = self.canvas.create_oval(
                x, y, x + Space_size, y + Space_size, fill=Snake_Color, tag="snake"
            )
            self.snake.squares.append(stomach)

        x = random.randint(0, (int)(GAME_WIDTH / Space_size) - 1) * Space_size
        y = random.randint(0, (int)(GAME_HEIGHT / Space_size) - 1) * Space_size
        self.food.coordinates = [x, y]
        self.canvas.create_polygon(
            x + Space_size / 2,
            y,
            x + Space_size,
            y + Space_size / 3,
            x + 3 * Space_size / 4,
            y + Space_size,
            x + Space_size / 4,
            y + Space_size,
            x,
            y + Space_size / 3,
            fill=Food_Color,
            tag="Jedzonko",
        )

        self.window.bind("<Escape>", lambda event: self.toggle_pause())

    def quit(self, event):
        self.root.destroy()
        self.pop_up = tk.Toplevel()
        self.pop_up.title("Snakey")
        self.pop_up.resizable(False, False)
        self.pop_up.geometry("300x100")
        self.pop_up_label = tk.Label(
            self.pop_up, text=f"Do you want to end game with score: {score}?", font=("Comic Sans", 30)
        ).pack()
        self.pop_up_button = tk.Button(self.pop_up, text="Yes", command=self.root.destroy).pack()
        self.pop_up_button = tk.Button(self.pop_up, text="No", command=self.pop_up.destroy).pack()

    def toggle_pause(self):
        self.paused = not self.paused

    def pause_game(self):
        if not self.paused:
            self.paused = True
            self.window.bind("<Escape>", lambda event: self.toggle_pause())
        else:
            self.paused = False
            self.window.unbind("<Escape>")

    def check_collisions(self):
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            self.game_over("Ściana!")

        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                self.game_over("Zjadł siebie!")

    def game_over(self, str1):
        self.canvas.delete(tk.ALL)

        if str1 == "Ściana!":
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                font=("Comic Sans", 80),
                text=f"({str1})",
                fill="purple",
                tag="gameover",
            )
            continue_game = messagebox.askyesno("Przegranko ;(", "Czy chcesz kontynuować?")
            if continue_game:
                self.restart_game()
            else:
                messagebox.showinfo("Przegranko ;(", "Dzięki za granie!")
                self.window.destroy()
        elif str1 == "Zjadł siebie!":
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                font=("Comic Sans", 80),
                text=f"{str1}",
                fill="purple",
                tag="gameover",
            )
            continue_game = messagebox.askyesno("Przegranko ;(", "Czy chcesz kontynuować?")
            if continue_game:
                self.restart_game()
            else:
                messagebox.showinfo("Przegranko ;(", "Dzięki za granie!")
                self.window.destroy()
        else:
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                font=("Comic Sans", 80),
                text=f"Przegrana ;(",
                fill="purple",
                tag="gameover",
            )
            messagebox.showinfo("Przegranko ;(", "Dzięki za granie!")
            self.window.destroy()

    def next_turn(self):
        if self.paused:
            self.window.after(Speed, self.next_turn)
            return

        x, y = self.snake.coordinates[0]

        if self.direction == "Up":
            y -= Space_size
        elif self.direction == "Down":
            y += Space_size
        elif self.direction == "Left":
            x -= Space_size
        elif self.direction == "Right":
            x += Space_size

        self.snake.coordinates.insert(0, (x, y))
        stomach = self.canvas.create_oval(x, y, x + Space_size, y + Space_size, fill=Snake_Color)

        self.snake.squares.insert(0, stomach)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.wyniczek += 1
            self.label.config(text="Wyniczek: {0}".format(self.wyniczek))
            self.canvas.delete("Jedzonko")
            self.food = Food(self.canvas, Space_size, Food_Color)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        self.check_collisions()

        self.window.after(Speed, self.next_turn)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Snanky")
    window.resizable(False, False)

    game = SnakeGame(window)
