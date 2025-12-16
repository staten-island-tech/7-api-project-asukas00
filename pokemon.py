import tkinter as tk
import requests
from PIL import Image, ImageTk # Requires the 'Pillow' library
from io import BytesIO

# --- Configuration ---
CHESS_API_BASE = "https://api.chess.com/pub/player/"
USERNAME = "hikaru" # Example: Hikaru Nakamura

# Global reference to hold the image object, preventing garbage collection
# This is CRITICAL in Tkinter when displaying images.
current_avatar_img = None 
avatar_label = None # Will hold the Tkinter Label widget

def load_avatar(username):
    """
    Fetches the avatar URL, downloads the image, and updates the Tkinter Label.
    """
    global current_avatar_img, avatar_label

    try:
        # 1. Fetch Player Data to get the Avatar URL
        player_url = f"{CHESS_API_BASE}{username}"
        player_response = requests.get(player_url, timeout=10)
        player_response.raise_for_status() # Raise error for bad status codes (4xx or 5xx)
        player_data = player_response.json()
        
        avatar_url = player_data.get("avatar")
        
        if not avatar_url:
            print(f"Error: No avatar URL found for user {username}")
            status_var.set(f"User '{username}' found, but no avatar available.")
            return

        # 2. Download the Image Data
        image_response = requests.get(avatar_url, timeout=10)
        image_response.raise_for_status()
        
        # 3. Convert Bytes to Tkinter PhotoImage (using Pillow)
        image_data = image_response.content
        img = Image.open(BytesIO(image_data))
        
        # Optional: Resize the image for display (e.g., to 100x100)
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        
        # Convert the PIL image to a Tkinter PhotoImage object
        photo_img = ImageTk.PhotoImage(img)
        
        # 4. Display the Image in the Label
        if avatar_label:
            # Update the existing label
            avatar_label.config(image=photo_img)
            
            # CRITICAL: Keep a reference to the PhotoImage object. 
            # If you don't, Python's garbage collector will delete it, 
            # and the label will appear empty.
            current_avatar_img = photo_img 
            
            status_var.set(f"Avatar loaded for {username}")

    except requests.exceptions.HTTPError as err:
        status_var.set(f"HTTP Error: Player '{username}' not found or API failed.")
        print(f"HTTP Error: {err}")
    except requests.exceptions.RequestException as err:
        status_var.set(f"Connection Error: Check API URL or internet connection.")
        print(f"Connection Error: {err}")
    except Exception as e:
        status_var.set(f"An unexpected error occurred: {e}")
        print(f"Unexpected Error: {e}")


# --- Tkinter Setup ---
root = tk.Tk()
root.title("Chess.com Avatar Viewer")

# Input field for username
tk.Label(root, text="Enter Chess.com Username:").pack(pady=5)
username_var = tk.StringVar(value=USERNAME)
username_entry = tk.Entry(root, textvariable=username_var, width=30)
username_entry.pack(pady=5)

# Button to trigger the image load
load_button = tk.Button(root, 
                        text="Load Avatar", 
                        command=lambda: load_avatar(username_var.get()))
load_button.pack(pady=10)

# Label to display the avatar (starts empty)
avatar_label = tk.Label(root, text="(Avatar appears here)")
avatar_label.pack(pady=10, padx=10)

# Status message label
status_var = tk.StringVar(value="Ready.")
status_label = tk.Label(root, textvariable=status_var, fg="gray")
status_label.pack(pady=5)

# Load the default avatar immediately on startup
load_avatar(USERNAME)

root.mainloop()