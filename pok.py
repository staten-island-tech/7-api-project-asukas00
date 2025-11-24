from tkinter import *
import requests

## ⚙️ Tkinter Setup
window = Tk()
window.geometry("500x500")
# FIX: Use the title() method
window.title("Pokemon Data")

# --- Widgets ---
enteruser = Entry(window, font="Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg = "yellow")
# Add justify and wraplength for better text display
poke_datalabel = Label(window, font="Arial, 12", justify=LEFT, wraplength=450)

# --- Functionality ---
def getPoke():
    """Fetches Pokémon data from the PokeAPI and updates the GUI label."""
    poke_name_input = enteruser.get().strip()
    
    # 1. Input Validation
    if not poke_name_input:
        poke_datalabel.config(text="Please enter a Pokémon name or ID.", fg="red")
        return

    # Set loading message
    poke_datalabel.config(text=f"Fetching data for {poke_name_input.capitalize()}...", fg="blue")
    window.update_idletasks()

    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_name_input.lower()}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Process data into a dictionary
            pokemon_data = {
                "name": data["name"].capitalize(),
                "id": data["id"],
                "height": data["height"] / 10,  # Convert decimeters to meters
                "weight": data["weight"] / 10,  # Convert hectograms to kilograms
                "types": [t["type"]["name"].capitalize() for t in data["types"]]
            }
            
            type_str = ", ".join(pokemon_data["types"])
            
            # 2. FIX: Create the display string directly
            display_text = (
                f"Pokémon: {pokemon_data['name']} (ID: {pokemon_data['id']})\n"
                f"Height: {pokemon_data['height']} m\n"
                f"Weight: {pokemon_data['weight']} kg\n"
                f"Types: {type_str}"
            )
            
            # 2. FIX: Update the label using the config method
            poke_datalabel.config(text=display_text, fg="black")
            
        else:
            # Error Case: Pokemon not found (HTTP 404)
            error_message = f"Error: No Pokémon named '{poke_name_input.capitalize()}' found. Try again."
            poke_datalabel.config(text=error_message, fg="red")

    except requests.exceptions.ConnectionError:
        poke_datalabel.config(text="Connection Error: Could not connect to the API.", fg="red")
        
# --- Main Logic ---
submit_button.config(command=getPoke)

# Place widgets on the window
enteruser.pack(pady=10)
submit_button.pack(pady=5)
poke_datalabel.pack(pady=20)

window.mainloop()