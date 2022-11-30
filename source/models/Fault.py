class Fault:
    Wire: str
    Value: int
    IsDetected: bool = False
    DetectedOn: list[str] = []
    IsFanout: bool = False

    def __init__(
        self, wire: str,
        value: int,
        isDetected: bool = False,
        detectedOn: str = [],
        isFanout: bool = False):
        
        self.Wire = wire
        self.Value = value
        self.IsDetected = isDetected
        self.DetectedOn = detectedOn
        self.IsFanout = isFanout
