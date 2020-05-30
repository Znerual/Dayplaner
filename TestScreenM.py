import unittest
from Farbkonzept import Farbkonzept
from tkinter import *
from Zeit import Zeit
from ScreenManager import ScreenManager as SM
from TimeManager import TimeManager as TM


class TestScreenManager(unittest.TestCase):

    def callbackClick(self, event):
        SM.canvas.itemconfig(self.text, text=str(event.x) + " " + str(event.y) + " " + str(SM.pixelZuZeit(event.y)))

    def test_Farben(self):
        SM.init()
        # root = Tk()
        # canvas = Canvas(root, width=250, height=400)
        # canvas.pack() #beim rectangle(x1,y1,x2,y2) koo der linken oberen und rechten unteren ecke

        #recvm = SM.canvas.create_rectangle(50, 50, 200, 100, fill=Farbkonzept.vormittag())
        #recvmm = SM.canvas.create_rectangle(50, 100, 200, 150, fill=Farbkonzept.vormittag_markiert())
        #recmi = SM.canvas.create_rectangle(50, 150, 200, 200, fill=Farbkonzept.mittagspause())
        #recmim = SM.canvas.create_rectangle(50, 200, 200, 250, fill=Farbkonzept.mittagspause_markiert())
        #recnm = SM.canvas.create_rectangle(50, 250, 200, 300, fill=Farbkonzept.nachmittag())
        #recnmm = SM.canvas.create_rectangle(50, 300, 200, 350, fill=Farbkonzept.nachmittag_markiert())
        self.text = SM.canvas.create_text(100, 20, text="Position")
        SM.canvas.create_text(100,50, text=f"{SM.canvasHeight} vs {SM.screenHeight}")
        SM.canvas.bind("<Button-1>", self.callbackClick)
        SM.zeichneHintergrund()

        SM.run()
        # kann rectangle nicht als objekt übergeben, hat nicht property configure

        # root.mainloop()
        # self.assertEqual(test, '#012040')

    def test_pixelZeit(self):
        SM.canvasHeight = 600
        z = Zeit(12, 0)
        zeit1 = SM.pixelZuZeit(500)
        y1 = SM.zeitZuPixel(zeit1)
        y2 = SM.zeitZuPixel(z)
        zeit2 = SM.pixelZuZeit(y2)

        self.assertEqual(500, y1)
        self.assertEqual(z, zeit2)

    def test_pixelZuZeit(self):
        SM.canvasHeight = 500
        TM.aufstehzeit = Zeit(10, 0)
        TM.schlafenszeit = Zeit(18, 0)

        y1 = 50  # erster Valider Wert
        y2 = 100

        lsg1 = TM.aufstehzeit
        lsg2 = Zeit(11, 0)

        zeit1 = SM.pixelZuZeit(y1)
        zeit2 = SM.pixelZuZeit(y2)

        self.assertEqual(str(zeit1), str(lsg1))
        self.assertEqual(str(zeit2), str(lsg2))

    def test_zeitZuPixel(self):
        SM.canvasHeight = 500
        TM.aufstehzeit = Zeit(10, 0)
        TM.schlafenszeit = Zeit(18, 0)

        zeit1 = TM.aufstehzeit
        zeit2 = Zeit(11, 0)

        lsg1 = 50  # erster Valider Wert
        lsg2 = 100

        y1 = SM.zeitZuPixel(zeit1)
        y2 = SM.zeitZuPixel(zeit2)

        self.assertEqual(y1, lsg1)
        self.assertEqual(y2, lsg2)


if __name__ == '__main__':
    unittest.main()
