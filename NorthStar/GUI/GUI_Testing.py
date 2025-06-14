import customtkinter
from tkdial import Meter
import time
from tkinter import *

app = customtkinter.CTk()
# app.geometry("950x350")

# meter1 = Meter(app, radius=300, start=0, end=160, border_width=0,
#                fg="black", text_color="white", start_angle=270, end_angle=-270,
#                text_font="DS-Digital 30", scale_color="white", needle_color="red")
# meter1.set_mark(140, 160) # set red marking from 140 to 160
# meter1.grid(row=0, column=1, padx=20, pady=30)

# meter2 = Meter(app, radius=260, start=0, end=200, border_width=5,
#                fg="black", text_color="white", start_angle=270, end_angle=-360,
#                text_font="DS-Digital 30", scale_color="black", axis_color="white",
#                needle_color="white")
# meter2.set_mark(1, 100, "#92d050")
# # meter2.set_mark(105, 150, "yellow")
# # meter2.set_mark(155, 196, "red")
# meter2.set(80) # set value
# meter2.grid(row=0, column=0, padx=20, pady=30)
# meter3 = Meter(app, fg="#242424", radius=300, start=0, end=50,
#             border_width=0, text_color="white",
#                start_angle=0, end_angle=-360, scale_color="white", axis_color="cyan",
#                needle_color="white",  scroll_steps=1, text="")
# meter3.set(15)
# meter3.grid(row=0, column=2, pady=30)

# for i, tick in enumerate(meter3.find_withtag('scale')):
#     meter3.itemconfig(tick, text="")

def click():
    progress.step()
    
progress = customtkinter.CTkProgressBar(app, orientation="vertical", width=20, height=300,corner_radius=0)
progress.pack(pady=40)
progress.set(0)
button = customtkinter.CTkButton(app,text="",command=click)
button.pack(pady=20)


app.mainloop()
