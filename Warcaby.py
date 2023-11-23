import tkinter as tk

class Warcaby:
    def __init__(self, root):
        self.root = root
        self.root.title("Warcaby")
        self.canvas = tk.Canvas(root, width=450, height=450, bg='white')
        self.canvas.pack()
        self.plansza = [[' ']*8 for _ in range(8)]
        self.aktualny_gracz = 'O'
        self.wybrany_pionek = None
        self.utworz_plansze()
        self.ustaw_pionki()

        # Dodajemy obsługę zdarzeń myszki
        self.canvas.bind('<Button-1>', self.kliknieto_pole)

    def utworz_plansze(self):
        # Dodajemy oznaczenia nad planszą (litery A-H)
        for j in range(8):
            self.canvas.create_text((j+0.5)*50, 15, text=chr(ord('A') + j), fill='black', font=('Arial', 12, 'bold'))

        # Dodajemy oznaczenia obok planszy (cyfry 8-1)
        for i in range(8):
            self.canvas.create_text(15, (i+0.5)*50, text=str(8 - i), fill='black', font=('Arial', 12, 'bold'))

        for i in range(8):
            for j in range(8):
                kolor = 'white' if (i+j) % 2 == 0 else 'black'
                self.canvas.create_rectangle(j*50, i*50, (j+1)*50, (i+1)*50, fill=kolor)

        # Dodajemy oznaczenia pod planszą (litery A-H)
        for j in range(8):
            self.canvas.create_text((j+0.5)*50, 435, text=chr(ord('A') + j), fill='black', font=('Arial', 12, 'bold'))

        # Dodajemy oznaczenia obok planszy (cyfry 8-1)
        for i in range(8):
            self.canvas.create_text(435, (i+0.5)*50, text=str(8 - i), fill='black', font=('Arial', 12, 'bold'))

    def ustaw_pionki(self):
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 1 and i < 3:
                    self.plansza[i][j] = 'O'
                    self.rysuj_pionek(j, i, 'red')
                elif (i+j) % 2 == 1 and i > 4:
                    self.plansza[i][j] = 'X'
                    self.rysuj_pionek(j, i, 'blue')

    def rysuj_pionek(self, x, y, kolor):
        pionek_id = self.canvas.create_oval(x*50, y*50, (x+1)*50, (y+1)*50, fill=kolor)
        self.canvas.tag_bind(pionek_id, '<Button-1>', lambda event, row=y, col=x: self.kliknieto_pole(event, row, col))

    def kliknieto_pole(self, event, row, col):
        if self.plansza[row][col] == self.aktualny_gracz:
            self.wybrano_pionek(row, col)
        elif self.plansza[row][col] == ' ' and self.wybrany_pionek is not None:
            self.wykonaj_ruch(row, col)

    def wybrano_pionek(self, row, col):
        self.wybrany_pionek = (row, col)

    def wykonaj_ruch(self, row, col):
        x_pocz, y_pocz = self.wybrany_pionek
        if self.ruch_pionka(x_pocz, y_pocz, row, col):
            self.canvas.delete(self.aktualny_gracz)
            self.rysuj_pionek(col, row, 'red' if self.aktualny_gracz == 'O' else 'blue')
            self.aktualny_gracz = 'X' if self.aktualny_gracz == 'O' else 'O'
        self.wybrany_pionek = None

    def ruch_pionka(self, x_pocz, y_pocz, x_kon, y_kon):
        dx = x_kon - x_pocz
        dy = y_kon - y_pocz
        if abs(dx) == 1 and abs(dy) == 1 and self.plansza[y_kon][x_kon] == ' ':
            # Prosty ruch o jedno pole
            self.plansza[y_kon][x_kon] = self.plansza[y_pocz][x_pocz]
            self.plansza[y_pocz][x_pocz] = ' '
            return True
        elif abs(dx) == 2 and abs(dy) == 2 and self.plansza[y_kon][x_kon] == ' ':
            # Bicie pionka przeciwnika
            x_przeciwnika = x_pocz + dx // 2
            y_przeciwnika = y_pocz + dy // 2
            if self.plansza[y_przeciwnika][x_przeciwnika] == ('X' if self.aktualny_gracz == 'O' else 'O'):
                self.plansza[y_kon][x_kon] = self.plansza[y_pocz][x_pocz]
                self.plansza[y_przeciwnika][x_przeciwnika] = ' '
                self.plansza[y_pocz][x_pocz] = ' '
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = Warcaby(root)
    root.mainloop()
