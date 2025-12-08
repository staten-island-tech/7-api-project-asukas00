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
        data = requests.get(f"https://api.chess.com/pub/player/{chess.capitalize}")
        

        if data.status_code == 200:
            display_text = (
                f"avatar: {data['avatar']}",
                f"name:  {data['name']}",
                f"username: {data['username']}"
                f"League: {data['league']}",
                f"Location: {data['location']},"
                f"Url: {data['url']}"
            )
            chessplayerlabel.config(text= display_text , bg = "black")

        
        if not data.status_code == 200:
            error_message = f"Error: No player named '{chess.capitalize()}' found. Try again."
            chessplayerlabel.config(text=error_message, fg="red")


    except requests.ConnectionError:
       chessplayerlabel.config(text="Connection Error: Could not connect to the API.", fg="red")


submit_button.config(command=get_user)


enteruser.pack(pady=10)
submit_button.pack(pady=10)
chessplayerlabel.pack(pady=10)

window.mainloop()
