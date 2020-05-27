from Objekt import Objekt


class Event(Objekt):

    def __init__(self, startzeit, endzeit, istPause=False):
        self.startzeit = startzeit
        self.endzeit = endzeit

        self.startzeit.setEvent(self)
        self.endzeit.setEvent(self)

        self.text = ""
        self.eventDavor = None
        self.eventDanach = None
        self.form = []

        self.istPause = istPause

    def __str__(self):
        return f"Start {self.startzeit.stunde:02}:{self.startzeit.minute:02} Ende {self.endzeit.stunde:02}:{self.endzeit.minute:02}"

    def __eq__(self, other):
        if self is None and other is None: return True
        if self is None or other is None: return False
        return self.endzeit == other.endzeit and self.startzeit == other.startzeit

    def schneiden(self, other):
        if (self.endzeit > other.startzeit and self.startzeit < other.endzeit) or (
                other.startzeit < self.endzeit and other.endzeit > self.startzeit):
            return True
        return False

    def beruehrt(self, other):
        if ((self.endzeit >= other.startzeit and self.startzeit <= other.endzeit) or (
                other.startzeit <= self.endzeit and other.endzeit >= self.startzeit)):
            return True
        return False

    def callbackText(self, event):
        if event.keysym == "Return":
            self.unfokusiere()
        elif event.keysym == "BackSpace" and not self.istPause:
            self.text = self.text[:-1]
        elif event.keysym == "Delete":
            self.entferne()
        else:
            if not self.istPause:
                self.text += event.char

    def zeichne(self):
        from ScreenManager import ScreenManager as SM
        from Farbkonzept import Farbkonzept

        y1 = SM.zeitZuPixel(self.startzeit)
        y2 = SM.zeitZuPixel(self.endzeit)

        if self.form is None:
            self.form[0] = SM.canvas.create_rectangle(0, y1, SM.canvasWidth, y2 ,fill=Farbkonzept.vormittag())
        else:
            SM.canvas.coords(self.form[0], 0, y1, SM.canvasWidth, y2)
            SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.vormittag())


    def zeichneMarkiert(self):
        self.zeichne()

    def entferne(self):
        from EventManager import EventManager
        from ScreenManager import ScreenManager
        self.unfokusiere()
        #rufe entferne für die Zeiten auf, damit diese vom Canvas gelöscht werden können
        self.startzeit.entferne()
        self.endzeit.entferne()
        #entferne das events aus events[]
        EventManager.removeEvent(self)
        #lösche das Event vom Canvas
        for form in self.form:
            ScreenManager.canvas.delete(form)
    def fokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.tag_bind(self.form[0], "<Key>", self.callbackText)

    def unfokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.tag_unbind(self.form[0])
