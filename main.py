from ScreenManager import ScreenManager
from EventManager import EventManager as EM
from TimeManager import TimeManager as TM
import atexit
def main():
    TM.ladeZeiten()
    EM.ladeEvents()
    ScreenManager.init()
    ScreenManager.zeichneHintergrund()
    ScreenManager.run()

    #Führt beim beenden noch die Funktionen speichereEvents() und speichereZeiten() aus
    atexit.register(EM.speichereEvents)
    atexit.register(TM.speichereZeiten)
main()