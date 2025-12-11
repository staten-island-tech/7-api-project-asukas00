import tkinter as tk
import random
import pygame

# ----------------------------
# SOUND SETUP
# ----------------------------
pygame.mixer.init()
def play_sound(file):
    try:
        sound = pygame.mixer.Sound(file)
        sound.play()
    except Exception as e:
        print("Error playing sound:", e)

# ----------------------------
# STORY CUTSCENES
# ----------------------------
intro_story = [
    "In the year 2099, Brainrot levels have reached catastrophic levels.",
    "Ohio has expanded into 78% of the Earth.",
    "NPCs walk the streets speaking only in Skibidi Tongue.",
    "Humanity's last hope: YOU — the chosen Sigma.",
    "To ascend, you must prove mastery over all brainrot knowledge.",
    "Your journey begins now..."
]

mid_story_events = [
    "A mysterious Rizzler appears and nods approvingly.",
    "You pass by an NPC. It whispers: 'skibidi dop dop yes yes'. You ignore it.",
    "A Gyatt Shockwave shakes the ground. You remain unbothered.",
    "Fanum tries to tax your snacks, but you sidestep flawlessly.",
    "A GigaChad statue glows as you walk past. You feel stronger."
]

boss_intro = [
    "🔥 The sky cracks open…",
    "🔥 Reality glitches into Ohio Form…",
    "🔥 A 900-foot Skibidi Titan rises from the ground…",
    "It is THE OHIO OVERLORD.",
    "He speaks in a deep voice:",
    "\"Only the TRUE SIGMA may pass beyond this point…\""
]

