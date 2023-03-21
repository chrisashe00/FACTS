from customtkinter import *
# Setting up the Window
app=CTk()
#Giving it a size
app.geometry("1400x680")

#Create a label
text=CTkLabel(app, text="Hello World!")
text2=CTkLabel(app, text="How are you?")
#Showing the label
text.grid(row=0,column=0, padx=10)
text2.grid(row=0,column=1, padx=10)

#Create a button
btn=CTkButton(app, text="Click Me!")
btn.grid(row=1, column=0, padx=10 )

#Running an event loop
app.mainloop()




