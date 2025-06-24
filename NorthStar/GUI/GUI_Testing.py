import customtkinter as ctk
# from tkdial import Meter


root = ctk.CTk()
root._state_before_windows_set_titlebar_color = "zoomed"

frame1 = ctk.CTkFrame(root)
frame1.grid(row=0,column=0,sticky="nsew")
frame1.grid_columnconfigure(0,weight=1)
frame1.grid_columnconfigure(1,weight=2)
frame1.grid_columnconfigure(2,weight=3)
# frame1.grid_columnconfigure(3,weight=1)
# frame1.grid_columnconfigure(4,weight=1)

frame2 = ctk.CTkFrame(root)
frame2.grid(row=0,column=1)
frame2.grid_columnconfigure(1,weight=2)

button1 = ctk.CTkButton(frame1,text="This Is Button 1")
button1.grid(row=0,column=0)


button2 = ctk.CTkButton(frame1,text="This Is Button 2")
button2.grid(row=0,column=1)


button3 = ctk.CTkButton(frame1,text="This Is Button 3")
button3.grid(row=0,column=2,columnspan=2)


label = ctk.CTkLabel(frame2,text="Label")
label.grid(row=1,column=0)

frame3 = ctk.CTkFrame(root)
frame3.grid(row=1,column=0,columnspan=2,sticky="nsew")


    
for i in range(5):
    if i%2==1:
        frame3.grid_rowconfigure(i, weight=1)
    else:
        frame3.grid_rowconfigure(i, weight=2)
for i in range(5):
    button = ctk.CTkButton(frame3, text = f'Button {i}')
    button.grid(row=i,column=0,sticky="nsew")
root.mainloop()






