from enums.GateTypeEnum import GateTypeEnum

class LogicHelpers:

    # Sets the logical output for the specified gate.
    def GetLogicValue(
        gateType: GateTypeEnum,
        firstInput: int,
        secondInput: int = None):

        if gateType == GateTypeEnum.AND:
            return LogicHelpers.AND(firstInput, secondInput)
        
        elif gateType == GateTypeEnum.OR:
            return LogicHelpers.OR(firstInput, secondInput)
        
        elif gateType == GateTypeEnum.NAND:
            return LogicHelpers.NAND(firstInput, secondInput)
        
        elif gateType == GateTypeEnum.NOR:
            return LogicHelpers.NOR(firstInput, secondInput)
        
        elif gateType == GateTypeEnum.XOR:
            return LogicHelpers.XOR(firstInput, secondInput)
        
        elif gateType == GateTypeEnum.NOT:
            return LogicHelpers.NOT(firstInput)
    
    def AND(firstInput: int, secondInput: int) -> int:
        return int(firstInput == 1 and secondInput == 1)
    
    def OR(firstInput: int, secondInput: int) -> int:
        return int(firstInput == 1 or secondInput == 1)
    
    def NAND(firstInput: int, secondInput: int) -> int:
        return int(firstInput != 1 or secondInput != 1)
        
    def NOR(firstInput: int, secondInput: int) -> int:
        return int(firstInput == 0 and secondInput == 0)
    
    def XOR(firstInput: int, secondInput: int) -> int:
        return int(firstInput != secondInput)
    
    def NOT(firstInput: int) -> int:
        return int(not firstInput)

    def GetControlValue(gate: Gate) -> int:
        if(gate.Type == GateTypeEnum.AND):
            return 0
        elif(gate.Type == GateTypeEnum.OR):
            return 1
        elif(gate.Type == GateTypeEnum.NAND):
            return 0
        elif(gate.Type == GateTypeEnum.NOR):
            return 1
        elif(gate.Type == GateTypeEnum.XOR):
            return None
        elif(gate.Type == GateTypeEnum.NOT):
            return None