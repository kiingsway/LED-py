from tkinter import Tk, Canvas

window = Tk()

canvas = Canvas(window, width=300, height=300)

def clear():
    canvas.delete(ALL)

def clicked(*args):
    print("You clicked play!")

tag_atual = "playbutton"

playBtn = canvas.create_rectangle(75, 25, 225, 75, fill="red",tags="playbutton")
playTxt = canvas.create_text(150, 50, text="Play", font=("Papyrus", 26), fill='blue',tags=tag_atual)

canvas.tag_bind(tag_atual,"<Button-1>",clicked)

canvas.pack()

window.mainloop()