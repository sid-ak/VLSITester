import os
from helpers.CircuitHelpers import CircuitHelpers
from models.Circuit import Circuit
from models.Gate import Gate
from models.Input import Input
from models.Output import Output
from enums.GateTypeEnum import GateTypeEnum

COMMENT_CHAR: str = '$'
MAX_CHAR_COUNT: int = 5
PRIMARY_IN_STR: str = "primary input"
PRIMARY_OUT_STR: str = "primary output"

def GetFileNames() -> list[str]:
    return [
        "Type file name",
        "netlist.txt",
        "t4_3.ckt",
        "t4_21.ckt",
        "t5_10.ckt",
        "t5_26a.ckt",
        "t6_24_v1.ckt.txt",
        "t6_24.ckt"
    ]

def ReadFile(circuitName: str = "") -> Circuit:
    
    try:

        # Get file name.
        fileNames: list[str] = GetFileNames()
        print("\nPlease select one of the following input files or type a file name:\n")
        for i, name in enumerate(fileNames): print(f"[{i}] {name}")

        fileNameSelection: str = int(input("\nSelection: "))
        fileName: str = ""
        if fileNameSelection == 0:
            fileName = input("File name: ")
        else: fileName = fileNames[fileNameSelection]
        if circuitName != "": fileName = circuitName
        
        # Build the circuit.
        circuit: Circuit = ReadCircuit(fileName)
        
        # Print the circuit.
        print(f"\nInput File: {fileName}")
        CircuitHelpers.PrintCircuit(circuit)

        return circuit

    except Exception as e:
        raise Exception(
            f"Something went wrong while reading inputs from file {fileName}.\n{e}")

def ReadCircuit(fileName: str) -> Circuit:
    
    try:

        # Initialize primary inputs/outputs and gates.
        primaryInputs: list[Input] = []
        primaryOutputs: list[Output] = []
        gates: list[Gate] = []

        # Open the file and get all lines.
        filePath: str = os.path.join("benchmarks", fileName)
        with open(filePath, 'r') as file:
            lines: list[str] = file.readlines()

        # For each line in the file.
        for line in lines:
            line = line.strip()
            if line == "": continue
            
            # Ignore comments in the file.
            firstChar: str = line[0][0]
            if firstChar == COMMENT_CHAR: continue
            
            # Get primary inputs.
            if line.lower().find(PRIMARY_IN_STR) != -1:
                primaryInputWire: str = line[:MAX_CHAR_COUNT].strip()
                if primaryInputWire == "": continue
                primaryInput: Input = Input(wire = primaryInputWire, isPrimary = True)
                primaryInputs.append(primaryInput)
                continue
            
            # Get primary outputs.
            elif line.lower().find(PRIMARY_OUT_STR) != -1:
                primaryOutputWire: str = line[:MAX_CHAR_COUNT].strip()
                if primaryOutputWire == "": continue
                primaryOutput: Output = Output(wire = primaryOutputWire, isPrimary = True)
                primaryOutputs.append(primaryOutput)
                continue

            # Get gates: Get output.
            outputWire: str = line[:MAX_CHAR_COUNT].strip()
            isPrimaryOut: bool = outputWire in list(map(lambda e: e.Wire, primaryOutputs))
            output: Output = Output(wire = outputWire, isPrimary = isPrimaryOut)
            line = line.replace(outputWire, "", 1).strip()

            # Get gates: Get gate types.
            typeName: str = line[:MAX_CHAR_COUNT].strip()
            type: GateTypeEnum = GateTypeEnum[typeName.upper()]
            line = line.replace(typeName, "", 1).strip()

            # Get gates: Get inputs.
            inputCharCount: int = 2 if fileName == "t5_26a.ckt" else MAX_CHAR_COUNT
            inputs: list[Input] = []
            
            firstInputWire: str = line[:inputCharCount].strip()
            isPrimaryIn: bool = firstInputWire in list(map(lambda e: e.Wire, primaryInputs))
            firstInput: Input = Input(wire = firstInputWire, isPrimary = isPrimaryIn)
            line = line.replace(firstInputWire, "", 1).strip()
            inputs.append(firstInput)
            
            secondInputWire: str = line[:inputCharCount].strip()
            if secondInputWire != "":
                isPrimaryIn: bool = secondInputWire in list(map(lambda e: e.Wire, primaryInputs))
                secondInput: Input = Input(wire = secondInputWire, isPrimary = isPrimaryIn)
                inputs.append(secondInput)

            # Get gates: Construct gate and append.
            gate: Gate = Gate(type = type, inputs = inputs, output = output)
            gates.append(gate)

        if primaryInputs == []: raise Exception("No primary inputs found.")
        if primaryOutputs == []: raise Exception("No primary outputs found.")
        if gates == []: raise Exception("No gates found.")

        # Construct circuit and set fanouts.
        circuit: Circuit = Circuit(fileName, primaryInputs, primaryOutputs, gates)
        CircuitHelpers.SetFanouts(circuit)

        return circuit
    
    except Exception as e:
        raise Exception(f"Unable to read circuit from file {filePath}\n{e}")
