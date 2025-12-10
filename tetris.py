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
        headers = {"User-Agent": "Mozilla/5.0"} #i asked chatgpt why chess API didn't work and gpt said I needed a header

        response = requests.get(
            f"https://api.chess.com/pub/player/{chess}",
            headers=headers
        )
        if response.status_code == 200:
            info = response.json()
            display_text = (
                f"name: {info['name']}\n",
                f"player_id: {info['player_id']}\n",
                f"username: {info['username']}\n",
                f"title: {info['title']}\n",
                f"League: {info['league']}\n",
                f"Location: {info['location']}\n",
                f"Url: {info['url']}\n",
                
            )
            for info in display_text:
                Label(window, text = info).pack() 
        
        if  response.status_code != 200:
            error_message = f"Error: No player named '{chess.lower()}' found. Try again."
            chessplayerlabel.config(text=error_message, fg="red")


    except requests.ConnectionError:
       chessplayerlabel.config(text="Connection Error: Could not connect to the API.", fg="red")


submit_button.config(command=get_user)


enteruser.pack(pady=10)
submit_button.pack(pady=10)
chessplayerlabel.pack(pady=10)

window.mainloop()




