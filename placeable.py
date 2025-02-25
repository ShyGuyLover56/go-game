from abc import ABC, abstractmethod
class Placeble(ABC):
    def __init__(self, color: PlayerColors):
        self.__color = color
        pass