import unittest
from Event import Event
from Zeit import Zeit
from EventManager import EventManager as EM
from TimeManager import TimeManager as TM

# Hier wird die Klasse Event sowie die Klasse EventManager getestet
class TestEvent(unittest.TestCase):
    def test_schneiden(self):
        event1 = Event(Zeit(14, 0), Zeit(15, 0))
        event2 = Event(Zeit(14, 30), Zeit(15, 30))
        event3 = Event(Zeit(15, 0), Zeit(16, 0))
        event4 = Event(Zeit(15, 30), Zeit(16, 30))
        event5 = Event(Zeit(11, 30), Zeit(16, 30))

        self.assertTrue(event1.schneiden(event2))
        self.assertFalse(event1.schneiden(event4))
        self.assertFalse(event1.schneiden(event3))
        self.assertFalse(event3.schneiden(event1))
        self.assertTrue(event3.schneiden(event2))
        self.assertTrue(event5.schneiden(event4))
        self.assertTrue(event2.schneiden(event2))
    def test_beruehren(self):
        event1 = Event(Zeit(14, 0), Zeit(15, 0))
        event2 = Event(Zeit(14, 30), Zeit(15, 30))
        event3 = Event(Zeit(15, 0), Zeit(16, 0))
        event4 = Event(Zeit(17, 0), Zeit(18, 0))

        self.assertTrue(event1.beruehrt(event2))
        self.assertTrue(event1.beruehrt(event3))
        self.assertFalse(event1.beruehrt(event4))
        self.assertTrue(event3.beruehrt(event1))
        self.assertFalse(event4.beruehrt(event2))

    def test_initialisierung(self):
        zeit1 = Zeit(14, 0)
        event1 = Event(zeit1, Zeit(15, 0))

        self.assertEqual(str(event1), "Start 14:00 Ende 15:00")
        self.assertEqual(str(zeit1), "Zeit 14:00 zu Event Start 14:00 Ende 15:00")

    def test_addEvent(self):
        EM.events = []
        event1 = Event(Zeit(14, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(17, 00))
        event3 = Event(Zeit(14, 45), Zeit(17, 00))
        lsg1 = Event(Zeit(15, 0), Zeit(16, 30))

        EM.addEvent(event1)
        EM.addEvent(event2)
        # hinzufügen ohne Überlapp
        self.assertEqual(str(EM.events[0]), "Start 14:30 Ende 15:00")
        self.assertEqual(str(EM.events[1]), "Start 16:30 Ende 17:00")

        # mit überlapp
        EM.addEvent(event3)


        self.assertTrue(EM.hatEvent(lsg1))
        self.assertTrue(EM.hatEvent(event1))
        self.assertTrue(EM.hatEvent(event2))

    def test_verbindung(self):
        EM.events = []
        event1 = Event(Zeit(14, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(17, 00))
        event3 = Event(Zeit(14, 45), Zeit(17, 00))
        event4 = Event(Zeit(17, 00), Zeit(18, 00))
        event5 = Event(Zeit(11, 00), Zeit(14, 30))

        lsg1 = Event(Zeit(15, 0), Zeit(16, 30))

        EM.addEvent(event1)
        EM.addEvent(event2)
        EM.addEvent(event3)
        EM.addEvent(event4)
        EM.addEvent(event5)
        #for event in EM.events:
        #    print(f"{event}")

        self.assertEqual(event1.eventDanach, lsg1)
        self.assertEqual(event2.eventDavor, lsg1)
        self.assertEqual(event2.eventDanach, event4)
        self.assertEqual(event5.eventDanach, event1)

    def test_findeEvent(self):
        EM.events = []
        event1 = Event(Zeit(14, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(17, 00))
        event3 = Event(Zeit(14, 45), Zeit(17, 00))

        EM.addEvent(event1)
        EM.addEvent(event2)
        EM.addEvent(event3)

        lsg1 = EM.findeEvent(Zeit(14,45))
        lsg2 = EM.findeEvent(Zeit(15,00))
        lsg3 = EM.findeEvent(Zeit(16,30))

        self.assertEqual(event1, lsg1)
        self.assertEqual(event3, lsg2)
        self.assertEqual(event2, lsg3)

    def test_findeEvents(self):
        EM.events = []
        event1 = Event(Zeit(14, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(17, 00))
        event3 = Event(Zeit(14, 45), Zeit(17, 00))

        EM.addEvent(event1)
        EM.addEvent(event2)
        EM.addEvent(event3)

        lsg = EM.findeEvents(Zeit(15, 0), Zeit(20,0))


        self.assertTrue(event2 in lsg and event3 in lsg)
        self.assertFalse(event1 in lsg)

    def test_trenneEvent(self):
        EM.events = []

        event1 = Event(Zeit(11, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(22, 00))
        event3 = Event(Zeit(14, 45), Zeit(17, 00))

        lsg1 =Event(Zeit(11, 30), Zeit(14, 30))
        lsg2 =Event(Zeit(14, 30), Zeit(15,0))
        lsg3 = Event(Zeit(14,45), Zeit(15,00))
        EM.addEvent(event1)
        EM.addEvent(event2)
        EM.addEvent(event3)

        EM.trenneEvent(event1, Zeit(14,30))
        self.assertEqual(str(EM.findeEvent(Zeit(12,0))), str(lsg1))
        self.assertEqual(str(EM.findeEvent(Zeit(14,30))), str(lsg2))
        EM.trenneEvent(EM.findeEvent(Zeit(14,55)), Zeit(14,45)) #trenne ein getrenntes Event
        self.assertEqual(str(EM.findeEvent(Zeit(14,55))), str(lsg3))

        EM.events = []
        event1 = Event(Zeit(11, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(22, 00))
        event3 = Event(Zeit(14, 45), Zeit(17, 00))
        EM.addEvent(event1)
        EM.addEvent(event2)
        EM.addEvent(event3)

        EM.trenneEvent(event3, Zeit(17, 0))  # event3 endet bei 16:30, dh trennung bei 17 tut nichts
        self.assertEqual(str(EM.findeEvent(Zeit(16, 55))), str(event2))
    def test_removeElement(self):
        EM.events = []
        event1 = Event(Zeit(11, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(22, 00))
        event3 = Event(Zeit(14, 45), Zeit(17, 00))
        EM.addEvent(event1)
        EM.addEvent(event2)
        EM.addEvent(event3)
        EM.removeEvent(event1)
        self.assertIsNone(EM.findeEvent(Zeit(12,0)))
        self.assertEqual(len(EM.events), 2)
    def test_verschiebeEventsUmSimple(self):
        EM.events = []
        TM.schlafenszeit = Zeit(23, 0)
        EM.mittagspause = Event(Zeit(0, 0), Zeit(0, 0))
        event1 = Event(Zeit(12, 0), Zeit(14, 00))
        event2 = Event(Zeit(14, 0), Zeit(16, 00))

        EM.addEvent(event1)
        EM.addEvent(event2)

        lsg1 = Event(Zeit(13, 0), Zeit(15, 00))
        lsg2 = Event(Zeit(15, 0), Zeit(17, 00))
        EM.verschiebeEventUm(event1, Zeit(1,0))
        self.assertEqual(str(event1), str(lsg1))
        self.assertEqual(str(event2), str(lsg2))

    def test_verschiebeEventsUmSimple2(self):
        EM.events = []
        TM.schlafenszeit = Zeit(23, 0)
        EM.mittagspause = Event(Zeit(0, 0), Zeit(0, 0))
        event1 = Event(Zeit(12, 0), Zeit(14, 00))
        event2 = Event(Zeit(14, 0), Zeit(16, 00))

        EM.addEvent(event1)
        EM.addEvent(event2)

        lsg1 = Event(Zeit(11, 0), Zeit(13, 00))
        lsg2 = Event(Zeit(13, 0), Zeit(15, 00))
        EM.verschiebeEventUm(event2, Zeit(-1,0))
        self.assertEqual(str(event1), str(lsg1))
        self.assertEqual(str(event2), str(lsg2))

    def test_verschiebeUmMittagspause(self):
        EM.events = []
        TM.schlafenszeit = Zeit(23, 0)
        EM.mittagspause = Event(Zeit(12, 0), Zeit(13, 0))

        event1 = Event(Zeit(10, 0), Zeit(12, 00))
        event2 = Event(Zeit(13, 0), Zeit(15, 00))

        EM.addEvent(event1)
        EM.addEvent(event2)
        lsg1 = Event(Zeit(13, 0), Zeit(15, 00))
        lsg2 = Event(Zeit(15, 0), Zeit(17, 00))
        EM.verschiebeEventUm(event1, Zeit(3,0))

        
        self.assertEqual(str(event1), str(lsg1))
        self.assertEqual(str(event2), str(lsg2))
    def test_verschiebeEventUm(self):
        EM.events = []
        TM.schlafenszeit = Zeit(23,0)
        EM.mittagspause = Event(Zeit(0,0), Zeit(0,0))
        event1 = Event(Zeit(11, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(22, 00))
        event3 = Event(Zeit(15, 00), Zeit(16, 30))

        lsg1 = Event(Zeit(17, 30), Zeit(23, 00))
        lsg2 = Event(Zeit(18, 30), Zeit(23, 00))

        lsg3 = Event(Zeit(12, 30), Zeit(16, 00)) #event1 3. Verschiebung
        lsg4 = Event(Zeit(16,0), Zeit(17, 30)) #event3 3.V
        lsg5 = Event(Zeit(18, 30), Zeit(23, 00)) #event2 3.V
        EM.addEvent(event1)
        EM.addEvent(event2)
        EM.addEvent(event3)
        EM.verschiebeEventUm(event2, Zeit(1,0))
        self.assertEqual(str(EM.findeEvent(Zeit(18,00))), str(lsg1))
        self.assertEqual(lsg1, event2)

        EM.verschiebeEventUm(event2, Zeit(1,0)) #verschiebe in die Schlafenszeit hinein
        self.assertEqual(str(EM.findeEvent(Zeit(19, 00))), str(lsg2))
        self.assertEqual(lsg2, event2)

        EM.verschiebeEventUm(event1, Zeit(1,0)) #verschiebe mit anhängenden Events

        self.assertEqual(str(EM.findeEvent(Zeit(13,0))), str(lsg3)) #event1 verschoben
        self.assertEqual(str(event1), str(lsg3))

        self.assertEqual(str(EM.findeEvent(Zeit(17, 0))), str(lsg4))  # event3 verschoben
        self.assertEqual(str(event3), str(lsg4))

        self.assertEqual(str(EM.findeEvent(Zeit(20, 0))), str(lsg5)) # event2 verschoben
        self.assertEqual(event2, lsg5)

    def test_verschiebeZeitNach(self):
        EM.events = []
        TM.schlafenszeit = Zeit(23, 0)
        EM.mittagspause = Event(Zeit(0, 0), Zeit(0, 0))
        event1 = Event(Zeit(11, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(22, 00))

        lsg1 = Event(Zeit(11, 30), Zeit(16, 30))
        lsg2 = Event(Zeit(11, 30), Zeit(17, 00))
        lsg3 = Event(Zeit(17, 00), Zeit(22, 00))

        EM.addEvent(event1)
        EM.addEvent(event2)

        EM.verschiebeZeitNach(event1, False, Zeit(16,30))
        self.assertEqual(str(event1.eventDanach), str(event2))
        self.assertEqual(str(event2.eventDavor), str(event1))
        self.assertEqual(str(event1), str(lsg1))

        EM.verschiebeZeitNach(event1, False, Zeit(17,0))
        self.assertEqual(str(event1.eventDanach), str(event2))
        self.assertEqual(str(event2.eventDavor), str(event1))
        self.assertEqual(str(event1), str(lsg2))
        self.assertEqual(str(event2), str(lsg3))

    def test_addPause(self):
        EM.events = []
        TM.schlafenszeit = Zeit(23, 0)
        EM.mittagspause = Event(Zeit(0, 0), Zeit(0, 0))


        event1 = Event(Zeit(11, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(22, 00))

        EM.addEvent(event1)
        EM.addEvent(event2)

        lsg1 = Event(Zeit(11, 30), Zeit(13, 00))
        pause = Event(Zeit(13, 0), Zeit(13, 15))
        lsg2 = Event(Zeit(13, 15), Zeit(15, 15))
        lsg3 = Event(Zeit(16, 30), Zeit(22, 00))
        EM.addPause(Zeit(13,00), Zeit(0,15))

        self.assertEqual(str(event1), str(lsg1))
        self.assertEqual(str(EM.findeEvent(Zeit(13,5))), str(pause))
        self.assertTrue(EM.findeEvent(Zeit(13,5)).istPause)
        self.assertEqual(str(EM.findeEvent(Zeit(13,20))), str(lsg2))
        self.assertEqual(str(event2), str(lsg3))

    def test_addPause2(self):
        EM.events = []
        TM.schlafenszeit = Zeit(23, 0)
        EM.mittagspause = Event(Zeit(0, 0), Zeit(0, 0))


        event1 = Event(Zeit(11, 30), Zeit(15, 00))
        event2 = Event(Zeit(16, 30), Zeit(22, 00))

        EM.addEvent(event1)
        EM.addEvent(event2)

        lsg1 = Event(Zeit(11, 30), Zeit(13, 00))
        pause = Event(Zeit(13, 0), Zeit(15, 0))
        lsg2 = Event(Zeit(15, 0), Zeit(17, 00))
        lsg3 = Event(Zeit(17, 00), Zeit(22, 30))
        EM.addPause(Zeit(13,00), Zeit(2,0))

        self.assertEqual(str(event1), str(lsg1))
        self.assertEqual(str(EM.findeEvent(Zeit(13,5))), str(pause))
        self.assertTrue(EM.findeEvent(Zeit(13,5)).istPause)
        self.assertEqual(str(EM.findeEvent(Zeit(15,20))), str(lsg2))
        self.assertEqual(str(event2), str(lsg3))
if __name__ == '__main__':
    unittest.main()
