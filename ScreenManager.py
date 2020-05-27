from tkinter import *


class ScreenManager:
    canvas = None

    screenWidth = 0
    screenHeight = 0
    canvasWidth = 0
    canvasHeight = 0

    selected = None

    # ZeitZuPixel hat immer x = 0  und y als aktuelle Höhe
    @staticmethod
    def zeitZuPixel(zeit):
        pass

    @staticmethod
    def pixelZuZeit(y):
        pass

    def __init__(self):
        self.root = Tk()
        ScreenManager.screenWidth = self.root.winfo_screenwidth()
        ScreenManager.screenHeight = self.root.winfo_screenheight()
        self.root.geometry(f"{ScreenManager.screenWidth / 3}x{ScreenManager.screenHeight}")
        ScreenManager.canvas = Canvas(self.root, bg="green", width=self.root.winfo_width(),
                                      height=self.root.winfo_height())  ##ndere white zu colormanager
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.callbackLeftClick)
        self.canvas.bind("<Button-3>", self.callbackRightClick)
        self.root.update()
        ScreenManager.canvasWidth = self.canvas.winfo_width()
        ScreenManager.canvasHeight = self.canvas.winfo_height()

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