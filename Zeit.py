from Objekt import Objekt
from datetime import date, timedelta

class Zeit(Objekt):
    # Bestimmt die Zeit aus einem String, kann entweder im Format 12 oder 12:00 gemacht werden
    @staticmethod
    def fromString(text):
        if len(text) <= 2:
            try:
                stunde = int(text)
                if 0 <= stunde <= 24:
                    zeit = Zeit(stunde, 0)
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
                    zeit = Zeit(stunde, minute)
                    return zeit
                else:
                    return None
            except ValueError:
                return None

    def __init__(self, stunde, minute, datum=date.today(),event=None):
        self.stunde = stunde
        self.minute = minute
        self.event = event
        self.text = f"{self.stunde:02}:{self.minute:02}"
        self.form = []
        self.datum = datum
    def __str__(self):
        if self.event is None:
            return f"Zeit {self.stunde:02}:{self.minute:02} am {self.datum.strftime('%d.%m.%Y')}"
        else:
            return f"Zeit {self.stunde:02}:{self.minute:02} am {self.datum.strftime('%d.%m.%Y')} zu Event {self.event}"

    def __add__(self, other):
        assert (not (self.event is not None and other.event is not None) or self.event == other.event)
        #assert (self.stunde + other.stunde + (self.minute + other.minute) / 60 <= 24) #achtung, Stunde kann damit > 24 sein!
        assert self.datum == other.datum
        stunde = self.stunde + other.stunde
        minute = self.minute + other.minute
        datum = self.datum
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
        if self.datum > other.datum: return True
        if self.datum < other.datum: return False
        if self.stunde > other.stunde: return True
        if self.stunde < other.stunde: return False
        if self.minute > other.minute: return True
        return False

    def __ge__(self, other):
        if self.datum > other.datum: return True
        if self.datum < other.datum: return False
        if self.stunde > other.stunde: return True
        if self.stunde < other.stunde: return False
        if self.minute >= other.minute: return True
        return False

    def __lt__(self, other):
        return not (self >= other)

    def __le__(self, other):
        return not (self > other)

    def __sub__(self, other):
        assert self.datum == other.datum
        stunde = self.stunde - other.stunde
        minute = self.minute - other.minute
        datum = self.datum
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
        return self.datum == other.datum and self.stunde == other.stunde and self.minute == other.minute

    def setEvent(self, event):
        self.event = event

    def set(self, other):
        self.stunde = other.stunde
        self.minute = other.minute
        self.datum = other.datum
        self.text = other.text

    def erhalteDatum(self):
        return self.datum.strftime('%d.%m.%Y')

    def verschiebeAufMorgen(self):
        self.datum += timedelta(days=1)
        return self

    def verschiebeAufGestern(self):
        self.datum += timedelta(days=-1)
        return self

    def circa(self, zeit):
        from TimeManager import TimeManager as TM
        if self.datum == zeit.datum and abs(self.stunde - zeit.stunde) <= TM.genauigkeit.stunde and abs(self.minute - zeit.minute) <= TM.genauigkeit.minute:
            return True
        return False

    def runde(self, genauigkeit):
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

        #TODO: Vormittag - Nachmittag Unterscheidung
        #TODO: Schritart anpassen
        x1 = 0
        y1 = SM.zeitZuPixel(self)

        x2 = SM.canvasWidth


        if len(self.form) == 0:
            self.form.append(SM.canvas.create_line(x1, y1, x2, y1, fill=Farbkonzept.vormittag_markiert()))
            self.form.append(SM.canvas.create_text(int((x2 - x1) / 2), y1, fill="Black",text=self.text))
        else:
            SM.canvas.coords(self.form[0], x1, y1, x2, y1)
            SM.canvas.coords(self.form[1], int((x2 - x1) / 2), y1)
            SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.vormittag())
            SM.canvas.itemconfig(self.form[1], fill="Black", text=self.text)

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
        ScreenManager.canvas.bind("<Key>", self.callbackVerschiebe)
        print("Fokusiere Zeit")

    def unfokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.unbind("<Key>")
        self.aktualisiereText()

