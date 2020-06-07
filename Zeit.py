from Objekt import Objekt
from datetime import date, timedelta

class Zeit(Objekt):
    @staticmethod
    def intervalFromString(text):
        pos = text.find("-")
        if pos != -1:
            zeit1 = Zeit.fromString(text[0:pos])
            zeit2 = Zeit.fromString(text[pos+1:])
            if zeit1 is not None and zeit2 is not None: return (zeit1, zeit2)
        return (None, None)
    # Bestimmt die Zeit aus einem String, kann entweder im Format 12 oder 12:00 gemacht werden
    @staticmethod
    def fromString(text):
        from TimeManager import TimeManager
        if len(text) <= 2:
            try:
                stunde = int(text)
                if 0 <= stunde <= 24:
                    zeit = Zeit(stunde, 0, None)
                    return zeit
                else:
                    return None
            except ValueError:
                return None
        elif len(text) <= 5:
            try:
                pos = text.find(":")
                if pos == -1: return None
                stunde = int(text[:pos])
                minute = int(text[pos +1 :])
                if 0 <= stunde <= 24 and 0 <= minute <= 60:
                    zeit = Zeit(stunde, minute, None)
                    return zeit
                else:
                    return None
            except ValueError:
                return None


    def __init__(self, stunde, minute, datum=date.today(),event=None):

        self.stunde = stunde
        self.minute = minute
        self.datum = datum
        self.event = event
        self.text = f"{self.stunde:02}:{self.minute:02}"
        self.form = []
        self.id = None
    def __str__(self):
        if self.datum is None:
            if self.event is None:
                return f"Zeit {self.stunde:02}:{self.minute:02}"
            else:
                return f"Zeit {self.stunde:02}:{self.minute:02} zu Event {self.event}"
        else:
            if self.event is None:
                return f"Zeit {self.stunde:02}:{self.minute:02} am {self.datum.strftime('%d.%m.%Y')}"
            else:
                return f"Zeit {self.stunde:02}:{self.minute:02} am {self.datum.strftime('%d.%m.%Y')} zu Event {self.event}"

    def __add__(self, other):
        assert (not (self.event is not None and other.event is not None) or self.event == other.event)
        #assert (self.stunde + other.stunde + (self.minute + other.minute) / 60 <= 24) #achtung, Stunde kann damit > 24 sein!
        #assert self.datum == other.datum
        stunde = self.stunde + other.stunde
        minute = self.minute + other.minute

        if self.datum is None:
            datum = other.datum
        elif other.datum is None:
            datum = self.datum
        elif self.datum != date.today():
            datum = self.datum
        else:
            datum = other.datum

        if minute >= 60:
            stunde += 1
            minute -= 60
        if minute < 0:
            stunde -= 1
            minute += 60
        event = self.event
        if event is None:
            event = other.event
        return Zeit(stunde, minute, datum, event)

    def __gt__(self, other):
        #if self.datum > other.datum: return True
        #if self.datum < other.datum: return False
        if self.stunde > other.stunde: return True
        if self.stunde < other.stunde: return False
        if self.minute > other.minute: return True
        return False

    def __ge__(self, other):
        #if self.datum > other.datum: return True
        #if self.datum < other.datum: return False
        if self.stunde > other.stunde: return True
        if self.stunde < other.stunde: return False
        if self.minute >= other.minute: return True
        return False

    def __lt__(self, other):
        return not (self >= other)

    def __le__(self, other):
        return not (self > other)

    def __sub__(self, other):
        #assert self.datum == other.datum
        stunde = self.stunde - other.stunde
        minute = self.minute - other.minute
        if self.datum is None:
            datum = other.datum
        elif other.datum is None:
            datum = self.datum
        elif self.datum != date.today():
            datum = self.datum
        else:
            datum = other.datum
        if minute < 0:
            stunde -= 1
            minute += 60
        if minute > 60:
            stunde += 1
            minute -= 60
        event = self.event
        if event is None:
            event = other.event
        return Zeit(stunde, minute, datum, event)

    def __eq__(self, other):
        if self is None and other is None: return True
        if self is None or other is None: return False
        return self.stunde == other.stunde and self.minute == other.minute

    def setEvent(self, event):
        self.event = event

    def set(self, other):
        self.stunde = other.stunde
        self.minute = other.minute
        self.datum = other.datum
        self.text = other.text

    def erhalteDatum(self):
        return self.datum.strftime('%d.%m.%Y')

    def erhalteDatumLang(self):
        return self.datum.strftime('%A %d.%m')
    def verschiebeAufMorgen(self):
        self.datum += timedelta(days=1)
        return self

    def verschiebeAufGestern(self):
        self.datum += timedelta(days=-1)
        return self

    def circa(self, zeit, genauigkeit = None):
        from TimeManager import TimeManager as TM
        if genauigkeit is None:
            genauigkeit = TM.genauigkeit
        if (TM.null <= (self - zeit) <= genauigkeit or TM.null <= (zeit - self) <= genauigkeit):
            return True
        return False

    def runde(self, genauigkeit=None):
        from TimeManager import TimeManager as TM
        if genauigkeit is None: genauigkeit = TM.genauigkeit
        mod = self.zeitInMinuten() % genauigkeit.zeitInMinuten()
        if mod == 0:
            return self
        elif mod < genauigkeit.zeitInMinuten() / 2:
            return self.vonMinuten(self.zeitInMinuten() - mod)
        else:
            return self.vonMinuten(self.zeitInMinuten() + (genauigkeit.zeitInMinuten() - mod))

    def istStartzeit(self):
        if self.circa(self.event.startzeit): return True

    def istEndzeit(self):
        if self.circa(self.event.endzeit): return True

    def callbackVerschiebe(self, event):
        from EventManager import EventManager
        from TimeManager import TimeManager
        if event.keysym == "Return":
            nach = Zeit.fromString(self.text)
            self.unfokusiere()
            self.aktualisiereText() #setzt den Text auf die gespeicherte Zeit, wird nur überschrieben falls nach passt
            if nach is not None:
                if self.event is not None:
                    EventManager.verschiebeZeitNach(self.event, self.istStartzeit(), nach)
                    self.text = nach.text

                    # überprüft ob die Zeit die Start oder Endzeit ist wenn sie einem Event zugeordnet ist
                    assert (self.istStartzeit() or self.istEndzeit())
                    assert not( self.istStartzeit() and self.istEndzeit())
                else:
                    TimeManager.verschiebeZeit(self, nach)
            self.zeichne()
        elif event.keysym == "BackSpace":
            self.text = self.text[:-1]
        elif event.keysym == "Delete":
            self.unfokusiere()
        else:
            self.text += event.char
        self.zeichneMarkiert()
    def zeitInMinuten(self):
        return self.stunde * 60 + self.minute

    def vonMinuten(self, minuten):
        self.stunde = int(minuten / 60)
        self.minute = int(minuten % 60)
        self.text = f"{self.stunde:02}:{self.minute:02}"
        return self

    def aktualisiereText(self):
        self.text = f"{self.stunde:02}:{self.minute:02}"

    def zeichne(self):
        from ScreenManager import ScreenManager as SM
        from Farbkonzept import Farbkonzept

        #TODO: Vormittag - Nachmittag Unterscheidung //sollten linien verschiedene farben haben?
        x1 = SM.canvasWidth/30
        y1 = SM.zeitZuPixel(self)
        x2 = x1*29
        x_mitteStart = SM.canvasWidth/2 - 2*x1
        x_mitteEnde = SM.canvasWidth/2 + 2*x1
        yVerschiebung= SM.canvasHeight/80
        xVerschiebung=x1*3


        if len(self.form) == 0:

            if self.event is None: #achtung form kann jetzt 2 oder 3 einträge haben
                self.form.append(SM.canvas.create_line(x1, y1, x_mitteStart, y1, fill=Farbkonzept.Linien()))
                self.form.append(SM.canvas.create_line(x_mitteEnde, y1, x2, y1, fill=Farbkonzept.Linien()))
                self.form.append(SM.canvas.create_text(SM.canvasWidth/2, y1, text=self.text,font=("BellMT",10)))
            elif self.event.startzeit==self:
                self.form.append(SM.canvas.create_line(x1, y1, x2, y1, fill=Farbkonzept.Linien()))
                self.form.append(SM.canvas.create_text(xVerschiebung, y1+yVerschiebung, text=self.text, font=("BellMT", 10)))
            elif self.event.endzeit==self:
                self.form.append(SM.canvas.create_line(x1, y1, x2, y1, fill=Farbkonzept.Linien()))
                self.form.append(SM.canvas.create_text(SM.canvasWidth-xVerschiebung, y1 - yVerschiebung, text=self.text, font=("BellMT", 10)))
            #elif what happended
        else:
            if self.event is None:
                SM.canvas.coords(self.form[0], x1, y1, x_mitteStart, y1)
                SM.canvas.coords(self.form[1], x_mitteEnde, y1, x2,y1)
                SM.canvas.coords(self.form[2], SM.canvasWidth/2, y1 )
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.Linien())
                SM.canvas.itemconfig(self.form[1], fill=Farbkonzept.Linien())
                SM.canvas.itemconfig(self.form[2], text=self.text)
            elif self.event.startzeit == self:
                SM.canvas.coords(self.form[0], x1, y1, x2, y1)
                SM.canvas.coords(self.form[1], xVerschiebung, y1 + yVerschiebung)
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.Linien())
                SM.canvas.itemconfig(self.form[1], text=self.text)
            elif self.event.endzeit == self:
                SM.canvas.coords(self.form[0], x1, y1, x2, y1)
                SM.canvas.coords(self.form[1], SM.canvasWidth-xVerschiebung, y1-yVerschiebung)
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.Linien())
                SM.canvas.itemconfig(self.form[1], text=self.text)#könnten hier jeweils noch mit fill die textfarbe ändern


    def zeichneMarkiert(self):
        self.zeichne()
        #TODO: Ausprogrammieren

    def entferne(self):
        from ScreenManager import ScreenManager
        #löse den eventuellen Fokus
        self.unfokusiere()
        #lösche die Zeitelemente vom Canvas
        for form in self.form:
            ScreenManager.canvas.delete(form)

    def fokusiere(self):
        from ScreenManager import ScreenManager
        self.text = ""
        ScreenManager.canvas.unbind("<Key>")
        ScreenManager.canvas.bind("<Key>", self.callbackVerschiebe)
        print("Fokusiere Zeit")

    def unfokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.unbind("<Key>")
        ScreenManager.canvas.bind("<Key>", ScreenManager.keyInput)
        self.aktualisiereText()

