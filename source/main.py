import FileReader as readFile
import Simulate as simulation
from models.Circuit import Circuit
from models.Fault import Fault
from helpers.FaultHelpers import FaultHelpers
from helpers.VectorHelpers import VectorHelpers

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
        
        if choice == 0:
            circuit = readFile.ReadFile()
        
        elif choice == 1:
            print("Under Construction")
        
        elif choice == 2:
            print("Under Construction")

        elif choice == 3:
            if circuit == None:
                raise Exception(
                    "Please select option 0 to load a circuit first.")
            
            primaryInputsCount: int = len(circuit.PrimaryInputs)

            inputStr = input(
                "Enter your input vector for " +
                str(primaryInputsCount) +
                " primary inputs (Example: 0, 1, 0, 1, 1): ")
            
            inputVector: list[int] = VectorHelpers.GetInputVector(
                inputStr, primaryInputsCount)
            
            faultsInput: str = input("Enter faults (Example: 1gat/0, 2gat/1): ")
            faults: list[Fault] = FaultHelpers.GetFaultsInput(faultsInput)
            
            simulation.Simulate(circuit, inputVector, faults)
        
        elif choice == 4:
            print("Under Construction")
        
        elif choice == 5:
            break
        
    except Exception as e:
        print(f"\nSomething went wrong.\n{e}")