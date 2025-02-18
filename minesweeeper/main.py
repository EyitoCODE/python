"""
Minesweeper Game
Date: [2005-02-17]
Version: 1.0
Python Version: 3.13.1
"""

from tkinter import *
from cell import Cell
import settings
import utils



root = Tk()


# Override the settings of the window
root.configure(bg="Black") # Background color of the window
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}') # Windows size
root.title('Minesweeper') # Window Title
root.resizable(False, False) # To not allow the windows size to be changed


# Filling the top part of the frame with the color Black 
# Width and height is used specify the area that its going to cover
top_frame = Frame(
    root,
    bg='Black', 
    width = settings.WIDTH,
    height= utils.height_prct(25)
)

# The starting point of where to fill
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg='Black',
    fg='White',
    text='Minesweeper Game',
    font=('', 48)
)

game_title.place(
    x=utils.width_prct(25), y=0
)

# Filling the left part of the frame with the color Black
left_frame = Frame(
    root,
    bg='Black',
    width=utils.width_prct(75),
    height= utils.height_prct(75) 
)

# The starting point of where to fill
left_frame.place(x=0, y=utils.height_prct(25))

# Filling the center part of the frame with the color Black
center_frame = Frame(
    root,
    bg='Black', 
    width=utils.width_prct(75),
    height= utils.height_prct(75) 
)

# The starting point of where to fill
center_frame.place(x=utils.width_prct(25), y=utils.height_prct(25))


# Making a grid for the game
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x,y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=x, row=y
            )
        
# Call the label from the cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(
    x=0, y=0
)

Cell.randomize_mines()

# for c in Cell.all:    # Testing if i was able to make mines
#     print(c.is_mine)

# Run the window
root.mainloop()