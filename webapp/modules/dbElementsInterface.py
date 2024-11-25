from abc import ABC, abstractmethod

class DBElemensInterface(ABC):
    
    @abstractmethod
    def toDict(self):
        pass