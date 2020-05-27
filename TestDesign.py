import unittest
from Farbkonzept import Farbkonzept
from tkinter import *


class MyTestCase(unittest.TestCase):
    def test_Farben(self):
        root = Tk()
        canvas = Canvas(root, width=250, height=400)
        canvas.pack() #beim rectangle(x1,y1,x2,y2) koo der linken oberen und rechten unteren ecke
        recvm = canvas.create_rectangle(50, 50, 200, 100 ,fill=Farbkonzept.vormittag())
        recvmm= canvas.create_rectangle(50, 100, 200, 150 ,fill=Farbkonzept.vormittag_markiert())
        recmi = canvas.create_rectangle(50,150, 200, 200, fill=Farbkonzept.mittagspause())
        recmim= canvas.create_rectangle(50, 200, 200, 250 ,fill=Farbkonzept.mittagspause_markiert())
        recnm = canvas.create_rectangle(50, 250, 200, 300, fill=Farbkonzept.nachmittag())
        recnmm= canvas.create_rectangle(50, 300, 200, 350, fill=Farbkonzept.nachmittag_markiert())

        #kann rectangle nicht als objekt übergeben, hat nicht property configure
        root.mainloop()
        #self.assertEqual(test, '#012040')

    #def test_PixelZeit(self):
     #   from ScreenManager import ScreenManager
      #  z="12:00"
       # #zeit1=ScreenManager.PixelZuZeit(500)
        ##y1=ScreenManager.ZeitZuPixel(zeit1)
        #y2=ScreenManager.ZeitZuPixel(z)
        ##zeit2=ScreenManager.PixelZuZeit(y2)
        #self.assertEqual(y2,400)#wär eh false gewesen, wollte aber schaun (ob) was für y2 rauskommt
        ##self.assertEqual(500,y1)
        ##self.assertEqual(z,zeit2)
if __name__ == '__main__':
    unittest.main()
