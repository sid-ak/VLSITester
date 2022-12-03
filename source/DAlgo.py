from models.Circuit import Circuit
from models.Fault import Fault
from models.Gate import Gate
from models.Input import Input
from helpers.GateHelpers import GateHelpers
from helpers.CircuitHelpers import CircuitHelpers
from helpers.LogicHelpers import LogicHelpers

# Calls the D-Algorithm and sets initial values.
def DAlgorithm(circuit: Circuit, faults: list[Fault] = []):
    try:
        DFrontier: set[Gate] = set()
        JFrontier: set[Gate] = set()
        
        if circuit == None: raise Exception("Circuit was None.")

        if faults == []: raise Exception(
            "No faults provided to generate test vectors.")
            
        for fault in faults:
            
            print(f"\nLog: Starting D-Algorithm for fault: {fault.Wire}/{fault.Value}")
            
            # Set fault for gate.
            for gate in circuit.Gates:
                for gateInput in gate.Inputs:
                    inputFault: Fault = next((
                        e for e in faults if e.Wire == gateInput.Wire), None)
                    if inputFault == None: continue
                    gateInput.Value = inputFault.Value
                outputFault: Fault = next((
                    e for e in faults if e.Wire == gate.Output.Wire), None)
                if outputFault  == None: continue
                gate.Output.Value = outputFault.Value
            
            # Perform D algo.
            testVector: list[list[int]] = DAlgoRec(circuit, fault, DFrontier, JFrontier)

        return testVector

    except Exception as e:
        raise Exception(f"DAlgorithm error\n{e}")

# The D-Algorithm that calls itself recursively.
def DAlgoRec(
    circuit: Circuit,
    fault: Fault,
    DFrontier: set[Gate],
    JFrontier: set[Gate],
    gateToRemove: Gate = None) -> list[list[int]]:
    
    try:
        faultyGates: list[Gate] = CircuitHelpers.GetFaultyGates(circuit, fault)

        if len(faultyGates) != 0:
            
            # Remove the tried gate from the D-Frontier.
            if gateToRemove != None and gateToRemove in DFrontier:
                print(f"Log: Removing {gateToRemove.Output.Wire} from D-Frontier.")
                DFrontier.remove(gateToRemove)
            
            # Update the D-Frontier.
            DFrontier.update(faultyGates)

        print("Log: Updated D-Frontier:")
        for DFrontierGate in DFrontier:
            print(f"\t{DFrontierGate.Output.Wire}")
        print()

        if not CircuitHelpers.OutputPropagated(circuit):
            
            # If D-Frontier is empty, return failure.
            if len(DFrontier) == 0:
                print("Failure: DFrontier is empty")
                return False

            # Get the first untried gate from the D-Frontier,
            gate: Gate = list(DFrontier)[0]
            controlValue = LogicHelpers.GetControlValue(gate.Type)
            for gateInput in gate.Inputs:
                
                # Get inputs of that gate w/ value -1 then set to non control value.
                if gateInput.Value == -1:
                    gateInput.Value = int(not controlValue)
                    print(f"Log: Set control value of {gateInput.Wire} to {gateInput.Value}")

                # If this input is not a PI add gate to J-Frontier.
                if not gateInput.IsPrimary:
                    if gateToRemove != None and gateToRemove.Output.Wire != gateInput.Wire:
                        gateJFrontier: Gate = GateHelpers.GetGateFromOutput(
                            circuit.Gates, gateInput)
                    
                        if gateJFrontier != None:
                            JFrontier.add(gateJFrontier)
                            print("Log: Updated J-Frontier:")
                            for JFrontierGate in JFrontier:
                                print(f"\t{JFrontierGate.Output.Wire}")
                    
            firstInput: Input = gate.Inputs[0]
            secondInput: Input = None
            if len(gate.Inputs) > 1: secondInput = gate.Inputs[1]
            
            # If value of both inputs are set.
            if firstInput != -1 and secondInput != -1:

                # Set gate output and input.
                GateHelpers.SetGateOutput(gate)
                GateHelpers.SetGatesInputs(circuit.Gates, gate.Output)
                
                # Check if output wire is not PO.
                if not gate.Output.IsPrimary:
                    
                    # Add wires where this output inputs to to d-frontier.
                    fault.Wire = gate.Output.Wire
                    fault.Value = gate.Output.Value
                    
                    # Call algorithm recursively.
                    DAlgoRec(
                        circuit = circuit,
                        fault = fault,
                        DFrontier = DFrontier,
                        JFrontier = JFrontier,
                        gateToRemove = gate)
                
                
        print(f"Success: Fault {fault.Wire}/{fault.Value} propagated to {gate.Output.Wire}")
        if len(JFrontier) == 0: return True

        #select gate from JFrontier
        #find control value of that gate (might be easier to reverse order)

        #for gate in JFrontier:
            #find an input of gate with value -1
            #set control value to gate.value
            #if DAlgoRec == Success: return success
            #set non control value to gate.value
        #return fail

    except Exception as e:
        raise Exception(f"DAlgo error\n{e}")
