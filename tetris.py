from tkinter import *
import requests
window = Tk()
window.geometry("500x500")
window.title =("Pokemon Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg = "yellow")
chessplayerlabel = Label(window, font="Arial, 12")
def get_user(name):
    name = enteruser.get()  
    response = requests.get(f"https://lichess.org/player{name.lower()}")
    data = response.json()
    if response.status_code == 200:
        display_text = (
            f"Pokémon: {data['name']} (ID: {data['id']})",
            f"Height: {data['height']}",
            f"Weight: {data['weight']}",
            f"Types: {data['types']}"
        )
    chessplayerlabel.config(text=display_text, fg="black")


submit_button.config(command=get_user)
enteruser.pack(pady=10)
submit_button.pack(pady=10)
chessplayerlabel.pack(pady=10)

window.mainloop()