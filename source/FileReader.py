
def ReadFile() -> dict:
    primaryInputs: dict = {}
    primaryOutputs: dict = {}
    gate: list = []
    gates: list = []
    tabLineCount: int = 0

    with open('netlist.txt', 'r') as file:
        fileLines: list[str] = file.readlines()
    
    for line in fileLines:
        
        if line[0] != '$':
            
            if line[0] == '\t':
                tabLineCount += 1
            
            if line[0] != '\t' and tabLineCount == 0:
                primaryInputs[line.split(' ')[0]] = False
            
            elif line[0] != '\t' and line[0] != '\n' and tabLineCount == 1:
                primaryOutputs[line.split(' ')[0]] = False
                
            #gets gate details
            elif line[0] == '\t' and tabLineCount > 2:
                temp = line.split('\t')[1].split('\n')[0]
                gateDetails = temp.split(' ')
                
                while "" in gateDetails:
                    gateDetails.remove("")
                
                #splits the details up
                output = gateDetails[0]
                gateType = gateDetails[1]
                input1 = gateDetails[2]
                
                #not gate only has 1 input
                if gateType == "NOT":
                    input2 = "NONE"
                else:
                    input2 = gateDetails[3]
                
                gate = [output, gateType, input1, input2]
                gates.append(gate)

    return {
        "PrimaryInputs" : primaryInputs,
        "PrimaryOutputs" : primaryOutputs,
        "Gates" : gates
    }
        