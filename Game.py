from tkinter import *
import requests

# Create the main window
window = Tk()
window.geometry("1000x1000")
window.title("Pokemon Data")

# Create the entry widget, button, and label
enteruser = Entry(window, font="Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12")
poke_data_label = Label(window, font="Arial, 12")

# Function to fetch Pokémon data
def getPoke():
    poke = enteruser.get()  # Get the Pokémon name entered by the user
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke.lower()}")
    
    if response.status_code != 200:
        poke_data_label.config(text="Error fetching data!")
        return None
    
    data = response.json()
    pokemon = {
        "name": data["name"].capitalize(),
        "height": data["height"],
        "weight": data["weight"],
        "types": [t["type"]["name"] for t in data["types"]]
    }

    # Update the label with the fetched Pokémon data
    poke_data_label.config(
        text=f"Name: {pokemon['name']}\nHeight: {pokemon['height']} decimeters\nWeight: {pokemon['weight']} hectograms\nTypes: {', '.join(pokemon['types'])}"
    )

# Attach the function to the button
submit_button.config(command=getPoke)

# Pack the widgets to display them
enteruser.pack()
submit_button.pack()
poke_data_label.pack()

# Start the Tkinter event loop
window.mainloop()
