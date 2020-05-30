from tkinter import *


class ScreenManager:
    root = None
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
  
    @staticmethod
    def init():
        ScreenManager.root = Tk()
        ScreenManager.root.title("Tagesplaner")
        ScreenManager.screenWidth = int(ScreenManager.root.winfo_screenwidth() / 3)
        ScreenManager.screenHeight = int(ScreenManager.root.winfo_screenheight() *0.9)
        ScreenManager.root.geometry(f"{ScreenManager.screenWidth}x{ScreenManager.screenHeight}+0+0")
        ScreenManager.canvas = Canvas(ScreenManager.root, bg="white", width=ScreenManager.screenWidth,
                                      height=ScreenManager.screenHeight)  ##ndere white zu colormanager
        ScreenManager.canvas.pack()
        ScreenManager.canvas.bind("<Button-1>", ScreenManager.callbackLeftClick)
        ScreenManager.canvas.bind("<Button-3>", ScreenManager.callbackRightClick)
        ScreenManager.root.update()
        ScreenManager.root.bind("<Configure>", ScreenManager.callbackScreenSizeChanged)
        ScreenManager.canvas.focus_set()
        ScreenManager.canvasWidth = ScreenManager.canvas.winfo_width()
        ScreenManager.canvasHeight = ScreenManager.canvas.winfo_height()

    @staticmethod
    def zeichneHintergrund():
        from TimeManager import TimeManager as TM
        from EventManager import EventManager as EM

        EM.mittagspause.zeichne()
        EM.testEvent.zeichne()
        EM.testNachmEvent.zeichne()

        #zeichne wichtige Linien
        for zeit in TM.zeiten:
           zeit.zeichne()

    def zeichneEvent(self):
        pass


    @staticmethod
    def run():
        ScreenManager.root.mainloop()

    @staticmethod
    def callbackLeftClick(clickEvent):
        from EventManager import EventManager
        from TimeManager import TimeManager
        from Event import Event

        if ScreenManager.selected is not None:  # auswahl für altes Element aufheben
            ScreenManager.selected.zeichne() #damit es neu, ohne Markierung gezeichnet wird
            ScreenManager.selected.unfokusiere()

        pixel = (clickEvent.x, clickEvent.y) # oder event.x für absolute SCeen position
        # x_root ist realtiv zum canvas

        zeit = ScreenManager.pixelZuZeit(pixel[1]).runde(TimeManager.genauigkeit)  # ausgewählte Zeit, gerundet
        event = EventManager.findeEvent(zeit)
        if event is None:
            if TimeManager.aufstehzeit <= zeit < TimeManager.schlafenszeit:
                neuesEvent = EventManager.addEvent(Event(zeit, zeit + EventManager.eventLaenge))
                ScreenManager.selected = neuesEvent
        else:
            if zeit.circa(event.startzeit):
                ScreenManager.selected = event.startzeit
            elif zeit.circa(event.endzeit):
                ScreenManager.selected = event.endzeit
            else:
                ScreenManager.selected = event

        ScreenManager.selected.zeichneMarkiert()
        ScreenManager.selected.fokusiere()

    @staticmethod
    def callbackRightClick(clickEvent):
        from EventManager import EventManager
        from TimeManager import TimeManager
        from Event import Event

        if ScreenManager.selected is not None:  # auswahl für altes Element aufheben
            ScreenManager.selected.zeichne()
            ScreenManager.selected.unfokusiere()

        pixel = (clickEvent.x, clickEvent.y)
        # x_root ist realtiv zum canvas

        zeit = ScreenManager.pixelZuZeit(pixel[1]).runde(TimeManager.genauigkeit)  # ausgewählte Zeit, gerundet
        event = EventManager.findeEvent(zeit)
        if event is not None:
            pause = EventManager.addPause(zeit, EventManager.pausenLaenge)
            pause.zeichne()
            ScreenManager.selected = pause.endzeit
            ScreenManager.selected.zeichneMarkiert()
            ScreenManager.selected.fokusiere()

    @staticmethod
    def callbackScreenSizeChanged(ScreenEvent):
        from EventManager import EventManager as EM

        #aktualisiere die Variablen
        ScreenManager.screenHeight =  ScreenEvent.height #ScreenManager.root.winfo_height()
        ScreenManager.screenWidth = ScreenEvent.width#ScreenManager.root.winfo_width()
        ScreenManager.canvasHeight = ScreenManager.screenHeight
        ScreenManager.canvasWidth = ScreenManager.screenWidth

        #passe Canvas an
        ScreenManager.canvas.configure(width=ScreenManager.canvasWidth, height=ScreenManager.canvasHeight)

        #zeichnet den Hintergrund neu, dafür muss die Mittagspause sowie die Zeit veraltet werden
        ScreenManager.veralteHintergrund()
        ScreenManager.zeichneHintergrund()

        #zeichne die Events neu
        for event in EM.events:
            event.veralten()
            event.zeichne()
        if ScreenManager.selected is not None:
            ScreenManager.selected.zeichneMarkiert()

    @staticmethod
    def veralteHintergrund():
        from EventManager import EventManager as EM
        from TimeManager import TimeManager as TM
        EM.mittagspause.veralten()
        for z in TM.zeiten:
            z.veralte()