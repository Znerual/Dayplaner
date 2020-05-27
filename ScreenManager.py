from tkinter import *


class ScreenManager:
    canvas = None

    screenWidth = 0
    screenHeight = 0
    canvasWidth = 0
    canvasHeight = 0
    
    selected = None



    @staticmethod
    def zeitZuPixel(zeit):
        from TimeManager import TimeManager
        from Zeit import Zeit
        zeitspannePix = ScreenManager.canvasHeight / 5 * 4
        aufstehLiniePix = ScreenManager.canvasHeight / 10  # 1/10 oben 1/10 unten platz

        ratio=zeitspannePix / (TimeManager.schlafenszeit-TimeManager.aufstehzeit).inMinuten() #Pixel/Minute
        zeitNachAufstehenInMinuten = (zeit-TimeManager.aufstehzeit).inMinuten() #Zeit relativ zur Aufstehzeit
        ypixel=aufstehLiniePix + zeitNachAufstehenInMinuten * ratio
        return ypixel

    @staticmethod
    def pixelZuZeit(y):
        from TimeManager import TimeManager
        from Zeit import Zeit
        zeit = Zeit(0, 0)

        zeitspannePix = ScreenManager.canvasHeight / 5 * 4 #nutzbarer Bereich
        aufstehLiniePix = ScreenManager.canvasHeight / 10
        #rechne in Minuten
        ratio = zeitspannePix / (TimeManager.schlafenszeit - TimeManager.aufstehzeit).inMinuten()
        zeitInMinuten = (y-aufstehLiniePix)/ratio + TimeManager.aufstehzeit.inMinuten()
        zeit.vonMinuten(zeitInMinuten)
        return zeit
  

    def __init__(self):
        self.root = Tk()
        ScreenManager.screenWidth = int(self.root.winfo_screenwidth() / 3)
        ScreenManager.screenHeight = self.root.winfo_screenheight()
        self.root.geometry(f"{ScreenManager.screenWidth}x{ScreenManager.screenHeight}")
        ScreenManager.canvas = Canvas(self.root, bg="white", width=ScreenManager.screenWidth,
                                      height=ScreenManager.screenHeight)  ##ndere white zu colormanager
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.callbackLeftClick)
        self.canvas.bind("<Button-3>", self.callbackRightClick)
        self.root.update()
        ScreenManager.canvasWidth = self.canvas.winfo_width()
        ScreenManager.canvasHeight = self.canvas.winfo_height()
        #self.root.mainloop() stattdessen beim testn "run" verwenden



    def run(self):
        self.root.mainloop()

    def callbackLeftClick(self, clickEvent):
        from EventManager import EventManager
        from TimeManager import TimeManager
        from Event import Event

        if ScreenManager.selected is not None:  # auswahl für altes Element aufheben
            ScreenManager.selected.unfokusiere()

        pixel = (clickEvent.x_root, clickEvent.y_root) # oder event.x für absolute SCeen position
        # x_root ist realtiv zum canvas

        zeit = ScreenManager.pixelZuZeit(pixel[1]).runde(TimeManager.genauigkeit)  # ausgewählte Zeit, gerundet
        event = EventManager.findeEvent(zeit)
        if event is None:
            neuesEvent = EventManager.addEvent(Event(zeit, zeit + EventManager.eventLaenge))
            ScreenManager.selected = neuesEvent
        else:
            if zeit.circa(event.startzeit):
                ScreenManager.selected = event.startzeit
            elif zeit.circa(event.endzeit):
                ScreenManager.selected = event.endzeit
            else:
                ScreenManager.selected = event

        ScreenManager.selected.fokusiere()

    def callbackRightClick(self, clickEvent):
        from EventManager import EventManager
        from TimeManager import TimeManager
        from Event import Event

        if ScreenManager.selected is not None:  # auswahl für altes Element aufheben
            ScreenManager.selected.unfokusiere()

        pixel = (clickEvent.x_root, clickEvent.y_root)  # oder event.x für absolute SCeen position
        # x_root ist realtiv zum canvas

        zeit = ScreenManager.pixelZuZeit(pixel[1]).runde(TimeManager.genauigkeit)  # ausgewählte Zeit, gerundet
        event = EventManager.findeEvent(zeit)
        if event is not None:
            pause = EventManager.addPause(zeit, EventManager.pausenLaenge)
            ScreenManager.selected = pause.endzeit
            ScreenManager.selected.fokusiere()

