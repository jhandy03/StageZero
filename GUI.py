"""

Author(s): Jordan Handy

Last Updated: 06/12/2025

Description:
    GUI used for the test stand BLANK for the Gallus Engine
    
Feature List:
    
    
Notes:
    Before running, make sure the following libraries/packages are installed:
    - customtkinter
    - ttkbootstrap
    - matplotlib
    - tkdial
    To install, use pip in the terminal as: pip install *library_name*
    To check current libraries, use pip list

"""


import customtkinter as ctk
import ttkbootstrap as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkdial import Meter
import time


def main():
    ctk.set_appearance_mode("dark")
    # root = ttk.Window(themename = 'darkly')
    root = ctk.CTk()
    # root.state('zoomed')
    oximeter = OxiMeter(root)
    oximeter.grid(row=0, column=0)
    fuelmeter = FuelMeter(root)
    fuelmeter.grid(row=0, column=1)
    root.mainloop()
   
def OxiMeter(root):
    oxmeter = Meter(root,fg = "black",radius=250,start=0,end=2000,axis_color="white",
                     start_angle=225, end_angle=-270,text_color='white',text_font=("Courier New Bold",20),
                     scale_color="white",scroll_steps=1,scroll=False,major_divisions=200)
    oxmeter.set(0)
    oxmeter.set_mark(0,1170, "#92d050")
    oxmeter.set_mark(1171,1760, "yellow")
    oxmeter.set_mark(1761,2000, "red")
    
    
    for i, tick in enumerate(oxmeter.find_withtag('scale')):
        value = (i*(2000/100))/1000
        oxmeter.itemconfig(tick,text=f"{value:.3f}")
    
    def update_meter():
        current_value = oxmeter.get()
        if current_value < 2000:
            oxmeter.set(current_value + 1)
            oxmeter.itemconfig('text',text=f"\n {current_value/1000:.3f} \n  kg/s")
            root.after(10, update_meter)  # Schedule next update in 100ms (0.1 sec)
    
    oxmeter.itemconfig('text',text=f"{0/1000:.3f} kg/s")
    root.after(100, update_meter)  # Start the updates
    return oxmeter
   
def FuelMeter(root):
    fuelmeter = Meter(root,fg = "black",radius=250,start=0,end=350,axis_color="white",
                     start_angle=225, end_angle=-270,text_color='white',text_font=("Courier New Bold",20),
                     scale_color="white",scroll_steps=1,scroll=False,major_divisions=25)
    fuelmeter.set(0)
    fuelmeter.set_mark(0,210, "#92d050")
    fuelmeter.set_mark(211,315, "yellow")
    fuelmeter.set_mark(316,348, "red")


    for i, tick in enumerate(fuelmeter.find_withtag('scale')):
        value = (i*(348/100))/1000
        fuelmeter.itemconfig(tick,text=f"{value:.3f}")

    def update_meter():
        current_value = fuelmeter.get()
        if current_value < 348:
            fuelmeter.set(current_value + 1)
            fuelmeter.itemconfig('text',text=f"\n {current_value/1000:.3f} \n  kg/s")
            root.after(10, update_meter)  # Schedule next update in 100ms (0.1 sec)

    fuelmeter.itemconfig('text',text=f"{0/1000:.3f} kg/s")
    root.after(100, update_meter)  # Start the updates
    return fuelmeter


# def startbutton():
#     startButton = ctk.CTkButton(root, text="Start", command=None)

# def abortbutton():
#     abortButton = ctk.CTkButton(root, text="Abort", command=None)

if __name__ == '__main__':
        main()