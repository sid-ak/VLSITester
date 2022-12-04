from enums.GateTypeEnum import GateTypeEnum
from models.Circuit import Circuit
from models.Fault import Fault
from models.Gate import Gate
from models.Input import Input
from helpers.GateHelpers import GateHelpers
from helpers.CircuitHelpers import CircuitHelpers
from helpers.LogicHelpers import LogicHelpers
from helpers.PrintHelpers import PrintHelpers
from models.Output import Output

faultyWires: list[str] = []
DAlgoSuccess: bool

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
            DAlgoRec(
                circuit,
                fault,
                DFrontier,
                JFrontier,
                isFirstIteration = True)
            print(DAlgoSuccess)
            if DAlgoSuccess:
                CircuitHelpers.SetAllPrimaryInputs(circuit)
                for primaryInput in circuit.PrimaryInputs:
                    print(f"{primaryInput.Wire} - {primaryInput.Value}")
            
            PrintHelpers.PrintThickDivider()

    except Exception as e:
        raise Exception(f"DAlgorithm error\n{e}")

# The D-Algorithm that calls itself recursively.
def DAlgoRec(
    circuit: Circuit,
    fault: Fault,
    DFrontier: list[Gate],
    JFrontier: list[Gate],
    isFirstIteration: bool,
    gateToRemove: Gate = None):
    
    try:
        global DAlgoSuccess
        global faultyWires
        
        faultyGates: list[Gate] = CircuitHelpers.GetFaultyGates(circuit, fault)
        faultyWires.append(fault.Wire)

        if len(faultyGates) != 0:
            
            # Remove the tried gate from the D-Frontier.
            if gateToRemove != None and gateToRemove in DFrontier:
                DFrontier.remove(gateToRemove)
                print(f"Log: Removed {gateToRemove.Output.Wire} from D-Frontier.")
            
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
                    if gateToRemove != None and gateToRemove.Output.Wire != gateInput.Wire:
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
                        gateToRemove = gate)
                
                
        if gate.Output.IsPrimary:
            
            if len(JFrontier) == 0:
                print("J-Frontier is empty.")
                DAlgoSuccess = True
                return

            #select gate from JFrontier
            #find control value of that gate (might be easier to reverse order)

            #for gate in JFrontier:
                #find an input of gate with value -1
                #set control value to gate.value
                #if DAlgoRec == Success: return success
                #set non control value to gate.value
            #return fail

            # If not empty, then get a gate from the J-Frontier.
            gateJFrontier: Gate = JFrontier[-1]
            print(f"\n\nLine justification started for {gateJFrontier.Output.Wire}.")
            PrintHelpers.PrintThinDivider()

            # Get control value for the gate in J-Frontier.
            controlValueJFrontier: int = LogicHelpers.GetControlValue(gateJFrontier.Type)

            # For each input of the gate.
            for gateInput in gateJFrontier.Inputs:
                if gateInput.Value != -1 and gateInput.IsPrimary and gateInput.Wire not in faultyWires:
                    gateInput.Value = int(not(controlValueJFrontier))
                    GateHelpers.SetGatesInputs(circuit.Gates, gateJFrontier.Output)
                    print(f"Log: Reversed primary input {gateInput.Wire} to {gateInput.Value}")

                # Set the control value to the inputs.
                elif gateInput.Value == -1 and gateInput.IsPrimary:
                    gateInput.Value = controlValueJFrontier
                    print(f"Log: Set control value of primary input {gateInput.Wire} to {controlValueJFrontier}")

                
                # If not primary, add gate to J-Frontier.
                elif not gateInput.IsPrimary:
                    gateJFrontierToAdd: Gate = GateHelpers.GetGateFromOutput(circuit.Gates, gateInput)
                    JFrontier.append(gateJFrontierToAdd)
                    print(f"Log: Added {gateJFrontierToAdd.Output.Wire} to J-Frontier.")

                    print("\nLog: J-Frontier:")
                    for JFrontierGate in JFrontier:
                        print(JFrontierGate.Output.Wire)
                        print()

            gateInputValues: list[int] = list(map(lambda e: e.Value, gateJFrontier.Inputs))
            
            # If justified, remove justified gate from J-Frontier.
            if -1 not in gateInputValues:
                circuitGate: Gate = GateHelpers.GetGateFromOutput(
                    circuit.Gates, gateJFrontier.Output)
                
                GateHelpers.SetGateOutput(circuitGate)

                if not IsConflict(circuit, circuitGate):
                    GateHelpers.SetGatesInputs(circuit.Gates, gateJFrontier.Output)
                else:
                    print(f"Conflict at {circuitGate.Output.Wire}")
                
                JFrontier.remove(gateJFrontier)
                print(f"Log: Removed {gateJFrontier.Output.Wire} from J-Frontier, already justified.")
                
                print("\nLog: J-Frontier:")
                for JFrontierGate in JFrontier:
                    print(JFrontierGate.Output.Wire)
                    print()

                # Remove from D-Frontier if exists.
                if gateJFrontier in DFrontier:
                    DFrontier.remove(gateJFrontier)
                    print(f"Log: Removed {gateJFrontier.Output.Wire} from D-Frontier.")
                    
                    print("\nLog: D-Frontier:")
                    for DFrontierGate in DFrontier:
                        print(DFrontierGate.Output.Wire)
                        print()
                
            # Call recursively.
            DAlgoRec(
                circuit = circuit,
                fault = fault,
                DFrontier = DFrontier,
                JFrontier = JFrontier,
                isFirstIteration = False)

    except Exception as e:
        raise Exception(f"DAlgo error\n{e}")

def IsConflict(circuit: Circuit, gate: Gate) -> bool:
    global DAlgoSuccess
    gateOutput: Output = gate.Output
    inputGates: list[Gate] = GateHelpers.GetGatesFromInput(circuit.Gates, gate.Output)
    
    for inputGate in inputGates:
        for inputGate in inputGates:
            if -1 in list(map(lambda e: e.Value, inputGate.Inputs)): continue
            for gateInput in inputGate.Inputs:
                if gateInput.Wire == gateOutput.Wire:
                    if gateInput.Value != gateOutput.Value: 
                        print(f"Conflict at {gateInput.Wire}")
                        DAlgoSuccess = True
                        return
                    else:
                        DAlgoSuccess = False
                        return
