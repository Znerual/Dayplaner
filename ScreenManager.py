from tkinter import *


class ScreenManager:
    canvas = None
    screenWidth = 0
    screenHeight = 0
    canvasWidth = 0
    canvasHeight = 0

    # ZeitZuPixel hat immer x = 0  und y als aktuelle Höhe
    @staticmethod
    def ZeitZuPixel(zeit):
        pass

    @staticmethod
    def PixelZuZeit(y):
        pass

    def __init__(self):
        self.root = Tk()
        ScreenManager.screenWidth = self.root.winfo_screenwidth()
        ScreenManager.screenHeight = self.root.winfo_screenheight()
        self.root.geometry(f"{ScreenManager.screenWidth / 3}x{ScreenManager.screenHeight}")
        ScreenManager.canvas = Canvas(self.root, bg="green", width=self.root.winfo_width(),
                                      height=self.root.winfo_height())  ##ndere white zu colormanager
        self.canvas.pack()
        self.root.update()
        ScreenManager.canvasWidth = self.canvas.winfo_width()
        ScreenManager.canvasHeight = self.canvas.winfo_height()
        self.root.mainloop()
