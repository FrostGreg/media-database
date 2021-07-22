import tkinter as tk
from .style import Style


class SplashScreen:
    def __init__(self):
        self.splash_screen = tk.Tk()  # creates a window
        self.width = 800
        self.height = 600
        self.splash_screen.title("Media Database")
        self.splash_screen.call('wm', 'iconphoto', self.splash_screen._w, tk.PhotoImage(file='assets/icon.png'))
        self.splash_screen.configure(bg=Style.bg)
        # defines attributes of window
        logo = tk.PhotoImage(file="assets/splash-screen.png")  # loads image for splashscreen

        canvas = tk.Canvas(self.splash_screen, height=self.height * 0.8, width=self.width * 0.8,
                           bg=Style.bg)  # creates canvas for image
        canvas.pack()
        canvas.create_image(self.width * 0.8 / 2, self.height * 0.8 / 2,
                            image=logo)  # displays image on canvas
        canvas.pack()

        self.splash_screen.bind("<Button-1>", self.close)  # if LMB is clicked then close the window

        self.splash_screen.mainloop()

    def close(self, event):  # closes the splash screen
        self.splash_screen.destroy()
