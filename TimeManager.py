from Zeit import Zeit


class TimeManager:

    aufstehzeit = Zeit(8, 0)
    mittagspauseStart = Zeit(12, 30)
    mittagspauseEnde = Zeit(13, 30)
    schlafenszeit = Zeit(23, 00)
    zeiten = (aufstehzeit, mittagspauseStart, mittagspauseEnde, schlafenszeit)
    null = Zeit(0, 0)
    genauigkeit = Zeit(0,10)
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
        return zeit
