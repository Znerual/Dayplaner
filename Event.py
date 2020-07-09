from Objekt import Objekt


class Event(Objekt):

    def __init__(self, startzeit, endzeit, istPause=False, text="Test"):
        self.startzeit = startzeit
        self.endzeit = endzeit

        self.startzeit.setEvent(self)
        self.endzeit.setEvent(self)

        self.text = "Test"
        self.eventDavor = None
        self.eventDanach = None
        self.form = []
        self.istPause = istPause
        self.id = None
    def __str__(self):
        return f"Start {self.startzeit.stunde:02}:{self.startzeit.minute:02} Ende {self.endzeit.stunde:02}:{self.endzeit.minute:02} am {self.startzeit.erhalteDatum()}"

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
            self.zeichne()
            self.unfokusiere()
        elif event.keysym == "BackSpace" and not self.istPause:
            self.text = self.text[:-1]
            self.zeichneMarkiert()
        elif event.keysym == "Delete":
            self.entferne()
        else:
            if not self.istPause:
                self.text += event.char
                self.zeichneMarkiert()


    def zeichne(self):
        from ScreenManager import ScreenManager as SM
        from TimeManager import TimeManager as TM
        from Farbkonzept import Farbkonzept


        x1 = SM.canvasWidth/30
        y1 = SM.zeitZuPixel(self.startzeit)

        x2 = x1*29
        y2 = SM.zeitZuPixel(self.endzeit)

        if len(self.form) == 0:
            if self.endzeit <= TM.mittagspauseStart:
                self.form.append(SM.canvas.create_rectangle(x1, y1, x2, y2 ,fill=Farbkonzept.vormittag(), outline=''))
            if self.startzeit >= TM.mittagspauseEnde:
                self.form.append(SM.canvas.create_rectangle(x1, y1, x2, y2, fill=Farbkonzept.nachmittag(), outline=''))
            if self.startzeit >= TM.mittagspauseStart and self.endzeit <=TM.mittagspauseEnde:
                self.form.append(SM.canvas.create_rectangle(x1, y1, x2, y2 ,fill=Farbkonzept.mittagspause(),outline=''))
            self.form.append(SM.canvas.create_text(SM.canvasWidth/2, int(y1 + (y2 - y1) / 2), text=self.text, font=("Dubai",10)))

        else:
            SM.canvas.coords(self.form[0], x1, y1, x2, y2)
            SM.canvas.coords(self.form[1], SM.canvasWidth/2, int(y1 + (y2-y1)/2))
            if self.endzeit <= TM.mittagspauseStart:
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.vormittag())
                SM.canvas.itemconfig(self.form[1], text=self.text)#fill=Farbkonzept.vormittag_markiert()
            elif self.startzeit >= TM.mittagspauseEnde:
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.nachmittag())
                SM.canvas.itemconfig(self.form[1], text=self.text)
            elif self.startzeit >= TM.mittagspauseStart and self.endzeit <= TM.mittagspauseEnde:
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.mittagspause())
                SM.canvas.itemconfig(self.form[1], text=self.text)

        self.startzeit.zeichne()
        self.endzeit.zeichne()

    def zeichneMarkiert(self):
        from ScreenManager import ScreenManager as SM
        from TimeManager import TimeManager as TM
        from Farbkonzept import Farbkonzept

        if self.endzeit <= TM.mittagspauseStart:
            SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.vormittag_markiert())
        elif self.startzeit >= TM.mittagspauseEnde:
            SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.nachmittag_markiert())
        elif self.startzeit >= TM.mittagspauseStart and self.endzeit <= TM.mittagspauseEnde:
            SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.mittagspause_markiert())

        self.startzeit.zeichneMarkiert()
        self.endzeit.zeichneMarkiert()

    def verstecke(self):
        from ScreenManager import ScreenManager
        self.unfokusiere()
        # rufe entferne für die Zeiten auf, damit diese vom Canvas gelöscht werden können
        self.startzeit.entferne()
        self.endzeit.entferne()
        # lösche das Event vom Canvas
        for form in self.form:
            ScreenManager.canvas.delete(form)

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
        ScreenManager.canvas.unbind("<Key>")
        ScreenManager.canvas.bind("<Key>", self.callbackText)

    def unfokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.unbind("<Key>")
        ScreenManager.canvas.bind("<Key>", ScreenManager.keyInput)

