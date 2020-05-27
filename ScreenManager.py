from tkinter import *


class ScreenManager:
    canvas = None
    screenWidth = 0
    screenHeight = 0
    canvasWidth = 0
    canvasHeight = 0



    @staticmethod
    def ZeitZuPixel(zeit, aufstehZeit, schlafensZeit):
        ratio=zeitspannePix/(schlafensZeit-aufstehZeit)
        pixel=aufstehLiniePix + (zeit-aufstehZeit)*ratio
        return pixel

    @staticmethod
    def PixelZuZeit(y, aufstehZeit, schlafensZeit):
        ratio=zeitspannePix/(schlafensZeit-aufstehZeit)
        zeit=(y-aufstehLiniePix)/ratio +aufstehZeit #achtung hier noch nachkommastellen in minuten umrechnen
        return zeit

    def __init__(self):
        self.root = Tk()
        ScreenManager.screenWidth = self.root.winfo_screenwidth()
        ScreenManager.screenHeight = self.root.winfo_screenheight()
        self.root.geometry(f"{ScreenManager.screenWidth/3}x{ScreenManager.screenHeight}")
        ScreenManager.canvas = Canvas(self.root, bg="green", width=self.root.winfo_width(),
                                      height=self.root.winfo_height())  ##ndere white zu colormanager
        self.canvas.pack()
        self.root.update()
        ScreenManager.canvasWidth = self.canvas.winfo_width()
        ScreenManager.canvasHeight = self.canvas.winfo_height()
        self.root.mainloop()

        zeitspannePix = ScreenManager.canvas.winfo_height() / 5 * 4
        aufstehLiniePix = ScreenManager.canvas.winfo_height() / 10  # 1/10 oben 1/10 unten platz
        schlafensLiniePix = aufstehLiniePix + zeitspannePix


