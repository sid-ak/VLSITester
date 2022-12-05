from helpers.PrintHelpers import PrintHelpers
from helpers.CommonHelpers import CommonHelpers
from helpers.LogicHelpers import LogicHelpers
from models.Circuit import Circuit
from models.Gate import Gate
from models.Input import Input
from models.Output import Output
from models.Fault import Fault

class GateHelpers:

    def PrintGates(gates: list[Gate], faultyCircuit: Circuit = None):
        try:
            
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
                        
                        if secondInput != None and faultySecondInput != None:
                            if secondInput.Wire == faultySecondInput.Wire and secondInput.Value != faultySecondInput.Value:
                                secondInputDiff = f"->{faultySecondInput.Value}"
                        
                        if gate.Output.Wire == faultyGate.Output.Wire and gate.Output.Value != faultyGate.Output.Value:
                            outputDiff = f"->{faultyGate.Output.Value}"

                printStr: str = f"{gate.Output.Wire}\t({gate.Output.Value}{outputDiff}){tabs}"
                printStr += f"{gate.Type.name}{tabs}"
                printStr += f"{firstInput.Wire}\t({firstInput.Value}{firstInputDiff})\t"
                if secondInput != None: printStr += f"{secondInput.Wire}\t({secondInput.Value}{secondInputDiff})"

                print(printStr)
            
        except Exception as e:
            raise Exception("Unable to print gates.\n{e}")

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
                if fault == None: continue
                if fault.Wire != gateInput.Wire: continue
                gateInput.Value = fault.Value

            gate.Inputs = gateInputs

        except:
            raise Exception(f"Failed to set gate inputs for {gate.Output.Wire}.")
    
    # Sets all the inputs for gates that have the matching input wire.
    def SetGatesInputs(gates: list[Gate], gateInputToSet: Input):

        try:
            for gate in gates:
                for gateInput in gate.Inputs:
                    if gateInput.Wire == gateInputToSet.Wire:
                        gateInput.Value = gateInputToSet.Value

        except Exception as e:
            raise Exception(f"Unable to set inputs for multiple gates.\n{e}")
    
    # Sets the inputs for a gate while considering fanouts.
    def SetGateFanouts(gates: list[Gate]):

        try:
            fanoutInputWires: list[str] = []
            for gate in gates:
                firstInput: Input = gate.Inputs[0]
                secondInput: Input = None
                if len(gate.Inputs) > 1: secondInput = gate.Inputs[1]

                if firstInput.IsFanout:
                    if firstInput.Wire not in fanoutInputWires:
                        fanoutInputWires.append(firstInput.Wire) 
                        firstInput.Wire = f"{firstInput.Wire}_a"
                    else:
                        firstInput.Wire = f"{firstInput.Wire}_b"
                
                if secondInput != None and secondInput.IsFanout:
                    if secondInput.Wire not in fanoutInputWires:
                        fanoutInputWires.append(secondInput.Wire)
                        secondInput.Wire = f"{secondInput.Wire}_a"
                    else:
                        secondInput.Wire = f"{secondInput.Wire}_b"
                
        except Exception as e:
            raise Exception(f"Unable to set gate fanouts.\n{e}")

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
            raise Exception(f"Failed to set gate output for {gate.Output.Wire}.")

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

    # Gets the gate based on the output of that gate.
    def GetGateFromOutput(gates: list[Gate], output: Output) -> Gate:
        
        try:
            
            for gate in gates:
                if output.Wire == gate.Output.Wire:
                    return gate
            
            return None

        except Exception as e:
            raise Exception(f"Unable to get gate from output.\n{e}")
    
    # Gets the gate based on the inputs of that gate.
    def GetGatesFromInput(gates: list[Gate], gateInputToCheck: Input) -> list[Gate]:
        
        try:
            gatesToReturn: list[Gate] = []
            
            for gate in gates:
                for gateInput in gate.Inputs:
                    if gateInputToCheck.Wire == gateInput.Wire:
                        gatesToReturn.append(gate)
            
            return gatesToReturn

        except Exception as e:
            raise Exception(f"Unable to get gate from input.\n{e}")
