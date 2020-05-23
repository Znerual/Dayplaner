import unittest
from Zeit import Zeit


class TestKlasse(unittest.TestCase):
    def test_Zeit_von_String(self):
        test1 = "13"
        test2 = "25"
        test3 = "14:30"
        test4 = "15:312"
        zeit1 = Zeit.fromString(test1)
        zeit2 = Zeit.fromString(test2)
        zeit3 = Zeit.fromString(test3)
        zeit4 = Zeit.fromString(test4)
        lsg1 = "Zeit 13:00"
        lsg3 = "Zeit 14:30"
        self.assertEqual(str(zeit1), lsg1)
        self.assertIsNone(zeit2, "Zeit richtig verworfen")
        self.assertEqual(str(zeit3), lsg3)
        self.assertIsNone(zeit4, "Zeit richtig verworfen")
    def test_circa(self):
        zeit1 = Zeit(14,35)
        zeit2 = Zeit(14,32)
        zeit3 = Zeit(15,00)
        Zeit.toleranz = (0,5)
        self.assertTrue(zeit1.circa(zeit2))
        self.assertTrue(zeit2.circa(zeit2))
        self.assertFalse(zeit1.circa(zeit3))
        self.assertFalse(zeit3.circa(zeit1))

    def test_addition(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit3 = Zeit(3,30)
        zeit4 = Zeit(12,30)
        self.assertEqual(str(zeit1 + zeit2), "Zeit 16:35")
        self.assertEqual(str(zeit1 + zeit3), "Zeit 18:05")
        #self.assertIsNone(str(zeit1 + zeit4))

    def test_subtraktion(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit3 = Zeit(3, 40)
        zeit4 = Zeit(12, 30)
        self.assertEqual(str(zeit1 - zeit2), "Zeit 12:35")
        self.assertEqual(str(zeit1 - zeit3), "Zeit 10:55")
        #self.assertIsNone(str(zeit3 - zeit4))
    def test_groesser(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit3 = Zeit(2, 0)
        zeit4 = Zeit(12, 30)

        self.assertTrue(zeit1 > zeit2)
        self.assertTrue(zeit1 > zeit4)
        self.assertFalse(zeit2 > zeit3)
        self.assertFalse(zeit4 > zeit1)

    def test_groesser_gleich(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit4 = Zeit(12, 30)

        self.assertTrue(zeit2 >= zeit2)
        self.assertFalse(zeit4 >= zeit1)
        self.assertTrue(zeit1 >= zeit2)

    def test_kleiner(self):
        zeit1 = Zeit(14, 35)
        zeit2 = Zeit(2, 0)
        zeit3 = Zeit(12, 30)

        self.assertTrue(zeit2 < zeit1)
        self.assertTrue(zeit3 < zeit1)
        self.assertFalse(zeit3 < zeit2)
        self.assertFalse(zeit2 < zeit2)
if __name__ == '__main__':
    unittest.main()