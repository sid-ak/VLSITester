class Input:
    Name: str
    IsPrimary: bool
    Value: int

    def __init__(self, name: str, isPrimary: bool, value: int = -1):
        self.Name = name
        self.IsPrimary = isPrimary
        self.Value = value
