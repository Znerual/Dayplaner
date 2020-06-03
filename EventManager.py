from TimeManager import TimeManager
from Event import Event
from Zeit import Zeit

class EventManager:
    events = []
    mittagspause = Event(TimeManager.mittagspauseStart, TimeManager.mittagspauseEnde, False, "Mittagspause")

    eventLaenge = Zeit(1,30)
    pausenLaenge = Zeit(0,10)
    #Es hat passieren können das beim Verschieben zwei Elemente exakt übereinder ilegen und damit beide
    # nicht in die oevents List hinzugefügt werden
    @staticmethod
    def getEventsWithoutEvent(event):
        found = False
        events = []
        for ev in EventManager.events:
            if found:
                events.append(ev)
            else:
                if ev == event:
                    found = True
                else:
                    events.append(ev)
        return events


    @staticmethod
    def addEvent(event):
        if event.endzeit <= event.startzeit: return

        #prüft ob das event hinzugefügt werden darf
        if event.startzeit >= TimeManager.schlafenszeit or event.endzeit <= TimeManager.aufstehzeit:
            return
        elif event.startzeit < TimeManager.aufstehzeit:
            event.startzeit.set(TimeManager.aufstehzeit)
        elif event.endzeit > TimeManager.schlafenszeit:
            event.endzeit.set(TimeManager.schlafenszeit)
        elif event.schneiden(EventManager.mittagspause):
            if event.startzeit < EventManager.mittagspause.startzeit:
                event.endzeit.set(EventManager.mittagspause.startzeit)
            elif event.endzeit > EventManager.mittagspause.endzeit:
                event.startzeit.set(EventManager.mittagspause.endzeit)
            else:
                return
        # passe das einzufügende Event an die Lücke an, dh überprüfen ob es überschneidungen gibt, Verknüpfungen
        # erstellen und nicht wie beim VerschiebenNach das andere Event anpassen, sonder das neue Event anpassen
        geschnitten = False
        beruehrt = False
        for oevent in EventManager.events:
            if event.schneiden(oevent):
                geschnitten = True
                if event.startzeit < oevent.startzeit < event.endzeit:  # Event liegt oberhalb von OEvent
                    event.endzeit.set(oevent.startzeit)
                    EventManager.addEvent(event)
                    return event
                elif oevent.startzeit == event.startzeit and oevent.endzeit == event.endzeit:  # beide elemente decken sich komplett
                    return event
                elif event.startzeit < oevent.endzeit < event.endzeit:  # Event liegt unterhalb von oevent
                    event.startzeit.set(oevent.endzeit)
                    EventManager.addEvent(event)
                    return event
                else:  # das Element überlappt nicht aber berüht vl andere Events, rufe verschiebeZeitNach auf um Andocken rictig zu machen
                    EventManager.verschiebeZeitNach(event, True, event.startzeit)
                    EventManager.verschiebeZeitNach(event, False, event.endzeit)
                    EventManager.events.append(event)
            elif event.beruehrt(oevent):
                beruehrt = True
        if not geschnitten:
            if beruehrt:
                EventManager.verschiebeZeitNach(event, True, event.startzeit)
                EventManager.verschiebeZeitNach(event, False, event.endzeit)
            EventManager.events.append(event)
            return event
    @staticmethod
    def removeEvent(event):
        # lösche die Verknüpfungen über Vorheriges Element und folgendes Element
        if event.eventDanach is not None:
            event.eventDanach.eventDavor = None
        if event.eventDavor is not None:
            event.eventDavor.eventDanach = None

        EventManager.events.remove(event)

    # Methode um Events zu verschieben
    # Wenn das Event das nachstehende oder vorherstehende Element weiß kann es die Verschiebung weitergeben und
    # aufs nächste Element anweden
    # Falls nicht sucht es noch überschneidenden Elemente und verschiebt diese dann um die fehlende Differenz
    @staticmethod
    def verschiebeEventUm(event, zeit):
        #sorgt dafür, dass bei Addition und Subtraktion das  Event in event.endzeit erhalten bleibt
        zeit.event = None

        # Prüft ob es Anhängende Events gib die leicht verschoben werden können
        #Geht diese Rekursiv durch bis eines kein nächstes Event mehr hat
        #if zeit > TimeManager.null: #verschiebung nach unten
        #    if event.eventDanach is not None:
        #        EventManager.verschiebeEventUm(event.eventDanach, zeit)
        #elif zeit < TimeManager.null:
        #    if event.eventDavor is not None:
        #        EventManager.verschiebeEventUm(event.eventDavor, zeit)

        #trenne die Verknüpfungen zu den Elementen von denen weggeschoben wird
        if zeit > TimeManager.null and not event.eventDavor is None: #es wird nach unten geschoben
            event.eventDavor.eventDanach = None
            event.eventDavor = None
        elif zeit < TimeManager.null and not event.eventDanach is None:
            event.eventDanach.eventDavor = None
            event.eventDanach = None

        #verschiebe das Event
        event.startzeit += zeit
        event.endzeit += zeit

        # Prüft nach ob das Event in eine der verbotenen Bereiche überlappt udn kürzt oder löscht das Event
        if event.startzeit < TimeManager.aufstehzeit:
            EventManager.verschiebeZeitNach(event, True, TimeManager.aufstehzeit)
        if event.endzeit > TimeManager.schlafenszeit:
            EventManager.verschiebeZeitNach(event, False, TimeManager.schlafenszeit)
        if event.schneiden(EventManager.mittagspause):
            if zeit < TimeManager.null:
                if event.endzeit <= TimeManager.mittagspauseEnde: EventManager.removeEvent(event)
                EventManager.verschiebeZeitNach(event, True, TimeManager.mittagspauseEnde)
            elif zeit >= TimeManager.null:
                if event.startzeit >= TimeManager.mittagspauseStart: EventManager.removeEvent(event)
                EventManager.verschiebeZeitNach(event, False, TimeManager.mittagspauseStart)



        # Prüft ob das Event mit anderen Events kollidiert und verschiebt diese entsprechend, danach werden auch noch
        #Events davor und danach richtig gesetzt
        otherEvents = EventManager.getEventsWithoutEvent(event)
        for oevent in otherEvents:
            if event.schneiden(oevent):
                if (event.startzeit >= event.startzeit and oevent.endzeit <= event.endzeit):  # das Oevent liegt im Event
                    if zeit < TimeManager.null:
                        EventManager.verschiebeEventUm(oevent,
                                                       event.startzeit - oevent.endzeit)  # verschiebe Event nach vorne
                        event.eventDavor = oevent
                        oevent.eventDanach = event

                    if zeit > TimeManager.null:
                        EventManager.verschiebeEventUm(oevent,
                                                       event.endzeit - oevent.startzeit)  # verschiebe Event nach hinten
                        event.eventDanach = oevent
                        oevent.eventDavor = event
                    break
                elif oevent.startzeit <= event.startzeit <= oevent.endzeit:
                    if zeit < TimeManager.null:
                        EventManager.verschiebeEventUm(oevent,
                                                       event.startzeit - oevent.endzeit)  # verschiebe Event nach vorne
                        event.eventDavor = oevent
                        oevent.eventDanach = event
                    if zeit > TimeManager.null:
                        EventManager.verschiebeEventUm(oevent,
                                                       event.endzeit - oevent.startzeit)  # verschiebe Event nach hinten
                        event.eventDanach = oevent
                        oevent.eventDavor = event
                    break
                elif oevent.startzeit > event.startzeit and oevent.endzeit > event.endzeit:  # anderes event runtscht von unten hinein
                    if zeit < TimeManager.null:
                        EventManager.verschiebeEventUm(oevent, event.startzeit - oevent.endzeit)
                        event.eventDavor = oevent
                        oevent.eventDanach = event
                    if zeit > TimeManager.null:
                        EventManager.verschiebeEventUm(oevent, event.endzeit - oevent.startzeit)
                        event.eventDanach = oevent
                        oevent.eventDavor = event
                    break
            elif event.beruehrt(oevent):
                if (oevent.startzeit < event.startzeit):
                    oevent.eventDanach = event
                    event.eventDavor = oevent
                elif (oevent.endzeit > event.endzeit):
                    oevent.eventDavor = event
                    event.eventDanach = oevent

    # Verschiebt eine Zeit, nur falls startzeit vor endzeit liegt
    @staticmethod
    def verschiebeZeitNach(event, istStartzeit, zeit):
        # überprüft ob verschiebung erlaubt
        if istStartzeit:
            if event.endzeit - zeit <= TimeManager.null: return
            event.startzeit.set(zeit)
        else:
            if zeit - event.startzeit <= TimeManager.null: return
            event.endzeit.set(zeit)

        # überschneidungen korrigieren, indem die Grenzen strikt neu verändern werden. Anhängende Teile werden nicht
        # verschoben sonder gekürzt
        otherEvents = EventManager.getEventsWithoutEvent(event)
        for oevent in otherEvents:
            if event.schneiden(oevent):
                if oevent.startzeit > event.startzeit and oevent.endzeit < event.endzeit:  # das Event liegt im neuen Element
                    EventManager.removeEvent(oevent)
                    break
                elif oevent.startzeit < event.startzeit < oevent.endzeit:  # anderes Event schneidet von oben hinein
                    oevent.endzeit.set(event.startzeit)
                    oevent.eventDanach = event
                    event.eventDavor = oevent
                    break
                elif oevent.startzeit > event.startzeit and oevent.endzeit > event.endzeit:  # anderes event runtscht von unten hinein
                    oevent.startzeit.set(event.endzeit)
                    oevent.eventDavor = event
                    event.eventDanach = oevent
                    break
            elif event.beruehrt(oevent):
                if istStartzeit and oevent.endzeit == event.startzeit:
                    event.eventDavor = oevent
                    oevent.eventDanach = event
                elif not istStartzeit and oevent.startzeit == event.endzeit:
                    event.eventDanach = oevent
                    oevent.eventDavor = event

    # Methode um Event in zwei kleinere Events zur Zeit zeit aufzuspalten
    @staticmethod
    def trenneEvent(event, zeit):
        deltaZeit = event.endzeit - zeit
        deltaZeit.event = None #damit es bei der Addition zu keinen Problemen kommt, weil beide Zeiten mit Events verknüpft sind
        if deltaZeit < TimeManager.null or zeit < event.startzeit: return  # Zeit zum Aufeilen liegt nicht im Event

        EventManager.verschiebeZeitNach(event, False, zeit)
        event2 = Event(event.endzeit, event.endzeit + deltaZeit)
        EventManager.addEvent(event2)
        return (event, event2)
    #findet event falls die Zeit zwischen inklusive Anfangszeit und exklusive Endzeit des EVents liegt
    @staticmethod
    def findeEvent(zeit):
        for event in EventManager.events:
            if event.startzeit <= zeit < event.endzeit:
                return event
        return None

    #finde Events exklusive der Grenzen
    @staticmethod
    def findeEvents(startzeit, endzeit):
        events = []
        for event in EventManager.events:
            if event.endzeit > startzeit and event.startzeit < endzeit:
                events.append(event)
        return events

    @staticmethod
    def hatEvent(event):
        return event in EventManager.events

    @staticmethod
    def addPause(zeit, dauer):
        pause = Event(zeit, zeit + dauer, True)
        events = EventManager.findeEvents(zeit, zeit + dauer)
        if len(events) == 0:
            EventManager.addEvent(pause)
        elif len(events) == 1:  # verschiebe das Event so, dass die Pause anliegt
            if (events[0].startzeit != zeit):
                events[0] = EventManager.trenneEvent(events[0], zeit)[1]
            EventManager.verschiebeEventUm(events[0], zeit + dauer - events[0].startzeit)
            EventManager.addEvent(pause)
        else:  # verschiebe alle Events so das die Pause zwar nicht anliegen muss, aber sicher genug Platz ist
            for event in events:
                EventManager.verschiebeEventUm(event, dauer)
            EventManager.addEvent(pause)
        return pause