class Wire:
    Name: str
    IsPrimary: bool = False
    IsFanout: bool = False

    def __init__(
        self,
        name: str,
        isPrimary: bool = False,
        isFanout: bool = False):
        
        self.Name = name
        self.IsPrimary = isPrimary
        self.IsFanout = isFanout
