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
        self.form = []

        self.istPause = istPause

    def __str__(self):
        return f"Start {self.startzeit.stunde:02}:{self.startzeit.minute:02} Ende {self.endzeit.stunde:02}:{self.endzeit.minute:02}"

    def __eq__(self, other):
        if self is None and other is None: return True
        if self is None or other is None: return False
        return self.endzeit == other.endzeit and self.startzeit == other.startzeit

    def schneiden(self, other):
        if ((self.endzeit > other.startzeit and self.startzeit < other.endzeit) or (other.startzeit < self.endzeit and other.endzeit > self.startzeit) ):
            return True
        return False

    def beruehrt(self, other):
        if ((self.endzeit >= other.startzeit and self.startzeit <= other.endzeit) or (
                other.startzeit <= self.endzeit and other.endzeit >= self.startzeit)):
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
        #self.form.append("j") #wird mit allen benötigten Formen gefüllt, dh mit dem Grundrechteckt,dass gefüllt wird, Rahmen und Text
        #self.form[0]
        #if len(self.form) == 0:
        #    ...
        #ScreenManager.canvas #canvas zum zeichnen
        #google nach canvas.move oder moveto ...

        #from ScreenManager import ScreenManager
        #sm = ScreenManager() erzeugt Canvas zum Testen, befüllt ScreenManager
        pass

    def zeichneMarkiert(self, screenManager):
        from ScreenManager import ScreenManager
        pass

    def entferne(self):
        from ScreenManager import ScreenManager
        pass

    def fokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.tag_bind(self.form[0], "<Key>", self.callback_text)

    def unfokusiere(self):
        from ScreenManager import ScreenManager
        ScreenManager.canvas.tag_unbind(self.form[0])
