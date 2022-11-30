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
        
        faultFreeCircuit: Circuit = CircuitHelpers.SimulateCircuit(
            circuit = circuit,
            primaryInputs = primaryInputs)

        # Print the fault free simulated circuit and return if not faults.
        if (faults == []):
            CircuitHelpers.PrintCircuit(faultFreeCircuit)
            return
        
        for fault in faults:

            faultStr: str = f"{fault.Wire}/{fault.Value}"
            
            print(f"\n\nLog: Simulating fault {faultStr} for {circuit.Name}\n")
            
            # Run the simulation for each provided fault.
            faultyCircuit: Circuit = CircuitHelpers.SimulateCircuit(
                circuit = circuit,
                primaryInputs = primaryInputs,
                fault = fault)

            # Print the faulty circuit.
            CircuitHelpers.PrintCircuit(faultyCircuit)

            # Print the faults that propagated to the primary outputs.
            primaryOutputValues: list[int] = list(map(lambda e: e.Value, circuit.PrimaryOutputs))
            for faultyPrimaryOutput in faultyCircuit.PrimaryOutputs:
                if faultyPrimaryOutput.Value not in primaryOutputValues:
                    fault.IsDetected = True
                    fault.DetectedOn = faultyPrimaryOutput.Wire
            
            if fault.IsDetected: print(f"\nResult: Detected fault {faultStr} on {fault.DetectedOn}\n")
            else: print(f"Result: Could not detect fault {faultStr} on any primary output.")
    
    except Exception as e:
        raise Exception(f"Could not simulate circuit.\n{e}")
