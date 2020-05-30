from Objekt import Objekt


class Zeit(Objekt):
    # Bestimmt die Zeit aus einem String, kann entweder im Format 12 oder 12:00 gemacht werden
    @staticmethod
    def fromString(text):
        if len(text) == 2:
            try:
                stunde = int(text)
                if 0 <= stunde <= 24:
                    zeit = Zeit(stunde, 0)
                    return zeit
                else:
                    return None
            except ValueError:
                return None
        if len(text) == 5:
            try:
                stunde = int(text[0:2])
                minute = int(text[3:5])
                if 0 <= stunde <= 24 and 0 <= minute <= 60:
                    zeit = Zeit(stunde, minute)
                    return zeit
                else:
                    return None
            except ValueError:
                return None

    def __init__(self, stunde, minute, event=None):
        self.stunde = stunde
        self.minute = minute
        self.event = event
        self.text = f"{self.stunde:02}:{self.minute:02}"
        self.form = []
        self.veraltet = False
    def __str__(self):
        if self.event is None:
            return f"Zeit {self.stunde:02}:{self.minute:02}"
        else:
            return f"Zeit {self.stunde:02}:{self.minute:02} zu Event {self.event}"

    def __add__(self, other):
        assert (not (self.event is not None and other.event is not None) or self.event == other.event)
        #assert (self.stunde + other.stunde + (self.minute + other.minute) / 60 <= 24) #achtung, Stunde kann damit > 24 sein!
        stunde = self.stunde + other.stunde
        minute = self.minute + other.minute
        if minute >= 60:
            stunde += 1
            minute -= 60
        if minute < 0:
            stunde -= 1
            minute += 60
        event = self.event
        if event is None:
            event = other.event
        return Zeit(stunde, minute, event)

    def __gt__(self, other):
        if self.stunde > other.stunde: return True
        if self.stunde < other.stunde: return False
        if self.minute > other.minute: return True
        return False

    def __ge__(self, other):
        if self.stunde > other.stunde: return True
        if self.stunde < other.stunde: return False
        if self.minute >= other.minute: return True
        return False

    def __lt__(self, other):
        return not (self >= other)

    def __le__(self, other):
        return not (self > other)

    def __sub__(self, other):
        stunde = self.stunde - other.stunde
        minute = self.minute - other.minute
        if minute < 0:
            stunde -= 1
            minute += 60
        if minute > 60:
            stunde += 1
            minute -= 60

        event = self.event
        if event is None:
            event = other.event
        return Zeit(stunde, minute, event)

    def __eq__(self, other):
        if self is None and other is None: return True
        if self is None or other is None: return False
        return self.stunde == other.stunde and self.minute == other.minute

    def setEvent(self, event):
        self.event = event

    def set(self, other):
        self.stunde = other.stunde
        self.minute = other.minute
        self.text = other.text

    def circa(self, zeit):
        from TimeManager import TimeManager as TM
        if abs(self.stunde - zeit.stunde) <= TM.genauigkeit.stunde and abs(self.minute - zeit.minute) <= TM.genauigkeit.minute:
            return True
        return False

    def runde(self, genauigkeit):
        mod = self.inMinuten() % genauigkeit.inMinuten()
        if mod == 0:
            return self
        elif mod < genauigkeit.inMinuten() / 2:
            return self.vonMinuten(self.inMinuten() - mod)
        else:
            return self.vonMinuten(self.inMinuten() + (genauigkeit.inMinuten() - mod))

    def istStartzeit(self):
        if self.circa(self.event.startzeit): return True

    def istEndzeit(self):
        if self.circa(self.event.endzeit): return True

    def callbackVerschiebe(self, event):
        from EventManager import EventManager
        if event.keysym == "Return":
            self.unfokusiere()
            nach = Zeit.fromString(self.text)
            if nach is not None:
                if self.event is not None:
                    EventManager.verschiebeZeitNach(self.event, event.istStartzeit(), nach)
                    # überprüft ob die Zeit die Start oder Endzeit ist wenn sie einem Event zugeordnet ist
                    assert (self.istStartzeit() or self.istEndzeit())
                    assert (not self.istStartzeit() and self.istEndzeit())
                else:
                    self.stunde = nach.stunde
                    self.minute = nach.minute
                    self.text = nach.text
        elif event.keysym == "BackSpace":
            self.text = self.text[:-1]
        elif event.keysym == "Delete":
            self.unfokusiere()
        else:
            self.text += event.char

    def inMinuten(self):
        return self.stunde * 60 + self.minute

    def vonMinuten(self, minuten):
        self.stunde = int(minuten / 60)
        self.minute = int(minuten % 60)
        self.text = f"{self.stunde:02}:{self.minute:02}"
        return self

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
                self.form.append(SM.canvas.create_text(SM.canvasWidth/2, y1, text=self.text,font=("BellMT",8)))
            elif self.event.startzeit==self:
                self.form.append(SM.canvas.create_line(x1, y1, x2, y1, fill=Farbkonzept.Linien()))
                self.form.append(SM.canvas.create_text(xVerschiebung, y1+yVerschiebung, text=self.text, font=("BellMT", 8)))
            elif self.event.endzeit==self:
                self.form.append(SM.canvas.create_line(x1, y1, x2, y1, fill=Farbkonzept.Linien()))
                self.form.append(SM.canvas.create_text(SM.canvasWidth-xVerschiebung, y1 - yVerschiebung, text=self.text, font=("BellMT", 8)))
            #elif what happended
        else:
            if self.veraltet:
                self.form.clear()
                if self.event is None:  # achtung form kann jetzt 2 oder 3 einträge haben
                    self.form.append(SM.canvas.create_line(x1, y1, x_mitteStart, y1, fill=Farbkonzept.Linien()))
                    self.form.append(SM.canvas.create_line(x_mitteEnde, y1, x2, y1, fill=Farbkonzept.Linien()))
                    self.form.append(SM.canvas.create_text(SM.canvasWidth / 2, y1, text=self.text, font=("BellMT", 8)))
                elif self.event.startzeit == self:
                    self.form.append(SM.canvas.create_line(x1, y1, x2, y1, fill=Farbkonzept.Linien()))
                    self.form.append(SM.canvas.create_text(xVerschiebung, y1 + yVerschiebung, text=self.text, font=("BellMT", 8)))
                elif self.event.endzeit == self:
                    self.form.append(SM.canvas.create_line(x1, y1, x2, y1, fill=Farbkonzept.Linien()))
                    self.form.append(SM.canvas.create_text(SM.canvasWidth-xVerschiebung, y1 - yVerschiebung, text=self.text, font=("BellMT", 8)))
            if self.event is None:
                SM.canvas.coords(self.form[0], x1, y1, x_mitteStart, y1)
                SM.canvas.coords(self.form[1], x_mitteEnde, y1, x2,y1)
                SM.canvas.coords(self.form[2], SM.canvasWidth/2, y1 )
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.Linien())
                SM.canvas.itemconfig(self.form[1], fill=Farbkonzept.Linien())
                SM.canvas.itemconfig(self.form[2], text=self.text)
            if self.event.startzeit == self:
                SM.canvas.coords(self.form[0], x1, y1, x2, y1)
                SM.canvas.coords(self.form[1], xVerschiebung, y1 + yVerschiebung)
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.Linien())
                SM.canvas.itemconfig(self.form[1], text=self.text)
            if self.event.endzeit == self:
                SM.canvas.coords(self.form[0], x1, y1, x2, y1)
                SM.canvas.coords(self.form[1], SM.canvasWidth-xVerschiebung, y1-yVerschiebung)
                SM.canvas.itemconfig(self.form[0], fill=Farbkonzept.Linien())
                SM.canvas.itemconfig(self.form[1], text=self.text)#könnten hier jeweils noch mit fill die textfarbe ändern

    def zeichneMarkiert(self):
        pass
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
        ScreenManager.canvas.bind( "<Key>", self.callbackVerschiebe)

    def unfokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.unbind( "<Key>")

    def veralte(self):
        self.veraltet = True