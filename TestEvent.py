import unittest
from Event import Event
from Zeit import Zeit
class TestEvent(unittest.TestCase):
    def test_schneiden(self):
        event1 = Event(Zeit(14,0), Zeit(15,0))
        event2 = Event(Zeit(14,30), Zeit(15,30))
        event3 = Event(Zeit(15,0), Zeit(16,0))
        event4 = Event(Zeit(15,30), Zeit(16,30))
        self.assertTrue(event1.schneiden(event2))
        self.assertFalse(event1.schneiden(event4))
        self.assertTrue(event1.schneiden(event3))
        self.assertTrue(event3.schneiden(event1))
        self.assertTrue(event3.schneiden(event2))

    def test_initialisierung(self):
        zeit1 = Zeit(14, 0)
        zeit2 = Zeit(15, 30)
        event1 = Event(zeit1, Zeit(15, 0))


        self.assertEqual(str(event1), "Start 14:00 Ende 15:00")
        self.assertEqual(str(zeit1), "Zeit 14:00 zu Event Start 14:00 Ende 15:00")



if __name__ == '__main__':
    unittest.main()
