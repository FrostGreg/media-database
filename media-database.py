import tkinter as tk
from classes import style
from classes import menu
from classes import splash_screen


class MediaDatabase:
    def __init__(self):
        splash_screen.SplashScreen()

        window = tk.Tk()  # creates window
        window.title("Media Database")
        window.configure(bg=style.Style.bg)
        window.geometry("800x400")
        window.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='assets/icon.png'))  # adds favicon to window
        menu.MainMenu(window)  # creates object for the main menu

        window.mainloop()


if __name__ == "__main__":
    MediaDatabase()
