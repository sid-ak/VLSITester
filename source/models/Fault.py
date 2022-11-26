class Fault:
    Wire: str
    Value: int

    def __init__(self, wire: str, value: int):
        self.Wire = wire
        self.Value = value
