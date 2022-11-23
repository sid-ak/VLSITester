import FileReader as readFile
circuit = {}
while(True):
    print("[0] Read the input net-list")
    print("[1] Preform fault collapsing")
    print("[2] List fault classes")
    print("[3] Simulate")
    print("[4] Generate tests (D-Algorithm)")
    print("[5] Exit")

    choice = input()
    if choice == "0":
        circuit = readFile.ReadFile()
    elif choice == "1":
        print(choice)
    elif choice == "2":
        print(choice)
    elif choice == "3":
        print(choice)
    elif choice == "4":
        print(choice)
    elif choice =="5":
        print(choice)
        break
    print(circuit)