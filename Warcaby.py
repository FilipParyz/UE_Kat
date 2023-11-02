import tkinter as tk
import random

class CatcherGame:
    def __init__(self, canvas):
        self.canvas = canvas
        self.score = 0
        self.catchers = []
        self.game_over = False
        self.catchers_per_second = 1
        self.catchers_speed = 5
        self.catchers_size = 50
        self.catcher_color = "red"
        self.bucket_width = 100
        self.bucket_height = 50
        self.bucket_color = "blue"
        self.bucket = canvas.create_rectangle(canvas.winfo_width() // 2 - self.bucket_width // 2,
                                               canvas.winfo_height() - self.bucket_height,
                                               canvas.winfo_width() // 2 + self.bucket_width // 2,
                                               canvas.winfo_height(),
                                               fill=self.bucket_color)
        self.score_text = canvas.create_text(canvas.winfo_width() // 2, 20, text="Score: 0", font=("Comic Sans", 20))
        canvas.bind("<Motion>", self.move_bucket)
        self.spawn_catchers()

    def spawn_catchers(self):
        if not self.game_over:
            if self.catchers_size <= self.canvas.winfo_width():
                for _ in range(self.catchers_per_second):
                    x = random.randint(0, self.canvas.winfo_width() - self.catchers_size)
                    y = 0
                    catcher = self.canvas.create_oval(x, y, x + self.catchers_size, y + self.catchers_size, fill=self.catcher_color)
                    self.catchers.append(catcher)
            self.canvas.after(1000, self.spawn_catchers)

    def move_catchers(self):
        if not self.game_over:
            for catcher in self.catchers:
                self.canvas.move(catcher, 0, self.catchers_speed)
                if self.canvas.coords(catcher)[1] > self.canvas.winfo_height():
                    self.canvas.delete(catcher)
                    self.catchers.remove(catcher)
                    self.score -= 1
                    self.canvas.itemconfig(self.score_text, text="Score: {}".format(self.score))
            self.canvas.after(50, self.move_catchers)

    def move_bucket(self, event):
        x = event.x - self.bucket_width // 2
        if x < 0:
            x = 0
        elif x > self.canvas.winfo_width() - self.bucket_width:
            x = self.canvas.winfo_width() - self.bucket_width
        self.canvas.coords(self.bucket, x, self.canvas.winfo_height() - self.bucket_height, x + self.bucket_width, self.canvas.winfo_height())

    def check_catchers(self):
        if not self.game_over:
            for catcher in self.catchers:
                catcher_coords = self.canvas.coords(catcher)
                bucket_coords = self.canvas.coords(self.bucket)
                if catcher_coords[3] >= bucket_coords[1] and catcher_coords[0] >= bucket_coords[0] and catcher_coords[2] <= bucket_coords[2]:
                    self.canvas.delete(catcher)
                    self.catchers.remove(catcher)
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text="Score: {}".format(self.score))
            self.canvas.after(50, self.check_catchers)

    def start_game(self):
        self.spawn_catchers()
        self.move_catchers()
        self.check_catchers()
        self.canvas.after(10000, self.end_game)  # end game after 100 seconds

    def end_game(self):
        self.game_over = True
        self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, text="Game Over!", font=("Comic Sans", 30))
        self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2 + 30, text="Score: {}".format(self.score), font=("Comic Sans", 30))
# Create the main window and canvas widget
root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Start the game
game = CatcherGame(canvas)
game.start_game()

# Start the main event loop
root.mainloop()
