from enums.GateTypeEnum import GateTypeEnum
from models.Input import Input
from models.Output import Output as OutputModel

class Gate:
    Type: GateTypeEnum
    Inputs: list[Input]
    Output: OutputModel

    def __init__(
        self,
        type: GateTypeEnum,
        inputs: list[int],
        output: int):

        self.Type = type 
        self.Inputs = inputs
        self.Output = output
