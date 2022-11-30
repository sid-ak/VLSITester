import copy
from models.Circuit import Circuit
from models.Fault import Fault
from models.Gate import Gate
from models.Output import Output
from helpers.GateHelpers import GateHelpers
from helpers.CircuitHelpers import CircuitHelpers

def Simulate(circuit: Circuit, primaryInputs: list[int], faults: list[Fault] = []):
    try:
        if circuit == None: raise Exception(
            "Circuit was None.")

        if primaryInputs == []: raise Exception(
            "No inputs provided to simulate circuit.")

        faultyCircuit = copy.deepcopy(circuit)
        
        # 1. Set the primary inputs for the circuit.
        CircuitHelpers.SetPrimaryInputs(circuit, primaryInputs)
        
        # 2. Set the gate inputs and outputs.
        inputs = copy.deepcopy(circuit.PrimaryInputs)
        for gate in circuit.Gates:
            GateHelpers.SetGateInputs(gate, inputs)
            GateHelpers.SetGateOutput(gate)
            inputs.append(gate.Output)
        
        # 3. Set the primary outputs for the circuit.
        CircuitHelpers.SetPrimaryOutputs(circuit)

        if(faults == []): 
            CircuitHelpers.PrintCircuit(circuit)
            return
        
        # 1. Set the primary inptus for the faulty circuit
        for fault in faults:

            CircuitHelpers.SetPrimaryInputs(faultyCircuit, primaryInputs, fault)
            
            # 2. Set the gate inputs and outputs.
            inputs = copy.deepcopy(faultyCircuit.PrimaryInputs)
            for gate in faultyCircuit.Gates:
                GateHelpers.SetGateInputs(gate, inputs, fault)
                GateHelpers.SetGateOutput(gate, fault)
                inputs.append(gate.Output)

            # 3. Set the primary outputs for the circuit
            CircuitHelpers.SetPrimaryOutputs(faultyCircuit)

            CircuitHelpers.PrintCircuit(faultyCircuit)

            primaryOutputValues: list[int] = list(map(lambda e: e.Value, circuit.PrimaryOutputs))

            for faultyPrimaryOutput in faultyCircuit.PrimaryOutputs:
                if faultyPrimaryOutput.Value not in primaryOutputValues:
                    print(f"{fault.Wire}/{fault.Value} propogates to output {faultyPrimaryOutput.Wire}")
                else:
                    print(f"{fault.Wire}/{fault.Value} does not propogate")
    
    except Exception as e:
        raise Exception(f"Could not simulate circuit.\n{e}")
