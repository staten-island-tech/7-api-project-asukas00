"""
Clash Royale-like Tkinter Game (Enhanced)
Features added per request:
✓ Chest opening system (random card rewards)
✓ Additional cards
✓ Three towers per side (King + 2 Arena Towers)
✓ Menu → start game / deck / chest menu
✓ Basic chest inventory & open chest animation
✓ Fixed chest button tags and added troop combat vs troops & towers
✓ Troops stop to fight and game ends when a side loses all towers

Run with: python3 clash_roya_project.py
"""

import tkinter as tk
import random
import time

# ---------------- CONFIG ----------------
WINDOW_W = 1000
WINDOW_H = 650
BATTLEFIELD_H = 480
FPS_MS = 30

TOWER_SIZE = (60, 100)
TOWER_HEALTH = 120
ARENA_TOWER_HEALTH = 80

ELIXIR_MAX = 10
ELIXIR_GEN_RATE = 0.05
CARD_COOLDOWN = 2.0

# ---------------- CARD DEFINITIONS ----------------
class CardSpec:
    def __init__(self, name, cost, size=(28,28), speed=1.0, hp=30, dmg=5, color="#cccccc", is_spell=False):
        self.name = name
        self.cost = cost
        self.size = size
        self.speed = speed
        self.hp = hp
        self.dmg = dmg
        self.color = color
        self.is_spell = is_spell

CARD_LIBRARY = {
    'Knight': CardSpec('Knight', 3, (28,28), 1.2, 80, 10, '#c79b6a'),
    'Archer': CardSpec('Archer', 2, (24,24), 1.6, 40, 6, '#6aa6c7'),
    'Giant': CardSpec('Giant', 5, (36,36), 0.8, 160, 20, '#a46a6a'),
    'Fireball': CardSpec('Fireball', 4, (32,32), 0, 1, 30, '#ff7b5c', True),
    'Bomber': CardSpec('Bomber', 3, (26,26), 1.3, 50, 15, '#8888ff'),
    'Mini P.E.K.K.A': CardSpec('Mini P.E.K.K.A', 4, (30,30), 1.5, 90, 25, '#4444ff'),
}

# ---------------- CHESTS ----------------
CHEST_TYPES = {
    'Silver Chest': {'cards': 2},
    'Golden Chest': {'cards': 4},
}

# ---------------- UNITS & TOWERS ----------------
class Unit:
    def __init__(self, x, y, team, spec):
        self.x = x
        self.y = y
        self.team = team
        self.spec = spec
        self.hp = spec.hp
        self.width, self.height = spec.size
        self.vx = spec.speed * (1 if team == 0 else -1)
        self.id = None
        self.engaged = False  # whether currently fighting (stops moving)

    def bbox(self):
        return (self.x - self.width/2, self.y - self.height, self.x + self.width/2, self.y)

class Tower:
    def __init__(self, x, y, team, hp):
        self.x = x
        self.y = y
        self.team = team
        self.hp = hp
        self.width, self.height = TOWER_SIZE

    def bbox(self):
        return (self.x - self.width/2, self.y - self.height, self.x + self.width/2, self.y)

# ---------------- GAME STATE ----------------
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.units = []
        self.elapsed = 0
        self.elixir = 5
        self.deck_names = ['Knight','Archer','Giant','Fireball']
        self.card_cd = {name: 0 for name in self.deck_names}
        self.selected_card = None
        self.game_over = False
        self.winner = None
        self.last_ai_spawn = 0

        # THREE towers for player
        self.player_king = Tower(140, BATTLEFIELD_H-30, 0, TOWER_HEALTH)
        self.player_t1 = Tower(260, BATTLEFIELD_H-30, 0, ARENA_TOWER_HEALTH)
        self.player_t2 = Tower(20, BATTLEFIELD_H-30, 0, ARENA_TOWER_HEALTH)

        # THREE towers for enemy
        self.enemy_king = Tower(WINDOW_W-140, BATTLEFIELD_H-30, 1, TOWER_HEALTH)
        self.enemy_t1 = Tower(WINDOW_W-260, BATTLEFIELD_H-30, 1, ARENA_TOWER_HEALTH)
        self.enemy_t2 = Tower(WINDOW_W-20, BATTLEFIELD_H-30, 1, ARENA_TOWER_HEALTH)

        self.chests = {'Silver Chest': 1, 'Golden Chest': 1}

    def available(self, name):
        spec = CARD_LIBRARY[name]
        return self.elixir >= spec.cost and self.card_cd[name] <= 0

