
def Simulate(circuit, inputVector, setOfFaults):
    simulatedGates = {}
    primaryIn = list(circuit.values())[0]
    for key in primaryIn:
        index = list(primaryIn).index(key)
        if inputVector[index] == "1":
            primaryIn[key] = True
        else:
            primaryIn[key] = False
    #print(primary)
    primaryOut = list(circuit.values())[1]

    gates = list(circuit.values())[2]
    for i in range (len(gates)):
        output = gates[i][0]
        gateType = gates[i][1]
        input1 = gates[i][2]
        input2 = gates[i][3]

        if input1 in primaryIn:
            input1 = primaryIn[input1]
        else:
            temp = []
            temp.append(simulatedGates[input1])
            input1 = temp
            
        if input2 in primaryIn:
            input2 = primaryIn[input2]
        else:
            temp = []
            temp.append(simulatedGates[input2])
            temp2 = temp

        if gateType == "and":
            simGate = input1 & input2 
        elif gateType == "or":
            simGate = input1 | input2
        elif gateType == "nand":
            simGate = not(input1 and input2)
        elif gateType == "nor":
            simGate = not(input1 or input2)
        elif gateType == "xor":
            simGate = input1 ^ input2
        elif gateType == "not":
            simGate = not(input1)
        simulatedGates[output] = simGate
    if(setOfFaults != ""):
        print("There is a fault")
    print(simulatedGates)
