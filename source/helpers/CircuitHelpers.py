from enums.GateTypeEnum import GateTypeEnum
from models.Circuit import Circuit
from helpers.GateHelpers import GateHelpers
from helpers.PrintHelpers import PrintHelpers
from models.Gate import Gate
from models.Input import Input

class CircuitHelpers:

    def PrintCircuit(circuit: Circuit, printValues = True):
        PrintHelpers.PrintThickDivider()

        print(
            "\nNote: Value of -1 signifies that the value for that wire has not been set.\n")
        
        print("\nPrimary Inputs")
        PrintHelpers.PrintThinDivider()
        for primaryInput in circuit.PrimaryInputs:
            print(f"{primaryInput.Wire}\t({primaryInput.Value})")
        
        print("\n\nPrimary Outputs")
        PrintHelpers.PrintThinDivider()
        for primaryOutput in circuit.PrimaryOutputs:
            print(f"{primaryOutput.Wire}\t({primaryOutput.Value})")

        print("\n\nGates")
        PrintHelpers.PrintThinDivider()
        GateHelpers.PrintGates(circuit.Gates, printValues = printValues)

        PrintHelpers.PrintThickDivider()

    # Sets the primary inputs for a circuit.
    def SetPrimaryInputs(circuit: Circuit, inputs: list[int]):
        
        try:
            if len(circuit.PrimaryInputs) != len(inputs):
                raise Exception(
                    "Number of primary inputs do not equal provided inputs for circuit.")

            for i, primaryInput in enumerate(circuit.PrimaryInputs):
                primaryInput.Value = inputs[i]

        except Exception as e:
            raise Exception(f"Could not set primary inputs.\n{e}")
    
    # Sets the primary outputs for a circuit.
    def SetPrimaryOutputs(circuit: Circuit) -> Circuit:

        try:
            primaryGates: list[Gate] = list(filter(
                lambda e: e.Output.IsPrimary == True, circuit.Gates))
            
            for i in range(len(circuit.PrimaryOutputs)):
                circuit.PrimaryOutputs[i] = primaryGates[i].Output
            
        except Exception as e:
            raise Exception(f"Could not set primary outputs.\n{e}")
