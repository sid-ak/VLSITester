from models.Circuit import Circuit
from models.Fault import Fault
from models.Gate import Gate
from models.Input import Input
from helpers.GateHelpers import GateHelpers
from helpers.CircuitHelpers import CircuitHelpers
from helpers.LogicHelpers import LogicHelpers
from helpers.PrintHelpers import PrintHelpers

# Calls the D-Algorithm and sets initial values.
def DAlgorithm(circuit: Circuit, faults: list[Fault] = []):
    try:
        DFrontier: list[Gate] = list()
        JFrontier: list[Gate] = list()
        
        if circuit == None: raise Exception("Circuit was None.")

        if faults == []: raise Exception(
            "No faults provided to generate test vectors.")
        
        for fault in faults:
            
            # Clear the frontiers.
            DFrontier.clear()
            JFrontier.clear()

            print(f"\n\nLog: Starting D-Algorithm for fault: {fault.Wire}/{fault.Value}")
            PrintHelpers.PrintThickDivider()
            
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
            DAlgoSuccess: bool = DAlgoRec(
                circuit,
                fault,
                DFrontier,
                JFrontier,
                isFirstIteration = True)
            
            testVector: list[int] = []
            if DAlgoSuccess:
                CircuitHelpers.SetAllPrimaryInputs(circuit)
                for primaryInput in circuit.PrimaryInputs:
                    print(primaryInput)
            
            PrintHelpers.PrintThickDivider()

        return testVector

    except Exception as e:
        raise Exception(f"DAlgorithm error\n{e}")

# The D-Algorithm that calls itself recursively.
def DAlgoRec(
    circuit: Circuit,
    fault: Fault,
    DFrontier: list[Gate],
    JFrontier: list[Gate],
    isFirstIteration: bool,
    DFrontierGateToRemove: Gate = None) -> bool:
    
    try:
        faultyGates: list[Gate] = CircuitHelpers.GetFaultyGates(circuit, fault)

        if len(faultyGates) != 0:
            
            # Remove the tried gate from the D-Frontier.
            if DFrontierGateToRemove != None and DFrontierGateToRemove in DFrontier:
                DFrontier.remove(DFrontierGateToRemove)
                print(f"Log: Removed {DFrontierGateToRemove.Output.Wire} from D-Frontier.")
            
            # Update the D-Frontier.
            for faultyGate in faultyGates:
                if faultyGate not in DFrontier:
                    DFrontier.append(faultyGate)
                    print(f"Log: Added {faultyGate.Output.Wire} to D-Frontier.")


        print("\nLog: D-Frontier:")
        for DFrontierGate in DFrontier: print(DFrontierGate.Output.Wire)
        print()

        gate: Gate = DFrontier[0] if isFirstIteration else DFrontier[-1]
        
        if not gate.Output.IsPrimary or gate.Output.Value == -1:
            
            # If D-Frontier is empty, return failure.
            if len(DFrontier) == 0:
                print("Failure: DFrontier is empty.")
                return False

            # Get the latest untried gate from the D-Frontier.
            print(f"Log: At {gate.Output.Wire}")
            controlValueDFrontier: int = LogicHelpers.GetControlValue(gate.Type)
            for gateInput in gate.Inputs:
                
                # Get inputs of that gate w/ value -1 then set to non control value.
                if gateInput.Value == -1:
                    gateInput.Value = int(not controlValueDFrontier)
                    print(f"Log: Set non-control value of {gateInput.Value} to {gateInput.Wire}")

                # If this input is not a PI and it is untried, add gate to J-Frontier.
                if not gateInput.IsPrimary:
                    if DFrontierGateToRemove != None and DFrontierGateToRemove.Output.Wire != gateInput.Wire:
                        gateJFrontier: Gate = GateHelpers.GetGateFromOutput(
                            circuit.Gates, gateInput)
                    
                        if gateJFrontier != None:
                            JFrontier.append(gateJFrontier)
                            print(f"Log: Added {gateJFrontier.Output.Wire} to J-Frontier.")
                            print("\nLog: J-Frontier:")
                            for JFrontierGate in JFrontier:
                                print(JFrontierGate.Output.Wire)
                            print()
                    
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
                            isFirstIteration = False,
                            DFrontierGateToRemove = gate)

        # If at the primary output.
        if gate.Output.IsPrimary:

            # If J-Frontier is empty, return success.
            if len(JFrontier) == 0:
                print("Success: J-Frontier is empty.")
                return True
            
            # If not empty, then get a gate from the J-Frontier.
            gateJFrontier: Gate = JFrontier[-1]
            print(f"\n\nLine justification started for {gateJFrontier.Output.Wire}.")
            PrintHelpers.PrintThinDivider()

            # Get control value for the gate in J-Frontier.
            controlValueJFrontier: int = LogicHelpers.GetControlValue(gateJFrontier.Type)

            # Justify the gate inputs.
            for gateInput in gateJFrontier.Inputs:
                
                # Set the control value to the inputs.
                if gateInput.Value == -1 and gateInput.IsPrimary:
                    
                    gateInput.Value = controlValueJFrontier
                    print(f"Log: Set control value of primary input {gateInput.Wire} to {controlValueJFrontier}")

                elif not gateInput.IsPrimary:
                    gateJFrontierToAdd: Gate = GateHelpers.GetGateFromOutput(circuit.Gates, gateInput)
                    JFrontier.append(gateJFrontierToAdd)
                    print(f"Log: Added {gateJFrontierToAdd.Output.Wire} to J-Frontier.")
                
            # Check for conflict.
            previousGate: Gate = GateHelpers.GetGateFromOutput(circuit.Gates, gateInput)
            if previousGate != None:
                if previousGate.Output.Value != gateInput.Value:
                    print(f"Log: Conflict at {gateInput.Wire}")
                    return False
        
            # Remove justified gate from J-Frontier.
            gateInputValues: list[int] = list(map(lambda e: e.Value, gateJFrontier.Inputs))
            
            if -1 not in gateInputValues:
                
                circuitGate: Gate = GateHelpers.GetGateFromOutput(
                    circuit.Gates, gateJFrontier.Output)
                GateHelpers.SetGateOutput(circuitGate)
                
                JFrontier.remove(gateJFrontier)
                print(f"Log: Removed {gateJFrontier.Output.Wire} from J-Frontier.")
            
            if -1 not in gateInputValues and gateJFrontier in DFrontier:
                DFrontier.remove(gateJFrontier)
                print(f"Log: Removed {gateJFrontier.Output.Wire} from D-Frontier.")
                print("\nLog: D-Frontier:")
                for DFrontierGate in DFrontier:
                    print(DFrontierGate.Output.Wire)
                    print()

            print("\nLog: J-Frontier:")
            for JFrontierGate in JFrontier:
                print(JFrontierGate.Output.Wire)
            print()

            DAlgoRec(
                circuit = circuit,
                fault = fault,
                DFrontier = DFrontier,
                JFrontier = JFrontier,
                isFirstIteration = False)
            
        #for gate in JFrontier:
            #find an input of gate with value -1
            #set control value to gate.value
            #if DAlgoRec == Success: return success
            #set non control value to gate.value
        #return fail

    except Exception as e:
        raise Exception(f"DAlgo error\n{e}")
