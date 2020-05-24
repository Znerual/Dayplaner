import unittest
from Farbkonzept import Farbkonzept


class MyTestCase(unittest.TestCase):
    def test_Farben(self):
        root = Tk()
        canvas = Canvas(root, width=800, height=600, bg='yellow')
        canvas.pack()
        rec = canvas.create_rectangle(10, 20, 60, 40, fill='green')
        test = Farbkonzept.vormittag(rec)
        self.assertEqual(test, '#012040')


if __name__ == '__main__':
    unittest.main()
