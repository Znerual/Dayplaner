from Zeit import Zeit


class TimeManager:

    aufstehzeit = Zeit(8, 0)
    mittagspauseStart = Zeit(12, 30)
    mittagspauseEnde = Zeit(13, 30)
    schlafenszeit = Zeit(23, 00)
    zeiten = (aufstehzeit, mittagspauseStart, mittagspauseEnde, schlafenszeit)
    null = Zeit(0, 0)
    genauigkeit = Zeit(0,2)

    @staticmethod
    def findeZeit(zeit):
        for z in TimeManager.zeiten:
            if z.circa(zeit):
                return z
        return None

