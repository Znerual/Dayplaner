#from tkinter import *


class ScreenManager:
    canvas = None
    screenWidth = 0
    screenHeight = 0

    def __init__(self):
        self.root = Tk()
        ScreenManager.screenWidth = self.root.winfo_width()
        ScreenManager.screenHeight = self.root.winfo_height()
        self.root.geometry(f"{ScreenManager.screenWidth}x{ScreenManager.screenHeight}")
        ScreenManager.canvas = Canvas(self.root, bg="white", width=ScreenManager.screenWidth,
                                      height=ScreenManager.screenHeight)  ##ndere white zu colormanager
