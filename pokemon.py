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
    if response.status_code == 200:
            data = response.json()
            display_text = (
                f"Pokémon: {data['name']} (ID: {data['id']})",
                f"Height: {data['height']}/n",
                f"Weight: {data['weight']}/n",
                f"Types: {data['types']}/n"
            )
            
            poke_datalabel.config(text=display_text, fg="black")
            
    if not response.status_code == 200:
            error_message = f"Error: No Pokémon named '{poke_datalabel.capitalize()}' found. Try again."
            poke_datalabel.config(text=error_message, fg="red")

        

submit_button.config(command=getPoke)
enteruser.pack()
submit_button.pack()
poke_datalabel.pack()

window.mainloop()