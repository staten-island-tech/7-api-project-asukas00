import tkinter as tk
import random
from tkinter import messagebox


# -----------------------------
#        GAME DATA
# -----------------------------
ALL_CARDS = ["Knight", "Archer", "Giant", "Mini P.E.K.K.A", "Bomber"]
STARTING_CARDS = ["Knight", "Archer"]

CHEST_REWARDS = ["Wooden Chest", "Silver Chest", "Golden Chest"]


# -----------------------------
#        MAIN GAME CLASS
# -----------------------------
class ClashRoyaleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Clash Royale Prototype")

        self.cards_owned = STARTING_CARDS.copy()
        self.chests = []

        self.main_menu()

    # -------------------------
    #         MAIN MENU
    # -------------------------
    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="CLASH ROYALE PROTOTYPE",
                 font=("Arial", 24, "bold")).pack(pady=20)

        tk.Button(self.root, text="Battle", width=20,
                  command=self.start_match).pack(pady=10)

        tk.Button(self.root, text="Chests", width=20,
                  command=self.chest_screen).pack(pady=10)

        tk.Button(self.root, text="My Cards", width=20,
                  command=self.cards_screen).pack(pady=10)

    # -------------------------
    #       START MATCH
    # -------------------------
    def start_match(self):
        # Random opponent cards
        self.opponent_cards = random.sample(ALL_CARDS, 3)
        self.player_lanes = ["EMPTY", "EMPTY", "EMPTY"]
        self.opponent_lanes = ["EMPTY", "EMPTY", "EMPTY"]

        self.battle_screen()

    # -------------------------
    #        CHEST SCREEN
    # -------------------------
    def chest_screen(self):
        self.clear_window()

        tk.Label(self.root, text="CHESTS", font=("Arial", 20)).pack(pady=10)

        if not self.chests:
            tk.Label(self.root, text="No chests available. Win battles to earn more!").pack(pady=10)
        else:
            for chest in self.chests:
                tk.Button(self.root, text=f"Open {chest}",
                          command=lambda c=chest: self.open_chest(c)).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=20)

    # -------------------------
    #       OPEN CHEST
    # -------------------------
    def open_chest(self, chest):
        self.chests.remove(chest)

        unlock = random.choice(ALL_CARDS)
        new = ""

        if unlock not in self.cards_owned:
            self.cards_owned.append(unlock)
            new = f"You unlocked a NEW card: {unlock}"
        else:
            new = f"You got: {unlock} (duplicate card)"

        messagebox.showinfo("Chest Opened!", new)
        self.chest_screen()

    # -------------------------
    #         CARD SCREEN
    # -------------------------
    def cards_screen(self):
        self.clear_window()

        tk.Label(self.root, text="MY CARDS", font=("Arial", 20)).pack(pady=10)

        for c in sorted(self.cards_owned):
            tk.Label(self.root, text=c).pack()

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=20)

    # -------------------------
    #        BATTLE SCREEN
    # -------------------------
    def battle_screen(self):
        self.clear_window()

        tk.Label(self.root, text="BATTLEFIELD", font=("Arial", 20)).pack(pady=5)

        field = tk.Frame(self.root)
        field.pack(pady=10)

        # Lanes for player and opponent
        self.player_labels = []
        self.opponent_labels = []

        for i in range(3):
            tk.Label(field, text=f"Lane {i+1}", font=("Arial", 14, "bold")).pack()

            opp = tk.Label(field, text=f"Opponent: {self.opponent_lanes[i]}",
                           font=("Arial", 12), width=30)
            opp.pack()
            self.opponent_labels.append(opp)

            me = tk.Label(field, text=f"You: {self.player_lanes[i]}",
                          font=("Arial", 12), width=30)
            me.pack()
            self.player_labels.append(me)

            tk.Label(field, text="---------------").pack()

        # Player card deploy buttons
        tk.Label(self.root, text="Deploy A Card:", font=("Arial", 16)).pack(pady=5)
        card_frame = tk.Frame(self.root)
        card_frame.pack()

        for card in self.cards_owned:
            tk.Button(card_frame, text=card, width=12,
                      command=lambda c=card: self.deploy_card(c)).pack(side="left", padx=5)

        # Resolve match
        tk.Button(self.root, text="Finish Battle",
                  command=self.finish_battle).pack(pady=15)

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=20)

    # -------------------------
    #       DEPLOY CARD
    # -------------------------
    def deploy_card(self, card):
        lane_index = random.randint(0, 2)
        self.player_lanes[lane_index] = card
        self.player_labels[lane_index].config(text=f"You: {card}")

        # Opponent plays too
        opp_card = random.choice(self.opponent_cards)
        self.opponent_lanes[lane_index] = opp_card
        self.opponent_labels[lane_index].config(text=f"Opponent: {opp_card}")

    # -------------------------
    #       FINISH MATCH
    # -------------------------
    def finish_battle(self):
        score = 0

        for p, o in zip(self.player_lanes, self.opponent_lanes):
            if p == "EMPTY":
                continue
            if o == "EMPTY" or ALL_CARDS.index(p) > ALL_CARDS.index(o):
                score += 1

        if score >= 2:
            # Win → give random chest
            chest = random.choice(CHEST_REWARDS)
            self.chests.append(chest)
            messagebox.showinfo("Victory!", f"You WIN!\nYou earned a {chest}!")
        else:
            messagebox.showinfo("Defeat", "You lost the battle. Try again!")

        self.main_menu()

    # -------------------------
    #        UTILITIES
    # -------------------------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# -----------------------------
#            RUN
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x650")
    app = ClashRoyaleGame(root)
    root.mainloop()
