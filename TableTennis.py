import tkinter as tk
import random

# Constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120
BALL_SIZE = 25
PADDLE_SPEED = 5
BALL_SPEED = 5

# Initialize variables
player1_score = 0
player2_score = 0


# Function to update the score and reset the ball position
def update_score(player):
    global player1_score, player2_score
    if player == 1:
        player1_score += 1
    elif player == 2:
        player2_score += 1
    update_score_display()
    reset_ball()


# Function to update the score display
def update_score_display():
    canvas.itemconfig(score_display1, text=f"POINTS: {player1_score}")
    canvas.itemconfig(score_display2, text=f"POINTS: {player2_score}")


# Function to reset the ball position
def reset_ball():
    canvas.coords(ball, WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2,
                  WIDTH / 2 + BALL_SIZE / 2, HEIGHT / 2 + BALL_SIZE / 2)
    global ball_speed_x, ball_speed_y
    ball_speed_x = BALL_SPEED * random.choice([-1, 1])
    ball_speed_y = BALL_SPEED * random.choice([-1, 1])


# Function to update the ball position
def update_ball():
    global ball_speed_x, ball_speed_y
    ball_coords = canvas.coords(ball)
    ball_x = (ball_coords[0] + ball_coords[2]) / 2
    ball_y = (ball_coords[1] + ball_coords[3]) / 2

    # Check collision with paddles
    if (canvas.coords(paddle1)[0] < ball_x < canvas.coords(paddle1)[2]) and (
            canvas.coords(paddle1)[1] < ball_y < canvas.coords(paddle1)[3]):
        ball_speed_x = abs(ball_speed_x)

    if (canvas.coords(paddle2)[0] < ball_x < canvas.coords(paddle2)[2]) and (
            canvas.coords(paddle2)[1] < ball_y < canvas.coords(paddle2)[3]):
        ball_speed_x = -abs(ball_speed_x)

    # Check collision with top and bottom walls
    if ball_coords[1] <= 0 or ball_coords[3] >= HEIGHT:
        ball_speed_y *= -1

    # Check if the ball passed the paddles
    if ball_coords[0] <= 0:
        update_score(2)
    elif ball_coords[2] >= WIDTH:
        update_score(1)

    # Move the ball
    canvas.move(ball, ball_speed_x, ball_speed_y)

    # Schedule the next update
    canvas.after(20, update_ball)


# Function to move the paddles smoothly
def move_paddle_smoothly():
    paddle_speed = PADDLE_SPEED
    canvas.move(paddle1, 0, paddle_speed * direction_paddle1)
    canvas.move(paddle2, 0, paddle_speed * direction_paddle2)
    prevent_paddle_beyond_boundaries()
    canvas.after(10, move_paddle_smoothly)


# Function to prevent paddles from going beyond the game window boundaries
def prevent_paddle_beyond_boundaries():
    paddle1_coords = canvas.coords(paddle1)
    paddle2_coords = canvas.coords(paddle2)

    if paddle1_coords[1] < 0:
        canvas.move(paddle1, 0, -paddle1_coords[1])
    elif paddle1_coords[3] > HEIGHT:
        canvas.move(paddle1, 0, HEIGHT - paddle1_coords[3])

    if paddle2_coords[1] < 0:
        canvas.move(paddle2, 0, -paddle2_coords[1])
    elif paddle2_coords[3] > HEIGHT:
        canvas.move(paddle2, 0, HEIGHT - paddle2_coords[3])


# Function to handle key press events
def on_key_press(event):
    global direction_paddle1, direction_paddle2
    if event.keysym == 'Up':
        direction_paddle2 = -1
    elif event.keysym == 'Down':
        direction_paddle2 = 1
    elif event.keysym == 'w':
        direction_paddle1 = -1
    elif event.keysym == 's':
        direction_paddle1 = 1


# Function to handle key release events
def on_key_release(event):
    global direction_paddle1, direction_paddle2
    if event.keysym in ('Up', 'Down'):
        direction_paddle2 = 0
    elif event.keysym in ('w', 's'):
        direction_paddle1 = 0


# Create the main window
root = tk.Tk()
root.title("Table Tennis Game")

# Create the canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="grey15")
canvas.pack()

# Create the bounding box
line_width = 5  # Adjust this value for the desired line thickness
canvas.create_rectangle(0, 0, WIDTH, HEIGHT, outline="white", width=line_width)

# Create the paddles and ball
paddle1 = canvas.create_rectangle(0, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH,
                                  HEIGHT / 2 + PADDLE_HEIGHT / 2, fill="white")
paddle2 = canvas.create_rectangle(WIDTH - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2,
                                  WIDTH, HEIGHT / 2 + PADDLE_HEIGHT / 2, fill="white")
ball = canvas.create_oval(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2,
                          WIDTH / 2 + BALL_SIZE / 2, HEIGHT / 2 + BALL_SIZE / 2, fill="white")

# Create the dotted line
dot_gap = 10
canvas.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white", dash=(dot_gap, dot_gap))

# Create the score displays
score_display1 = canvas.create_text(WIDTH / 4, 30, text="POINTS: 0", fill="white", font=("Helvetica", 16))
score_display2 = canvas.create_text(3 * WIDTH / 4, 30, text="POINTS: 0", fill="white", font=("Helvetica", 16))

# Initialize ball speed
ball_speed_x = BALL_SPEED * random.choice([-1, 1])
ball_speed_y = BALL_SPEED * random.choice([-1, 1])

# Initialize paddle directions
direction_paddle1 = 0
direction_paddle2 = 0

# Bind key events
canvas.bind_all('<KeyPress>', on_key_press)
canvas.bind_all('<KeyRelease>', on_key_release)

# Start the game loop
update_ball()
move_paddle_smoothly()

# Run the application
root.mainloop()
