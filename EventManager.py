
class EventManager:
    events = []
    @staticmethod
    def addEvent(event):
        # passe das einzufügende Event an die Lücke an, dh überprüfen ob es überschneidungen gibt, Verknüpfungen
        # erstellen und nicht wie beim VerschiebenNach das andere Event anpassen, sonder das neue Event anpassen
        for oevent in EventManager.events:
            if event.schneiden(oevent):
                if (oevent.startzeit >= event.startzeit and oevent.endzeit <= event.endzeit): # das Event liegt im neuen Element
                    EventManager.events.append(None)
                    break
                elif (oevent.startzeit > event.startzeit and oevent.endzeit > event.endzeit): #anderes event runtscht von unten hinein
                    event.endzeit = oevent.startzeit
                    oevent.eventDavor = event
                    event.eventDanach = oevent
                    EventManager.events.append(event)
                    break

    @staticmethod
    def removeEvent(event):
        #lösche die Verknüpfungen über Vorheriges Element und folgendes Element
        if (event.eventDanach != None):
            event.eventDanach.eventDavor = None
        if (event.eventDavor != None):
            event.eventDanach.eventDanach = None

        EventManager.events.remove(event)
    @staticmethod
    def verschiebeEventNach(event, istStartzeit, zeit):
        deltaZeit = event.endzeit - event.startzeit
        if istStartzeit:
            event.startzeit = zeit
            if event.endzeit - event.startzeit <= 0: event.endzeit = event.startzeit + deltaZeit
        else:
            event.endzeit = zeit
            if event.endzeit - event.startzeit <= 0: event.endzeit = event.startzeit + deltaZeit

        # überschneidungen korrigieren, indem die Grenzen strikt neu verändern werden. Anhängende Teile werden nicht
        # verschoben sonder gekürzt
        otherEvents = list(filter(lambda x: x != event))
        for oevent in otherEvents:
            if (event.schneiden(oevent)):
                if (oevent.startzeit >= event.startzeit and oevent.endzeit <= event.endzeit): # das Event liegt im neuen Element
                    EventManager.removeEvent(oevent)
                    break
                elif (oevent.startzeit < event.startzeit and oevent.endzeit > event.startzeit): #anderes Event schneidet von oben hinein
                    oevent.endzeit = event.startzeit
                    oevent.eventDanach = event
                    event.eventDavor = oevent
                    break
                elif (oevent.startzeit > event.startzeit and oevent.endzeit > event.endzeit): #anderes event runtscht von unten hinein
                    oevent.startzeit = event.endzeit
                    oevent.eventDavor = event
                    event.eventDanach = oevent
                    break

    @staticmethod
    def verschiebeEventUm(event, zeit):
        event.startzeit += zeit
        event.endzeit += zeit
        if event.eventDanach != None:
            event.eventDanach.startzeit += zeit
            event.eventDanach.endzeit += zeit
        otherEvents = list(filter(lambda x: x != event))
        for oevent in otherEvents:
            if (event.schneiden(oevent)):
                if (oevent.startzeit >= event.startzeit and oevent.endzeit <= event.endzeit): # das Event liegt im neuen Element
                    deltaZeit = event.endzeit - event.startzeit
                    event.endzeit = oevent.startzeit
                    event.startzeit = event.endzeit- deltaZeit
                    event.eventDanach = oevent
                    oevent.eventDavor = event
                    break
                elif (oevent.startzeit < event.startzeit and oevent.endzeit > event.startzeit): #anderes Event schneidet von oben hinein
                    #sollte nicht eintreten, wenn die Zeit nur positiv ist
                    event.startzeit = oevent.endzeit
                    oevent.eventDanach = event
                    event.eventDavor = oevent
                    break
                elif (oevent.startzeit > event.startzeit and oevent.endzeit > event.endzeit): #anderes event runtscht von unten hinein
                    oevent.eventDavor = event
                    event.eventDanach = oevent
                    EventManager.verschiebeEventUm(oevent, event.endzeit - oevent.startzeit)
                    break

