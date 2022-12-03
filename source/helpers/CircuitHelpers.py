import copy
from models.Circuit import Circuit
from helpers.GateHelpers import GateHelpers
from helpers.PrintHelpers import PrintHelpers
from models.Gate import Gate
from models.Input import Input
from models.Output import Output
from subclasses.SetReturns import SetReturns
from models.Fault import Fault

class CircuitHelpers:

    def PrintCircuit(circuit: Circuit, faultyCircuit: Circuit = None):

        try:
            PrintHelpers.PrintThickDivider()

            print("\nNote: Value of -1 signifies that the value for that wire has not been set.\n")
            
            # Print the primary inputs and its differences from the faulty inputs if exists.
            print("\nPrimary Inputs")
            PrintHelpers.PrintThinDivider()
            for primaryInput in circuit.PrimaryInputs:
                inputDiff: str = ""

                if faultyCircuit != None:
                    for faultyInput in faultyCircuit.PrimaryInputs:
                        if primaryInput.Wire == faultyInput.Wire and primaryInput.Value != faultyInput.Value:
                            inputDiff = f"->{faultyInput.Value}"
                
                print(f"{primaryInput.Wire}\t({primaryInput.Value}{inputDiff})")

            # Print the primary outputs and its differences from the faulty outputs if exists.
            print("\n\nPrimary Outputs")
            PrintHelpers.PrintThinDivider()
            for primaryOutput in circuit.PrimaryOutputs:
                outputDiff: str = ""

                if faultyCircuit != None:
                    for faultyOutput in faultyCircuit.PrimaryOutputs:
                        if primaryOutput.Wire == faultyOutput.Wire and primaryOutput.Value != faultyOutput.Value:
                            outputDiff = f"->{faultyOutput.Value}"
                
                print(f"{primaryOutput.Wire}\t({primaryOutput.Value}{outputDiff})")

            print("\n\nGates")
            PrintHelpers.PrintThinDivider()
            
            # Print the gates.
            GateHelpers.PrintGates(circuit.Gates, faultyCircuit)

            PrintHelpers.PrintThickDivider()

        except Exception as e:
            raise Exception(f"Unable to print circuit {circuit.Name}.\n{e}")
        
    # Sets the primary inputs for a circuit.
    def SetPrimaryInputs(circuit: Circuit, inputs: list[int], fault: Fault = None):
        
        try:
            if len(circuit.PrimaryInputs) != len(inputs):
                raise Exception(
                    "Number of primary inputs do not equal provided inputs for circuit.")

            for i, primaryInput in enumerate(circuit.PrimaryInputs):
                primaryInput.Value = inputs[i]

                if(fault == None): continue
                
                #Set Primary inputs to the fault value
                if fault.Wire != primaryInput.Wire: continue

                primaryInput.Value = fault.Value

        except Exception as e:
            raise Exception(f"Could not set primary inputs.\n{e}")
    
    # Sets the primary outputs for a circuit.
    def SetPrimaryOutputs(circuit: Circuit):

        try:
            primaryGates: list[Gate] = list(filter(
                lambda e: e.Output.IsPrimary == True, circuit.Gates))
            
            for i in range(len(circuit.PrimaryOutputs)):
                circuit.PrimaryOutputs[i] = primaryGates[i].Output
            
        except Exception as e:
            raise Exception(f"Could not set primary outputs.\n{e}")

    # Sets all the fanout wires for a circuit.
    def SetFanouts(circuit: Circuit):
        
        try:
            allInputsList: list[Input] = []
            allInputWiresSet: SetReturns[str] = SetReturns()
            fanoutWires: list[str] = []

            # Set all gate input fanouts.
            for gate in circuit.Gates:
                for gateInput in gate.Inputs:
                    
                    allInputsList.append(gateInput)
                    
                    if not allInputWiresSet.add(gateInput.Wire):
                        gateInput.IsFanout = True
                        fanoutWires.append(gateInput.Wire)
                        
                        fanoutInput: Input = next((
                            e for e in allInputsList if e.Wire == gateInput.Wire), None)
                        if fanoutInput != None: fanoutInput.IsFanout = True

            # Set all primary input fanouts.
            for fanoutWire in fanoutWires:
                primaryInputFanout: Input = next((
                    e for e in circuit.PrimaryInputs if e.Wire == fanoutWire), None)
                if primaryInputFanout != None:
                    primaryInputFanout.IsFanout = True
            
            # Set all gate output fanouts.
            allOutputsList: list[Output] = list(map(lambda e: e.Output, circuit.Gates))
            for output in allOutputsList:
                if output.Wire in fanoutWires:
                    output.IsFanout = True
            
            # Primary outputs can never fanout (as far as I know).
            
        except Exception as e:
            raise Exception(
                f"\nSomething went wrong while setting fanouts for circuit {circuit.Name}.\n{e}\n")

    # Simulates a circuit using primary inputs and returns the simulated circuit.
    def SimulateCircuit(
        circuit: Circuit,
        primaryInputs: list[int],
        fault: Fault = None):

        try:
            # 1. Set the primary inputs for the circuit.
            CircuitHelpers.SetPrimaryInputs(circuit, primaryInputs, fault)
            
            # 2. Set the gate inputs and outputs.
            inputs: list[Input] = copy.deepcopy(circuit.PrimaryInputs)
            GateHelpers.SetGateInputsOutputs(circuit.Gates, inputs, fault)
            
            # 3. Set the primary outputs for the circuit.
            CircuitHelpers.SetPrimaryOutputs(circuit)

        except Exception as e:
            raise Exception(f"Circuit simulation failed.\n{e}")

    def OutputPropagated(circuit: Circuit) -> bool:

        try:
            for primaryOutputs in circuit.PrimaryOutputs:
                if primaryOutputs.Value != -1:
                    return True

            return False

        except Exception as e:
            raise Exception(f"Cannot find primary outputs\n{e}")


    def GetFaultyGates(circuit: Circuit, fault: Fault) -> list[Gate]:
        try:
            gates: list[Gate] = []
            for gate in circuit.Gates:
                for gateInputs in gate.Inputs:
                    if gateInputs.Wire == fault.Wire:
                        gates.append(gate)

            return gates
        except Exception as e:
            raise Exception(f"Cannot get faulty gates\n{e}")

