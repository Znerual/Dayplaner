from Zeit import Zeit


class TimeManager:

    aufstehzeit = Zeit(8, 0)
    mittagspauseStart = Zeit(12, 30)
    mittagspauseEnde = Zeit(13, 30)
    schlafenszeit = Zeit(23, 00)
    zeiten = (aufstehzeit, mittagspauseStart, mittagspauseEnde, schlafenszeit)
    null = Zeit(0, 0)
    genauigkeit = Zeit(0,5)

    @staticmethod
    def findeZeit(zeit):
        for z in TimeManager.zeiten:
            if z.circa(zeit):
                return z
        return None

    @staticmethod
    def verschiebeZeit(zeit, nach):
        if zeit == TimeManager.aufstehzeit:
            if nach > TimeManager.mittagspauseStart: return None
        elif zeit == TimeManager.schlafenszeit:
            if nach < TimeManager.mittagspauseEnde: return None
        elif zeit == TimeManager.mittagspauseStart:
            if nach < TimeManager.aufstehzeit or nach > TimeManager.mittagspauseEnde: return None
        elif zeit == TimeManager.mittagspauseEnde:
            if nach < TimeManager.mittagspauseStart or nach > TimeManager.schlafenszeit: return None
        zeit.stunde = nach.stunde
        zeit.minute = nach.minute
        zeit.text = nach.text
        return zeit
