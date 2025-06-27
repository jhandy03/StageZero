"""

Author(s): Jordan Handy, Alex Barnes

Last Updated: 06/26/2025

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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   #use later for the thrust plot
from PIL import Image, ImageTk


class TestStandGUI:
    def __init__(self):
        self.create_gui()
        return
    
    def create_gui(self):
        self.root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        self.root._state_before_windows_set_titlebar_color = 'zoomed'
        self.root.title("NorthStar Test Stand GUI")

        tabs = ctk.CTkTabview(self.root, width=300, height=300, anchor="w",border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b") #anchor='w' make them left aligned
        tabs.pack(padx=20, pady=20, anchor="w",expand=True,fill='both')
        tabs.add("Main")
        tabs.add("Settings")
        maintab = tabs.tab("Main")
        settingstab = tabs.tab("Settings")  #may add more later


        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0,weight=1)

        metric_frame = ctk.CTkFrame(maintab,border_width = 2, fg_color = "#4622D8")
        metric_frame.grid(row=0, column=0,sticky="nsew")

        metric_frame.grid_rowconfigure(0,weight=0)
        mass_flow_label = ctk.CTkLabel(metric_frame,text='Mass Flow Rate',font=('Computer Modern',25))
        mass_flow_label.grid(row=0, column=0,sticky='ns',pady=10,padx=10)

        metric_frame.grid_rowconfigure(1,weight=1)
        mass_flow_frame = ctk.CTkFrame(metric_frame, fg_color="#4F4D4D", border_width=2)
        mass_flow_frame.grid(row=1, column=0, sticky="nsew")
        self.oximeter = self.create_oximeter(mass_flow_frame)
        self.oximeter.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)
        self.fuelmeter = self.create_fuelmeter(mass_flow_frame)
        self.fuelmeter.grid(row=0,column=1,sticky='nsew',padx=10,pady=10)

        metric_frame.grid_rowconfigure(2,weight=0)
        pressure_label = ctk.CTkLabel(metric_frame,text='Pressure',font=('Computer Modern',25))
        pressure_label.grid(row=2, column=0,sticky='ns')

        metric_frame.grid_rowconfigure(3,weight=1)
        pressure_frame = ctk.CTkFrame(metric_frame, fg_color="#4F4D4D", border_width=2)
        pressure_frame.grid(row=3, column=0, sticky="nsew")
        self.oximeterpressure = self.create_oximeter_pressure(pressure_frame)
        self.oximeterpressure.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)
        self.fuelmeterpressure = self.create_fuelmeter_pressure(pressure_frame)
        self.fuelmeterpressure.grid(row=0,column=1,sticky='nsew',padx=10,pady=10)
    
        metric_frame.grid_rowconfigure(4,weight=0)
        temperature_label = ctk.CTkLabel(metric_frame,text='Temperature',font=('Computer Modern',25))
        temperature_label.grid(row=4, column=0,sticky='ns',pady=10,padx=10)

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
        control_label.grid(row=0, column=0,sticky='ns',pady=10,padx=10)
        
        control_frame_inputs = ctk.CTkFrame(control_frame, fg_color="#4F4D4D")
        control_frame_inputs.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        for i in range(3):
            control_frame_inputs.grid_columnconfigure(i, weight=1)
            control_frame_inputs.grid_rowconfigure(i, weight=1)
            
        control_buttons = ['Button 1', 'Button 2', 'Button 3','Button 4','Button 5','Button 6','Button 7','Button 8','Button 9']
        for i, ctrl in enumerate(control_buttons):
            button = ctk.CTkButton(control_frame_inputs, text=ctrl, width=100, height=50)
            button.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
        
        status_label = ctk.CTkLabel(control_frame, text="Status", font=('Computer Modern', 20))
        status_label.grid(row=2, column=0, sticky='ns')
        
        status_frame = ctk.CTkFrame(control_frame, fg_color="#4F4D4D")
        status_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(3):
            status_frame.grid_columnconfigure(i, weight=1)
            status_frame.grid_rowconfigure(i, weight=1)
            
        status_good = "#4cff66"
        status_bad = "#ff4c4c"
        status_unknown = "#ffcc00"
        
        status_items = [
            ("Blank 1", status_good),
            ("Blank 2", status_unknown),
            ("Blank 3", status_bad),
            ("Blank 4", status_good),
            ("Blank 5", status_unknown),
            ("Blank 6", status_bad),
            ("Blank 7", status_good),
            ("Blank 8", status_good),
            ("Blank 9", status_unknown)
        ]
        
        for i, (label, color) in enumerate(status_items):
            row = i // 3
            col = i % 3
                
            item_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                   
            led = ctk.CTkLabel(item_frame, text='●', text_color=color, font=('Computer Modern', 70))
            led.pack()

            status_label = ctk.CTkLabel(item_frame, text=label, font=('Computer Modern', 20))
            status_label.pack()
            
        controls_buttons_frame = ctk.CTkFrame(control_frame, fg_color="#4F4D4D")
        controls_buttons_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
        
        controls_buttons_frame.grid_columnconfigure(0, weight=1)
        controls_buttons_frame.grid_columnconfigure(1, weight=1)
        controls_buttons_frame.grid_columnconfigure(2, weight=1)
        controls_buttons_frame.grid_rowconfigure(0, weight=1)
        
        ctrl_buttons = ['Control 1', 'Control 2', 'Control 3', 'Control 4']
        for i, ctrl in enumerate(ctrl_buttons):
            button = ctk.CTkButton(controls_buttons_frame, text=ctrl, font=('Computer Modern', 20), width=100, height=50) #width and height are set so they don't clip outside the screen
            button.grid(row=0, column=i+1, padx=5, pady=5, sticky="sew")

        for i in range(8):
            temperature_frame.grid_rowconfigure(i, weight=1)
        temperature_frame.grid_columnconfigure(0, weight=1)
        temperature_frame.grid_columnconfigure(1, weight=3)
        temperature_frame.grid_columnconfigure(2, weight=1)
        
        temp_sens_labels = ['Temp Sensor 1', 'Temp Sensor 2', 'Temp Sensor 3','Temp Sensor 4','Temp Sensor 5','Temp Sensor 6','Temp Sensor 7']
        self.temp_sens_values = []
        for i, label in enumerate(temp_sens_labels):
            temp_label = ctk.CTkLabel(temperature_frame, text=label, font=('Computer Modern', 15))
            temp_label.grid(row=i, column=0, sticky='ns', padx=5, pady=5)
            
            temp_bar = ctk.CTkProgressBar(temperature_frame, orientation='horizontal')
            temp_bar.grid(row=i, column=1, sticky='nsew', padx=5, pady=5)
            temp_bar.set(50) 
            
            temp_values = ctk.CTkLabel(temperature_frame, text="0 K", font=('Computer Modern', 15))
            temp_values.grid(row=i, column=2, sticky='ns', padx=5, pady=5)
            
            self.temp_sens_values.append(temp_values)



        self.thrust_fig, self.thrust_ax = plt.subplots(figsize=(8, 6.5))
        self.thrust_ax.set_title("Thrust vs Time")
        self.thrust_ax.set_xlabel("Time (s)")
        self.thrust_ax.set_ylabel("Thrust (N)")
        self.thrust_canvas = FigureCanvasTkAgg(self.thrust_fig, master=thrustgraph)
        self.thrust_canvas.get_tk_widget().grid(row=0,column=0,pady=10,padx=10,sticky='nsew')
        self.thrust_ax.grid(True,linestyle='--',alpha=0.5)
        
        thrust_metric.grid_columnconfigure(0, weight=1)
        thrust_metric.grid_columnconfigure(1, weight=1)
        thrust_metric.grid_rowconfigure(0, weight=1)
        thrust_metric.grid_rowconfigure(1, weight=2)
        
        thrust_label = ctk.CTkLabel(thrust_metric, text="Thrust", font=('Computer Modern', 30))
        thrust_label.grid(row=0, column=0, sticky="ns")
        throttle_label = ctk.CTkLabel(thrust_metric, text="Throttle", font=('Computer Modern', 30))
        throttle_label.grid(row=0, column=1, sticky="ns")

        thrust_value = ctk.CTkLabel(thrust_metric, text="0 N", font=('Computer Modern', 30))
        thrust_value.grid(row=1, column=0, sticky="ns")
        throttle_value = ctk.CTkLabel(thrust_metric, text="0%", font=('Computer Modern', 30))
        throttle_value.grid(row=1, column=1, sticky="ns")
        
        thrust_control.grid_columnconfigure(0, weight=1)
        thrust_control.grid_columnconfigure(1, weight=1)
        thrust_control.grid_columnconfigure(2, weight=1)
        thrust_control.grid_rowconfigure(0, weight=1)
        
        ignite_button = ctk.CTkButton(thrust_control, text="Ignite",font=('Computer Modern',25), command=None)
        ignite_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        reset_button = ctk.CTkButton(thrust_control, text="Reset",font=('Computer Modern',25), command=None)
        reset_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        abort_button = ctk.CTkButton(thrust_control, text="Abort",font=('Computer Modern',25), command=None)
        abort_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
    
    
    
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  
        self.root.mainloop()
        
  
    
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

    def on_close(self):
        self.root.quit()














































































































































































































































































































































































































































































































































































































































































































































































































    































































































































    






























































































































# balls lmao