# to do: dodać przyspieszanie piłeczki, dodać granice okna, żeby paletka nie wychodziła. + zmienić ruch paletki?

import tkinter as tk
import random

class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong Game")
        self.root.geometry("600x400")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()

        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="white")
        self.paddle = self.canvas.create_rectangle(250, 380, 350, 400, fill="white")

        self.ball_speed = [random.choice([-2, 2]), -2]
        self.paddle_speed = 0

        self.score = 0
        self.score_label = self.canvas.create_text(
            50, 20, text=f"Score: {self.score}", font=("Helvetica", 12), fill="white"
        )

        self.misses = 0
        self.max_misses = 3

        self.canvas.bind("<Left>", self.move_paddle_left)
        self.canvas.bind("<Right>", self.move_paddle_right)
        self.canvas.focus_set()

        self.game_loop()

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_speed[0], self.ball_speed[1])

        ball_pos = self.canvas.coords(self.ball)

        if ball_pos[0] <= 0 or ball_pos[2] >= 600:
            self.ball_speed[0] *= -1

        if ball_pos[1] <= 0:
            self.ball_speed[1] *= -1

        if (
            ball_pos[3] >= 380
            and ball_pos[2] >= self.canvas.coords(self.paddle)[0]
            and ball_pos[0] <= self.canvas.coords(self.paddle)[2]
        ):
            self.ball_speed[1] *= -1
            self.score += 1
            self.update_score()

        if ball_pos[3] >= 400:
            self.misses += 1
            if self.misses >= self.max_misses:
                self.game_over()

    def move_paddle_left(self, event):
        paddle_left = self.canvas.coords(self.paddle)[0]
        if paddle_left > 0:
            self.paddle_speed = -3
            self.canvas.move(self.paddle, self.paddle_speed, 0)

    def move_paddle_right(self, event):
        paddle_right = self.canvas.coords(self.paddle)[2]
        if paddle_right < 600:
            self.paddle_speed = 3
            self.canvas.move(self.paddle, self.paddle_speed, 0)

    def game_loop(self):
        self.move_ball()
        self.canvas.move(self.paddle, self.paddle_speed, 0)

        self.root.after(10, self.game_loop)

    def update_score(self):
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

    def game_over(self):
        self.canvas.create_text(
            300, 200, text="Game Over", font=("Helvetica", 20), fill="white"
        )
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()
