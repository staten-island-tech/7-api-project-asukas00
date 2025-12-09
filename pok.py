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
        chess = enteruser.get().strip().lower()

        # Chess.com API requires User-Agent header
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(
            f"https://api.chess.com/pub/player/{chess}",
            headers=headers
        )

        if response.status_code == 200:
            info = response.json()

            return info

        chessplayerlabel.config(text=info, bg="black", fg="white")



    except requests.ConnectionError:
        chessplayerlabel.config(
            text="Connection Error: Could not connect to the API.",
            fg="red"
        )

submit_button.config(command=get_user)

enteruser.pack(pady=10)
submit_button.pack(pady=10)
chessplayerlabel.pack(pady=10)

window.mainloop()
