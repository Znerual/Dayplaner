import tkinter
from Objekt import Objekt
from ScreenManager import ScreenManager
from EventManager import EventManager


class Zeit(Objekt):
    toleranz = (0, 5)

    @staticmethod
    def distanz(self, other):
        return abs(self.stunde * 60 - other.stunde * 60 + self.minute - other.minute)

    # Bestimmt die Zeit aus einem String, kann entweder im Format 12 oder 12:00 gemacht werden
    @staticmethod
    def fromString(text):
        if (len(text) == 2):
            try:
                stunde = int(text)
                if (stunde >= 0 and stunde <= 24):
                    zeit = Zeit(stunde, 0)
                    return zeit
                else:
                    return None
            except ValueError:
                return None
        if (len(text) == 5):
            try:
                stunde = int(text[0:2])
                minute = int(text[3:5])
                if (stunde >= 0 and stunde <= 24 and minute >= 0 and minute <= 60):
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

    def __str__(self):
        if (self.event == None):
            return f"Zeit {self.stunde:02}:{self.minute:02}"
        else:
            return f"Zeit {self.stunde:02}:{self.minute:02} zu Event {self.event}"

    def __add__(self, other):
        assert (not (self.event != None and other.evet != None))
        assert (self.stunde + other.stunde + (self.minute + other.minute) / 60 <= 24)
        stunde = self.stunde + other.stunde
        minute = self.minute + other.minute
        if (minute >= 60):
            stunde += 1
            minute -= 60
        event = self.event
        if (event == None):
            event = other.event
        return Zeit(stunde, minute, event)

    def __gt__(self, other):
        if (self.stunde > other.stunde): return True
        if (self.stunde < other.stunde): return False
        if (self.minute > other.minute): return True
        return False
    def __ge__(self, other):
        if (self.stunde >= other.stunde): return True
        if (self.stunde < other.stunde): return False
        if (self.minute >= other.minute): return True
        return False

    def __lt__(self, other):
        return not (self >= other)

    def __le__(self, other):
        return not (self > other)

    def __sub__(self, other):
        assert (not (self.event != None and other.evet != None))
        stunde = self.stunde - other.stunde
        minute = self.minute - other.minute
        if (minute < 0):
            stunde -= 1
            minute += 60
        assert (self.stunde - other.stunde >= 0)
        event = self.event
        if (event == None):
            event = other.event
        return Zeit(stunde, minute, event)

    def circa(self, zeit):
        if (abs(self.stunde - zeit.stunde) <= Zeit.toleranz[0] and abs(self.minute - zeit.minute) <= Zeit.toleranz[1]):
            return True
        return False

    def istStartzeit(self):
        if self.circa(self.event.startzeit): return True

    def istEndzeit(self):
        if self.circa(self.event.endzeit): return True

    def callback_verschiebe(self, event):
        if (event.keysym == "Return"):
            self.unfokusiere()
            nach = Zeit.fromString(self.text)
            if (nach != None):
                if self.event != None:
                    EventManager.verschiebeEventNach(self.event, event.istStartzeit(), nach)
                    # überprüft ob die Zeit die Start oder Endzeit ist wenn sie einem Event zugeordnet ist
                    assert (self.istStartzeit() or self.istEndzeit())
                    assert (not self.istStartzeit() and self.istEndzeit())
                else:
                    self = nach
        elif (event.keysym == "BackSpace" and self.istPause == False):
            self.text = self.text[:-1]
        elif (event.keysym == "Delete"):
            self.unfokusiere()
        else:
            self.text += event.char

    def zeichne(self, screenManager):
        pass

    def zeichneMarkiert(self, screenManager):
        pass

    def fokusiere(self):
        ScreenManager.canvas.tag_bind(str(self), "<Key>", self.callback_verschiebe)

    def unfokusiere(self):
        ScreenManager.canvas.tag_unbind(str(self))
