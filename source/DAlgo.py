import copy
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
            
            initialFault: Fault = copy.deepcopy(fault)
            
            # Perform D algo.
            DAlgoRec(
                circuit,
                fault,
                DFrontier,
                JFrontier,
                isFirstIteration = True)
            
            # If D Algorithm succeeded.
            if DAlgoSuccess:
                print(f"\n\nVector that detects: {initialFault.Wire}/{initialFault.Value} for {circuit.Name}")
                PrintHelpers.PrintThinDivider()
                CircuitHelpers.SetAllPrimaryInputs(circuit)
                
                for primaryInput in circuit.PrimaryInputs:
                    if primaryInput.Wire == initialFault.Wire:
                        primaryInput.Value = int(not(initialFault.Value))
                    print(f"{primaryInput.Wire} - {'x' if primaryInput.Value == -1 else primaryInput.Value}")

                PrintHelpers.PrintThinDivider()
            
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
    conflictEncountered: bool = False,
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
                print(f"\nLog: Removed {gateToRemove.Output.Wire} from D-Frontier.")
                print("D-Frontier:")
                for DFrontierGate in DFrontier: print(DFrontierGate.Output.Wire)
            
            # Update the D-Frontier.
            for faultyGate in faultyGates:
                if faultyGate not in DFrontier:
                    DFrontier.append(faultyGate)
                    print(f"\nLog: Added {faultyGate.Output.Wire} to D-Frontier.")
                    print("D-Frontier:")
                    for DFrontierGate in DFrontier: print(DFrontierGate.Output.Wire)

        gate: Gate = DFrontier[0] if isFirstIteration else DFrontier[-1]
        if not gate.Output.IsPrimary or gate.Output.Value == -1:
            
            # If D-Frontier is empty, return failure.
            if len(DFrontier) == 0:
                print("\nFailure: DFrontier is empty.")
                DAlgoSuccess = False
                return

            # Get the latest untried gate from the D-Frontier.
            print(f"\nLog: At {gate.Output.Wire}")
            controlValueDFrontier: int = LogicHelpers.GetControlValue(gate.Type)
            for gateInput in gate.Inputs:
                
                # Get inputs of that gate w/ value -1 then set to non control value.
                if gateInput.Value == -1:
                    gateInput.Value = int(not controlValueDFrontier)
                    print(f"Log: Set {gateInput.Wire} to non-control value: {gateInput.Value}")

                # If this input is not a PI and it is untried, add gate to J-Frontier.
                if not gateInput.IsPrimary:
                    if gateToRemove != None and gateToRemove.Output.Wire != gateInput.Wire:
                        gateJFrontier: Gate = GateHelpers.GetGateFromOutput(
                            circuit.Gates, gateInput)
                    
                        if gateJFrontier != None:
                            JFrontier.append(gateJFrontier)
                            print(f"\nLog: Added {gateJFrontier.Output.Wire} to J-Frontier.")
                            print("J-Frontier:")
                            for JFrontierGate in JFrontier: print(JFrontierGate.Output.Wire)
                    
            firstInput: Input = gate.Inputs[0]
            secondInput: Input = None
            if len(gate.Inputs) > 1: secondInput = gate.Inputs[1]
            
            # If value of both inputs are set.
            if firstInput != -1 and secondInput != -1:

                # Set gate output and input.
                GateHelpers.SetGateOutput(gate)
                GateHelpers.SetGatesInputs(circuit.Gates, gate.Output)
                print(f"Log: {gate.Output.Wire} -> {gate.Output.Value}")
                
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
                        gateToRemove = gate,
                        conflictEncountered = conflictEncountered)
                
        if gate.Output.IsPrimary:
            
            if len(JFrontier) == 0:
                print("\nLog: J-Frontier is empty.")
                DAlgoSuccess = True
                return

            # If not empty, then get a gate from the J-Frontier.
            gateJFrontier: Gate = JFrontier[-1]
            print(f"\nLog: Justifying {gateJFrontier.Output.Wire}.")

            # Get control value for the gate in J-Frontier.
            controlValueJFrontier: int = LogicHelpers.GetControlValue(gateJFrontier.Type)
            
            # If it is an invertor then get the control value of the previous J Frontier gate and invert that.
            if gateJFrontier.Type == GateTypeEnum.NOT and len(JFrontier) > 1:
                controlValueJFrontier = int(not(LogicHelpers.GetControlValue(JFrontier[-2].Type)))

            # For each input of the J-Frontier gate.
            for gateInput in gateJFrontier.Inputs:
                
                # If conflict then reverse decision.
                if conflictEncountered and gateInput.Value != -1 and gateInput.IsPrimary and gateInput.Wire not in faultyWires:
                    gateInput.Value = int(not(controlValueJFrontier))
                    GateHelpers.SetGatesInputs(circuit.Gates, gateJFrontier.Output)
                    print(f"Log: Inverted primary input {gateInput.Wire} to {gateInput.Value}")

                # Set the control value to the inputs.
                elif gateInput.Value == -1 and gateInput.IsPrimary:
                    gateInput.Value = controlValueJFrontier
                    print(f"Log: Set {gateInput.Wire} to control value: {controlValueJFrontier}")
                
                # If not primary, add gate to J-Frontier.
                elif not gateInput.IsPrimary and gateInput.Value != int(not(controlValueJFrontier)):
                    gateJFrontierToAdd: Gate = GateHelpers.GetGateFromOutput(circuit.Gates, gateInput)
                    JFrontier.append(gateJFrontierToAdd)
                    print(f"\nLog: Added {gateJFrontierToAdd.Output.Wire} to J-Frontier.")
                    print("J-Frontier:")
                    for JFrontierGate in JFrontier: print(JFrontierGate.Output.Wire)

            gateInputValues: list[int] = list(map(lambda e: e.Value, gateJFrontier.Inputs))
            
            # If justified, remove justified gate from J-Frontier.
            if -1 not in gateInputValues:
                circuitGate: Gate = GateHelpers.GetGateFromOutput(
                    circuit.Gates, gateJFrontier.Output)
                
                GateHelpers.SetGateOutput(circuitGate)
                print(f"Log: {circuitGate.Output.Wire} -> {circuitGate.Output.Value}")

                # Check for conflict and handle.
                print(f"\nLog: Checking conflict on {circuitGate.Output.Wire}")
                if not IsConflict(circuit, circuitGate):
                    
                    conflictEncountered = False
                    
                    GateHelpers.SetGatesInputs(circuit.Gates, gateJFrontier.Output)

                    JFrontier.remove(gateJFrontier)
                    print(f"\nLog: Removed justified {gateJFrontier.Output.Wire} from J-Frontier.")
                    print("J-Frontier:")
                    for JFrontierGate in JFrontier: print(JFrontierGate.Output.Wire)

                    # Remove from D-Frontier if exists.
                    if gateJFrontier in DFrontier:
                        DFrontier.remove(gateJFrontier)
                        print(f"\nLog: Removed {gateJFrontier.Output.Wire} from D-Frontier.")
                        print("D-Frontier:")
                        for DFrontierGate in DFrontier: print(DFrontierGate.Output.Wire)
                
                else:
                    conflictEncountered = True
                    DAlgoSuccess = False
                    print(f"Log: Conflict on {circuitGate.Output.Wire}")
                
            # Call recursively.
            DAlgoRec(
                circuit = circuit,
                fault = fault,
                DFrontier = DFrontier,
                JFrontier = JFrontier,
                isFirstIteration = False,
                conflictEncountered = conflictEncountered)

    except Exception as e:
        raise Exception(f"DAlgo error\n{e}")

# Checks if there is a conflict on the specified gate of the circuit.
def IsConflict(circuit: Circuit, gate: Gate) -> bool:
    gateOutput: Output = gate.Output
    inputGates: list[Gate] = GateHelpers.GetGatesFromInput(circuit.Gates, gate.Output)
    
    for inputGate in inputGates:
        for inputGate in inputGates:
            if -1 in list(map(lambda e: e.Value, inputGate.Inputs)): continue
            for gateInput in inputGate.Inputs:
                if gateInput.Wire == gateOutput.Wire:
                    if gateInput.Value != gateOutput.Value: 
                        return True
                    else:
                        return False
