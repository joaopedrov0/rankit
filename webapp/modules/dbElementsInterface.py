from abc import ABC, abstractmethod

class DBElemensInterface(ABC):
    
    @abstractmethod
    def createDict(self):
        pass