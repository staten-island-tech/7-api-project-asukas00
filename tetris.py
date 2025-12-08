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
        chess = enteruser.get() 
        data = requests.get(f"https://api.chess.com/pub/player/{chess.lower()}")
        info = data.json()

        if data.status_code == 200:
            display_text = (
                f"avatar:{info.get['avatar']}",
                f"name:  {info.get['name']}",
                f"username: {info.get['username']}"
                f"title: {info.get['title']}",
                f"League: {info.get['league']}",
                f"Location: {info.get['location']}",
                f"Url: {info.get['url']}",
                f"record:{info.get['record']}"
            )
            chessplayerlabel.config(text= display_text , bg = "black")

        
        if  data.status_code != 200:
            error_message = f"Error: No player named '{chess.lower()}' found. Try again."
            chessplayerlabel.config(text=error_message, fg="red")


    except requests.ConnectionError:
       chessplayerlabel.config(text="Connection Error: Could not connect to the API.", fg="red")


submit_button.config(command=get_user)


enteruser.pack(pady=10)
submit_button.pack(pady=10)
chessplayerlabel.pack(pady=10)

window.mainloop()