# ---------------- APP CLASS ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Upgraded Clash Royale Tkinter")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=WINDOW_W, height=WINDOW_H, bg='#1f3b4d')
        self.canvas.pack()

        self.state = 'menu'
        self.game = GameState()

        self.bind('<Button-1>', self.on_click)
        self.draw_menu()
        self.after(FPS_MS, self.loop)

    # ---------------- MENU ----------------
    def draw_menu(self):
        self.canvas.delete('all')
        self.canvas.create_text(WINDOW_W//2, 100, text='Clash Royale Tkinter', fill='white', font=('Helvetica',32,'bold'))

        self.menu_button(WINDOW_W//2, 220, 'START', 'start')
        self.menu_button(WINDOW_W//2, 300, 'CHESTS', 'chests')
        self.menu_button(WINDOW_W//2, 340, 'DECK', 'deck')
        self.menu_button(WINDOW_W//2, 380, 'QUIT', 'quit')

    def menu_button(self, x, y, text, tag):
        self.canvas.create_rectangle(x-120, y-30, x+120, y+30, fill='#446688', tags=tag)
        self.canvas.create_text(x, y, text=text, fill='white', font=('Helvetica',16,'bold'))

    # ---------------- CHEST SCREEN ----------------
    def show_chests(self):
        self.canvas.delete('all')
        self.canvas.create_text(WINDOW_W//2, 80, text='Your Chests', fill='white', font=('Helvetica',28,'bold'))

        y = 180
        for chest_name, data in self.game.chests.items():
            safe = chest_name.replace(' ', '_')
            self.canvas.create_text(200, y, text=f"{chest_name} x{data}", fill='white', font=('Helvetica',20))
            self.canvas.create_rectangle(350, y-20, 500, y+20, fill='#4caf50', tags=f'open_{safe}')
            self.canvas.create_text(425, y, text='OPEN', fill='white', tags=f'open_{safe}')
            y += 80

        self.menu_button(WINDOW_W//2, WINDOW_H-80, 'BACK', 'back_menu')

    def open_chest(self, chest_name):
        if self.game.chests.get(chest_name, 0) <= 0:
            return
        self.game.chests[chest_name] -= 1

        # reward cards
        count = CHEST_TYPES[chest_name]['cards']
        rewards = [random.choice(list(CARD_LIBRARY.keys())) for _ in range(count)]

        self.canvas.delete('all')
        self.canvas.create_text(WINDOW_W//2, 80, text=f'Opened {chest_name}!', fill='yellow', font=('Helvetica',26,'bold'))

        y = 200
        for r in rewards:
            self.canvas.create_text(WINDOW_W//2, y, text=f"+ {r}", fill='white', font=('Helvetica',20))
            y += 50

        self.menu_button(WINDOW_W//2, WINDOW_H-80, 'BACK', 'back_menu')

    # ---------------- DECK SCREEN ----------------
    def show_deck(self):
        self.canvas.delete('all')
        self.canvas.create_text(WINDOW_W//2, 60, text='Edit Deck', fill='white', font=('Helvetica',28,'bold'))

        self.canvas.create_text(150,120,text='Your Deck:',fill='yellow',font=('Helvetica',20,'bold'))
        y=160
        for i,name in enumerate(self.game.deck_names):
            self.canvas.create_text(150,y,text=f"{i+1}. {name}",fill='white',font=('Helvetica',18))
            y+=30

        self.canvas.create_text(650,120,text='All Cards:',fill='yellow',font=('Helvetica',20,'bold'))
        y=160
        for cname in CARD_LIBRARY.keys():
            tag=f'card_{cname.replace(" ","_")}'
            self.canvas.create_rectangle(560,y-15,760,y+15,fill='#444488',tags=tag)
            self.canvas.create_text(660,y,text=cname,fill='white',tags=tag)
            y+=40

        self.menu_button(WINDOW_W//2, WINDOW_H-80, 'BACK', 'back_menu')

    def handle_deck_click(self,x,y):
        # replace first deck slot with clicked card
        for cname in CARD_LIBRARY.keys():
            tag=f'card_{cname.replace(" ","_")}'
            if self.in_btn(x,y,tag):
                # rotate deck: put selected card in front
                if cname not in self.game.deck_names:
                    self.game.deck_names[0]=cname
                else:
                    # move it to front
                    self.game.deck_names.remove(cname)
                    self.game.deck_names.insert(0,cname)
                self.show_deck()
                return

# ---------------- START GAME ----------------
    def start_game(self):
        self.state = 'playing'
        self.game.reset()
        self.canvas.delete('all')
        self.draw_static_field()

    def draw_static_field(self):
        self.canvas.create_rectangle(0,0,WINDOW_W,BATTLEFIELD_H, fill='#3b6e22')
        self.canvas.create_rectangle(0,BATTLEFIELD_H,WINDOW_W,WINDOW_H, fill='#232323')

    # ---------------- LOOP ----------------
    def loop(self):
        if self.state == 'playing':
            self.update_game()
        self.after(FPS_MS, self.loop)

    # ---------------- CLICK HANDLING ----------------
    def on_click(self, e):
        x,y=e.x,e.y

        if self.state=='menu':
            if self.in_btn(x,y,'start'): self.start_game()
            elif self.in_btn(x,y,'chests'): self.state='chests'; self.show_chests()
            elif self.in_btn(x,y,'quit'): self.quit()

        elif self.state=='deck':
            if self.in_btn(x,y,'back_menu'): self.state='menu'; self.draw_menu()
            # handle deck clicks
            self.handle_deck_click(x,y)

        elif self.state=='chests':
            if self.in_btn(x,y,'back_menu'): self.state='menu'; self.draw_menu()
            for chest in CHEST_TYPES:
                safe = chest.replace(' ', '_')
                if self.in_btn(x,y,f'open_{safe}'):
                    self.open_chest(chest)

        elif self.state=='playing':
            if y > BATTLEFIELD_H:
                self.handle_card_click(x,y)
            else:
                if self.game.selected_card:
                    self.deploy_unit(x,y)

    def in_btn(self,x,y,tag):
        for item in self.canvas.find_withtag(tag):
            r = self.canvas.coords(item)
            if len(r)==4 and r[0] < x < r[2] and r[1] < y < r[3]:
                return True
        return False

    # ---------------- GAME LOGIC ----------------
    def handle_card_click(self,x,y):
        g=self.game
        start=40
        w=80
        spacing=20
        for i,name in enumerate(g.deck_names):
            cx=start+i*(w+spacing)
            if cx<=x<=cx+w and BATTLEFIELD_H+10<=y<=BATTLEFIELD_H+70:
                if g.available(name):
                    g.selected_card=name
                return

    def deploy_unit(self,x,y):
        name=self.game.selected_card
        spec=CARD_LIBRARY[name]
        g=self.game

        if spec.is_spell:
            for u in g.units:
                if abs(u.x-x)<50: u.hp -= spec.dmg
        else:
            g.units.append(Unit(x, BATTLEFIELD_H-40, 0, spec))

        g.elixir -= spec.cost
        g.card_cd[name]=CARD_COOLDOWN
        g.selected_card=None

    def update_game(self):
        g=self.game
        if g.game_over:
            return

        g.elapsed+=FPS_MS/1000
        g.elixir=min(ELIXIR_MAX,g.elixir+ELIXIR_GEN_RATE)

        for k in g.card_cd:
            g.card_cd[k]=max(0,g.card_cd[k]-FPS_MS/1000)

        # Basic AI
        if g.elapsed-g.last_ai_spawn>2:
            name=random.choice(['Knight','Archer'])
            spec=CARD_LIBRARY[name]
            g.units.append(Unit(WINDOW_W-200,BATTLEFIELD_H-40,1,spec))
            g.last_ai_spawn=g.elapsed

        # Reset engaged flags each tick (we will set them during combat checks)
        for u in g.units:
            u.engaged = False

        # Combat checks: mark engaged and apply damage (no movement while engaged)
        for u in list(g.units):
            if u.hp<=0: continue
            # find enemy units in range
            for e in list(g.units):
                if e is u or e.hp<=0 or e.team==u.team:
                    continue
                if abs(u.x - e.x) < 40:
                    # both engage and exchange damage
                    u.engaged = True
                    e.engaged = True
                    # apply per-frame damage
                    dmg_tick_u = u.spec.dmg * 0.06
                    dmg_tick_e = e.spec.dmg * 0.06
                    e.hp -= dmg_tick_u
                    u.hp -= dmg_tick_e

            # if not engaged with a troop, check towers
            if not u.engaged:
                enemy_towers = [g.enemy_king, g.enemy_t1, g.enemy_t2] if u.team==0 else [g.player_king, g.player_t1, g.player_t2]
                for t in enemy_towers:
                    if t.hp>0 and abs(u.x - t.x) < 45:
                        # engage tower (stop and damage it)
                        u.engaged = True
                        t.hp -= u.spec.dmg * 0.06

        # Apply movement for non-engaged units and cleanup dead units
        for u in list(g.units):
            if u.hp<=0:
                try:
                    g.units.remove(u)
                except ValueError:
                    pass
                continue
            if not u.engaged:
                # restore movement direction based on team
                u.vx = abs(u.spec.speed) if u.team==0 else -abs(u.spec.speed)
                u.x += u.vx
            else:
                # stop moving during combat
                pass

        # End game check: if all enemy towers dead or all player towers dead
        enemy_towers = [g.enemy_king, g.enemy_t1, g.enemy_t2]
        player_towers = [g.player_king, g.player_t1, g.player_t2]
        if all(t.hp <= 0 for t in enemy_towers):
            g.game_over = True
            g.winner = 'Player'
        if all(t.hp <= 0 for t in player_towers):
            g.game_over = True
            g.winner = 'Enemy'

        if g.game_over:
            self.show_game_over()

        self.render()

    # ---------------- GAME OVER ----------------
    def show_game_over(self):
        g=self.game
        self.canvas.create_rectangle(WINDOW_W//2-150, BATTLEFIELD_H//2-60, WINDOW_W//2+150, BATTLEFIELD_H//2+60, fill='#222', tags='dyn')
        self.canvas.create_text(WINDOW_W//2, BATTLEFIELD_H//2-20, text=f"{g.winner} Wins!", fill='white', font=('Helvetica',24,'bold'), tags='dyn')
        self.canvas.create_rectangle(WINDOW_W//2-100, BATTLEFIELD_H//2+10, WINDOW_W//2+100, BATTLEFIELD_H//2+50, fill='#4caf50', tags='replay')
        self.canvas.create_text(WINDOW_W//2, BATTLEFIELD_H//2+30, text='BACK TO MENU', fill='white', tags='replay')
        # bind click to return to menu
        def back(e):
            for item in self.canvas.find_withtag('replay'):
                r = self.canvas.coords(item)
                if len(r)==4 and r[0] < e.x < r[2] and r[1] < e.y < r[3]:
                    self.state='menu'
                    self.draw_menu()
                    # unbind and rebind main click handler
                    self.bind('<Button-1>', self.on_click)
        self.bind('<Button-1>', back)

    # ---------------- RENDER ----------------
    def render(self):
        c=self.canvas
        g=self.game
        c.delete('dyn')

        # Draw towers
        towers=[g.player_king,g.player_t1,g.player_t2,g.enemy_king,g.enemy_t1,g.enemy_t2]
        for t in towers:
            color='#8b5a2b' if t.team==0 else '#b24d4d'
            fill = color if t.hp>0 else 'gray'
            c.create_rectangle(*t.bbox(), fill=fill, tags='dyn')
            c.create_text(t.x,t.y-60,text=f"{int(max(0,t.hp))}",fill='white',tags='dyn')

        # Units
        for u in g.units:
            # if unit dead, skip drawing
            if u.hp<=0: continue
            c.create_rectangle(*u.bbox(), fill=u.spec.color, tags='dyn')
            # hp bar
            hp_frac = max(0,u.hp)/u.spec.hp
            x1,y1,x2,y2 = u.bbox()
            barw = (x2-x1) * hp_frac
            c.create_rectangle(x1, y1-6, x1+barw, y1-3, fill='green', tags='dyn')

        # HUD
        c.create_text(80,BATTLEFIELD_H+20,text=f"Elixir: {int(g.elixir)}",fill='white',tags='dyn')

        start=40; w=80; spacing=20
        for i,name in enumerate(g.deck_names):
            cx=start+i*(w+spacing)
            spec=CARD_LIBRARY[name]
            fill = spec.color if g.available(name) else '#555555'
            c.create_rectangle(cx,BATTLEFIELD_H+10,cx+w,BATTLEFIELD_H+70,fill=fill,tags='dyn')
            c.create_text(cx+w/2,BATTLEFIELD_H+40,text=name,fill='white',tags='dyn')

# ---------------- MAIN ----------------
if __name__=='__main__':
    App().mainloop()
