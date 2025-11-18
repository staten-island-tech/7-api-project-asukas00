from tkinter import *
import requests
window = Tk()
window.geometry("1000x1000")
window.title =("Pokemon Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12")
poke_data_label = Label(window, font="Arial, 12")
def getPoke():
    poke = enteruser.get()
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke.lower()}")
    if response.status_code != 200:
        print("Error fetching data!")
        return None
    
    data = response.json()
    response = ({
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "types": [t["type"]["name"] for t in data["types"]]
    })
submit_button.config(command= getPoke)
poke_data_label.pack()
enteruser.pack()
submit_button.pack()
window.mainloop()