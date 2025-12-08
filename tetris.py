from tkinter import *
import requests

window = Tk()
window.geometry("500x500")
window.title("Chess Data")

enteruser = Entry(window, font="Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg="yellow")
chessplayerlabel = Label(window, font="Arial, 12")


def get_user():

  
    try:
        response = requests.get(f"https://api.chess.com/pub/player/{username}")
        
        if response.status_code == 200:
            data = response.json()









    if username == "":
        chessplayerlabel.config(text="Please enter a username.", fg="red")
        return

    except:
        


submit_button.config(command=get_user)

enteruser.pack(pady=10)
submit_button.pack(pady=10)
chessplayerlabel.pack(pady=10)

window.mainloop()
