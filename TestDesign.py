import unittest
from Farbkonzept import Farbkonzept


class MyTestCase(unittest.TestCase):
    #def test_Farben(self):
     #   root = Tk()
     #   canvas = Canvas(root, width=800, height=600, bg='yellow')
     #   canvas.pack()
     #   rec = canvas.create_rectangle(10, 20, 60, 40, fill='green')
     #   test = Farbkonzept.vormittag(rec)
     #   self.assertEqual(test, '#012040')

    def test_PixelZeit(self):
        from ScreenManager import ScreenManager
        z="12:00"
        #zeit1=ScreenManager.PixelZuZeit(500)
        #y1=ScreenManager.ZeitZuPixel(zeit1)
        y2=ScreenManager.ZeitZuPixel(z)
        #zeit2=ScreenManager.PixelZuZeit(y2)
        self.assertEqual(y2,400)#wär eh false gewesen, wollte aber schaun (ob) was für y2 rauskommt
        #self.assertEqual(500,y1)
        #self.assertEqual(z,zeit2)
if __name__ == '__main__':
    unittest.main()
