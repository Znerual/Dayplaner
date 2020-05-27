from tkinter import *


class ScreenManager:
    canvas = None
    screenWidth = 0
    screenHeight = 0
    canvasWidth = 0
    canvasHeight = 0



    @staticmethod
    def ZeitZuPixel(zeit):
        from TimeManager import TimeManager
        from Zeit import Zeit
        zeitspannePix = ScreenManager.canvasHeight / 5 * 4
        aufstehLiniePix = ScreenManager.canvasHeight / 10  # 1/10 oben 1/10 unten platz
        deci1=Zeit.ZeitzuDecimal(TimeManager.schlafenszeit-TimeManager.aufstehzeit)
        ratio=zeitspannePix/deci1
        deci2=Zeit.ZeitzuDecimal(zeit-TimeManager.aufstehzeit)
        ypixel=aufstehLiniePix + deci2*ratio
        return ypixel

    @staticmethod
    def PixelZuZeit(y):
        from TimeManager import TimeManager
        from Zeit import Zeit
        zeitspannePix = ScreenManager.canvasHeight / 5 * 4
        aufstehLiniePix = ScreenManager.canvasHeight / 10
        deci1 = Zeit.ZeitzuDecimal(TimeManager.schlafenszeit-TimeManager.aufstehzeit)
        ratio = zeitspannePix / deci1
        tmp=(y-aufstehLiniePix)/ratio +Zeit.ZeitzuDecimal(TimeManager.aufstehzeit)
        zeit=Zeit.DecimalzuZeit(tmp)
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
        #self.root.mainloop() stattdessen beim testn "run" verwenden


