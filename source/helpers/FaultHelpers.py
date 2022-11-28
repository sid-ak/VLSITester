from models.Fault import Fault
from models.Circuit import Circuit
from models.Gate import Gate
from models.Input import Input
from models.Output import Output

class FaultHelpers: 

    def GetFaultsInput(faultsInput: str) -> list[Fault]:
        
        if faultsInput == "": return []

        try:
            faultsStr: list[str] = faultsInput.split(",")
            faults: list[Fault] = []
            for faultStr in faultsStr:
                wire: str = faultStr.split("/")[0].strip()
                value: int = int(faultStr.split("/")[1])
                fault: Fault = Fault(wire, value)
                faults.append(fault)
            
            return faults
            
        except Exception as e:
            raise Exception(f"Invalid faults input.\n" +
                "Faults must be separated by commas and must be in the format:" +
                "<input/output name>/<fault value>\n" +
                f"Example: 1gat/0, 2gat/1\n{e}\n")

    def PrintFaults(faults: set[Fault]):
        if faults == []: return

        for fault in faults:
            print(f"\t{fault.Wire}/{fault.Value}")
    
    def SortedFaults(faults: set[Fault]) -> set[Fault]:
        try:
            sortedFaults: set[Fault] = sorted(
                faults, key = lambda e: int(e.Wire.rstrip("gat")))
            return sortedFaults

        except:
            sortedFaults: set[Fault] = sorted(
                faults, key = lambda e: e.Wire.rstrip("gat"))
            return sortedFaults
        
    def GetFaultUniverse(circuit: Circuit) -> set[Fault]:

        try:
            faultUniverse: set[Fault] = set()
            for gate in circuit.Gates:
                gateFaults: set[Fault] = FaultHelpers.GetAllGateFaults(gate)
                faultUniverse.update(gateFaults)
            
            sortedFaults: set[Fault] = FaultHelpers.SortedFaults(faultUniverse)
            return sortedFaults

        except Exception as e:
            raise Exception(
                f"\nSomething went wrong while getting fault universe for circuit {circuit.Name}.\n{e}\n")

    def GetAllGateFaults(gate: Gate) -> set[Fault]:

        try:
            faults: set[Fault] = set()

            inputs: list[Input] = gate.Inputs
            output: Output = gate.Output

            # Append input faults.
            for gateInput in inputs:
                faults.add(Fault(gateInput.Wire, 0))
                faults.add(Fault(gateInput.Wire, 1))
            
            # Append output faults.
            faults.add(Fault(output.Wire, 0))
            faults.add(Fault(output.Wire, 1))

            return faults

        except Exception as e:
            raise Exception(
                f"\nSomething went wrong while getting faults for gate.\n{e}\n")

        
