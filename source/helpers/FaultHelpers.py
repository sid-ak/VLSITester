from helpers.LogicHelpers import LogicHelpers
from helpers.WireHelpers import WireHelpers
from models.Fault import Fault
from models.Circuit import Circuit
from models.Input import Input
from models.Wire import Wire
from models.Gate import Gate
from helpers.PrintHelpers import PrintHelpers
from helpers.CommonHelpers import CommonHelpers

class FaultHelpers: 

    def PrintFaults(faults: set[Fault]):
    
        try:
            if faults == []: return

            PrintHelpers.PrintThickDivider()
            for i, fault in enumerate(faults):
                i += 1
                print(f"{i}.\t{fault.Wire}/{fault.Value}")
            
            print(f"\nTotal:\t{i}")
            PrintHelpers.PrintThickDivider()
        
        except Exception as e:
            raise Exception(f"Unable to print faults.\n{e}")

    # Converts a faults input string to a list of Faults.
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
   
    # Sorts all the faults using the wire name as the key.
    def SortedFaults(faults: set[Fault]) -> set[Fault]:
        try:
            sortedFaults: set[Fault] = sorted(
                faults, key = lambda e: int(e.Wire.rstrip("gat")) + e.Value)
            return sortedFaults

        except:
            sortedFaults: set[Fault] = sorted(
                faults, key = lambda e: e.Wire.rstrip("gat"))
            return sortedFaults
    
    # Gets a list of all checkpoint fault classes in a circuit.
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
                    faults.append(Fault(f"{wire.Name}_a", 0))
                    faults.append(Fault(f"{wire.Name}_a", 1))
                    faults.append(Fault(f"{wire.Name}_b", 0))
                    faults.append(Fault(f"{wire.Name}_b", 1))
                
            return faults

        except Exception as e:
            raise Exception(
                f"\nSomething went wrong while getting fault universe for circuit {circuit.Name}.\n{e}\n")
        
    def EqualizeFaults(gate: Gate, faults: list[Fault]):
        
        try:

            # Return if gate has only one input.
            gateInputWires: list[Input] = list(map(lambda e: e.Wire, gate.Inputs))
            if len(gateInputWires) < 2: return
            
            # Set the control value and get the names of the fault wires.
            controlValue: int = LogicHelpers.GetControlValue(gate.Type)
            faultWires: list[str] = list(map(lambda e: e.Wire, faults))
            
            # Return if both inputs of a gate are not faults.
            firstInputWire: str = gate.Inputs[0].Wire
            secondInputWire: str = ""
            secondInputWire = gate.Inputs[1].Wire
            bothInputsAreFaults: bool = firstInputWire in faultWires and secondInputWire in faultWires
            if not bothInputsAreFaults: return

            # Get the faults that match the gate input wires.
            gateInputFaults: list[Fault] = []
            for inputWire in gateInputWires:
                if inputWire in faultWires:
                    inputFaults: list[Fault] = list(filter(lambda e: e.Wire == inputWire, faults))
                    gateInputFaults.extend(inputFaults)
            if gateInputFaults == []: return
            
            # Equalize the faults.
            for inputFault in gateInputFaults:
                if bothInputsAreFaults and inputFault.Value == controlValue:
                    faultToRemove: Fault = next((
                        e for e in faults if
                            e.Wire == inputFault.Wire
                            and e.Value == controlValue
                        ), None)
                    print(f"Collapsed:\t{faultToRemove.Wire}/{faultToRemove.Value}")
                    faults.remove(faultToRemove)
                    return
            
        except Exception as e:
            raise Exception(f"Unable to equalize faults.\n{e}")
