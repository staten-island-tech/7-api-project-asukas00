from tkinter import *
window = Tk()
window.geometry("1000x1000")
window.title =("Tetris Data")
enteruser = Entry(window, font = "Arial, 12")
submit_button = Button(window, text="Submit Data", font="Arial, 12")
submit_button.pack()
window.mainloop()