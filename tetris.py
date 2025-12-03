from tkinter import *
import requests
window = Tk()
window.geometry("500x500")
window.title =("Chess Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg = "yellow")
chessplayerlabel = Label(window, font="Arial, 12")
def get_user(username):
    username = enteruser.get() 
    response = requests.get(f"https://api.chess.com/pub/player/{username}")
    data = response
    





submit_button.config(command=get_user)
enteruser.pack(pady=10)
submit_button.pack(pady=10)
chessplayerlabel.pack(pady=10)

window.mainloop()