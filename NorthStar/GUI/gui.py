"""

Author(s): Jordan Handy

Last Updated: 06/14/2025

Description:
    GUI used for the test stand BLANK for the Gallus Engine
    
Feature List:

TODO:
    make the whole thing a class
    
    
Notes:
    Before running, make sure the following libraries/packages are installed:
    - customtkinter
    - matplotlib
    - tkdial
    To install, use pip in the terminal as: pip install *library_name*
    To check current libraries, use pip list

"""
import customtkinter as ctk
# import ttkbootstrap as ttk #might not be needed. tkinter doesn't like working with both ttk and ctk
from tkdial import Meter
import time
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   #use later for the thrust plot
from PIL import Image, ImageTk


class TestStandGUI:
    def __init__(self):
        self.abort_state = {'aborted': False}
        self.oximeter_running = False
        self.fuelmeter_running = False
        self.arrange_gui()
        
    def arrange_gui(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root._state_before_windows_set_titlebar_color = 'zoomed'
        self.root.title('NorthStar')
        
        proptitle = ctk.CTkLabel(self.root, text="Propellant System", font=("Courier New Bold", 24))
        proptitle.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        
        self.prop_frame = ctk.CTkFrame(self.root)
        self.prop_frame.grid(row=1, column=0,columnspan=2, padx=10, pady=10)
        self.oximeter = self._create_oximeter(self.prop_frame)
        self.oximeter.grid(row=0, column=0, padx=10, pady=10)
        self.fuelmeter = self._create_fuelmeter(self.prop_frame)
        self.fuelmeter.grid(row=0, column=1, padx=10, pady=10)
        
        pressuretitle = ctk.CTkLabel(self.root,text='Tank Pressure', font=("Courier New Bold", 24))
        pressuretitle.grid(row=2,column=0,columnspan=2, pady=(5, 10))
        self.pressure_frame = ctk.CTkFrame(self.root)
        self.pressure_frame.grid(row=3,column=0,columnspan=2, padx=10, pady=10)
        self.pressure_fuel = self._create_fuel_pressure(self.pressure_frame)
        self.pressure_fuel.grid(row=0, column=0, padx=10, pady=10)
        self.pressure_ox = self._create_ox_pressure(self.pressure_frame)
        self.pressure_ox.grid(row=0,column=1, padx=10, pady=10)
        
        temptitle = ctk.CTkLabel(self.root,text='Temperature', font=("Courier New Bold", 24))
        temptitle.grid(row=4,column=0,columnspan=2, pady=(5, 10))
        self.temp_frame = ctk.CTkFrame(self.root)
        self.temp_frame.grid(row=5,column=0,columnspan=2, padx=10, pady=10,sticky='ew')
        self.temp_frame.columnconfigure(0, weight=0)
        self.temp_frame.columnconfigure(1, weight=1)
        self.temp_frame.columnconfigure(2, weight=0)
        self.temp_throat = self._create_temperature_bars(self.temp_frame, "Throat Temp", 0, 1000)
        self.temp_chamber = self._create_temperature_bars(self.temp_frame, "Chamber Temp", 0, 3500)
        self.temp_nozzle = self._create_temperature_bars(self.temp_frame, "Nozzle Temp", 0, 800)
        self.temp_ambient = self._create_temperature_bars(self.temp_frame, "Other", 0, 150)
        self.temp_throat.grid(row=0,column=0, padx=0, pady=(10,5),sticky='ew')
        self.temp_chamber.grid(row=1,column=0, padx=0, pady=5,sticky='ew')
        self.temp_nozzle.grid(row=2,column=0, padx=0, pady=5,sticky='ew')
        self.temp_ambient.grid(row=3,column=0, padx=0, pady=(5,10),sticky='ew')
        
        
        
        #TODO: Find where the buttons should go
        # self.start_button = self._create_start_button()
        # self.start_button.grid(row=1, column=0, columnspan=2, pady=(10, 5))
        
        # self.abort_button = self._create_abort_button()
        # self.abort_button.grid(row=2, column=0, columnspan=2, pady=(5, 10))
        
        self.root.mainloop()
    
        
    
    def _create_oximeter(self,parent=None):
        if parent is None:
            parent = self.root
        oxmeter = Meter(parent, fg="black", radius=250, start=0, end=2000, axis_color="#242424",
                       start_angle=225, end_angle=-270, text_color='white', text_font=("Courier New Bold", 20),
                       scale_color="white", scroll_steps=1, scroll=False, major_divisions=200)
        oxmeter.set(0)
        oxmeter.set_mark(0, 1170, "#92d050")
        oxmeter.set_mark(1171, 1760, "yellow")
        oxmeter.set_mark(1761, 2000, "red")
        
        for i, tick in enumerate(oxmeter.find_withtag('scale')):
            value = (i * (2000/100)) / 1000
            oxmeter.itemconfig(tick, text=f"{value:.3f}")
        
        oxmeter.itemconfig('text', text=f"{0/1000:.3f} kg/s")
        return oxmeter

    def _create_fuelmeter(self,parent=None):
        if parent is None:
            parent = self.root
        fuelmeter = Meter(parent, fg="black", radius=250, start=0, end=350, axis_color="#242424",
                         start_angle=225, end_angle=-270, text_color='white', text_font=("Courier New Bold", 20),
                         scale_color="white", scroll_steps=1, scroll=False, major_divisions=25)
        fuelmeter.set(0)
        fuelmeter.set_mark(0, 210, "#92d050")
        fuelmeter.set_mark(211, 315, "yellow")
        fuelmeter.set_mark(316, 348, "red")

        for i, tick in enumerate(fuelmeter.find_withtag('scale')):
            value = (i * (348/100)) / 1000
            fuelmeter.itemconfig(tick, text=f"{value:.3f}")

        fuelmeter.itemconfig('text', text=f"{0/1000:.3f} kg/s")
        return fuelmeter

    def _create_start_button(self):
        def start_meters():
            self.abort_state['aborted'] = False
            
            if not self.oximeter_running:
                self.oximeter_running = True
                self._update_meters(self.oximeter, self.oximeter_running)

            if not self.fuelmeter_running:
                self.fuelmeter_running = True
                self._update_meters(self.fuelmeter, self.fuelmeter_running)
        
        # TODO: finish later        
        # def start_pressure():
        #     self.abort_state['aborted'] = False
        #     if not self.fuel_pressure_running:
        #         self.fuel_pressure_running = True

        return ctk.CTkButton(self.root, text="Start", command=start_meters)

    def _create_abort_button(self):
        def abort_all():
            self.abort_state['aborted'] = True
            for widget in self.root.winfo_children():
                if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Start":
                    widget.configure(state="disabled")
        
        return ctk.CTkButton(self.root, text="Abort", command=abort_all)

    def _update_meters(self,meter,running, text_format="\n {value:.3f} \n kg/s"):
        if not getattr(self,running) or self.abort_state['aborted']:
            setattr(self, running, False)
            return
        current_value = meter.get()
        while running == True:
            meter.itemconfig('text', text=text_format.format(value=current_value/1000))
            self.root.after(1, lambda: self._update_meters(meter, running, text_format))
            return
                    
    def _create_fuel_pressure(self,parent=None):
        if parent is None:
            parent = self.root
        fuel_pressure = Meter(parent, fg="black", radius=250, start=0, end=1000, axis_color="#242424",
                              start_angle=225, end_angle=-270, text_color='white',text_font=("Courier New Bold",20),
                              scale_color="white", scroll_steps=0.5, scroll=False, major_divisions=50)
        fuel_pressure.set(0)
        fuel_pressure.set_mark(0,600, "#92d050")
        fuel_pressure.set_mark(601, 800, "yellow")
        fuel_pressure.set_mark(801, 1000, "red")
        fuel_pressure.itemconfig('text',text=f"{0:.3f} psi")
        return fuel_pressure
    
    def _create_ox_pressure(self,parent=None):
        if parent is None:
            parent = self.root
        ox_pressure = Meter(parent, fg="black", radius=250, start=0, end=1000, axis_color="#242424",
                              start_angle=225, end_angle=-270, text_color='white',text_font=("Courier New Bold",20),
                              scale_color="white", scroll_steps=0.5, scroll=False, major_divisions=50)
        ox_pressure.set(0)
        ox_pressure.set_mark(0,600, "#92d050")
        ox_pressure.set_mark(601, 800, "yellow")
        ox_pressure.set_mark(801, 1000, "red")
        ox_pressure.itemconfig('text',text=f"{0:.3f} psi")
        return ox_pressure
    
    def _create_thrust_plot(self,parent=None):
        #TODO: finish implementing
        return None
        
        
    def _create_temperature_bars(self, parent, label, min_val, max_val):
        if parent is None:
            parent = self.root
        
        temp_container = ctk.CTkFrame(parent)
        temp_container.columnconfigure(0,weight=0)
        temp_container.columnconfigure(1, weight=1)
        temp_container.columnconfigure(2, weight=0)
        
        label_widget = ctk.CTkLabel(temp_container, text=f"{label}", 
                                   font=("Courier New", 12))
        label_widget.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        progress_bar = ctk.CTkProgressBar(temp_container, orientation="horizontal", 
                                        width=200, height=20, corner_radius=10)
        progress_bar.set(0)
        progress_bar.grid(row=0, column=1, padx=10, pady=5)
        
        value_label = ctk.CTkLabel(temp_container, text=f"{min_val:.2f} K", 
                                  font=("Courier New", 12))
        value_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        
        temp_bar_data = {
            'bar': progress_bar,
            'min': min_val,
            'max': max_val,
            'label': label_widget,
            'value_label': value_label
        }
        
        if not hasattr(self, 'temp_bars'):
            self.temp_bars = {}
        
        self.temp_bars[label] = temp_bar_data
        
        return temp_container















































































































































































































































































































































































































































































































































































































































































































































































































    































































































































    






























































































































# balls lmao