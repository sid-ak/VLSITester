from models.Circuit import Circuit
from models.Fault import Fault
from models.Gate import Gate
from models.Output import Output
from helpers.GateHelpers import GateHelpers
from helpers.CircuitHelpers import CircuitHelpers
from helpers.LogicHelpers import LogicHelpers

def DAlgorithm(circuit: Circuit, faults: list[Fault] = []):
    try:
        DFrontier: set[Gate] = set()
        JFrontier: set[Gate] = set()
        
        if circuit == None: raise Exception("Circuit was None.")

        if faults == []: raise Exception(
            "No faults provided to generate test vectors.")
            
        for fault in faults:
            
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

def DAlgoRec(
    circuit: Circuit,
    fault: Fault,
    DFrontier: set[Gate],
    JFrontier: set[Gate]) -> list[list[int]]:
    
    try:
        faultyGates: list[Gate] = CircuitHelpers.GetFaultyGates(circuit, fault)

        if(len(faultyGates) != 0):
            DFrontier.update(faultyGates)

        for gate in DFrontier:
            print(f"Added {gate.Output.Wire} to DFrontier")

        if not CircuitHelpers.OutputPropagated(circuit):
            print("Start D ALGO")

            if len(DFrontier) == 0:
                print("DFrontier is empty")
                return False

            for gate in DFrontier:
                controlValue = LogicHelpers.GetControlValue(gate.Type)
                for gateInput in gate.Inputs:
                    
                    # Get inputs of that gate w/ value -1 then set to non control value
                    if gateInput.Value == -1:
                        gateInput.Value = int(not controlValue)
                        print(f"Set control value of {gateInput.Wire} to {gateInput.Value}")

                    # If this input is not a PI add gate to J-Frontier
                    if not gateInput.IsPrimary: 
                        gateJFrontier: Gate = GateHelpers.GetGatesFromOutput(
                            circuit.Gates, gateInput)
                        
                        if gateJFrontier != None:
                            JFrontier.add(gateJFrontier)
                        
                # If value of both inputs == value set to output
                firstInput: Input = gateInput[0]
                secondInput: Input = None
                if len(gate.Inputs) > 1: secondInput = gateInput[1]
                if firstInput != -1 and secondInput != -1:

                    # Set gate output.                    
                    GateHelpers.SetGateOutput(gate)
                    
                    # Check if output wire is PO.
                    if gate.Output.IsPrimary:

                        #if not add wires where this output inputs to to d-frontier

                #if DAlgoRec = Success return success
                #if all gates from dfrontier has been tried 
                    #return fail
        else:
            if(len(JFrontier) == 0): return True

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
