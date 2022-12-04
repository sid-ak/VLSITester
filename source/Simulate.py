import copy
from models.Circuit import Circuit
from models.Fault import Fault
from helpers.CircuitHelpers import CircuitHelpers

# Runs a fault free and a faulty simulation for a circuit using provide primary inputs.
def Simulate(circuit: Circuit, primaryInputs: list[int], faults: list[Fault] = []):
    try:
        if circuit == None: raise Exception(
            "Circuit was None.")

        if primaryInputs == []: raise Exception(
            "No inputs provided to simulate circuit.")

        # Run the simulation for a fault free circuit first.
        print(f"\nLog: Simulating fault free circuit for {circuit.Name}\n")
        CircuitHelpers.SimulateCircuit(
            circuit = circuit,
            primaryInputs = primaryInputs)

        # Make a copy of the fault free circuit.
        faultFreeCircuit: Circuit = copy.deepcopy(circuit)

        # Print the fault free simulated circuit and return if no faults.
        if (faults == []):
            CircuitHelpers.PrintCircuit(circuit)
            return
        
        # Run the simulation for each provided fault.
        for fault in faults:

            faultStr: str = f"{fault.Wire}/{fault.Value}"
            
            # Simulate the circuit this time with the provided fault.
            print(f"\n\nLog: Simulating fault {faultStr} for {circuit.Name}\n")
            CircuitHelpers.SimulateCircuit(
                circuit = circuit,
                primaryInputs = primaryInputs,
                fault = fault)
            
            # Make a copy of the faulty circuit.
            faultyCircuit: Circuit = copy.deepcopy(circuit)

            # Print the faulty circuit.
            CircuitHelpers.PrintCircuit(faultFreeCircuit, faultyCircuit)

            # Determine the detected faults by comparing the fault free and fault outputs.
            for i, faultyOutput in enumerate(faultyCircuit.PrimaryOutputs):
                if faultyOutput.Value != faultFreeCircuit.PrimaryOutputs[i].Value:
                    fault.IsDetected = True
                    fault.DetectedOn.append(faultyOutput.Wire)
            
            # Print the detected faults if any.
            if fault.IsDetected:
                print(f"\nResult: Detected fault {faultStr} on wire(s)", *fault.DetectedOn, sep = ", ")
            else: print(f"\nResult: Could not detect fault {faultStr} on any primary output.\n")
            
            # Clear faults fault detection list so to prevent appending on next run.
            fault.DetectedOn.clear()
    
    except Exception as e:
        raise Exception(f"Could not simulate circuit.\n{e}")
