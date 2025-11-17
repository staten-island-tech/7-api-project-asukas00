# TETR.IO API Example
from tkinter import *
import requests
window = Tk()
window.geometry("1000x1000")
window.title =("Tetris Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12")
url = "https://tetr.io/about/api/"
headers = {
    "Content-Type": "application/json"
}

response = requests.get(url)
data = response.json()

enteruser.pack()
submit_button.pack()
window.mainloop()