from Zeit import Zeit
from Db import Db

class TimeManager:

    aufstehzeit = Zeit(8, 0, None)
    aktuellesDatum = Zeit(0,0)
    #TODO: Mittagspause hier herauslöschen und nur über EventManager.mittagspause verändern
    mittagspauseStart = Zeit(12, 30, None)
    mittagspauseEnde = Zeit(13, 30, None)
    schlafenszeit = Zeit(23, 00, None)
    zeiten = (aufstehzeit, mittagspauseStart, mittagspauseEnde, schlafenszeit)
    null = Zeit(0, 0, None)
    genauigkeit = Zeit(0,10, None)
    genauigkeitsfaktor = 60
    @staticmethod
    def findeZeit(zeit):
        for z in TimeManager.zeiten:
            if z.circa(zeit):
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
        zeiten = Db.erhalteAlleZeiten(Db.conn)
        if len(zeiten) > 0:
            TimeManager.zeiten = zeiten
            TimeManager.aufstehzeit = TimeManager.zeiten[0]
            TimeManager.mittagspauseStart = TimeManager.zeiten[1]
            TimeManager.mittagspauseEnde =TimeManager.zeiten[2]
            TimeManager.schlafenszeit = TimeManager.zeiten[3]
            EM.mittagspause = Event(TimeManager.mittagspauseStart, TimeManager.mittagspauseEnde)

    @staticmethod
    def speichereZeiten():
        if not Db.initialisiert: Db.init()
        for zeit in TimeManager.zeiten:
            if zeit.id is None:
                zeit.id = Db.addZeit(Db.conn, zeit)
            else:
                Db.updateZeit(Db.conn, zeit)

        Db.conn.commit()
