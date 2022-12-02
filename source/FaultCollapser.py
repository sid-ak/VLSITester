import copy
from helpers.PrintHelpers import PrintHelpers
from models.Circuit import Circuit
from models.Fault import Fault
from helpers.FaultHelpers import FaultHelpers
from helpers.GateHelpers import GateHelpers

class FaultCollapser:

    def Collapse(circuit: Circuit, listCollapsedFaults: bool = False) -> list[Fault]:
        
        try:

            # Get the fault universe, only checkpoint faults.
            faultUniverse: set[Fault] = FaultHelpers.GetFaultUniverse(circuit)
            print("\nFault Universe Before Collapsing:")
            FaultHelpers.PrintFaults(faultUniverse)
            
            # Set the fanout names for the gates.
            GateHelpers.SetGateFanouts(circuit.Gates)
            
            # Collapse the faults.
            print("\nCollapsing Input Faults")
            PrintHelpers.PrintThickDivider()
            collapsedFaults: set[Fault] = copy.deepcopy(faultUniverse)
            for gate in circuit.Gates:
                FaultHelpers.EqualizeFaults(gate, collapsedFaults)
            PrintHelpers.PrintThickDivider()

            # List the collapsed faults.
            if listCollapsedFaults:
                print("\nFault Classes After Collapsing:")
                FaultHelpers.PrintFaults(collapsedFaults)

        except Exception as e:
            raise Exception(
                f"\nSomething went wrong while fault collapsing for circuit {circuit.Name}.\n{e}\n")
