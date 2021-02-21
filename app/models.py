import enum
import os
class Colors(enum.Enum):
    Hearts = "H"
    Tiles = "T"
    Clovers = "C"
    Pikes = "P"
    Error = "X"

class Card:
    def __init__(self, value: str, color: Colors):
        self.value = value
        self.color = color
    
    def __str__(self):
        return self.color.value + self.value

    # seems like printing lists requires that one
    def __repr__(self):
        return self.color.value + self.value

    def __eq__(self, other):
        return self.value == other.value and self.color == other.color

class Screenshot:
    tableName = ""
    filename  = ""
    def __init__(self, tableName, screenshot):
        self.tableName = tableName
        self.filename = screenshot

    def __str__(self):
        return self.filename

    def __del__(self):
        # __del__ is not a destructor in a classic way
        # it is called by GC when it destroys an object
        # so this is pretty nice way to remove screenshot from hdd
        os.remove(self.filename)