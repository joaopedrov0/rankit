from abc import ABC, abstractmethod

class DBElementsInterface(ABC):
    
    @abstractmethod
    def toDict(self):
        pass