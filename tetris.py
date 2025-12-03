from tkinter import *
import requests

window = Tk()
window.geometry("500x500")
window.title("Chess Data")

enteruser = Entry(window, font="Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12", bg="yellow")
chessplayerlabel = Label(window, font="Arial, 12", justify=LEFT)


def get_user():
    username = enteruser.get().lower().strip()

    if username == "":
        chessplayerlabel.config(text="Please enter a username.", fg="red")
        return

    response = requests.get(f"https://api.chess.com/pub/player/{username}")

    if response.status_code == 200:
        data = response.json()

        # Build cleaned dictionary with real API values
        user_data = {
            "player_id": data.get("player_id", ""),
            "@id": data.get("@id", ""),
            "url": data.get("url", ""),
            "name": data.get("name", username),
            "username": data.get("username", ""),
            "followers": data.get("followers", ""),
            "country": data.get("country", ""),
            "last_online": data.get("last_online", ""),
            "joined": data.get("joined", ""),
            "status": data.get("status", ""),
            "is_streamer": data.get("is_streamer", False),
            "verified": data.get("verified", False),
            "league": data.get("league", ""),
            "streaming_platforms": data.get("streaming_platforms", [])
        }

        # Turn into readable text
        info = "\n".join([f"{k}: {v}" for k, v in user_data.items()])

        chessplayerlabel.config(text=info, fg="black")

    else:
        chessplayerlabel.config(
            text=f"Error: No player named '{username}' found.",
            fg="red"
        )


submit_button.config(command=get_user)

enteruser.pack(pady=10)
submit_button.pack(pady=10)
chessplayerlabel.pack(pady=10)

window.mainloop()
