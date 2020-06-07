from ScreenManager import ScreenManager
from EventManager import EventManager as EM
from TimeManager import TimeManager as TM

def beenden():
    EM.speichereEvents()
    TM.speichereZeiten()
    try:
        ScreenManager.root.destroy()
    except:
        exit()


def main():
    ScreenManager.init()
    TM.ladeZeiten()
    EM.ladeEvents()
    ScreenManager.zeichneHintergrund()
    ScreenManager.root.protocol("WM_DELETE_WINDOW",beenden)
    ScreenManager.run()


main()