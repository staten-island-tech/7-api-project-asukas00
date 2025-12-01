from tkinter import *
import requests
window = Tk()
window.geometry("500x500")
window.title =("Pokemon Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg = "yellow")
poke_datalabel = Label(window, font="Arial, 12")
def getPoke():
    poke = enteruser.get()  # Get the Pokémon name entered by the user
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke.lower()}")
    data = response.json()
    pokemon = {
                "name": data["name"].capitalize(),
                "id": data["id"],
                "height": data["height"] / 10,  # Convert decimeters to meters
                "weight": data["weight"] / 10,  # Convert hectograms to kilograms
                "types": [t["type"]["name"].capitalize() for t in data["types"]]
            }
    if response.status_code != 200:
        print("Error fetching data!")
        return print(text= "There is no pokemon with this name try again")
    if response.status_code == 200:
        submit_button.config(command=getPoke)
    



poke_datalabel.pack()
enteruser.pack()
submit_button.pack()
window.mainloop()