import unittest
from Event import Event
from Zeit import Zeit
from EventManager import EventManager as EM

#Hier wird die Klasse Event sowie die Klasse EventManager getestet
class TestEvent(unittest.TestCase):
    def test_schneiden(self):
        event1 = Event(Zeit(14,0), Zeit(15,0))
        event2 = Event(Zeit(14,30), Zeit(15,30))
        event3 = Event(Zeit(15,0), Zeit(16,0))
        event4 = Event(Zeit(15,30), Zeit(16,30))
        event5 = Event(Zeit(11,30), Zeit(16,30))

        self.assertTrue(event1.schneiden(event2))
        self.assertFalse(event1.schneiden(event4))
        self.assertFalse(event1.schneiden(event3))
        self.assertFalse(event3.schneiden(event1))
        self.assertTrue(event3.schneiden(event2))
        self.assertTrue(event5.schneiden(event4))

    def test_initialisierung(self):
        zeit1 = Zeit(14, 0)
        zeit2 = Zeit(15, 30)
        event1 = Event(zeit1, Zeit(15, 0))


        self.assertEqual(str(event1), "Start 14:00 Ende 15:00")
        self.assertEqual(str(zeit1), "Zeit 14:00 zu Event Start 14:00 Ende 15:00")

    def test_addEvent(self):
        EM.events = []
        event1 = Event(Zeit(14,30), Zeit(15,00))
        event2 = Event(Zeit(16,30), Zeit(17,00))
        event3 = Event(Zeit(14,45), Zeit(17,00))
        lsg1 = Event(Zeit(15,0), Zeit(16,30))

        EM.addEvent(event1)
        EM.addEvent(event2)
        #hinzufügen ohne Überlapp
        self.assertEqual(str(EM.events[0]), "Start 14:30 Ende 15:00")
        self.assertEqual(str(EM.events[1]), "Start 16:30 Ende 17:00")

        #mit überlapp
        EM.addEvent(event3)

        for event in EM.events:
            print(f"{event}")
        self.assertTrue(EM.hatEvent(lsg1))
        self.assertTrue(EM.hatEvent(event1))
        self.assertTrue(EM.hatEvent(event2))

if __name__ == '__main__':
    unittest.main()
