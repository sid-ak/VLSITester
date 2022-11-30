from helpers.PrintHelpers import PrintHelpers
from helpers.CommonHelpers import CommonHelpers
from helpers.LogicHelpers import LogicHelpers
from models.Gate import Gate
from enums.GateTypeEnum import GateTypeEnum
from models.Input import Input
from models.Fault import Fault

class GateHelpers:

    def PrintGates(gates: list[Gate]):
        tabs: str = "\t\t\t"
        
        print(f"Outputs (Value){tabs}Type{tabs}Inputs (Value)")
        PrintHelpers.PrintThinDivider()
        for gate in gates:
            firstInput: Input = gate.Inputs[0]
            secondInput: Input = None
            if len(gate.Inputs) > 1:
                secondInput = gate.Inputs[1]

            printStr: str = f"{gate.Output.Wire}\t({gate.Output.Value}){tabs}"
            printStr += f"{gate.Type.name}{tabs}"
            printStr += f"{firstInput.Wire}\t({firstInput.Value})\t"
            if secondInput!= None: printStr += f"{secondInput.Wire}\t({secondInput.Value})"

            print(printStr)

    # Sets the inputs for a gate.
    def SetGateInputs(gate: Gate, inputs: list[Input], fault: Fault = None):
        
        try:
            gateInputs: list[Input] = gate.Inputs

            for gateInput in gateInputs:
                inputToSet: Input = next(
                    (e for e in inputs if e.Wire == gateInput.Wire), None)
                if inputToSet == None: continue
                
                gateInput.Value = inputToSet.Value 

                # Force fault if exists.
                if(fault == None): continue
                if fault.Wire != gateInput.Wire: continue
                gateInput.Value = fault.Value

            gate.Inputs = gateInputs

        except Exception as e:
            raise Exception(f"Failed to set gate inputs.\n{e}")
    
    # Sets the outputs for a gate based on its input.k
    def SetGateOutput(gate: Gate, fault: Fault = None):

        try:
            inputs: list[Input] = gate.Inputs
            
            # If one of the inputs of a gate have not been set.
            for gateInput in inputs:
                if CommonHelpers.IsNotZeroOrOne(gateInput.Value):
                    return

            # Set the gate output.
            firstInput: int = inputs[0].Value
            secondInput: int = None
            if len(inputs) > 1: secondInput = inputs[1].Value
            gate.Output.Value = LogicHelpers.GetLogicValue(gate.Type, firstInput, secondInput)
            
            # Force fault if exists.
            if(fault == None): return
            if fault.Wire != gate.Output.Wire: return
            gate.Output.Value = fault.Value

        except Exception as e:
            raise Exception(f"Failed to set gate output.\n{e}")
