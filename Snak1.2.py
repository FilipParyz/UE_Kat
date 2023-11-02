# Autor: Mariusz Borczuk
# Data: 2023-10-24
# Opis: Gra Snake w Pythonie

import tkinter
import random
import tkinter as tk
from tkinter import messagebox

# Stałe gry
Game_Width = 840
Game_Height = 680
Speed = 300
Space_size = 40
Body_Parts = 3
Snake_Color = "#800080"  # Fioletowy
Food_Color = "#FF0000"  # Czerwony
Background_Color = "#000000"  # Czarny


class Snanky:
    # Inicializacja wężyka
    def __init__(self):
        self.body_size = Body_Parts
        self.coordinates = []
        self.squares = []

        # Stworzenie wężyka w rogu ekranu
        for i in range(0, Body_Parts):
            self.coordinates.append([0, 0])

        # Tworzenie ciała wężyka
        for x, y in self.coordinates:
            stomach = canvas.create_oval(
                x, y, x + Space_size, y + Space_size, fill=Snake_Color, tag="snake"
            )
            self.squares.append(stomach)


class The_Food:
    # Inicializacja jedzenia
    def __init__(self):
        x = random.randint(0, (int)(Game_Width / Space_size) - 1) * Space_size
        y = random.randint(0, (int)(Game_Height / Space_size) - 1) * Space_size

        self.coordinates = [x, y]
        # Tworzenie jedzenia japko
        canvas.create_polygon(
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

def popup():
    response = messagebox.askyesno("Game Controls", "Up: Up Arrow Key or W\nDown: Down Arrow Key or S\nLeft: Left Arrow Key or A\nRight: Right Arrow Key or D\nPause: Escape\nRestart: Backspace\nQuit: Q")
    if response == 1:
        root.destroy()
    else:
        root.destroy()
def Next_Turn(snakey, Jedzonko):
    """
    Przesuwa węża na następny kafelek na podstawie bieżącego kierunku i aktualizuje canvas.

    Parametry:
    Wężyk (Snakey): Obiekt węża, który ma zostać przesunięty.
    Jedzonko (Jedzenie): Obiekt jedzenia, które wąż może zjeść.

    Zwraca:
    """
    global paused
    if paused:
        window.after(Speed, Next_Turn, snakey, Jedzonko)
        return

    x, y = snakey.coordinates[0]
    # Określ kierunek węża
    if direction == "Up":
        y -= Space_size
    elif direction == "Down":
        y += Space_size
    elif direction == "Left":
        x -= Space_size
    elif direction == "Right":
        x += Space_size
    # Przenieś węża do nowej lokalizacji
    snakey.coordinates.insert(0, (x, y))
    # Stworzenie nowego kwadratu(brzusia) węża
    stomach = canvas.create_oval(x, y, x + Space_size, y + Space_size, fill=Snake_Color)

    snakey.squares.insert(0, stomach)
    # Sprawdź, czy wąż zjadł jedzenie
    if x == Jedzonko.coordinates[0] and y == Jedzonko.coordinates[1]:
        global wyniczek
        wyniczek += 1
        label.config(text="Wyniczek: {0}".format(wyniczek))
        canvas.delete("Jedzonko")
        Jedzonko = The_Food()
    else:
        # Usuń ostatni element z węża
        del snakey.coordinates[-1]
        canvas.delete(snakey.squares[-1])
        del snakey.squares[-1]
        # Sprawdź, czy wąż zjadł siebie
    if Check_Collisions(snakey) == True:
        Game_Over()
    else:
        # Wywołaj tę funkcję ponownie po określonym czasie(Speed gry)
        window.after(Speed, Next_Turn, snakey, Jedzonko)


def Change_Direction(New_Direction):
    global direction
    # Nie pozwól wężowi iść w przeciwnym kierunku niż obecny i skręć w nowym kierunku
    if New_Direction == "left" and direction != "Right":
        direction = "Left"
    elif New_Direction == "right" and direction != "Left":
        direction = "Right"
    elif New_Direction == "up" and direction != "Down":
        direction = "Up"
    elif New_Direction == "down" and direction != "Up":
        direction = "Down"


def Check_Collisions(snakey):
    x, y = snakey.coordinates[0]
    # Sprawdź, czy wąż uderzył w ścianę
    if x < 0 or x >= Game_Width:
        print("You hit the edge of the screen!")
        return True
    elif y < 0 or y >= Game_Height:
        print("You hit the edge of the screen!")
        return True
    # Sprawdź, czy wąż zjadł siebie
    for body_part in snakey.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("You ate yourself!")
            return True
    return False


def Game_Over():
    # Usuń wszystko z canvas
    canvas.delete(tkinter.ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("Comic Sans", 80),
        text="Przegrana ;( ",
        fill="purple",
        tag="gameover",
    )


def toggle_pause():
    global paused
    paused = not paused


def pause():
    global paused
    if not paused:
        paused = True
        window.bind("<Escape>", lambda event: toggle_pause())
    else:
        paused = False
        window.unbind("<Escape>")


def restart():
    global wyniczek
    wyniczek = 0
    label.config(text="Wyniczek: {0}".format(wyniczek))
    canvas.delete(tkinter.ALL)

    # przywracanie weza do pozycji początkowej
    snake.coordinates = []
    snake.squares = []
    for i in range(0, Body_Parts):
        snake.coordinates.append([0, 0])
    for x, y in snake.coordinates:
        stomach = canvas.create_oval(
            x, y, x + Space_size, y + Space_size, fill=Snake_Color, tag="snake"
        )
        snake.squares.append(stomach)
    # przywracanie jedzenia do pozycji początkowej
    x = random.randint(0, (int)(Game_Width / Space_size) - 1) * Space_size
    y = random.randint(0, (int)(Game_Height / Space_size) - 1) * Space_size
    Jedzonko.coordinates = [x, y]
    canvas.create_polygon(
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
    window.bind("<Escape>", lambda event: toggle_pause())


window = tkinter.Tk()
window.title("Snanky")
window.resizable(False, False)

wyniczek = 0
direction = "Right"
paused = False
# Tworzenie etykiety wyniczek
label = tkinter.Label(
    window, text="Wyniczek: {0}".format(wyniczek), font=("Orbitron", 30)
)
label.pack()
# Tworzenie canvas
canvas = tkinter.Canvas(
    window, bg=Background_Color, height=Game_Height, width=Game_Width
)
canvas.pack()

window.update()
# Ustawienie okna na środku ekranu
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# Ustawienie okna na środku ekranu
x = int(screen_width / 2 - window_width / 2)
y = int(screen_height / 2 - window_height / 2)

# Dodanie obsługi pauzy
window.bind("Q", lambda event: window.destroy())
window.bind("<Up>", lambda event: Change_Direction(("up")))
window.bind("<Down>", lambda event: Change_Direction(("down")))
window.bind("<Left>", lambda event: Change_Direction(("left")))
window.bind("<Right>", lambda event: Change_Direction(("right")))
window.bind("w", lambda event: Change_Direction(("up")))
window.bind("a", lambda event: Change_Direction(("left")))
window.bind("s", lambda event: Change_Direction(("down")))
window.bind("d", lambda event: Change_Direction(("right")))
window.bind("<Escape>", lambda event: pause())
window.bind("<BackSpace>", lambda event: restart())
window.bind("Q", lambda event: window.destroy())

root = tk.Tk()
root.withdraw()

snake = Snanky()
Jedzonko = The_Food()
popup()

Next_Turn(snake, Jedzonko)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.mainloop()
# Uruchomienie okna
window.mainloop()

#creating the  pop up window before the game starts with game controls and after its starts with the game






