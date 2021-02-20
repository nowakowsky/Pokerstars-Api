import enum

class Colors(enum.Enum):
    Hearts = "H"    # Kier (serce)
    Tiles = "T"     # Karo (diamenty)
    Clovers = "C"   # Trefl (żołędzie)
    Pikes = "P"     # Pik (wino)
    Error = "X"     # No color detecred

class Card:
    def __init__(self, value: str, color: Colors):
        self.value = value
        self.color = color
    
    def __str__(self):
        return self.color.value + self.value

if __name__ == "__main__":
    floop = Card("9", Colors.Hearts), Card("2", Colors.Pikes), Card("A", Colors.Clovers)
    print (*floop)