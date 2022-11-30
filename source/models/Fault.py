class Fault:
    Wire: str
    Value: int
    IsDetected: bool = False
    DetectedOn: list[str] = []

    def __init__(
        self, wire: str,
        value: int,
        isDetected: bool = False,
        detectedOn: str = []):
        
        self.Wire = wire
        self.Value = value
        self.IsDetected = isDetected
        self.DetectedOn = detectedOn
