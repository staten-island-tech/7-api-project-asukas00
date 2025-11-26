import tkinter as tk
from tkinter import ttk, messagebox
import random

class ClashSimApp:
    """
    A simplified Clash Royale Simulator featuring a main menu, 
    a battle simulation, and a chest opening mechanic.
    """
    def __init__(self, master):
        self.master = master
        master.title("Clash Sim")
        master.geometry("800x600")
        master.resizable(False, False)
        
        # --- Game State ---
        self.chests = 0
        self.total_cards_collected = 0
        self.gold_collected = 0
        self.elixir = 10
        self.elixir_loop_id = None # To manage the periodic elixir update
        
        # New Tower HP State
        self.blue_towers = {}
        self.red_towers = {}
        
        # Canvas IDs for HP text updates
        self.hp_text_ids = {}

        # --- Card Definitions (Simplified) ---
        self.CARD_SPECS = {
            "Knight": {"cost": 3, "rarity": "common", "color": "#8B4513"}, # Brown
            "Archers": {"cost": 3, "rarity": "common", "color": "#7CFC00"}, # Green
            "Goblins": {"cost": 2, "rarity": "common", "color": "#3CB371"}, # Dark Green
            "Zap": {"cost": 2, "rarity": "common", "color": "#ADD8E6"}, # Light Blue
            "Hog Rider": {"cost": 4, "rarity": "rare", "color": "#FF8C00"}, # Orange
            "Valkyrie": {"cost": 4, "rarity": "rare", "color": "#DC143C"}, # Red
            "P.E.K.K.A": {"cost": 7, "rarity": "epic", "color": "#4B0082"}, # Indigo
            "Prince": {"cost": 5, "rarity": "epic", "color": "#FFFF00"}, # Yellow
        }
        self.ALL_CARD_NAMES = list(self.CARD_SPECS.keys())
        self.deck = [] # Player's 4-card hand

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#1E1E1E')
        self.style.configure('TButton', font=('Arial', 12, 'bold'), padding=8, background='#333333', foreground='white')
        self.style.configure('Title.TLabel', font=('Arial', 28, 'bold'), foreground='#FFD700', background='#1E1E1E')
        self.style.configure('Status.TLabel', font=('Arial', 12), foreground='#AAAAAA', background='#1E1E1E')
        self.style.configure('Elixir.TLabel', font=('Arial', 14, 'bold'), foreground='#FF4500', background='#1E1E1E')
        self.style.map('TButton', background=[('active', '#555555')])
        self.style.map('Card.TButton', foreground=[('disabled', '#666666')])

        # Create the main container frame
        self.main_frame = tk.Frame(master, bg='#1E1E1E')
        self.main_frame.pack(fill='both', expand=True)

        # Initialize screen states
        self.main_menu_frame = None
        self.battle_frame = None
        self.chest_frame = None
        self.arena = None # Canvas widget for battle

        self.show_main_menu()

    def _clear_frame(self):
        """Removes all widgets from the main container frame and stops loops."""
        if self.elixir_loop_id:
            self.master.after_cancel(self.elixir_loop_id)
            self.elixir_loop_id = None
            
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def update_stats(self):
        """Updates the card and gold statistics on the main menu."""
        if self.main_menu_frame:
            self.chests_label.config(text=f"Chests Available: {self.chests}")
            self.cards_label.config(text=f"Total Cards: {self.total_cards_collected}")
            self.gold_label.config(text=f"Gold: {self.gold_collected}")
            
    # --- Battle Logic ---
    
    def _initialize_battle(self):
        """Sets up the initial state for a new battle."""
        self.elixir = 5 # Start with 5 elixir
        random.shuffle(self.ALL_CARD_NAMES)
        # Select a random 4-card hand for this simple simulator
        self.deck = self.ALL_CARD_NAMES[:4]
        
        # Reset Tower HPs (King: 2500, Princess: 1500)
        self.blue_towers = {'king': 2500, 'left': 1500, 'right': 1500}
        self.red_towers = {'king': 2500, 'left': 1500, 'right': 1500}
        
    def _update_tower_hps_visual(self):
        """Updates the HP text displayed on the arena (currently only initial display)."""
        if not self.arena or not self.hp_text_ids:
            return
            
        # This function can be expanded later if attack logic is added.
        # Blue Towers
        self.arena.itemconfig(self.hp_text_ids['b_k'], text=f"HP: {self.blue_towers['king']}")
        self.arena.itemconfig(self.hp_text_ids['b_l'], text=f"HP: {self.blue_towers['left']}")
        self.arena.itemconfig(self.hp_text_ids['b_r'], text=f"HP: {self.blue_towers['right']}")
        
        # Red Towers
        self.arena.itemconfig(self.hp_text_ids['r_k'], text=f"HP: {self.red_towers['king']}")
        self.arena.itemconfig(self.hp_text_ids['r_l'], text=f"HP: {self.red_towers['left']}")
        self.arena.itemconfig(self.hp_text_ids['r_r'], text=f"HP: {self.red_towers['right']}")

        
    def update_elixir(self):
        """Increments elixir and schedules the next update."""
        if self.elixir < 10:
            self.elixir = min(10, self.elixir + 1)
            self.elixir_label.config(text=f"ELIXIR: {self.elixir}/10")
            self._update_card_buttons()

        # Schedule the next update (Elixir regenerates every 1000ms)
        self.elixir_loop_id = self.master.after(1000, self.update_elixir)

    def _update_card_buttons(self):
        """Checks elixir and enables/disables card buttons."""
        for i, card_name in enumerate(self.deck):
            cost = self.CARD_SPECS[card_name]['cost']
            button = self.card_buttons[i]
            if cost <= self.elixir:
                button.config(state='normal')
            else:
                button.config(state='disabled')

    def play_card(self, card_name):
        """Spends elixir and places a unit on the canvas."""
        cost = self.CARD_SPECS[card_name]['cost']
        if self.elixir >= cost:
            self.elixir -= cost
            self.elixir_label.config(text=f"ELIXIR: {self.elixir}/10")
            
            # 1. Visual Placement (Player side, below the bridge)
            x = random.randint(50, 450) # Random x position across the width
            y = random.randint(200, 320) # Random y position (Player side, bottom half)
            unit_color = self.CARD_SPECS[card_name]['color']
            
            self.arena.create_oval(x - 10, y - 10, x + 10, y + 10, 
                                   fill=unit_color, 
                                   outline="#FFFFFF", 
                                   width=2)
            # Changed text color to black for better contrast
            self.arena.create_text(x, y, text=str(cost), fill="black", font=('Arial', 8, 'bold')) 
            
            # 2. Update button states
            self._update_card_buttons()
        
    # --- Screen Methods ---

    def show_main_menu(self):
        """Displays the main game menu."""
        self._clear_frame()
        self.main_menu_frame = ttk.Frame(self.main_frame, padding="20")
        self.main_menu_frame.pack(pady=50)

        # Title
        ttk.Label(self.main_menu_frame, text="CLASH SIMULATOR", style='Title.TLabel').pack(pady=20)
        
        # Stats Display
        stats_frame = ttk.Frame(self.main_menu_frame)
        stats_frame.pack(pady=20, padx=10, fill='x')
        
        self.chests_label = ttk.Label(stats_frame, text=f"Chests Available: {self.chests}", style='Status.TLabel')
        self.chests_label.pack(pady=5, padx=10, anchor='w')
        
        self.cards_label = ttk.Label(stats_frame, text=f"Total Cards: {self.total_cards_collected}", style='Status.TLabel')
        self.cards_label.pack(pady=5, padx=10, anchor='w')

        self.gold_label = ttk.Label(stats_frame, text=f"Gold: {self.gold_collected}", style='Status.TLabel')
        self.gold_label.pack(pady=5, padx=10, anchor='w')

        # Action Buttons
        ttk.Button(self.main_menu_frame, text="Start Battle", command=self.show_battle_screen, width=20).pack(pady=15)
        
        if self.chests > 0:
            ttk.Button(self.main_menu_frame, text=f"Open Chest ({self.chests})", command=self.show_chest_screen, width=20, style='TButton', ).pack(pady=15)
        else:
            # Placeholder/Disabled button if no chests
            ttk.Label(self.main_menu_frame, text="No chests to open. Win a battle!", style='Status.TLabel').pack(pady=15)


    def show_battle_screen(self):
        """Displays the interactive battle screen."""
        self._clear_frame()
        self.battle_frame = ttk.Frame(self.main_frame, padding="20")
        self.battle_frame.pack(fill='both', expand=True)

        self._initialize_battle() # Setup deck, elixir, and HPs

        ttk.Label(self.battle_frame, text="BATTLE ARENA", style='Title.TLabel').pack(pady=10)
        
        # Elixir Display
        self.elixir_label = ttk.Label(self.battle_frame, text=f"ELIXIR: {self.elixir}/10", style='Elixir.TLabel')
        self.elixir_label.pack(pady=5)
        
        # Battle Visual Representation (Simplified Arena)
        # Increased height to fit 3 towers and HP text
        self.arena = tk.Canvas(self.battle_frame, width=500, height=350, bg="#3366FF", highlightthickness=0)
        self.arena.pack(pady=10)
        
        # --- Arena Drawing ---
        
        # River/Middle Line (Bridge)
        self.arena.create_line(0, 175, 500, 175, fill="#FFFFFF", width=3, dash=(5, 5))
        
        # Lane Divider (emphasizing 2 lanes)
        self.arena.create_line(250, 0, 250, 350, fill="#FFFFFF", width=1, dash=(3, 3))
        
        # Blue Towers (Bottom/Player Side)
        # Princess Left (1500 HP)
        self.arena.create_rectangle(50, 250, 150, 350, fill="#0000FF", tags="tower")
        self.hp_text_ids['b_l'] = self.arena.create_text(100, 235, text=f"HP: {self.blue_towers['left']}", fill="#00FF00", font=('Arial', 8, 'bold'))
        # Princess Right (1500 HP)
        self.arena.create_rectangle(350, 250, 450, 350, fill="#0000FF", tags="tower")
        self.hp_text_ids['b_r'] = self.arena.create_text(400, 235, text=f"HP: {self.blue_towers['right']}", fill="#00FF00", font=('Arial', 8, 'bold'))
        # King Tower (2500 HP)
        self.arena.create_rectangle(200, 300, 300, 350, fill="#0000FF", tags="tower")
        self.hp_text_ids['b_k'] = self.arena.create_text(250, 285, text=f"HP: {self.blue_towers['king']}", fill="#00FF00", font=('Arial', 8, 'bold'))
        
        # Red Towers (Top/Opponent Side)
        # Princess Left (1500 HP)
        self.arena.create_rectangle(50, 0, 150, 100, fill="#FF0000", tags="tower")
        self.hp_text_ids['r_l'] = self.arena.create_text(100, 115, text=f"HP: {self.red_towers['left']}", fill="#00FF00", font=('Arial', 8, 'bold'))
        # Princess Right (1500 HP)
        self.arena.create_rectangle(350, 0, 450, 100, fill="#FF0000", tags="tower")
        self.hp_text_ids['r_r'] = self.arena.create_text(400, 115, text=f"HP: {self.red_towers['right']}", fill="#00FF00", font=('Arial', 8, 'bold'))
        # King Tower (2500 HP)
        self.arena.create_rectangle(200, 0, 300, 50, fill="#FF0000", tags="tower")
        self.hp_text_ids['r_k'] = self.arena.create_text(250, 65, text=f"HP: {self.red_towers['king']}", fill="#00FF00", font=('Arial', 8, 'bold'))
        
        # Card Hand Frame
        card_hand_frame = ttk.Frame(self.battle_frame)
        card_hand_frame.pack(pady=15)
        
        self.card_buttons = []
        for card_name in self.deck:
            cost = self.CARD_SPECS[card_name]['cost']
            # Create a button with card name and cost
            button_text = f"{card_name}\n({cost} Elixir)"
            btn = ttk.Button(card_hand_frame, 
                             text=button_text, 
                             command=lambda c=card_name: self.play_card(c), 
                             width=12, 
                             style='Card.TButton')
            btn.pack(side='left', padx=5)
            self.card_buttons.append(btn)
        
        self._update_card_buttons() # Set initial disabled state
        self.update_elixir() # Start the elixir generation loop

        # End Battle Button
        ttk.Button(self.battle_frame, text="End Battle & See Result", command=self.simulate_battle, width=25).pack(pady=20)
        ttk.Button(self.battle_frame, text="Back to Menu", command=self.show_main_menu, width=25).pack(pady=5)


    def show_chest_screen(self):
        """Displays the chest opening screen."""
        if self.chests == 0:
            messagebox.showinfo("Wait!", "You have no chests to open yet. Win a battle!")
            self.show_main_menu()
            return

        self._clear_frame()
        self.chest_frame = ttk.Frame(self.main_frame, padding="20")
        self.chest_frame.pack(fill='both', expand=True)

        ttk.Label(self.chest_frame, text="CHEST OPENING", style='Title.TLabel').pack(pady=20)
        
        # Visual of a chest (using styled text as a simple visual)
        chest_visual = tk.Label(self.chest_frame, text="[TREASURE CHEST]", 
                                font=('Courier New', 40, 'bold'), fg='#FFD700', bg='#1E1E1E')
        chest_visual.pack(pady=40)
        
        self.chest_info_label = ttk.Label(self.chest_frame, 
                                          text=f"You have {self.chests} chests available.", 
                                          style='Status.TLabel')
        self.chest_info_label.pack(pady=10)
        
        # Result Display Area
        self.result_text = tk.Text(self.chest_frame, height=10, width=50, state='disabled', bg='#2E2E2E', fg='#00FF00', font=('Courier New', 12))
        self.result_text.pack(pady=20)

        self.open_button = ttk.Button(self.chest_frame, text="Open Chest", command=self.open_chest, width=20)
        self.open_button.pack(pady=15)
        
        ttk.Button(self.chest_frame, text="Back to Menu", command=self.show_main_menu, width=20).pack(pady=10)


    # --- Game Logic ---

    def simulate_battle(self):
        """Simulates a battle outcome (random win/loss)."""
        # Stop the elixir loop before leaving the screen
        if self.elixir_loop_id:
            self.master.after_cancel(self.elixir_loop_id)
            self.elixir_loop_id = None
            
        outcome = random.choice(["win", "loss", "draw"])
        
        if outcome == "win":
            self.chests += 1
            messagebox.showinfo("Victory!", "You won the battle! You earned one Chest!")
        elif outcome == "loss":
            messagebox.showinfo("Defeat!", "You lost the battle. Better luck next time!")
        else:
            messagebox.showinfo("Draw!", "The battle ended in a tie. No rewards.")

        self.show_main_menu()

    def open_chest(self):
        """Deducts a chest and generates random rewards."""
        if self.chests <= 0:
            return

        self.chests -= 1
        rewards = self._generate_rewards()
        
        # Update text area with results
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "--- CHEST OPENED ---\n\n")
        
        # Display Gold
        self.result_text.insert(tk.END, f"💰 {rewards['gold']} Gold\n")
        self.gold_collected += rewards['gold']
        
        # Display Cards
        for card, count in rewards['cards'].items():
            self.result_text.insert(tk.END, f"🃏 {count}x {card}\n")
            self.total_cards_collected += count
            
        self.result_text.insert(tk.END, "\n--- REWARD COMPLETE ---")
        self.result_text.config(state='disabled')
        
        self.update_stats()
        self.chest_info_label.config(text=f"You have {self.chests} chests available.")

        if self.chests == 0:
            self.open_button.config(state='disabled')
            messagebox.showinfo("Empty Chest Queue", "All chests opened! Time for more battles.")


    def _generate_rewards(self):
        """Generates a random set of rewards from a 'Silver Chest' equivalent."""
        
        # 1. Gold Reward
        gold = random.randint(50, 150)
        
        # 2. Card Rewards (5-10 cards total)
        total_cards = random.randint(5, 10)
        cards = {}
        cards_added = 0
        
        # Ensure at least one common card
        common_cards = [c for c, spec in self.CARD_SPECS.items() if spec['rarity'] == 'common']
        rare_cards = [c for c, spec in self.CARD_SPECS.items() if spec['rarity'] == 'rare']
        epic_cards = [c for c, spec in self.CARD_SPECS.items() if spec['rarity'] == 'epic']
        
        cards[random.choice(common_cards)] = 1
        cards_added += 1

        while cards_added < total_cards:
            rarity_roll = random.random()
            
            if rarity_roll < 0.70: # 70% chance Common
                card_pool = common_cards
                max_count = 3
            elif rarity_roll < 0.95: # 25% chance Rare
                card_pool = rare_cards
                max_count = 1
            else: # 5% chance Epic
                card_pool = epic_cards
                max_count = 1
            
            # Skip if the pool is empty (shouldn't happen with current setup)
            if not card_pool:
                break
                
            chosen_card = random.choice(card_pool)
            
            # Decide how many to grant (up to remaining total or max per rarity)
            count = min(random.randint(1, max_count), total_cards - cards_added)
            
            if count > 0:
                cards[chosen_card] = cards.get(chosen_card, 0) + count
                cards_added += count
                
        return {"gold": gold, "cards": cards}


# Main execution block
if __name__ == '__main__':
    root = tk.Tk()
    app = ClashSimApp(root)
    root.mainloop()