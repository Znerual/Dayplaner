from abc import ABC, abstractmethod

class Objekt(ABC):
    @abstractmethod
    def zeichne(self):
        pass

    @abstractmethod
    def zeichneMarkiert(self):
        pass

    @abstractmethod
    def fokusiere(self):
        pass

    @abstractmethod
    def unfokusiere(self):
        pass
