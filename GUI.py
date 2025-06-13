"""

Author(s): Jordan Handy

Last Updated: 06/12/2025

Description:
    GUI used for the test stand BLANK for the Gallus Engine
    
Feature List:
    

"""


import tkinter
import ttkbootstrap as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main():
    root = ttk.Window(themename = 'darkly')
    # root.state('zoomed')
    ttk.Label(root,text='Balls lmao',font=('Arial', 100)).grid()

    root.mainloop()
    

if __name__ == '__main__':
        main()