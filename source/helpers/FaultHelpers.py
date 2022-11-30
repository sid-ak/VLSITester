from helpers.WireHelpers import WireHelpers
from models.Fault import Fault
from models.Circuit import Circuit
from models.Wire import Wire
from helpers.PrintHelpers import PrintHelpers

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

        PrintHelpers.PrintThickDivider()
        print("\nFault Universe:")
        PrintHelpers.PrintThinDivider()
        for i, fault in enumerate(faults):
            i += 1
            print(f"{i}.\t{fault.Wire}/{fault.Value}")
        
        print(f"\nTotal:\t{i}")
        PrintHelpers.PrintThickDivider()
    
    def SortedFaults(faults: set[Fault]) -> set[Fault]:
        try:
            sortedFaults: set[Fault] = sorted(
                faults, key = lambda e: int(e.Wire.rstrip("gat")) + e.Value)
            return sortedFaults

        except:
            sortedFaults: set[Fault] = sorted(
                faults, key = lambda e: e.Wire.rstrip("gat"))
            return sortedFaults
        
    def GetFaultUniverse(circuit: Circuit) -> set[Fault]:

        try:
            wires: set[Wire] = WireHelpers.GetAllWires(circuit)
            
            faults: list[Fault] = []
            for wire in wires:
                if wire.IsPrimaryInput:
                    faults.append(Fault(wire.Name, 0))
                    faults.append(Fault(wire.Name, 1))
            
            for wire in wires:
                if wire.IsFanout:
                    faults.append(Fault(f"{wire.Name}_2", 0))
                    faults.append(Fault(f"{wire.Name}_2", 1))
                    faults.append(Fault(f"{wire.Name}_3", 0))
                    faults.append(Fault(f"{wire.Name}_3", 1))
                
            return faults

        except Exception as e:
            raise Exception(
                f"\nSomething went wrong while getting fault universe for circuit {circuit.Name}.\n{e}\n")
