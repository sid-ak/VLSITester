from helpers.CommonHelpers import CommonHelpers

class VectorHelpers:

    def GetVectorInput(inputStr: str, primaryInputsCount: int) -> list[int]:

        try:
            inputVectorStr: list[str] = inputStr.split(",")
            
            if inputVectorStr == []: raise Exception()
            if len(inputVectorStr) != primaryInputsCount: raise Exception()

            inputVector: list[int] = list(map(lambda e: int(e.strip()), inputVectorStr))
            for inputInt in inputVector:
                if CommonHelpers.IsNotZeroOrOne(inputInt): raise Exception("Input vector must only contain 0 or 1.")

            return inputVector
        
        except Exception as e:
            raise Exception("Invalid vector input.\n" +
            "Input vector must be separated by commas " +
            f"and must be equal to length of primary inputs ({primaryInputsCount})\n"
            f"Example: 0, 1, 1, 0, 1\n{e}")
