from tkinter import Tk, Canvas, Frame, BOTH, Label

LED_COUNT = 120

root = Tk()

Label(root,text='Horizontal').grid(row=0,column=0)
canvas1 = Canvas(root)
canvas1.create_rectangle(10, 20, 30, 40,outline="#fb0", fill="#fb0")
canvas1.create_rectangle(40, 20, 60, 40,outline="#f50", fill="#f50")
canvas1.create_rectangle(70, 20, 90, 40,outline="#05f", fill="#05f")
canvas1.grid(row=1,column=0)

Label(root,text='Vertical').grid(row=2,column=0)
canvas1 = Canvas(root)
canvas1.create_rectangle(10, 20, 30, 40,outline="#fb0", fill="#fb0")
canvas1.create_rectangle(10, 50, 30, 70,outline="#f50", fill="#f50")
canvas1.create_rectangle(10, 80, 30, 100,outline="#05f", fill="#05f")
canvas1.grid(row=3,column=0)

Label(root,text='Horizontal 120').grid(row=0,column=1)
canvas1 = Canvas(root)
for led in range(LED_COUNT):
    base = 30*led
    canvas1.create_rectangle(10+base, 20, 30+base, 40,outline="#000", fill="#000")
canvas1.grid(row=1,column=1)

Label(root,text='Vertical 120').grid(row=2,column=1)
canvas1 = Canvas(root)
for led in range(LED_COUNT):
    base = 30*led
    canvas1.create_rectangle(10, 20+base, 30, 40+base,outline="#000", fill="#000")
canvas1.grid(row=3,column=1)

root.mainloop()