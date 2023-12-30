import tkinter as tk
import random

class TableTennisGame:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.PADDLE_WIDTH = 20
        self.PADDLE_HEIGHT = 120
        self.BALL_SIZE = 25
        self.PADDLE_SPEED = 5
        self.BALL_SPEED = 5

        self.player1_score = 0
        self.player2_score = 0

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()

        self.paddle1 = self.canvas.create_rectangle(50, self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
                                                    50 + self.PADDLE_WIDTH, self.HEIGHT / 2 + self.PADDLE_HEIGHT / 2,
                                                    fill="white")
        self.paddle2 = self.canvas.create_rectangle(self.WIDTH - 50 - self.PADDLE_WIDTH,
                                                    self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
                                                    self.WIDTH - 50, self.HEIGHT / 2 + self.PADDLE_HEIGHT / 2,
                                                    fill="white")
        self.ball = self.canvas.create_oval(self.WIDTH / 2 - self.BALL_SIZE / 2, self.HEIGHT / 2 - self.BALL_SIZE / 2,
                                            self.WIDTH / 2 + self.BALL_SIZE / 2, self.HEIGHT / 2 + self.BALL_SIZE / 2,
                                            fill="white")

        self.ball_speed_x = self.BALL_SPEED * random.choice([-1, 1])
        self.ball_speed_y = self.BALL_SPEED * random.choice([-1, 1])

        self.score_display1 = self.canvas.create_text(100, 50, text=f"POINTS: {self.player1_score}", fill="white",
                                                      font=("Arial", 20))
        self.score_display2 = self.canvas.create_text(self.WIDTH - 100, 50, text=f"POINTS: {self.player2_score}",
                                                      fill="white", font=("Arial", 20))

        self.direction_paddle1 = 0
        self.direction_paddle2 = 0

        self.canvas.bind_all("<KeyPress-w>", self.move_paddle1_up)
        self.canvas.bind_all("<KeyPress-s>", self.move_paddle1_down)
        self.canvas.bind_all("<KeyPress-Up>", self.move_paddle2_up)
        self.canvas.bind_all("<KeyPress-Down>", self.move_paddle2_down)
        self.canvas.bind_all("<KeyRelease-w>", self.stop_paddle1)
        self.canvas.bind_all("<KeyRelease-s>", self.stop_paddle1)
        self.canvas.bind_all("<KeyRelease-Up>", self.stop_paddle2)
        self.canvas.bind_all("<KeyRelease-Down>", self.stop_paddle2)

        self.move_paddle_smoothly()
        self.update_ball()

    def move_paddle1_up(self, event):
        self.direction_paddle1 = -1

    def move_paddle1_down(self, event):
        self.direction_paddle1 = 1

    def move_paddle2_up(self, event):
        self.direction_paddle2 = -1

    def move_paddle2_down(self, event):
        self.direction_paddle2 = 1

    def stop_paddle1(self, event):
        self.direction_paddle1 = 0

    def stop_paddle2(self, event):
        self.direction_paddle2 = 0

    def update_score(self, player):
        if player == 1:
            self.player1_score += 1
        elif player == 2:
            self.player2_score += 1
        self.update_score_display()
        self.reset_ball()

    def update_score_display(self):
        self.canvas.itemconfig(self.score_display1, text=f"POINTS: {self.player1_score}")
        self.canvas.itemconfig(self.score_display2, text=f"POINTS: {self.player2_score}")

    def reset_ball(self):
        self.canvas.coords(self.ball, self.WIDTH / 2 - self.BALL_SIZE / 2, self.HEIGHT / 2 - self.BALL_SIZE / 2,
                           self.WIDTH / 2 + self.BALL_SIZE / 2, self.HEIGHT / 2 + self.BALL_SIZE / 2)
        self.ball_speed_x = self.BALL_SPEED * random.choice([-1, 1])
        self.ball_speed_y = self.BALL_SPEED * random.choice([-1, 1])

    def update_ball(self):
        ball_coords = self.canvas.coords(self.ball)
        ball_x = (ball_coords[0] + ball_coords[2]) / 2
        ball_y = (ball_coords[1] + ball_coords[3]) / 2

        if (self.canvas.coords(self.paddle1)[0] < ball_x < self.canvas.coords(self.paddle1)[2]) and (
                self.canvas.coords(self.paddle1)[1] < ball_y < self.canvas.coords(self.paddle1)[3]):
            self.ball_speed_x = abs(self.ball_speed_x)

        if (self.canvas.coords(self.paddle2)[0] < ball_x < self.canvas.coords(self.paddle2)[2]) and (
                self.canvas.coords(self.paddle2)[1] < ball_y < self.canvas.coords(self.paddle2)[3]):
            self.ball_speed_x = -abs(self.ball_speed_x)

        if ball_coords[1] <= 0 or ball_coords[3] >= self.HEIGHT:
            self.ball_speed_y *= -1

        if ball_coords[0] <= 0:
            self.update_score(2)
        elif ball_coords[2] >= self.WIDTH:
            self.update_score(1)

        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        self.canvas.after(20, self.update_ball)

    def move_paddle_smoothly(self):
        paddle_speed = self.PADDLE_SPEED
        self.canvas.move(self.paddle1, 0, paddle_speed * self.direction_paddle1)
        self.canvas.move(self.paddle2, 0, paddle_speed * self.direction_paddle2)
        self.prevent_paddle_beyond_boundaries()
        self.canvas.after(10, self.move_paddle_smoothly)

    def prevent_paddle_beyond_boundaries(self):
        paddle1_coords = self.canvas.coords(self.paddle1)
        paddle2_coords = self.canvas.coords(self.paddle2)

        if paddle1_coords[1] < 0:
            self.canvas.move(self.paddle1, 0, -paddle1_coords[1])
        elif paddle1_coords[3] > self.HEIGHT:
            self.canvas.move(self.paddle1, 0, self.HEIGHT - paddle1_coords[3])

        if paddle2_coords[1] < 0:
            self.canvas.move(self.paddle2, 0, -paddle2_coords[1])
        elif paddle2_coords[3] > self.HEIGHT:
            self.canvas.move(self.paddle2, 0, self.HEIGHT - paddle2_coords[3])

    def start_game(self):
        self.root.mainloop()

def main():
    game = TableTennisGame()
    game.start_game()

if __name__ == '__main__':
    main()