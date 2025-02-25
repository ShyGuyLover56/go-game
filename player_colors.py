from enum import Enum

class PlayerColors(Enum):
    BLACK = 0
    WHITE = 1

    def opponent(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]