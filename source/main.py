import FileReader as readFile
import Simulate as simulation

circuit: dict = {}
gates: list = []

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
            
            inputVector = input(
                "Enter your input vector " +
                str(len(list(circuit.values())[0])) +
                " Primary Inputs: ")
            
            setOfFaults = input(
                "Input the set of faults (EX: gate1 Sa0): ")
            
            simulation.Simulate(circuit, inputVector, setOfFaults)
        
        elif choice == 4:
            print("Under Construction")
        
        elif choice == 5:
            break
        
        print(circuit)
    
    except Exception as e:
        print(f"Invalid input or something went wrong.\n{e}")