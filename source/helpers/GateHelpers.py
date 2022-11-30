from helpers.PrintHelpers import PrintHelpers
from helpers.CommonHelpers import CommonHelpers
from helpers.LogicHelpers import LogicHelpers
from models.Circuit import Circuit
from models.Gate import Gate
from models.Input import Input
from models.Fault import Fault

class GateHelpers:

    def PrintGates(gates: list[Gate], faultyCircuit: Circuit = None):
        tabs: str = "\t\t\t"
        
        # Print the gate information with any difference from the faulty gate input/output.
        print(f"Outputs (Value){tabs}Type{tabs}Inputs (Value)")
        PrintHelpers.PrintThinDivider()
        for gate in gates:
            firstInput: Input = gate.Inputs[0]
            secondInput: Input = None
            if len(gate.Inputs) > 1:
                secondInput = gate.Inputs[1]

            firstInputDiff: str = ""
            secondInputDiff: str = ""
            outputDiff: str = ""

            if faultyCircuit != None:
                for faultyGate in faultyCircuit.Gates:
                    faultyFirstInput: Input = faultyGate.Inputs[0]
                    faultySecondInput: Input = None
                    if len(faultyGate.Inputs) > 1:
                        faultySecondInput = faultyGate.Inputs[1]

                    if firstInput.Wire == faultyFirstInput.Wire and firstInput.Value != faultyFirstInput.Value:
                        firstInputDiff = f"->{faultyFirstInput.Value}"
                    
                    if secondInput.Wire == faultySecondInput.Wire and secondInput.Value != faultySecondInput.Value:
                        secondInputDiff = f"->{faultySecondInput.Value}"
                    
                    if gate.Output.Wire == faultyGate.Output.Wire and gate.Output.Value != faultyGate.Output.Value:
                        outputDiff = f"->{faultyGate.Output.Value}"

            printStr: str = f"{gate.Output.Wire}\t({gate.Output.Value}{outputDiff}){tabs}"
            printStr += f"{gate.Type.name}{tabs}"
            printStr += f"{firstInput.Wire}\t({firstInput.Value}{firstInputDiff})\t"
            if secondInput!= None: printStr += f"{secondInput.Wire}\t({secondInput.Value}{secondInputDiff})"

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

    # Sets all the inputs and outputs for all gates in a circuit.
    def SetGateInputsOutputs(gates: list[Gate], inputs: list[Input], fault = None):
        for gate in gates:
            GateHelpers.SetGateInputs(gate, inputs, fault)
            GateHelpers.SetGateOutput(gate, fault)
            inputs.append(gate.Output)
        
        if not GateHelpers.AllGateInputsOutputsSet(gates):
            GateHelpers.SetGateInputsOutputs(gates, inputs, fault)
    
    # Checks if all the gate inputs and outputs have been set for a circuit.
    def AllGateInputsOutputsSet(gates: list[Gate]) -> bool:

        for gate in gates:
            for gateInput in gate.Inputs:
                if gateInput.Value == -1:
                    return False
            
            if gate.Output.Value == -1:
                raise False

        return True
