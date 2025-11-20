from tkinter import *
import requests
window = Tk()
window.geometry("500x500")
window.title =("Pokemon Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg = "yellow")
poke_data_label = Label(window, font="Arial, 12")
def getPoke():
    poke = enteruser.get()  # Get the Pokémon name entered by the user
    data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke.lower()}")
    pokemon = {
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "types": [t["type"]["name"] for t in data["types"]]
    }  
    if  data != 200:
        poke_data_label.config(text="Error fetching data!")
        return None
    if data == poke:
        poke_data_label.config(text=f"{pokemon}")



submit_button.config(command = getPoke)
poke_data_label.pack()
enteruser.pack()
submit_button.pack()
window.mainloop()