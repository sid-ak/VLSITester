class Wire:
    Name: str
    IsPrimaryInput: bool = False
    IsPrimaryOutput: bool = False
    IsFanout: bool = False

    def __init__(
        self,
        name: str,
        isPrimaryInput: bool = False,
        isPrimaryOutput: bool = False,
        isFanout: bool = False):
        
        self.Name = name
        self.IsPrimaryInput = isPrimaryInput
        self.IsPrimaryOutput = isPrimaryOutput
        self.IsFanout = isFanout
