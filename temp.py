import tkinter as tk
window = tk.Tk()
window.title("Media Library")
window.configure(bg="white")
window.geometry("800x600")
window.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='MLIcon.png'))
v = tk.IntVar()
v.set(2)

def unlock():
    R1.configure(state=NORMAL)
    R2.config(state="enabled")

R1 = tk.Radiobutton(window, text="Yoghurt",variable=v,value=1,state="disabled").place(x=100,y=100)
R2 = tk.Radiobutton(window, text="Beans",variable=v, value=2,state="disabled").place(x=100,y=200)

but1 = tk.Button(window, text="Button", command=unlock).place(x=300, y=150)



window.mainloop()



