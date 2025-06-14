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

# I will not be commenting.iykyk :) - JH

def main():
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root._state_before_windows_set_titlebar_color = 'zoomed'
    oximeter = OxiMeter(root)
    oximeter.grid(row=0, column=0)
    fuelmeter = FuelMeter(root)
    fuelmeter.grid(row=0, column=1)
    start_button = startbutton(root, oximeter, fuelmeter)
    start_button.grid(row=1, column=0, columnspan=2, pady=(10, 5))
    abort_button = abortbutton(root, oximeter, fuelmeter)
    abort_button.grid(row=2, column=0, columnspan=2, pady=(5, 10))
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
    
    oxmeter.itemconfig('text',text=f"{0/1000:.3f} kg/s")
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

    fuelmeter.itemconfig('text',text=f"{0/1000:.3f} kg/s")
    return fuelmeter


abort_state = {'aborted': False}

def startbutton(root, oximeter, fuelmeter):

    oximeter_running = False
    fuelmeter_running = False
    
    def start_meters():
        nonlocal oximeter_running, fuelmeter_running
        
        abort_state['aborted'] = False
        
        def update_oximeter():
            nonlocal oximeter_running
            if not oximeter_running or abort_state['aborted']:
                oximeter_running = False
                return
            current_value = oximeter.get()
            if current_value < 2000:
                oximeter.set(current_value + 1)
                oximeter.itemconfig('text',text=f"\n {current_value/1000:.3f} \n  kg/s")
                root.after(10, update_oximeter)
            else:
                oximeter_running = False
        
        def update_fuelmeter():
            nonlocal fuelmeter_running
            if not fuelmeter_running or abort_state['aborted']:
                fuelmeter_running = False
                return
            current_value = fuelmeter.get()
            if current_value < 348:
                fuelmeter.set(current_value + 1)
                fuelmeter.itemconfig('text',text=f"\n {current_value/1000:.3f} \n  kg/s")
                root.after(10, update_fuelmeter)
            else:
                fuelmeter_running = False

        if not oximeter_running:
            oximeter_running = True
            update_oximeter()
        
        if not fuelmeter_running:
            fuelmeter_running = True
            update_fuelmeter()
    
    startButton = ctk.CTkButton(root, text="Start", command=start_meters)
    return startButton

def abortbutton(root, oximeter, fuelmeter):
    def abortAll():
        abort_state['aborted'] = True
        for widget in root.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Start":
                widget.configure(state="disabled")
    
    abortButton = ctk.CTkButton(root, text="Abort", command=abortAll)
    return abortButton

if __name__ == '__main__':
        main()