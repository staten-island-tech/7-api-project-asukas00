import tkinter as tk
from tkinter import messagebox
import requests
import html
import random

# ----------------------------------
# Fetch Questions from Trivia API
# ----------------------------------
def fetch_questions():
    url = "https://opentdb.com/api.php?amount=10&type=multiple"
    res = requests.get(url).json()
    
    questions = []
    
    for item in res["results"]:
        question = html.unescape(item["question"])
        correct = html.unescape(item["correct_answer"])
        incorrect = [html.unescape(ans) for ans in item["incorrect_answers"]]
        
        # Mix answers
        options = incorrect + [correct]
        random.shuffle(options)
        
        questions.append({
            "question": question,
            "options": options,
            "answer": correct
        })
    
    return questions


questions = fetch_questions()
index = 0
correct_count = 0
incorrect_count = 0


# ----------------------------------
# GUI Logic
# ----------------------------------
def handle_answer(selected):
    global index, correct_count, incorrect_count
    
    if selected == questions[index]["answer"]:
        correct_count += 1
        correct_label.config(text=f"Correct: {correct_count}")
    else:
        incorrect_count += 1
        incorrect_label.config(text=f"Incorrect: {incorrect_count}")

    index += 1

    if index < len(questions):
        load_question()
    else:
        messagebox.showinfo("Quiz Finished", 
                            f"Correct: {correct_count}\nIncorrect: {incorrect_count}")
        window.destroy()


def load_question():
    q = questions[index]
    question_label.config(text=q["question"])

    # Load button text
    for i, opt in enumerate(q["options"]):
        option_buttons[i].config(text=opt, command=lambda o=opt: handle_answer(o))


# ----------------------------------
# Tkinter UI Setup
# ----------------------------------
window = tk.Tk()
window.title("API Quiz Game")
window.geometry("500x400")

question_label = tk.Label(window, text="", font=("Arial", 16), wraplength=450)
question_label.pack(pady=20)

# Correct/Incorrect counters
counter_frame = tk.Frame(window)
counter_frame.pack()

correct_label = tk.Label(counter_frame, text="Correct: 0", font=("Arial", 12), fg="green")
correct_label.grid(row=0, column=0, padx=10)

incorrect_label = tk.Label(counter_frame, text="Incorrect: 0", font=("Arial", 12), fg="red")
incorrect_label.grid(row=0, column=1, padx=10)

# Buttons for answer choices
option_buttons = []
for _ in range(4):
    btn = tk.Button(window, text="", font=("Arial", 14), width=40)
    btn.pack(pady=5)
    option_buttons.append(btn)

load_question()
window.mainloop()
