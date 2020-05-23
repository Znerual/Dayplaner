from tkinter import *

def callback_click(event):
    print("You clicked")
    canvas.move("CanvasLabel", 50, 0) #https://www.python-forum.de/viewtopic.php?t=19129

def callback_keybord(event):
    print(f"You clicked {event.char} or {event.keysym}") #keysym beinhaltet alles, also auch Return und L_Shift und soweiter

def callback_drag(event):
    canvas.moveto("CanvasLabel", event.x, event.y)
root = Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
#root.geometry(f"{screenWidth}x{screenHeight}") #maximise the window
root.geometry("400x200") #maximise the window
#root.attributes("-fullscreen", True) #make the window fullscreen

l1 = Label(root, text="Hallo Welt")
l1.pack()
l1.bind("<Button-1>", callback_click)

canvas = Canvas(root, bg="white", width= screenWidth, height= screenHeight)
canvas.bind("<Key>", callback_keybord) #https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
canvas.bind("<B1-Motion>", callback_drag)
canvas.pack()
canvas.focus_set() #der Fokus muss auf dem Element liegen, damit die Tastatur aufgenommen wird
l2 = Label(root, text= "Auf ein zweites")
l2.pack()
root.update() # damit man winfo richtig erhält

canvas.create_text(50,50, text="Hallo", tag="CanvasLabel")

print(f"{canvas.winfo_height()} x {canvas.winfo_width()} {l2.winfo_height()}")
root.mainloop()
