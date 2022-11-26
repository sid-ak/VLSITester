from models.Fault import Fault

class FaultHelpers: 

    def GetFaultsInput(faultsInput: str) -> list[Fault]:
        
        if faultsInput == "": return []

        try:
            faultsStr: list[str] = faultsInput.split(",")
            faults: list[Fault] = []
            for faultStr in faultsStr:
                wire: str = faultStr.split("/")[0].strip()
                value: int = int(faultStr.split("/")[1])
                fault: Fault = Fault(wire, value)
                faults.append(fault)
            
            return faults
            
        except Exception as e:
            raise Exception(f"Invalid faults input.\n" +
                "Faults must be separated by commas and must be in the format:" +
                "<input/output name>/<fault value>\n" +
                f"Example: 1gat/0, 2gat/1\n{e}\n")