# ----------------------------
# QUESTIONS (50 brainrot)
# ----------------------------
questions = [
{"q":"What’s the correct response to someone saying 'gyatt'?","o":["Rizz them up","Touch some grass","Skibidi Ohio moment","Who asked"],"a":"Rizz them up"},
{"q":"What is the opposite of ‘L’?","o":["W","Sigma","Fanum Tax","Ohio"],"a":"W"},
{"q":"If someone says 'That's so skibidi', how do you respond?","o":["Yes yes yes","No cap","Rizz?","What the sigma"],"a":"Yes yes yes"},
{"q":"Who is the ultimate sigma?","o":["Patrick Bateman","Skibidi Toilet","The Rizzler","Goofy Ahh Uncle"],"a":"Patrick Bateman"},
{"q":"What is the national food of Ohio?","o":["Toilet water","Corn dog","Gyatt nuggets","Air"],"a":"Toilet water"},
{"q":"What does ‘NPC’ mean?","o":["Non-player character","Not playing cool","No point clown","Neutral processing cloud"],"a":"Non-player character"},
{"q":"Which is the biggest red flag?","o":["No rizz","Velcro shoes","Says 'skibidi' unironically","Fortnite default dance"],"a":"Says 'skibidi' unironically"},
{"q":"Who invented rizz?","o":["Kai Cenat","Mr Beast","Walter White","Fanum"],"a":"Kai Cenat"},
{"q":"What does ‘fanum tax’ mean?","o":["Food theft","Ohio tax law","Sigma points","Gym membership"],"a":"Food theft"},
{"q":"What is peak fiction?","o":["Skibidi Toilet Saga","Breaking Bad","Ohio Chronicles","Rizz Academy"],"a":"Breaking Bad"},
{"q":"What is the most sigma activity?","o":["Staring at a wall","Grinding at 4AM","Nodding silently","Touching grass"],"a":"Grinding at 4AM"},
{"q":"What does ‘delulu’ mean?","o":["Delusional","Delicious","Delicate","Delighted"],"a":"Delusional"},
{"q":"Who is the real skibidi rizzler?","o":["You","The guy behind you","Sigma cat","Ohio goblin"],"a":"You"},
{"q":"Where is the most sigma place?","o":["The gym","Ohio","Your room at 3AM","The void"],"a":"The gym"},
{"q":"Natural predator of the NPC?","o":["Sigma male","Gyatt enjoyer","Toilet titan","W-rizzler"],"a":"Sigma male"},
{"q":"Correct greeting for a Skibidi Toilet?","o":["Yes yes yes","Flush it","Run","Gyatt"],"a":"Yes yes yes"},
{"q":"Greatest threat to humanity?","o":["Ohio","The toilets","No rizz","Grass"],"a":"Ohio"},
{"q":"Correct response to 'Rizz me'?","o":["Light work","Nah bro","Skibidi","Call Ohio"],"a":"Light work"},
{"q":"Sigma Meal?","o":["Raw chicken","Protein shake","Cold shower water","Air"],"a":"Protein shake"},
{"q":"Gyatt Level Max?","o":["100","999","∞","Ohio"],"a":"∞"},
{"q":"If someone says 'skibidi bop', how do you respond?","o":["Yes yes yes","No cap","Bruh","Sigma silence"],"a":"Yes yes yes"},
{"q":"Who can survive a Gyatt Shockwave?","o":["True Sigma","NPC","Ohio citizen","Rizzling fanum"],"a":"True Sigma"},
{"q":"What is the sacred Ohio relic?","o":["Corn dog","Gyatt nugget","Skibidi toilet paper","Rizz crown"],"a":"Corn dog"},
{"q":"If someone calls you a 'simp', what do you do?","o":["Laugh","Ignore","Deploy Rizz","Cry"],"a":"Deploy Rizz"},
{"q":"What is forbidden in Sigma protocol?","o":["Talking to NPCs","Touching grass","Not rizzing","Eating fanum"],"a":"Not rizzing"},
{"q":"Best time to grind for rizz?","o":["4 AM","Noon","Midnight","8 PM"],"a":"4 AM"},
{"q":"Which is ultimate power move?","o":["Silent nod","Rizz deployment","Skibidi bop","Gyatt dodge"],"a":"Rizz deployment"},
{"q":"Fanum appears with snacks, you:","o":["Give them","Steal them","Ignore","Rizz past"],"a":"Steal them"},
{"q":"Skibidi Toilet calls you:","o":["Yes yes yes","Sigma bro","Fanum","NPC"],"a":"Yes yes yes"},
{"q":"What weapon defeats NPCs?","o":["Rizz","Corn dog","Skibidi dance","Gyatt bomb"],"a":"Rizz"},
{"q":"Highest rizz score achievable?","o":["∞","999","100","Ohio"],"a":"∞"},
{"q":"What is the ultimate red flag?","o":["No rizz","Velcro shoes","Talking to Ohio","Bringing water"],"a":"No rizz"},
{"q":"Which is most sigma:","o":["Ignoring chaos","Touching grass","Grinding","Sleeping"],"a":"Grinding"},
{"q":"The Skibidi anthem is:","o":["Yes yes yes","No cap","Bruh","Skibidi bop"],"a":"Yes yes yes"},
{"q":"If someone asks for 'fanum tax', you:","o":["Pay","Run","Rizz attack","Laugh"],"a":"Rizz attack"},
{"q":"Ohio Overlord's favorite food?","o":["Corn dog","Gyatt nugget","Air","Rizz juice"],"a":"Corn dog"},
{"q":"What unlocks infinite rizz?","o":["Grinding","Meditation","NPC defeat","Skipping breakfast"],"a":"Grinding"},
{"q":"True Sigma knows:","o":["Skibidi bop is life","NPCs talk","Fanum never pays","Ohio is safe"],"a":"Skibidi bop is life"},
{"q":"Gyatt Energy Source?","o":["Corn","Air","Rizz","Toilet water"],"a":"Rizz"},
{"q":"The ultimate Sigma statue is made of:","o":["Concrete","Gyatt nuggets","Corn","Skibidi toilet"],"a":"Gyatt nuggets"},
{"q":"If NPC attacks, you:","o":["Rizz counter","Run","Cry","Call Ohio"],"a":"Rizz counter"},
{"q":"Best counter to Ohio Overlord?","o":["Discipline","Infinite Rizz","Corn dog","Skibidi bop"],"a":"Discipline"},
{"q":"Most forbidden phrase in Sigma land?","o":["No rizz","Yes yes yes","Bruh","Skibidi bop"],"a":"No rizz"},
{"q":"If you hear 'Fanum tax', react:","o":["Steal snacks","Run","Ignore","Deploy Rizz"],"a":"Steal snacks"},
{"q":"What is Ohio's secret weapon?","o":["Skibidi Toilets","NPC horde","Gyatt bomb","Corn dog"],"a":"Skibidi Toilets"},
{"q":"If Skibidi sings, you:","o":["Join","Ignore","Fight","Cry"],"a":"Join"},
{"q":"Final Gyatt challenge is:","o":["Endless grind","Infinite Rizz","Skibidi bop","Fanum tax"],"a":"Endless grind"},
{"q":"True Sigma never:","o":["Touches grass","Deploys Rizz","Grinds","Sings skibidi"],"a":"Touches grass"},
{"q":"NPC horde approaches, you:","o":["Rizz counter","Run","Hide","Cry"],"a":"Rizz counter"},
{"q":"Most OP move?","o":["Gyatt strike","Infinite Rizz","Skibidi bop","Fanum dodge"],"a":"Infinite Rizz"},
{"q":"If Ohio Overlord laughs, you:","o":["Rizz forward","Retreat","Dance","Meditate"],"a":"Rizz forward"},
{"q":"The secret to peak fiction?","o":["Breaking Bad","Fanum","Gyatt","Ohio"],"a":"Breaking Bad"},
{"q":"Maximum Sigma hours per day?","o":["4","6","8","24"],"a":"4"},
{"q":"What breaks NPC control?","o":["Rizz","Corn dog","Skibidi bop","Air"],"a":"Rizz"},
{"q":"Final test before boss?","o":["Level 10","All Rizz deployed","Infinite XP","Touch grass"],"a":"All Rizz deployed"},
{"q":"The last Gyatt artifact is:","o":["Corn","Skibidi crown","Fanum","NPC mask"],"a":"Skibidi crown"},
{"q":"Who guards the final rizz?","o":["Ohio Overlord","NPC horde","Fanum","Skibidi toilet"],"a":"Ohio Overlord"}
]

