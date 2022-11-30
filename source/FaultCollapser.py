from models.Circuit import Circuit
from models.Fault import Fault
from helpers.FaultHelpers import FaultHelpers

class FaultCollapser:

    def Collapse(circuit: Circuit):
        
        try:
            faultUniverse: set[Fault] = FaultHelpers.GetFaultUniverse(circuit)
            FaultHelpers.PrintFaults(faultUniverse)

        except Exception as e:
            raise Exception(
                f"\nSomething went wrong while fault collapsing for circuit {circuit.Name}.\n{e}\n")
