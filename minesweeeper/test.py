from tkinter import Tk, Label

root = Tk()

btn = Label(root, text="Test", width=10, height=3, bg="white")
btn.pack()

def change_color(event):  # `event` is required for `bind`
    btn.configure(bg="blue")

btn.bind("<Button-1>", change_color)  # Left-click to change color

root.mainloop()

