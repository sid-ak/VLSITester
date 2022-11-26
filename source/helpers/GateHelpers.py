from helpers.PrintHelpers import PrintHelpers
from helpers.CommonHelpers import CommonHelpers
from models.Circuit import Circuit
from models.Gate import Gate
from enums.GateTypeEnum import GateTypeEnum
from models.Input import Input

class GateHelpers:

    def PrintGates(gates: list[Gate], printValues: bool = True):
        tabs: str = "\t\t\t"
        
        print(f"Outputs (Value){tabs}Type{tabs}Inputs (Value)")
        PrintHelpers.PrintThinDivider()
        for gate in gates:
            firstInput: Input = gate.Inputs[0]
            secondInput: Input = None
            if len(gate.Inputs) > 1:
                secondInput = gate.Inputs[1]

            printStr: str = f"{gate.Output.Wire} ({gate.Output.Value}){tabs}"
            printStr += f"{gate.Type.name}{tabs}"
            printStr += f"{firstInput.Wire} ({firstInput.Value})\t"
            if secondInput!= None: printStr += f"{secondInput.Wire} ({secondInput.Value})"

            print(printStr)

    # Gets gates based on the specified inputs.
    def GetGatesFromInputs(circuit: Circuit, specifiedInputs: list[Input]) -> list[Gate]:
        try:
            allGates: list[Gate] = circuit.Gates
            if specifiedInputs == []: return allGates

            specifiedInputWires: list[str] = list(map(
                lambda e: e.Wire, specifiedInputs))
            
            specifiedGates: set[Gate] = set()
            for gate in allGates:
                for gateInput in gate.Inputs:
                    if gateInput.Wire in specifiedInputWires:
                        specifiedGates.add(gate)

            return specifiedGates
        
        except Exception as e:
            raise Exception(f"Failed to get gates from specified inputs.\n{e}")
    
    # Sets the inputs for a gate.
    def SetGateInputs(gate: Gate, inputs: list[Input]):
        
        try:
            gateInputs: list[Input] = gate.Inputs

            for gateInput in gateInputs:
                inputToSet: Input = next(
                    (e for e in inputs if e.Wire == gateInput.Wire), None)
                if inputToSet == None: continue
                
                gateInput.Value = inputToSet.Value 
            
            gate.Inputs = gateInputs
            return gate

        except Exception as e:
            raise Exception(f"Failed to set gate inputs.\n{e}")
    
    # Sets the outputs for a gate based on its input.k
    def SetGateOutput(gate: Gate) -> Gate:

        try:
            inputs: list[Input] = gate.Inputs
            
            # If one of the inputs of a gate have not been set.
            for gateInput in inputs:
                if CommonHelpers.IsNotZeroOrOne(gateInput.Value):
                    return gate

            firstInput: int = inputs[0].Value
            secondInput: int = None
            if len(inputs) > 1: secondInput = inputs[1].Value

            if gate.Type == GateTypeEnum.AND:
                gate.Output.Value = GateHelpers.AND(firstInput, secondInput)
            
            elif gate.Type == GateTypeEnum.OR:
                gate.Output.Value = GateHelpers.OR(firstInput, secondInput)
            
            elif gate.Type == GateTypeEnum.NAND:
                gate.Output.Value = GateHelpers.NAND(firstInput, secondInput)
            
            elif gate.Type == GateTypeEnum.NOR:
                gate.Output.Value = GateHelpers.NOR(firstInput, secondInput)
            
            elif gate.Type == GateTypeEnum.XOR:
                gate.Output.Value = GateHelpers.XOR(firstInput, secondInput)
            
            elif gate.Type == GateTypeEnum.NOT:
                gate.Output.Value = GateHelpers.NOT(firstInput)
            
            return gate
        
        except Exception as e:
            raise Exception(f"Failed to set gate output.\n{e}")
    
    def AND(firstInput: int, secondInput: int) -> int:
        return int(firstInput == 1 and secondInput == 1)
    
    def OR(firstInput: int, secondInput: int) -> int:
        return int(firstInput == 1 or secondInput == 1)
    
    def NAND(firstInput: int, secondInput: int) -> int:
        return int(firstInput != 1 and secondInput != 1)
        
    def NOR(firstInput: int, secondInput: int) -> int:
        return int(firstInput == 0 and secondInput == 0)
    
    def XOR(firstInput: int, secondInput: int) -> int:
        return int(firstInput != secondInput)
    
    def NOT(firstInput: int) -> int:
        return int(not firstInput)
