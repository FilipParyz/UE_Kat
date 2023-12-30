import tkinter as tk
from functools import partial
try:
    import TableTennis
    import Snake
    import Saper
    import Checkers
except ModuleNotFoundError:
    pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gamehub")
        window_width = 1200
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.configure(bg="black")
        self.resizable(False, False)
        self.create_widgets()
        self.subwindows = []

    def close_subwindow(self, window):
        window.destroy()
        self.subwindows.remove(window)
        self.deiconify()
        self.focus()

    def create_widgets(self):
        self.label = tk.Label(self, text="Gamehub", font=("Arial", 24), bg="black", fg="white")
        self.label.pack(padx=10, pady=10)

        self.button = tk.Button(self, text="Play", font=("Arial", 22), bg="black", fg="white", command=self.play)
        self.button.pack(padx=10, pady=10)

        self.button = tk.Button(self, text="Leaderboard", font=("Arial", 22), bg="black", fg="white", command=self.leaderboard)
        self.button.pack(padx=10, pady=10)

        self.button = tk.Button(self, text="Achievements", font=("Arial", 22), bg="black", fg="white", command=self.achievements)
        self.button.pack(padx=10, pady=10)

        self.button = tk.Button(self, text="Credits", font=("Arial", 22), bg="black", fg="white", command=self.credits)
        self.button.pack(padx=10, pady=10)

        self.button = tk.Button(self, text="Quit", font=("Arial", 22), bg="black", fg="white", command=self.quit)
        self.button.pack(padx=10, pady=10)
    
    def play(self):
        self.withdraw()
        self.games_window = tk.Toplevel(self)
        self.subwindows.append(self.games_window)
        self.games_window.title("Games")
        self.games_window.geometry(self.geometry())
        self.games_window.configure(bg=self.cget("bg"))
        self.games_window.resizable(False, False)

        self.button = tk.Button(self.games_window, text="Table Tennis", font=("Arial", 24), bg="black", fg="white", command=partial(TableTennis.main))
        self.button.pack(padx=10, pady=10)

        self.button = tk.Button(self.games_window, text="Snake", font=("Arial", 24), bg="black", fg="white", command=partial(Snake.main))
        self.button.pack(padx=10, pady=10)

        # self.button = tk.Button(self.games_window, text="Saper", bg="black", fg="white", command=partial(Saper.main))
        # self.button.pack(padx=10, pady=10)

        # self.button = tk.Button(self.games_window, text="Checkers", bg="black", fg="white", command=partial(Checkers.main))
        # self.button.pack(padx=10, pady=10)

        button = tk.Button(self.games_window, text="Back", font=("Arial", 24), bg="white", fg="black", command=partial(self.close_subwindow, self.games_window))
        button.pack(padx=10, pady=20)
        
        self.games_window.focus()
        self.games_window.mainloop()

    
    def leaderboard(self):
        self.withdraw()
        self.leaderboard_window = tk.Toplevel(self)
        self.subwindows.append(self.leaderboard_window)
        self.leaderboard_window.title("Leaderboard")
        self.leaderboard_window.geometry(self.geometry())
        self.leaderboard_window.configure(bg=self.cget("bg"))
        self.leaderboard_window.resizable(False, False)

        with open("leaderboard.txt", "r") as file:
            leaderboard_data = file.read()

        label = tk.Label(self.leaderboard_window, text=leaderboard_data, font=("Arial", 22), fg="white", bg="black")
        label.pack()

        button = tk.Button(self.leaderboard_window, text="Back", font=("Arial", 24), bg="white", fg="black", command=partial(self.close_subwindow, self.leaderboard_window))
        button.pack(padx=10, pady=20)

        self.leaderboard_window.focus()
        self.leaderboard_window.mainloop()

    def achievements(self):
        self.withdraw()
        self.achievements_window = tk.Toplevel(self)
        self.subwindows.append(self.achievements_window)
        self.achievements_window.title("Achievements")
        self.achievements_window.geometry(self.geometry())
        self.achievements_window.configure(bg=self.cget("bg"))
        self.achievements_window.resizable(False, False)
        
        with open("achievements.txt", "r") as file:
            achievements_contents = file.read()

        label = tk.Label(self.achievements_window, text=achievements_contents, font=("Arial", 22), fg="white", bg="black")
        label.pack()

        button = tk.Button(self.achievements_window, text="Back", font=("Arial", 24), bg="white", fg="black", command=partial(self.close_subwindow, self.achievements_window))
        button.pack(padx=10, pady=20)

        self.achievements_window.focus()
        self.achievements_window.mainloop()
    
    def credits(self):
        self.withdraw()
        self.credits_window = tk.Toplevel(self)
        self.subwindows.append(self.credits_window)
        self.credits_window.title("Credits")
        self.credits_window.geometry(self.geometry())
        self.credits_window.configure(bg=self.cget("bg"))
        self.credits_window.resizable(False, False)
        
        with open("credits.txt", "r") as file:
            credits_contents = file.read()

        label = tk.Label(self.credits_window, text=credits_contents, font=("Arial", 22), fg="white", bg="black")
        label.pack()

        button = tk.Button(self.credits_window, text="Back", font=("Arial", 24), bg="white", fg="black", command=partial(self.close_subwindow, self.credits_window))
        button.pack(padx=10, pady=20)

        self.credits_window.focus()
        self.credits_window.mainloop()

    def quit(self):
        self.destroy()

if __name__ == '__main__':
    app = App()
    app.mainloop()