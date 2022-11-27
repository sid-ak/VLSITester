import copy
from models.Circuit import Circuit
from models.Fault import Fault
from models.Gate import Gate
from helpers.GateHelpers import GateHelpers
from helpers.CircuitHelpers import CircuitHelpers

def Simulate(circuit: Circuit, primaryInputs: list[int], faults: list[Fault] = []):
    
    try:
        if circuit == None: raise Exception(
            "Circuit was None.")

        if primaryInputs == []: raise Exception(
            "No inputs provided to simulate circuit.")

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

        CircuitHelpers.PrintCircuit(circuit)
    
    except Exception as e:
        raise Exception(f"Could not simulate circuit.\n{e}")
