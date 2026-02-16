import tkinter as tk
import customtkinter

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App Frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("HH Model GUI")

def show_values():
    print (w1.get())

#Adding UI Elements
title = customtkinter.CTkLabel(app, text="HH Model")
title.pack(padx=10, pady=10)
#Sliders
w1 = tk.Scale(app, from_=0, to=5,tickinterval=1, orient='horizontal', length = 400)
w1.pack()
tk.Button(app, text='Show', command= show_values).pack()

# Run App
app.mainloop()
