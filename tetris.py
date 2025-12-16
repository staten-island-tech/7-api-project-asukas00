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


        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(
            f"https://api.chess.com/pub/player/{chess}",
            headers=headers
        )

        if response.status_code == 200:
            info = response.json()

            display_text = (
                f"Avatar: {info.get('avatar', 'N/A')}\n"
                f"Name: {info.get('name', 'N/A')}\n"
                f"Username: {info.get('username', 'N/A')}\n"
                f"Status: {info.get('status', 'N/A')}\n"
                f"Location: {info.get('location', 'N/A')}\n"
                f"URL: {info.get('url', 'N/A')}"
            )

            chessplayerlabel.config(text=display_text, fg="black")

        else:
            chessplayerlabel.config(
                text=f"Error: No player named '{chess}' found.",
                fg="red"
            )

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



