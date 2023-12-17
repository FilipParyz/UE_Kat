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
    popup_window = tkinter.Toplevel()
    popup_window.title("Welcome to Snanky!")
    popup_window.geometry("860x710")
    popup_window.resizable(False, False)
    popup_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    
    #adding a label with controls
    label = tkinter.Label(
        popup_window, text="Controls:", font=("Comic Sans", 14)
    )
    label.pack(pady=20)
    label = tkinter.Label(
        popup_window, text="W, A, S, D or Arrow keys to move", font=("Comic Sans", 14)
    )
    label.pack(pady=20)
    label = tkinter.Label(
        popup_window, text="Backspace to restart", font=("Comic Sans", 14)
    )
    label.pack(pady=20)
    label = tkinter.Label(
        popup_window, text="Q to quit", font=("Comic Sans", 14)
    )
    label.pack(pady=20)
    label = tkinter.Label(
        popup_window, text="Esc to pause", font=("Comic Sans", 14)
    )
    label.pack(pady=20)
  

    label = tkinter.Label(
        popup_window, text="Press the button or Enter to start the game!", font=("Comic Sans", 14)
    )
    label.pack(pady=20)
    
    def close_popup(event=None):
        popup_window.destroy()
    
    button = tkinter.Button(
        popup_window, text="Start Game", font=("Comic Sans", 14), command=close_popup
    )
    button.pack(pady=10)
    
    popup_window.bind("<Return>", close_popup)
    
    popup_window.focus_set()
    popup_window.grab_set()
    popup_window.wait_window()   
   
   
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

    #zmiana kierunku znow na prawo
    global direction
    direction = "Right"

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

def Check_Collisions(snakey):
    x, y = snakey.coordinates[0]
    # Sprawdź, czy wąż uderzył w ścianę
    str1= "Ściana"
    if x < 0 or x >= Game_Width:
        str1= "Ściana!"
        show_controls()
        Game_Over(str1)
        return True, str1
    elif y < 0 or y >= Game_Height:
        str1= "Ściana!"
        show_controls()
        Game_Over(str1)
        return True, str1
    # Sprawdź, czy wąż zjadł siebie 
    for body_part in snakey.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            str1= "Zjadł siebie!"
            show_controls()
            Game_Over(str1)
            return True, str1
            break
    return False, str1

def Game_Over(str1):
    # Usuń wszystko z canvas
    canvas.delete(tkinter.ALL)

    # Wyświetl komunikat o przegranej
    if str1 == "Ściana!":
        canvas.create_text(
            canvas.winfo_width() / 2,
            canvas.winfo_height() / 2,
            font=("Comic Sans", 80),
            text=f"{str1}",
            fill="purple",
            tag="gameover",
        )
        pause()
        window.destroy()
        root.destroy()
    
    elif str1 == "Zjadł siebie!":
        canvas.create_text(
            canvas.winfo_width() / 2,
            canvas.winfo_height() / 2,
            font=("Comic Sans", 80),
            text=f"{str1}",
            fill="purple",
            tag="gameover",
        )
        pause()      
        window.destroy()
        root.destroy()
        
    else:
        canvas.create_text(
            canvas.winfo_width() / 2,
            canvas.winfo_height() / 2,
            font=("Comic Sans", 80),
            text=f"Przegrana ;(",
            fill="purple",
            tag="gameover",
        )
        messagebox.showinfo("Przegranko ;(", "Dzięki za granie!")
        window.destroy()
        root.destroy()
    
def Next_Turn(snakey, Jedzonko):    
    global paused
    if paused:
        window.after(Speed, Next_Turn, snakey, Jedzonko)
        return
    str1= ""
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
        Game_Over(str1)
        #
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


def show_controls():
    # Create a new popup screen showing the controls to restart or go back to the menu
    popup_window = tk.Toplevel(window)
    popup_window.title("Controls")
    popup_window.geometry("800x600")
    popup_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    popup_window.resizable(False, False)

    # Add labels for the controls
    
    path = r"D:\w2.png"
    img = tk.PhotoImage(file=path)
    new_img = img.subsample(2, 2)  
    new_img = new_img.subsample(2, 2)

    image = tk.Label(popup_window, image=new_img)
    image.pack()

    restart_label = tk.Label(popup_window, text="Press Backspace to restart", font=("Comic Sans", 14))
    restart_label.pack()
    
    menu_label = tk.Label(popup_window, text="Press Q to go back to the menu", font=("Comic Sans", 14))
    menu_label.pack()

    # Add a button to close the popup
    button = tk.Button(popup_window, text="Close", font=("Comic Sans", 14), command=popup_window.destroy)
    button.pack(pady=10)

    # Bind the enter key to the close button
    popup_window.bind("<Return>", lambda event: popup_window.destroy())

    popup_window.focus_set()
    popup_window.grab_set()
    popup_window.wait_window()
    popup_window.mainloop()


window = tkinter.Tk()
window.title("Snanky")
window.resizable(False, False)

wyniczek = 0
direction = "Right"
paused = False
# Tworzenie etykiety wyniczek
label = tkinter.Label(
    window, text="Wyniczek: {0}".format(wyniczek), font=("Comic Sans", 30)
)
label.pack()
# Tworzenie canvas gry za popupem
canvas = tkinter.Canvas(
    window,
    bg=Background_Color,
    height=Game_Height,
    width=Game_Width,
    highlightthickness=0,
)

canvas.pack()

window.update()
# Ustawienie okna na środku ekranu 
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# Ustawienie okna na środku ekranu za popupem
x = int(screen_width / 2 - window_width / 2)
y = int(screen_height / 2 - window_height / 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

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

