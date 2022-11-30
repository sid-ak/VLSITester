class Output:
    Wire: str
    IsPrimary: bool
    IsFanout: bool = False
    Value: int = -1

    def __init__(
        self,
        wire: str,
        isPrimary: bool,
        isFanout: bool = False,
        value: int = -1):
        
        self.Wire = wire
        self.IsPrimary = isPrimary
        self.IsFanout = isFanout
        self.Value = value
