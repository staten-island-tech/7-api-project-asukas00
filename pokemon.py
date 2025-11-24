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
    if response.status_code != 200:
        print("Error fetching data!")
        return print(f"{enteruser}", text= f"{"enteruser"}there is no pokemon with this name try again")
    data = response.json()
    pokemon = print({
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "types": [t["type"]["name"] for t in data["types"]]
    })


    



submit_button.config(command = getPoke)
poke_datalabel.pack(pady=5)
enteruser.pack()
submit_button.pack()
window.mainloop()