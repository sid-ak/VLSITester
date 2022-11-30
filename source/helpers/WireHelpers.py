from models.Wire import Wire
from models.Circuit import Circuit
from models.Input import Input
from models.Output import Output
from models.Gate import Gate
from subclasses.SetReturns import SetReturns

class WireHelpers:

    def SortedWires(wires: set[Wire]) -> set[Wire]:
        try:
            sortedWires: set[Wire] = sorted(
                wires, key = lambda e: int(e.Name.rstrip("gat")))
            return sortedWires

        except:
            sortedWires: set[Wire] = sorted(
                wires, key = lambda e: e.Name.rstrip("gat"))
            return sortedWires

    # Gets all wires from a circuit.
    def GetAllWires(circuit: Circuit) -> set[Wire]:

        try:
            wireSet: SetReturns[str] = SetReturns()
            wires: set[Wire] = set()
            
            # Add primary input wires.
            primaryInputs: list[Input] = circuit.PrimaryInputs
            for primaryInput in primaryInputs:
                if wireSet.add(primaryInput.Wire):
                    wires.add(Wire(
                        name = primaryInput.Wire,
                        isPrimaryInput = primaryInput.IsPrimary,
                        isFanout = primaryInput.IsFanout,
                    ))
            
            # Add primary output wires.
            primaryOutputs: list[Output] = circuit.PrimaryOutputs
            for primaryOutput in primaryOutputs:
                if wireSet.add(primaryOutput.Wire):
                    wires.add(Wire(
                        name = primaryOutput.Wire,
                        isPrimaryOutput = primaryOutput.IsPrimary,
                        isFanout = primaryOutput.IsFanout,
                    ))
            
            # Add all gate input and output wires.
            allGates: list[Gate] = circuit.Gates
            for gate in allGates:
                for gateInput in gate.Inputs:
                    if wireSet.add(gateInput.Wire):
                        wires.add(Wire(
                            name = gateInput.Wire,
                            isPrimaryInput = gateInput.IsPrimary,
                            isFanout = gateInput.IsFanout,
                        ))
                
                if wireSet.add(gate.Output.Wire):
                    wires.add(Wire(
                        name = gate.Output.Wire,
                        isPrimaryOutput = gate.Output.IsPrimary,
                        isFanout = gate.Output.IsFanout,
                    ))

            sortedWires: set[Wire] = WireHelpers.SortedWires(wires)
            return sortedWires

        except:
            raise Exception(f"Unable to get all wires from circuit {circuit.Name}\n{e}")
