class Input:
    Wire: str
    IsPrimary: bool
    Value: int = -1

    def __init__(self, wire: str, isPrimary: bool, value: int = -1):
        self.Wire = wire
        self.IsPrimary = isPrimary
        self.Value = value
