import tkinter as tk
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakey")
        self.root.resizable(False, False)
        self.paused = False
        self.direction = "Right"
        self.score = 0

        # Constants
        self.GAME_WIDTH = 840
        self.GAME_HEIGHT = 680
        self.SPEED = 300
        self.SPACE_SIZE = 40
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = "#800080"
        self.FOOD_COLOR = "#FF0000"
        self.BACKGROUND_COLOR = "#000000"

        # Canvas
        self.canvas = tk.Canvas(
            root,
            bg=self.BACKGROUND_COLOR,
            height=self.GAME_HEIGHT,
            width=self.GAME_WIDTH,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.root.update()

        # Score
        self.label = tk.Label(
            root, text=f"Score: {self.score}", font=("Comic Sans", 30)
        )
        self.label.pack(side="bottom", fill="both", expand="yes")

        # Snake
        self.snake = Snake(
            self.canvas, self.SPACE_SIZE, self.BODY_PARTS, self.SNAKE_COLOR
        )
        # Food
        self.food = Food(self.canvas, self.SPACE_SIZE, self.FOOD_COLOR)
        # Keybinds
        self.root.bind("<Left>", lambda event: self.snake.move("left"))
        self.root.bind("<Right>", lambda event: self.snake.move("right"))
        self.root.bind("<Up>", lambda event: self.snake.move("up"))
        self.root.bind("<Down>", lambda event: self.snake.move("down"))

        self.root.bind("<space>", self.toggle_pause)
        self.root.bind("<BackSpace>", self.restart)
        self.root.bind("<Escape>", self.quit)
        self.root.after(self.SPEED, self.perform_actions)

    def toggle_pause(self, event):
        self.paused = not self.paused

    def restart(self, event):
        self.canvas.delete(tk.ALL)
        self.snake.reset()
        self.food.generate_food()

    def quit(self, event):
        self.root.destroy()
        self.pop_up = tk.Toplevel()
        self.pop_up.title("Snakey")
        self.pop_up.resizable(False, False)
        self.pop_up.geometry("300x100")
        self.pop_up_label = tk.Label(
            self.pop_up, text=f"Do you want to end game with score: {score}?", font=("Comic Sans", 30)
        )
        self.pop_up_label.pack()
        self.pop_up_button = tk.Button(self.pop_up, text="Yes", command=self.root.destroy)
        self.pop_up_button.pack()
        self.pop_up_button = tk.Button(self.pop_up, text="No", command=self.pop_up.destroy)
        self.pop_up_button.pack()

    def perform_actions(self):
        if not self.paused:
            self.snake.move_snake()
            self.check_collision()
            self.root.after(self.SPEED, self.perform_actions)

    def check_collision(self):
        head_coords = self.snake.get_head_coords()
        food_coords = self.food.get_food_coords()
        if head_coords == food_coords:
            self.snake.add_body_part()
            self.food.generate_food()
            self.score += 1
            self.label.config(text=f"Score: {self.score}")

        
        self.root.mainloop()        
class Snake:
        #change movement
        def move(self, direction):
            self.direction = direction
            self.move_snake()