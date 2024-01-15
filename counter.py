stra = '''import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snanky")
        self.master.resizable(False, False)
        self.wyniczek = 0
        self.direction = "Right"
        self.paused = False

        # Game constants
        self.Game_Width = 840
        self.Game_Height = 680
        self.Speed = 300
        self.Space_size = 40
        self.Body_Parts = 3
        self.Snake_Color = "#800080"  # Fioletowy
        self.Food_Color = "#FF0000"  # Czerwony
        self.Background_Color = "#000000"  # Czarny

        # Create canvas
        self.canvas = tk.Canvas(
            master,
            bg=self.Background_Color,
            height=self.Game_Height,
            width=self.Game_Width,
            highlightthickness=0,
        )
        self.canvas.pack()

        # Create label for the score
        self.label = tk.Label(
            master, text=f"Wyniczek: {self.wyniczek}", font=("Comic Sans", 30)
        )
        self.label.pack()

        # Create snake and food instances
        self.snake = Snake(self.canvas, self.Space_size, self.Body_Parts, self.Snake_Color)
        self.food = Food(self.canvas, self.Space_size, self.Food_Color)

        # Set up key bindings
        self.master.bind("<Up>", lambda event: self.change_direction("up"))
        self.master.bind("<Down>", lambda event: self.change_direction("down"))
        self.master.bind("<Left>", lambda event: self.change_direction("left"))
        self.master.bind("<Right>", lambda event: self.change_direction("right"))
        self.master.bind("w", lambda event: self.change_direction("up"))
        self.master.bind("a", lambda event: self.change_direction("left"))
        self.master.bind("s", lambda event: self.change_direction("down"))
        self.master.bind("d", lambda event: self.change_direction("right"))
        self.master.bind("<Escape>", lambda event: self.pause())
        self.master.bind("<BackSpace>", lambda event: self.restart())
        self.master.bind("Q", lambda event: self.master.destroy())

        # Start the game loop
        self.next_turn()

    def change_direction(self, new_direction):
        if (
            new_direction == "left" and self.direction != "Right"
            or new_direction == "right" and self.direction != "Left"
            or new_direction == "up" and self.direction != "Down"
            or new_direction == "down" and self.direction != "Up"
        ):
            self.direction = new_direction

    def show_controls(self):
        # Create a new popup screen showing the controls to restart or go back to the menu
        popup_window = tk.Toplevel(self.master)
        popup_window.title("Controls")
        popup_window.geometry("800x600")
        popup_window.resizable(False, False)

        path = r"D:\w2.png"
        img = tk.PhotoImage(file=path)
        new_img = img.subsample(2, 2)
        new_img = new_img.subsample(2, 2)

        image = tk.Label(popup_window, image=new_img)
        image.pack()

        restart_label = tk.Label(
            popup_window, text="Press Backspace to restart", font=("Comic Sans", 14)
        )
        restart_label.pack()

        menu_label = tk.Label(
            popup_window, text="Press Q to go back to the menu", font=("Comic Sans", 14)
        )
        menu_label.pack()

        # Add a button to close the popup
        button = tk.Button(
            popup_window, text="Close", font=("Comic Sans", 14), command=popup_window.destroy
        )
        button.pack(pady=10)

        # Bind the enter key to the close button
        popup_window.bind("<Return>", lambda event: popup_window.destroy())

        popup_window.focus_set()
        popup_window.grab_set()
        popup_window.wait_window()

    def pause(self):
        self.paused = not self.paused

    def restart(self):
        self.wyniczek = 0
        self.label.config(text=f"Wyniczek: {self.wyniczek}")
        self.canvas.delete(tk.ALL)
        self.direction = "Right"
        self.snake.reset()
        self.food.reset()
        self.master.bind("<Escape>", lambda event: self.pause())

    def check_collisions(self):
        return self.snake.check_wall_collision(self.Game_Width, self.Game_Height) or self.snake.check_self_collision()

    def game_over(self, collision_type):
        self.canvas.delete(tk.ALL)

        if collision_type == "wall":
            message = "Ściana!"
        elif collision_type == "self":
            message = "Zjadł siebie!"
        else:
            message = "Przegrana ;("
            messagebox.showinfo("Przegranko ;(", "Dzięki za granie!")

        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            font=("Comic Sans", 80),
            text=message,
            fill="purple",
            tag="gameover",
        )

        self.pause()
        self.master.destroy()

    def next_turn(self):
        if self.paused:
            self.master.after(self.Speed, self.next_turn)
            return

        x, y = self.snake.coordinates[0]

        if self.direction == "Up":
            y -= self.Space_size
        elif self.direction == "Down":
            y += self.Space_size
        elif self.direction == "Left":
            x -= self.Space_size
        elif self.direction == "Right":
            x += self.Space_size

        self.snake.move(x, y)
        collision = self.check_collisions()

        if collision:
            self.game_over(collision)
        else:
            self.master.after(self.Speed, self.next_turn)


class Snake:
    def __init__(self, canvas, space_size, body_parts, color):
        self.coordinates = [(0, 0) for _ in range(body_parts)]
        self.squares = []
        self.canvas = canvas
        self.space_size = space_size
        self.color = color

        for x, y in self.coordinates:
            stomach = canvas.create_oval(
                x, y, x + space_size, y + space_size, fill=color, tag="snake"
            )
            self.squares.append(stomach)

    def move(self, x, y):
        self.coordinates.insert(0, (x, y))
        stomach = self.canvas.create_oval(x, y, x + self.space_size, y + self.space_size, fill=self.color)
        self.squares.insert(0, stomach)

        del self.coordinates[-1]
        self.canvas.delete(self.squares[-1])
        del self.squares[-1]

    def reset(self):
        self.coordinates = [(0, 0) for _ in range(len(self.coordinates))]
        self.squares = []

        for x, y in self.coordinates:
            stomach = self.canvas.create_oval(
                x, y, x + self.space_size, y + self.space_size, fill=self.color, tag="snake"
            )
            self.squares.append(stomach)

    def check_wall_collision(self, game_width, game_height):
        x, y = self.coordinates[0]
        return x < 0 or x >= game_width or y < 0 or y >= game_height

    def check_self_collision(self):
        x, y = self.coordinates[0]
        return any((x == part[0] and y == part[1]) for part in self.coordinates[1:])


class Food:
    def __init__(self, canvas, space_size, color):
        x = random.randint(0, (int)(canvas.winfo_reqwidth() / space_size) - 1) * space_size
        y = random.randint(0, (int)(canvas.winfo_reqheight() / space_size) - 1) * space_size

        self.coordinates = [x, y]
        canvas.create_polygon(
            x + space_size / 2,
            y,
            x + space_size,
            y + space_size / 3,
            x + 3 * space_size / 4,
            y + space_size,
            x + space_size / 4,
            y + space_size,
            x,
            y + space_size / 3,
            fill=color,
            tag="Jedzonko",
        )

    def reset(self):
        x = random.randint(0, (int)(self.canvas.winfo_reqwidth() / self.space_size) - 1) * self.space_size
        y = random.randint(0, (int)(self.canvas.winfo_reqheight() / self.space_size) - 1) * self.space_size

        self.coordinates = [x, y]
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
            fill=self.color,
            tag="Jedzonko",
        )


def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
'''
print(len(stra))
strb = ''' aaa b'''
print(len(strb))