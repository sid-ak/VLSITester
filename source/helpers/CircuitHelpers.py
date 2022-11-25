from models.Circuit import Circuit
from helpers.GateHelpers import GateHelpers
from helpers.PrintHelpers import PrintHelpers

class CircuitHelpers:

    def PrintCircuit(circuit: Circuit):
        PrintHelpers.PrintThickDivider()
        
        print("\nPrimary Inputs")
        PrintHelpers.PrintThinDivider()
        for primaryInput in circuit.PrimaryInputs: print(primaryInput.Name)
        
        print("\nPrimary Outputs")
        PrintHelpers.PrintThinDivider()
        for primaryOutput in circuit.PrimaryOutputs: print(primaryOutput.Name)

        print("\nGates")
        PrintHelpers.PrintThinDivider()
        GateHelpers.PrintGates(circuit.Gates)

        PrintHelpers.PrintThickDivider()
