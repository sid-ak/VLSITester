from helpers.WireHelpers import WireHelpers
from models.Fault import Fault
from models.Circuit import Circuit
from models.Wire import Wire
from helpers.PrintHelpers import PrintHelpers
from helpers.CommonHelpers import CommonHelpers

class FaultHelpers: 

    def GetFaultsInput(faultsInput: str, circuit: Circuit) -> list[Fault]:
        
        if faultsInput == "": return []
        allWires: list[Wire] = WireHelpers.GetAllWires(circuit)
        allWireNames: list[str] = list(map(lambda e: e.Name, allWires))

        try:
            faultsStr: list[str] = faultsInput.split(",")
            faults: list[Fault] = []
            for faultStr in faultsStr:
                wire: str = faultStr.split("/")[0].strip()
                if wire not in allWireNames: raise Exception("Wire does not exist.")
                
                value: int = int(faultStr.split("/")[1])
                if CommonHelpers.IsNotZeroOrOne(value): raise Exception("Fault value not 0 or 1.")

                fault: Fault = Fault(wire, value)
                faults.append(fault)
            
            return faults
            
        except Exception as e:
            raise Exception(f"Invalid faults input.\n" +
                "Faults must be separated by commas and must be in the format:" +
                "<wireName>/<faultValue>\n" +
                f"Example: 1gat/0, 2gat/1\n" +
                f"Also ensure that the wire exists and the fault value is is a 0 or 1.\n{e}\n")

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
