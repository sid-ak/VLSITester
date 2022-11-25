from helpers.PrintHelpers import PrintHelpers
from models.Gate import Gate

class GateHelpers:

    def PrintGates(gates: list[Gate]):
        tabs: str = "\t\t"
        
        print(f"Outputs{tabs}Type{tabs}Inputs")
        PrintHelpers.PrintThinDivider()
        for gate in gates:
            firstInputName: str = gate.Inputs[0].Name
            secondInputName: str = ""
            if len(gate.Inputs) > 1:
                secondInputName = gate.Inputs[1].Name

            print(f"{gate.Output.Name}{tabs}" +
                f"{gate.Type.name}{tabs}" +
                f"{firstInputName}\t{secondInputName}")
