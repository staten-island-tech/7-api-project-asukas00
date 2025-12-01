from tkinter import *
import requests
window = Tk()
window.geometry("500x500")
window.title =("Pokemon Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg = "yellow")
poke_datalabel = Label(window, font="Arial, 12")
def get_user(name):
    name = enteruser.get()  
    response = requests.get(f"https://lichess.org/player{name.lower()}")
    data = response.json()

