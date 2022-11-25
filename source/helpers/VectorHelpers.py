class VectorHelpers:

    def GetInputVector(inputStr: str, primaryInputsCount: int) -> list[int]:

        try:
            inputVectorStr: list[str] = inputStr.split(",")
            
            if inputVectorStr == []: raise Exception()
            if len(inputVectorStr) != primaryInputsCount: raise Exception()

            inputVector: list[int] = list(map(lambda e: int(e.strip()), inputVectorStr))
            return inputVector
        
        except Exception as e:
            raise Exception("Invalid vector input.\n" +
            "Input vector must be separated by commas " +
            f"and must be equal to length of primary inputs ({primaryInputsCount})\n"
            "Example: 0, 1, 1, 0, 1")
