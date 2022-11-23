
def ReadFile():
    primaryInputs = {}
    primaryOutputs = {}
    layout = {}
    tabLineCount = 0

    file = open('netlist.txt', 'r')
    read = file.readlines()
    for line in read:
        if line[0] != '$':
            if line[0] == '\t':
                tabLineCount += 1
            if line[0] != '\t' and tabLineCount == 0:
                primaryInputs[line.split(' ')[0]] = [False]
            elif line[0] != '\t' and line[0] != '\n' and tabLineCount == 1:
                primaryOutputs[line.split(' ')[0]] = [False]
            elif line[0] == '\t' and tabLineCount > 2:
                # layout[line.split('\t')[1].split('\n')[0]] = [False]
                temp = line.split('\t')[1].split('\n')[0]
                gateDetails = temp.split(' ')
                while "" in gateDetails:
                    gateDetails.remove("")
                output = gateDetails[0]
                gateType = gateDetails[1]
                input1 = gateDetails[2]
                input2 = gateDetails[3]
                if input1 in primaryInputs:
                    print("found")
                    input1 = primaryInputs[input1]
                    print(input1)
                if input2 in primaryInputs:
                    input2 = primaryInputs[input2]



    file.close()
    print(primaryInputs)
    print(primaryOutputs)
    print(layout)
    return {
        "PrimaryInputs" : primaryInputs,
        "PrimaryOutputs" : primaryOutputs,
        "Layout" : layout
    }
        