import pytest
import numpy as np
from qleet.pqc_property.expressibility import Expressibility
from qiskit import QuantumCircuit

class TestExpressibility:
    """ Test experessibility calculation functionality """

    def ansatz1(params, cparams=None):
        """
        Generate an templated ansatz with given parameters
        Args:
        params (array[float]): Parameters to initialize the parameterized unitary.
        num_qubits (int): Number of qubits in the circuit.
        Returns:
        ansatz (QuantumCircuit): Generated ansatz circuit
        """
        layers, num_qubits, depth = params.shape
        ansatz = QuantumCircuit(num_qubits, num_qubits)
        for idx in layers:
            for ind in num_qubits:
                ansatz.h(0)
                ansatz.rz(params[idx][ind][0], 0)
        
        return ansatz


    def ansatz2(params, cparams=None):
        """
        Generate an templated ansatz with given parameters
        Args:
        params (array[float]): Parameters to initialize the parameterized unitary.
        num_qubits (int): Number of qubits in the circuit.
        Returns:
        ansatz (QuantumCircuit): Generated ansatz circuit
        """
        layers, num_qubits, depth = params.shape
        ansatz = QuantumCircuit(num_qubits, num_qubits)
        for idx in layers:
            for ind in num_qubits:
                ansatz.h(0)
                ansatz.rz(params[idx][ind][0], 0)
                ansatz.rz(params[idx][ind][1], 0)
        return ansatz

    @pytest.mark.parametrize("circuits", [[temp1, temp2]])
    @pytest.mark.parametrize("measure", ["jsd", "kld"])
    def test_expressibility_circuits(self, circuits, measure):
        """ Tests that the expressibility measures give correct output """
        
        exp_res = []
        for circuit in circuits:
            exp_circ = Expressibility(circuit, [(1, 4, 2)])
            exp_res.append(exp_circ.expressibility(measure))

        assert exp_res[0] < exp_res[1]