random.shuffle(questions)

# ----------------------------
# FINAL BOSS QUESTION
# ----------------------------
final_boss = {
    "q": "THE OHIO OVERLORD ASKS:\n\"WHAT IS THE TRUE SOURCE OF SIGMA POWER?\"",
    "o": ["Discipline", "Ohio Radiation", "Infinite Rizz", "Skibidi Ancestry"],
    "a": "Discipline"
}

# ----------------------------
# LEVEL SYSTEM
# ----------------------------
level = 1
xp = 0
xp_needed = 5

def add_xp():
    global xp, level, xp_needed
    xp += 1
    if xp >= xp_needed:
        xp = 0
        level += 1
        xp_needed += 3
        play_sound("levelup.wav")
        show_story(random.choice(mid_story_events))
    level_label.config(text=f"Level: {level}  |  XP: {xp}/{xp_needed}")

# ----------------------------
# TKINTER UI
# ----------------------------
root = tk.Tk()
root.title("🧠 Brainrot Quiz — Story + Sound")
root.geometry("650x550")
root.config(bg="#111")

idx = -1
score = 0
btns = []

# ----------------------------
# STORY RENDERER
# ----------------------------
def show_story(text, next_action=None):
    for b in btns: b.destroy()
    btns.clear()
    question_label.config(text=text)
    next_btn = tk.Button(root, text="Continue →", bg="#333", fg="white",
                         font=("Arial", 13), width=20,
                         command=next_action or continue_quiz)
    next_btn.pack(pady=20)
    btns.append(next_btn)

def start_story():
    if intro_story:
        line = intro_story.pop(0)
        show_story(line, next_action=start_story)
    else:
        continue_quiz()

# ----------------------------
# QUIZ LOGIC
# ----------------------------
def continue_quiz():
    global idx
    idx += 1
    if idx < len(questions):
        load_question(questions[idx])
    else:
        start_boss_story()

def load_question(qdata):
    if qdata is final_boss:
        load_boss_question()
        return
    question_label.config(text=qdata["q"])
    for b in btns: b.destroy()
    btns.clear()
    for option in qdata["o"]:
        b = tk.Button(root, text=option, bg="#222", fg="white", font=("Arial", 13),
                      width=40, command=lambda o=option: check_answer(qdata, o))
        b.pack(pady=6)
        btns.append(b)

def check_answer(qdata, selected):
    global score
    if selected == qdata["a"]:
        score += 1
        play_sound("correct.wav")
        add_xp()
    else:
        play_sound("wrong.wav")
    continue_quiz()

# ----------------------------
# BOSS FIGHT
# ----------------------------
def start_boss_story():
    if boss_intro:
        line = boss_intro.pop(0)
        show_story(line, next_action=start_boss_story)
    else:
        play_sound("boss.wav")
        load_question(final_boss)

def load_boss_question():
    qdata = final_boss
    question_label.config(text=qdata["q"])
    for b in btns: b.destroy()
    btns.clear()
    for option in qdata["o"]:
        b = tk.Button(root, text=option, bg="#440000", fg="white", font=("Arial", 13),
                      width=40, command=lambda o=option: check_answer_boss(o))
        b.pack(pady=6)
        btns.append(b)

def check_answer_boss(selected):
    global score
    if selected == final_boss["a"]:
        score += 1
        play_sound("correct.wav")
    else:
        play_sound("wrong.wav")
    end_game()

def end_game():
    for b in btns: b.destroy()
    if score > len(questions) * 0.6:
        ending = (
            "🔥 YOU DEFEATED THE OHIO OVERLORD 🔥\n"
            "You have restored balance to the world.\n"
            "NPCs regain speech.\n"
            "Ohio shrinks back to normal size.\n"
            "You are crowned the TRUE SIGMA."
        )
    else:
        ending = (
            "💀 The Ohio Overlord consumes reality.\n"
            "The world becomes a Skibidi wasteland.\n"
            "Your rizz was not enough.\n"
            "The NPCs claim your soul."
        )
    question_label.config(text=f"FINAL SCORE: {score}/{len(questions)+1}\nLevel: {level}\n\n{ending}")

# ----------------------------
# UI ELEMENTS
# ----------------------------
level_label = tk.Label(root, text=f"Level: {level}  |  XP: {xp}/{xp_needed}",
                       bg="#111", fg="white", font=("Arial", 14))
level_label.pack(pady=10)

question_label = tk.Label(root, text="", bg="#111", fg="white",
                          font=("Arial", 16, "bold"), wraplength=550)
question_label.pack(pady=20)

# Start the game
start_story()

root.mainloop()
