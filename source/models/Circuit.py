from models.Gate import Gate
from models.Input import Input
from models.Output import Output

class Circuit:
    PrimaryInputs: list[Input]
    PrimaryOutputs: list[Output]
    Gates: list[Gate]

    def __init__(
        self,
        primaryInputs: list[Input],
        primaryOutputs: list[Output],
        gates: list[Gate]):

        self.PrimaryInputs = primaryInputs
        self.PrimaryOutputs = primaryOutputs
        self.Gates = gates
