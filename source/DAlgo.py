from models.Circuit import Circuit
from models.Fault import Fault
from models.Gate import Gate
from models.Output import Output
from helpers.GateHelpers import GateHelpers
from helpers.CircuitHelpers import CircuitHelpers
from helpers.LogicHelpers import LogicHelpers

def DAlgorithm(circuit: Circuit, faults: list[Fault] = []):
    DFrontier: list[Gate] = []
    JFrontier: list[Gate] = []
    try:
        if circuit == None: raise Exception(
            "Circuit was None.")

        if faults == []: raise Exception(
            "No faults provided to generate test vectors.")

        for gate in circuit.Gates:
            for gateInput in gate.Inputs:
                
                inputFault: Fault = next((
                    e for e in faults if e.Wire == gateInput.Wire), None)
                
                if fault != None: gateInput.Value = inputFault.Value

            outputFault: Fault = next((
                    e for e in faults if e.Wire == gate.Output.Wire), None)

            if fault != None: gate.Output.Value = outputFault.Value
            

        for fault in faults:
            testVector = DAlgoRec(circuit, fault, DFrontier, JFrontier)

        return testVector

    except Exception as e:
        raise Exception(f"DAlgorithm error\n{e}")

def DAlgoRec(circuit: Circuit, fault: Fault, DFrontier: list[Gate], JFrontier: list[Gate]):
    try:
        PrimaryOutputProp = CircuitHelpers.GetPrimaryOutputs(circuit)
        faultyOutputs: list[Output] = CircuitHelpers.GetFaultyOutputs(circuit, fault)

        if(len(faultyOutputs) != 0):
            DFrontier.extend(faultyOutputs)

        if PrimaryOutputProp == False:
            print("Start D ALGO")

            if len(DFrontier) == 0:
                print("DFrontier is empty")
                return False

            for gate in DFrontier:
                controlValue = LogicHelpers.GetControlValue(gate.Type)
                


    except Exception as e:
        raise Exception(f"DAlgo error\n{e}")
