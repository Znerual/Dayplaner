from tkinter import *


class ScreenManager:
    root = None
    canvas = None

    screenWidth = 0
    screenHeight = 0
    canvasWidth = 0
    canvasHeight = 0
    
    ausgewaehlt = None

    inputAnzeige = None
    inputText = ""

    datumAnzeige = None

    @staticmethod
    def zeitZuPixel(zeit):
        from TimeManager import TimeManager
        from Zeit import Zeit
        zeitspannePix = ScreenManager.canvasHeight / 5 * 4
        aufstehLiniePix = ScreenManager.canvasHeight / 10  # 1/10 oben 1/10 unten platz

        ratio=zeitspannePix / (TimeManager.schlafenszeit-TimeManager.aufstehzeit).zeitInMinuten() #Pixel/Minute
        zeitNachAufstehenInMinuten = (zeit-TimeManager.aufstehzeit).zeitInMinuten() #Zeit relativ zur Aufstehzeit
        ypixel=aufstehLiniePix + zeitNachAufstehenInMinuten * ratio
        return ypixel

    @staticmethod
    def pixelZuZeit(y):
        from TimeManager import TimeManager
        from Zeit import Zeit
        zeit = Zeit(0, 0, TimeManager.aktuellesDatum.datum)

        zeitspannePix = ScreenManager.canvasHeight / 5 * 4 #nutzbarer Bereich
        aufstehLiniePix = ScreenManager.canvasHeight / 10
        #rechne in Minuten
        ratio = zeitspannePix / (TimeManager.schlafenszeit - TimeManager.aufstehzeit).zeitInMinuten()
        zeitInMinuten = (y-aufstehLiniePix)/ratio + TimeManager.aufstehzeit.zeitInMinuten()
        zeit.vonMinuten(zeitInMinuten)
        return zeit
  
    @staticmethod
    def init():
        from TimeManager import TimeManager
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
        ScreenManager.inputAnzeige = ScreenManager.canvas.create_text(20, int(ScreenManager.canvasHeight - 20), text="Input:", anchor=SW)
        ScreenManager.datumAnzeige = ScreenManager.canvas.create_text(ScreenManager.canvasWidth/2, 20, text=TimeManager.aktuellesDatum.erhalteDatumLang())
        ScreenManager.canvas.bind("<Key>", ScreenManager.keyInput)
    @staticmethod
    def zeichneHintergrund():
        from TimeManager import TimeManager as TM
        from EventManager import EventManager as EM
        from Zeit import Zeit

        #passe Mittagspause an
        EM.mittagspause.startzeit.set(TM.mittagspauseStart)
        EM.mittagspause.endzeit.set(TM.mittagspauseEnde)
        EM.mittagspause.zeichne()

        #zeichne wichtige Linien
        for zeit in TM.zeiten:
            zeit.zeichne()

        #passe Genauigkeit an die neue Skalierung an, runde danach auf schöne 5 Min Intervalle
        TM.genauigkeit.vonMinuten((TM.schlafenszeit - TM.aufstehzeit).zeitInMinuten() / TM.genauigkeitsfaktor)
        TM.genauigkeit = TM.genauigkeit.runde(Zeit(0,5, None))

        #Inputanzeige und Datumanzeige korrekt verschieben
        ScreenManager.canvas.coords(ScreenManager.inputAnzeige,20, int(ScreenManager.canvasHeight - 20))
        ScreenManager.canvas.coords(ScreenManager.datumAnzeige,int(ScreenManager.canvasWidth/2), 20,)

    @staticmethod
    def run():
        ScreenManager.root.mainloop()

    @staticmethod
    def select(zeit):
        from TimeManager import TimeManager
        from EventManager import EventManager
        from Event import Event

        gefundeneZeit = TimeManager.findeZeit(zeit)
        if gefundeneZeit is not None:
            gefundeneZeit.zeichneMarkiert()
            ScreenManager.ausgewaehlt = gefundeneZeit
            ScreenManager.ausgewaehlt.fokusiere()
            return
        event = EventManager.findeEvent(zeit, TimeManager.genauigkeit)
        if event is None:
            zeit = zeit.runde()
            # ändere das Datum des neuen Events auf das Datum von akutellesDatum im TimeManager
            #zeit.datum = TimeManager.aktuellesDatum.datum
            if TimeManager.aufstehzeit <= zeit < TimeManager.schlafenszeit:
                neuesEvent = EventManager.addEvent(Event(zeit, zeit + EventManager.eventLaenge))
                ScreenManager.ausgewaehlt = neuesEvent
            else:
                return
        else:
            if zeit.circa(event.startzeit):
                ScreenManager.ausgewaehlt = event.startzeit
            elif zeit.circa(event.endzeit):
                ScreenManager.ausgewaehlt = event.endzeit
            else:
                ScreenManager.ausgewaehlt = event
        ScreenManager.ausgewaehlt.zeichneMarkiert()
        ScreenManager.ausgewaehlt.fokusiere()
    @staticmethod
    def callbackLeftClick(clickEvent):
        from EventManager import EventManager
        from TimeManager import TimeManager
        from Event import Event

        #TODO: Problem wenn <Key> Callback auf Text oder Zeit aktiviert ist und dann ein anderes Objekt ausgewählt wird

        if ScreenManager.ausgewaehlt is not None:  # auswahl für altes Element aufheben
            ScreenManager.ausgewaehlt.zeichne() #damit es neu, ohne Markierung gezeichnet wird
            ScreenManager.ausgewaehlt.unfokusiere()

        pixel = (clickEvent.x, clickEvent.y)
        zeit = ScreenManager.pixelZuZeit(pixel[1])  # ausgewählte Zeit, gerundet
        ScreenManager.select(zeit)


    @staticmethod
    def callbackRightClick(clickEvent):
        from EventManager import EventManager
        from TimeManager import TimeManager
        from Event import Event

        if ScreenManager.ausgewaehlt is not None:  # auswahl für altes Element aufheben
            ScreenManager.ausgewaehlt.zeichne()
            ScreenManager.ausgewaehlt.unfokusiere()

        pixel = (clickEvent.x, clickEvent.y)
        # x_root ist realtiv zum canvas

        zeit = ScreenManager.pixelZuZeit(pixel[1]).runde(TimeManager.genauigkeit)  # ausgewählte Zeit, gerundet
        event = EventManager.findeEvent(zeit)
        if event is not None:
            pause = EventManager.addPause(zeit, EventManager.pausenLaenge)
            pause.zeichne()
            ScreenManager.ausgewaehlt = pause.endzeit
            ScreenManager.ausgewaehlt.zeichneMarkiert()
            ScreenManager.ausgewaehlt.fokusiere()

    @staticmethod
    def keyInput(keyEvent):
        from Zeit import Zeit
        from TimeManager import TimeManager
        from EventManager import EventManager
        from Event import Event

        if keyEvent.keysym == "Return":
            #Parse different input
            zeit = Zeit.fromString(ScreenManager.inputText)
            zeit1, zeit2 = Zeit.intervalFromString(ScreenManager.inputText)

            #reset the input Text
            ScreenManager.inputText = ""
            if zeit is not None:
                ScreenManager.select(zeit)
                zeit.datum = TimeManager.aktuellesDatum.datum
            elif zeit1 is not None and zeit2 is not None:
                zeit1.datum = zeit2.datum = TimeManager.aktuellesDatum.datum
                if (TimeManager.aufstehzeit <= zeit1 < TimeManager.mittagspauseStart and zeit1 < zeit2 <= TimeManager.mittagspauseStart ) or (TimeManager.mittagspauseEnde <= zeit1 < TimeManager.schlafenszeit and zeit1 < zeit2 <= TimeManager.schlafenszeit):
                    neuesEvent = EventManager.addEvent(Event(zeit1, zeit2))
                    ScreenManager.ausgewaehlt = neuesEvent
                    ScreenManager.ausgewaehlt.zeichneMarkiert()
                    ScreenManager.ausgewaehlt.fokusiere()
                else:
                    ScreenManager.inputText = "Invalid Input for Interval"

        elif keyEvent.keysym == "BackSpace":
            ScreenManager.inputText = ScreenManager.inputText[:-1]
        elif keyEvent.keysym == "Delete":
            pass
        elif keyEvent.keysym == "Right":
            EventManager.speichereEvents()
            TimeManager.aktuellesDatum.verschiebeAufMorgen()
            for event in EventManager.events:
                event.verstecke()
            EventManager.ladeEvents()
            ScreenManager.canvas.itemconfig(ScreenManager.datumAnzeige, text=TimeManager.aktuellesDatum.erhalteDatumLang())
        elif keyEvent.keysym == "Left":
            EventManager.speichereEvents()
            TimeManager.aktuellesDatum.verschiebeAufGestern()
            for event in EventManager.events:
                event.verstecke()
            EventManager.ladeEvents()
            ScreenManager.canvas.itemconfig(ScreenManager.datumAnzeige, text=TimeManager.aktuellesDatum.erhalteDatumLang())
        else:
            ScreenManager.inputText += keyEvent.char
        ScreenManager.canvas.itemconfig(ScreenManager.inputAnzeige, text=f"Input: {ScreenManager.inputText}")

    @staticmethod
    def zeichneEventsNeu():
        from EventManager import EventManager as EM
        for event in EM.events:
            event.zeichne()
        if ScreenManager.ausgewaehlt is not None:
            ScreenManager.ausgewaehlt.zeichneMarkiert()

    @staticmethod
    def callbackScreenSizeChanged(ScreenEvent):
        from EventManager import EventManager as EM

        #aktualisiere die Variablen
        ScreenManager.screenHeight = ScreenEvent.height #ScreenManager.root.winfo_height()
        ScreenManager.screenWidth = ScreenEvent.width#ScreenManager.root.winfo_width()
        ScreenManager.canvasHeight = ScreenManager.screenHeight
        ScreenManager.canvasWidth = ScreenManager.screenWidth

        #passe Canvas an
        ScreenManager.canvas.configure(width=ScreenManager.canvasWidth, height=ScreenManager.canvasHeight)

        #zeichnet den Hintergrund neu
        ScreenManager.zeichneHintergrund()

        #zeichne die Events neu
        ScreenManager.zeichneEventsNeu()

    #TODO: Key callback falls nichts ausgewählt ist, dass die Auswahl mit der Tastatur zulösst und neue Events
    #erstellen lösst. Außerdem optional noch falls man +drückt das Event um die danach eingegebene Zeit verschiebt
