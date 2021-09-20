import pytest

import numpy as np
from qiskit import QuantumCircuit

from qleet.analyzers.expressibility import Expressibility


def generate_ansatz_1(params: np.ndarray, _c_params=None):
    """
    Generate an templated ansatz with given parameters
    :param params: Parameters to initialize the parameterized unitary.
    :param _c_params: Ignored argument for controller parameters.
    :returns ansatz (QuantumCircuit): Generated ansatz circuit
    """
    layers, num_qubits, depth = params.shape
    ansatz = QuantumCircuit(num_qubits, num_qubits)
    for idx in layers:
        for ind in num_qubits:
            ansatz.h(0)
            ansatz.rz(params[idx][ind][0], 0)

    return ansatz


def generate_ansatz_2(params: np.ndarray, _c_params=None):
    """
    Generate an templated ansatz with given parameters
    Args:
    :param params: Parameters to initialize the parameterized unitary.
    :param _c_params: Ignored argument for controller parameters.
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


@pytest.mark.xfail
@pytest.mark.parametrize("circuits", [[generate_ansatz_1, generate_ansatz_2]])
@pytest.mark.parametrize("measure", ["jsd", "kld"])
def test_expressibility_circuits(circuits, measure):
    """Tests that the expressibility measures give correct output."""
    exp_res = []
    for circuit in circuits:
        exp_circ = Expressibility(circuit, [(1, 4, 2)])
        exp_res.append(exp_circ.expressibility(measure))
    assert exp_res[0] < exp_res[1]
