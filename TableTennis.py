import tkinter as tk
import random

class TableTennisGame:
    def __init__(self, root, width, height):
        self.root = root
        self.root.title("Table Tennis Game")

        self.WIDTH = width
        self.HEIGHT = height
        self.PADDLE_WIDTH = 20
        self.PADDLE_HEIGHT = 120
        self.BALL_SIZE = 25
        self.PADDLE_SPEED = 5
        self.BALL_SPEED = 5

        self.player1_score = 0
        self.player2_score = 0

        self.direction_paddle1 = 0
        self.direction_paddle2 = 0

        self.create_widgets()
        self.initialize_game()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT, bg="grey15")
        self.canvas.pack()

        line_width = 5
        self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, outline="white", width=line_width)

        self.paddle1 = self.canvas.create_rectangle(0, self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
                                                   self.PADDLE_WIDTH, self.HEIGHT / 2 + self.PADDLE_HEIGHT / 2,
                                                   fill="white")
        self.paddle2 = self.canvas.create_rectangle(self.WIDTH - self.PADDLE_WIDTH,
                                                   self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
                                                   self.WIDTH, self.HEIGHT / 2 + self.PADDLE_HEIGHT / 2,
                                                   fill="white")
        self.ball = self.canvas.create_oval(self.WIDTH / 2 - self.BALL_SIZE / 2,
                                            self.HEIGHT / 2 - self.BALL_SIZE / 2,
                                            self.WIDTH / 2 + self.BALL_SIZE / 2,
                                            self.HEIGHT / 2 + self.BALL_SIZE / 2, fill="white")

        dot_gap = 10
        self.canvas.create_line(self.WIDTH / 2, 0, self.WIDTH / 2, self.HEIGHT, fill="white", dash=(dot_gap, dot_gap))

        self.score_display1 = self.canvas.create_text(self.WIDTH / 4, 30, text="POINTS: 0", fill="white",
                                                      font=("Helvetica", 16))
        self.score_display2 = self.canvas.create_text(3 * self.WIDTH / 4, 30, text="POINTS: 0", fill="white",
                                                      font=("Helvetica", 16))

    def initialize_game(self):
        self.ball_speed_x = self.BALL_SPEED * random.choice([-1, 1])
        self.ball_speed_y = self.BALL_SPEED * random.choice([-1, 1])

        self.canvas.bind_all('<KeyPress>', self.on_key_press)
        self.canvas.bind_all('<KeyRelease>', self.on_key_release)

        self.move_paddle_smoothly()
        self.center_window()

        self.update_ball()

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

        self.check_collision_with_paddles(ball_x, ball_y)
        self.check_collision_with_walls(ball_coords)
        self.check_goal(ball_coords)

        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        self.canvas.after(20, self.update_ball)

    def check_collision_with_paddles(self, ball_x, ball_y):
        paddle1_coords = self.canvas.coords(self.paddle1)
        paddle2_coords = self.canvas.coords(self.paddle2)

        if (paddle1_coords[0] < ball_x < paddle1_coords[2]) and (paddle1_coords[1] < ball_y < paddle1_coords[3]):
            self.ball_speed_x = abs(self.ball_speed_x)

        if (paddle2_coords[0] < ball_x < paddle2_coords[2]) and (paddle2_coords[1] < ball_y < paddle2_coords[3]):
            self.ball_speed_x = -abs(self.ball_speed_x)

    def check_collision_with_walls(self, ball_coords):
        if ball_coords[1] <= 0 or ball_coords[3] >= self.HEIGHT:
            self.ball_speed_y *= -1

    def check_goal(self, ball_coords):
        if ball_coords[0] <= 0:
            self.update_score(2)
        elif ball_coords[2] >= self.WIDTH:
            self.update_score(1)

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

    def on_key_press(self, event):
        if event.keysym == 'Up':
            self.direction_paddle2 = -1
        elif event.keysym == 'Down':
            self.direction_paddle2 = 1
        elif event.keysym == 'w':
            self.direction_paddle1 = -1
        elif event.keysym == 's':
            self.direction_paddle1 = 1

    def on_key_release(self, event):
        if event.keysym in ('Up', 'Down'):
            self.direction_paddle2 = 0
        elif event.keysym in ('w', 's'):
            self.direction_paddle1 = 0

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (self.WIDTH / 2)
        y = (screen_height / 2) - (self.HEIGHT / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.WIDTH, self.HEIGHT, x, y))


if __name__ == "__main__":
    root = tk.Tk()
    game = TableTennisGame(root, 800, 600)
    root.mainloop()
