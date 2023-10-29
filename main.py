import tkinter as tk

def enter_username(root):
    root.title('Enter Username')
    root.geometry('400x200')
    root.resizable(False, False)

    label = tk.Label(root, text='Enter Username', font=('Comic Sans MS', 16))
    label.pack(pady=10)

    entry = tk.Entry(root, font=('Comic Sans MS', 16))
    entry.pack(pady=10)

    button = tk.Button(root, text='Enter', font=('Comic Sans MS', 16), command=lambda: root.destroy())
    button.pack(pady=10)

    return entry.get()


if __name__ == '__main__':
    
    root = tk.Tk()

    username = enter_username(root)
    print(username)
    
    root.mainloop()