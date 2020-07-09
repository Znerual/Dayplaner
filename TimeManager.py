from Zeit import Zeit
from Db import Db
from datetime import date

class TimeManager:

    aufstehzeit = Zeit(8, 0, date.today())
    aktuellesDatum = Zeit(0,0, date.today())
    mittagspauseStart = Zeit(12, 30, date.today())
    mittagspauseEnde = Zeit(13, 30, date.today())
    schlafenszeit = Zeit(23, 00, date.today())
    zeiten = (aufstehzeit, mittagspauseStart, mittagspauseEnde, schlafenszeit)
    null = Zeit(0, 0, None)
    genauigkeit = Zeit(0,10, None)
    genauigkeitsfaktor = 60
    @staticmethod
    def findeZeit(zeit, genauigkeit=None):
        for z in TimeManager.zeiten:
            if z.circa(zeit, genauigkeit):
                return z
        return None

    @staticmethod
    def verschiebeZeit(zeit, nach):
        from ScreenManager import ScreenManager
        from EventManager import EventManager as EM

        if zeit == TimeManager.mittagspauseStart:
            EM.verschiebeZeitNach(EM.mittagspause, True, nach)
            return
        elif zeit == TimeManager.mittagspauseEnde:
            EM.verschiebeZeitNach(EM.mittagspause, False, nach)
            return

        if zeit == TimeManager.aufstehzeit:
            if nach > EM.findeKleinsteStartzeit(): return None
        elif zeit == TimeManager.schlafenszeit:
            if nach < EM.findeGroessteEndzeit(): return None
        zeit.stunde = nach.stunde
        zeit.minute = nach.minute
        zeit.text = nach.text
        ScreenManager.zeichneHintergrund()
        ScreenManager.zeichneEventsNeu()
        #TimeManager.speichereZeiten()
        return zeit

    @staticmethod
    def ladeZeiten():
        from EventManager import EventManager as EM
        from Event import Event
        if not Db.initialisiert: Db.init()
        zeiten = Db.erhalteAlleZeitenAm(Db.conn, TimeManager.aktuellesDatum.datum)
        print(f"Datum in Ordianl {TimeManager.aktuellesDatum.datum.toordinal()}")
        if len(zeiten) == 4:
            TimeManager.zeiten = zeiten
            TimeManager.aufstehzeit = TimeManager.zeiten[0]
            TimeManager.mittagspauseStart = TimeManager.zeiten[1]
            TimeManager.mittagspauseEnde =TimeManager.zeiten[2]
            TimeManager.schlafenszeit = TimeManager.zeiten[3]
            EM.mittagspause = Event(TimeManager.mittagspauseStart, TimeManager.mittagspauseEnde, False, "Mittagspause")
            TimeManager.mittagspauseStart.event = EM.mittagspause
            TimeManager.mittagspauseEnde.event = EM.mittagspause

        else:
            TimeManager.aufstehzeit = Zeit(8, 0, TimeManager.aktuellesDatum.datum)
            TimeManager.aktuellesDatum = Zeit(0, 0, TimeManager.aktuellesDatum.datum)
            TimeManager.mittagspauseStart = Zeit(12, 30, TimeManager.aktuellesDatum.datum)
            TimeManager.mittagspauseEnde = Zeit(13, 30, TimeManager.aktuellesDatum.datum)
            TimeManager.schlafenszeit = Zeit(23, 00, TimeManager.aktuellesDatum.datum)
            TimeManager.zeiten = (TimeManager.aufstehzeit, TimeManager.mittagspauseStart, TimeManager.mittagspauseEnde, TimeManager.schlafenszeit)
            EM.mittagspause = Event(TimeManager.mittagspauseStart, TimeManager.mittagspauseEnde, False, "Mittagspause")
            TimeManager.mittagspauseStart.event = EM.mittagspause
            TimeManager.mittagspauseEnde.event = EM.mittagspause
        for zeit in TimeManager.zeiten:
            zeit.zeichne()
    @staticmethod
    def speichereZeiten():
        if not Db.initialisiert: Db.init()
        for zeit in TimeManager.zeiten:
            if zeit.id is None:
                zeit.id = Db.addZeit(Db.conn, zeit)
            else:
                Db.updateZeit(Db.conn, zeit)

        Db.conn.commit()
