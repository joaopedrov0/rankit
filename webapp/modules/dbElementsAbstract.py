from abc import ABC, abstractmethod

class DBElementsAbstract(ABC):
    
    @abstractmethod
    def toDict(self):
        pass