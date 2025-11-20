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
    data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke.lower()}")
    pokemon = {
        "name": data["name"].capitalize(),
        "height": data["height"],
        "weight": data["weight"],
        "types": [t["type"]["name"] for t in data["types"]]
    }  
    if  data != 200:
        poke_data_label.config(text="Error fetching data!")
        return None
    if data == poke:
        poke_data_label.config(text=f"{pokemon}")


    # Update the label with the fetched Pokémon data


# Attach the function to the button
submit_button.config(command=getPoke)

# Pack the widgets to display them
enteruser.pack()
submit_button.pack()
poke_data_label.pack()

# Start the Tkinter event loop
window.mainloop()
