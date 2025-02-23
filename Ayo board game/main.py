"""
Author: Oritse-tsegbemi Eyito
Ayo board Game
Date: [2005-02-23]
Version: 1.0
Python Version: 3.13.1
"""


import tkinter as tk
from gui import AyoGUI

def main():
    root = tk.Tk()
    app = AyoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
