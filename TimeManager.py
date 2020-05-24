from Zeit import Zeit
from EventManager import EventManager

class TimeManager:
    aufstehzeit = Zeit(8,0)
    mittagspauseStart = Zeit(12,30)
    mittagspauseEnde = Zeit(13,30)
    schlafenszeit = Zeit(23,00)
    null = Zeit(0,0)

    #Verschiebt eine Zeit, nur falls startzeit vor endzeit liegt
    @staticmethod
    def verschiebeZeitNach(event, istStartzeit, zeit):
        #überprüft ob verschiebung erlaubt
        if istStartzeit:
            if event.endzeit - zeit <= 0: return
            event.startzeit.set(zeit)
        else:
            if zeit - event.startzeit <= 0: return
            event.endzeit.set(zeit)

        # überschneidungen korrigieren, indem die Grenzen strikt neu verändern werden. Anhängende Teile werden nicht
        # verschoben sonder gekürzt
        otherEvents = list(filter(lambda x: x != event))
        for oevent in otherEvents:
            if (event.schneiden(oevent)):
                if (oevent.startzeit >= event.startzeit and oevent.endzeit <= event.endzeit):  # das Event liegt im neuen Element
                    EventManager.removeEvent(oevent)
                    break
                elif (oevent.startzeit <= event.startzeit and oevent.endzeit >= event.startzeit):  # anderes Event schneidet von oben hinein
                    oevent.endzeit.set(event.startzeit)
                    oevent.eventDanach = event
                    event.eventDavor = oevent
                    break
                elif (oevent.startzeit >= event.startzeit and oevent.endzeit >= event.endzeit):  # anderes event runtscht von unten hinein
                    oevent.startzeit.set(event.endzeit)
                    oevent.eventDavor = event
                    event.eventDanach = oevent
                    break

