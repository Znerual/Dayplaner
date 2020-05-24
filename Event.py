from Objekt import Objekt


from Zeit import Zeit


class Event(Objekt):

    def __init__(self, startzeit, endzeit, istPause=False):
        self.startzeit = startzeit
        self.endzeit = endzeit

        self.startzeit.setEvent(self)
        self.endzeit.setEvent(self)

        self.text = ""
        self.eventDavor = None
        self.eventDanach = None

        self.istPause = istPause

    def __str__(self):
        return f"Start {self.startzeit.stunde:02}:{self.startzeit.minute:02} Ende {self.endzeit.stunde:02}:{self.endzeit.minute:02}"

    def schneiden(self, other):
        if (Zeit.distanz(self.startzeit, other.startzeit) <= min(Zeit.distanz(self.startzeit, self.endzeit),
                                                                Zeit.distanz(other.startzeit, other.endzeit))):
            return True
        return False

    def callback_text(self, event):
        if (event.keysym == "Return"):
            self.unfokusiere()
        elif (event.keysym == "BackSpace" and self.istPause == False):
            self.text = self.text[:-1]
        elif (event.keysym == "Delete"):
            self.unfokusiere()
            from EventManager import EventManager
            EventManager.removeEvent(self)
        else:
            if self.istPause == False:
                self.text += event.char

    def zeichne(self, screenManager):
        from ScreenManager import ScreenManager
        pass

    def zeichneMarkiert(self, screenManager):
        from ScreenManager import ScreenManager
        pass

    def fokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.tag_bind(str(self), "<Key>", self.callback_text)

    def unfokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.tag_unbind(str(self))
