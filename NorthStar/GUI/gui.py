"""

Author(s): Jordan Handy

Last Updated: 06/14/2025

Description:
    GUI used for the test stand NorthStar for the Gallus Engine
    
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
from tkdial import Meter
import time
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   #use later for the thrust plot
from PIL import Image, ImageTk


class TestStandGUI:
    def __init__(self):
        self.create_gui()
        return
    
    def create_gui(self):
        root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        root._state_before_windows_set_titlebar_color = 'zoomed'
        root.title("NorthStar Test Stand GUI")
        
        tabs = ctk.CTkTabview(root, width=300, height=300, anchor="w",border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b") #anchor='w' make them left aligned
        tabs.pack(padx=20, pady=20, anchor="w",expand=True,fill='both')
        tabs.add("Main")
        tabs.add("Settings")
        maintab = tabs.tab("Main")
        settingstab = tabs.tab("Settings")  #may add more later

        
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_rowconfigure(0,weight=1)
        
        metric_frame = ctk.CTkFrame(maintab,border_width = 2, fg_color = "#4622D8")
        metric_frame.grid(row=0, column=0,sticky="nsew")

        metric_frame.grid_rowconfigure(0,weight=0)
        mass_flow_label = ctk.CTkLabel(metric_frame,text='Mass Flow Rate',font=('Computer Modern',20))
        mass_flow_label.grid(row=0, column=0,sticky='ns')

        metric_frame.grid_rowconfigure(1,weight=1)
        mass_flow_frame = ctk.CTkFrame(metric_frame, fg_color="#4F4D4D", border_width=2)
        mass_flow_frame.grid(row=1, column=0, sticky="nsew")
        self.oximeter = self.create_oximeter(mass_flow_frame)
        self.oximeter.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)
        self.fuelmeter = self.create_fuelmeter(mass_flow_frame)
        self.fuelmeter.grid(row=0,column=1,sticky='nsew',padx=10,pady=10)

        metric_frame.grid_rowconfigure(2,weight=0)
        pressure_label = ctk.CTkLabel(metric_frame,text='Pressure',font=('Computer Modern',20))
        pressure_label.grid(row=2, column=0,sticky='ns')

        metric_frame.grid_rowconfigure(3,weight=1)
        pressure_frame = ctk.CTkFrame(metric_frame, fg_color="#4F4D4D", border_width=2)
        pressure_frame.grid(row=3, column=0, sticky="nsew")
        self.oximeterpressure = self.create_oximeter_pressure(pressure_frame)
        self.oximeterpressure.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)
        self.fuelmeterpressure = self.create_fuelmeter_pressure(pressure_frame)
        self.fuelmeterpressure.grid(row=0,column=1,sticky='nsew',padx=10,pady=10)
    
        metric_frame.grid_rowconfigure(4,weight=0)
        temperature_label = ctk.CTkLabel(metric_frame,text='Temperature',font=('Computer Modern',20))
        temperature_label.grid(row=4, column=0,sticky='ns')

        metric_frame.grid_rowconfigure(5,weight=1)
        temperature_frame = ctk.CTkFrame(metric_frame, fg_color="#4F4D4D", border_width=2)
        temperature_frame.grid(row=5, column=0, sticky="nsew")
        

        metric_frame.grid_columnconfigure(0,weight=1)
        
       
        thrust_frame = ctk.CTkFrame(maintab,border_width=2, fg_color = "#B82121")
        thrust_frame.grid(row=0, column=1,sticky="nsew")

        thrust_frame.grid_columnconfigure(0,weight=1)

        thrust_frame.grid_rowconfigure(0,weight=3)
        thrustgraph = ctk.CTkFrame(thrust_frame, fg_color="#4F4D4D")
        thrustgraph.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        thrust_frame.grid_rowconfigure(1,weight=1)
        thrust_metric = ctk.CTkFrame(thrust_frame, fg_color="#4F4D4D")
        thrust_metric.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        thrust_frame.grid_rowconfigure(2,weight=1)
        thrust_control = ctk.CTkFrame(thrust_frame, fg_color="#4F4D4D")
        thrust_control.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)


        
        control_frame = ctk.CTkFrame(maintab,border_width=2,fg_color = "#2C885C")
        control_frame.grid(row=0, column=2,sticky="nsew")
        control_frame.grid_columnconfigure(0,weight=1)

        control_frame.grid_rowconfigure(0,weight=0)
        control_label = ctk.CTkLabel(control_frame,text='Controls',font=('Computer Modern',20))
        control_label.grid(row=0, column=0,sticky='ns')

        control_frame.grid_rowconfigure(1,weight=2)
        control_buttons = ctk.CTkFrame(control_frame, fg_color="#4F4D4D")
        control_buttons.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        control_frame.grid_rowconfigure(2,weight=0)
        control_status = ctk.CTkLabel(control_frame, text="Status",font=('Computer Modern',20))
        control_status.grid(row=2, column=0, sticky='ns')

        control_frame.grid_rowconfigure(3,weight=1)
        control_status_frame = ctk.CTkFrame(control_frame, fg_color="#4F4D4D")
        control_status_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        control_frame.grid_rowconfigure(4,weight=1)
        control_dynamics = ctk.CTkFrame(control_frame, fg_color="#4F4D4D")
        control_dynamics.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
        
        temp_sensors = ['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4','Sensor 5','Sensor 6','Sensor 7']
        temp_sens_units = ['K','K','K','K','K','K','K']
        temp_sens_values = [0,0,0,0,0,0,0]
        for i in range(7):
            sensor_label = ctk.CTkLabel(temperature_frame, text=temp_sensors[i])
            sensor_label.grid(row=i,column=0,pady=5,padx=5,sticky="ew")
            
            sens_units = ctk.CTkLabel(temperature_frame, text=temp_sens_units[i])
            sens_units.grid(row=i,column=2,padx=5,pady=5,sticky="ew")
            sens_value = ctk.CTkLabel(temperature_frame, text=temp_sens_values[i])
            sens_value.grid(row=i,column=1,padx=5,pady=5,sticky="ew")

            i += 1


        
        root.mainloop()
        
  
    
    def create_oximeter(self,parent=None):
        if parent is None:
            parent = self.root
        oxmeter = Meter(parent, fg="black", radius=250, start=0, end=2000, axis_color="#242424",
                       start_angle=225, end_angle=-270, text_color='white', text_font=("Courier New Bold", 20),
                       scale_color="white", scroll_steps=1, scroll=True, major_divisions=200)
        oxmeter.set(0)
        oxmeter.set_mark(0, 1170, "#92d050")
        oxmeter.set_mark(1171, 1760, "yellow")
        oxmeter.set_mark(1761, 2000, "red")
        
        for i, tick in enumerate(oxmeter.find_withtag('scale')):
            value = (i * (2000/100)) / 1000
            oxmeter.itemconfig(tick, text=f"{value:.3f}")
        
        oxmeter.itemconfig('text', text=f"{0/1000:.3f} kg/s")
        return oxmeter
    
    def create_oximeter_pressure(self,parent=None):
        if parent is None:
            parent = self.root
        oxmeterpressure = Meter(parent, fg="black", radius=250, start=0, end=2000, axis_color="#242424",
                       start_angle=225, end_angle=-270, text_color='white', text_font=("Courier New Bold", 20),
                       scale_color="white", scroll_steps=1, scroll=True, major_divisions=200)
        oxmeterpressure.set(0)
        oxmeterpressure.set_mark(0, 1170, "#92d050")
        oxmeterpressure.set_mark(1171, 1760, "yellow")
        oxmeterpressure.set_mark(1761, 2000, "red")
        
        for i, tick in enumerate(oxmeterpressure.find_withtag('scale')):
            value = (i * (2000/100)) / 1000
            oxmeterpressure.itemconfig(tick, text=f"{value:.3f}")
        
        oxmeterpressure.itemconfig('text', text=f"{0/1000:.3f} psi")
        return oxmeterpressure

    def create_fuelmeter(self,parent=None):
        if parent is None:
            parent = self.root
        fuelmeter = Meter(parent, fg="black", radius=250, start=0, end=350, axis_color="#242424",
                         start_angle=225, end_angle=-270, text_color='white', text_font=("Courier New Bold", 20),
                         scale_color="white", scroll_steps=1, scroll=True, major_divisions=25)
        fuelmeter.set(0)
        fuelmeter.set_mark(0, 210, "#92d050")
        fuelmeter.set_mark(211, 315, "yellow")
        fuelmeter.set_mark(316, 348, "red")

        for i, tick in enumerate(fuelmeter.find_withtag('scale')):
            value = (i * (348/100)) / 1000
            fuelmeter.itemconfig(tick, text=f"{value:.3f}")

        fuelmeter.itemconfig('text', text=f"{0/1000:.3f} kg/s")
        return fuelmeter

   
    def create_fuelmeter_pressure(self,parent=None):
        if parent is None:
            parent = self.root
        fuelmeterpressure = Meter(parent, fg="black", radius=250, start=0, end=350, axis_color="#242424",
                         start_angle=225, end_angle=-270, text_color='white', text_font=("Courier New Bold", 20),
                         scale_color="white", scroll_steps=1, scroll=True, major_divisions=25)
        fuelmeterpressure.set(0)
        fuelmeterpressure.set_mark(0, 210, "#92d050")
        fuelmeterpressure.set_mark(211, 315, "yellow")
        fuelmeterpressure.set_mark(316, 348, "red")

        for i, tick in enumerate(fuelmeterpressure.find_withtag('scale')):
            value = (i * (348/100)) / 1000
            fuelmeterpressure.itemconfig(tick, text=f"{value:.3f}")

        fuelmeterpressure.itemconfig('text', text=f"{0/1000:.3f} psi")
        return fuelmeterpressure















































































































































































































































































































































































































































































































































































































































































































































































































    































































































































    






























































































































# balls lmao