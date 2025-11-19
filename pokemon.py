from tkinter import *
import requests
window = Tk()
window.geometry("500x500")
window.title =("Pokemon Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg = "yellow")
poke_data_label = Label(window, font="Arial, 12")
def getPoke():
    poke = enteruser.get()
    if not poke:
        poke_data_label.config(text = "Error fetching data", bg = "pink")
    

    poke = response.json()
    response = ({
        "name": poke["name"],
        "height": poke["height"],
        "weight": poke["weight"],
        "types": [t["type"]["name"] for t in poke["types"]]
    })
submit_button.config(command = getPoke)
poke_data_label.pack()
enteruser.pack()
submit_button.pack()
window.mainloop()