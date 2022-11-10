primaryInputs = []
primaryOutputs = []
layout = []
tabLineCount = 0


file = open('test.txt', 'r')
read = file.readlines()
for line in read:
    if line[0] != '$':
        if line[0] == '\t':
            tabLineCount += 1
        if line[0] != '\t' and tabLineCount == 0:
            primaryInputs.append(line.split(' ')[0])
        elif line[0] != '\t' and line[0] != '\n' and tabLineCount == 1:
            primaryOutputs.append(line.split(' ')[0])
        elif line[0] == '\t' and tabLineCount > 2:
            layout.append(line.split('\t')[1].split('\n')[0])
file.close()
print(primaryInputs)
print(primaryOutputs)
print(layout)
        