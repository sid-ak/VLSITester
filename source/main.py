import FileReader as readFile
import Simulate as simulation
import DAlgo as DAlgorithm
from models.Circuit import Circuit
from models.Fault import Fault
from helpers.FaultHelpers import FaultHelpers
from helpers.VectorHelpers import VectorHelpers
from FaultCollapser import FaultCollapser

circuit: Circuit = None

while(True):
    print("\n[0] Read the input net-list")
    print("[1] Perform fault collapsing")
    print("[2] List fault classes")
    print("[3] Simulate")
    print("[4] Generate tests (D-Algorithm)")
    print("[5] Exit\n")

    try:
        choice: int = int(input("Selection: "))
        
        # [0] Read the input net-list
        if choice == 0:
            circuit = readFile.ReadFile()
        
        # [1] Perform fault collapsing
        elif choice == 1:
            if circuit == None:
                raise Exception(
                    "Please select option 0 to load a circuit first.")

            # Reset circuit.
            circuitName: str = circuit.Name
            circuit = readFile.ReadCircuit(circuitName)
            
            collapsedFaults: list[Fault] = FaultCollapser.Collapse(circuit)
        
        # [2] List fault classes
        elif choice == 2:
            if circuit == None:
                raise Exception(
                    "Please select option 0 to load a circuit first.")

            # Reset circuit.
            circuitName: str = circuit.Name
            circuit = readFile.ReadCircuit(circuitName)
            
            collapsedFaults: list[Fault] = FaultCollapser.Collapse(
                circuit, listCollapsedFaults = True)

        # [3] Simulate
        elif choice == 3:
            if circuit == None:
                raise Exception(
                    "Please select option 0 to load a circuit first.")
            
            # Reset circuit.
            circuitName: str = circuit.Name
            circuit = readFile.ReadCircuit(circuitName)
            
            # Get vector input.
            primaryInputsCount: int = len(circuit.PrimaryInputs)
            inputStr = input(
                "Enter your input vector for " +
                str(primaryInputsCount) +
                " primary inputs (Example: 0, 1, 0, 1, 1): ")
            inputs: list[int] = VectorHelpers.GetVectorInput(
                inputStr, primaryInputsCount)
            
            # Get faults input.
            faultsInput: str = input("Enter faults (Example: 1gat/0, 2gat/1): ")
            faults: list[Fault] = FaultHelpers.GetFaultsInput(faultsInput, circuit)
            
            # Simulate the circuit using the vector and faults.
            simulation.Simulate(circuit, inputs, faults)
        
        # [4] Generate tests (D-Algorithm)
        elif choice == 4:
            if circuit == None:
                raise Exception(
                    "Please select option 0 to load a circuit first.")
            
            # Get faults input.
            faultsInput: str = input("Enter faults (Example: 1gat/0, 2gat/1): ")
            faults: list[Fault] = FaultHelpers.GetFaultsInput(faultsInput, circuit)
            
            # Reset circuit.
            circuitName: str = circuit.Name
            circuit = readFile.ReadCircuit(circuitName)
            
            debugMode: bool = bool(int(input("Debug mode? (1/0): ")))
            
            DAlgorithm.DAlgorithm(circuit, faults, debugMode)
        
        # [5] Exit
        elif choice == 5:
            break
        
    except Exception as e:
        print(f"\nSomething went wrong.\n{e}")
