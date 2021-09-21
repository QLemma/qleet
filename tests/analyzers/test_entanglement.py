import pytest
import numpy as np

import qiskit
import cirq
import pyquil
from qiskit import QuantumCircuit

import qleet
from qleet.analyzers.entanglement import EntanglementCapability


def test_entanglement_local():
    """Test entanglement capability of a circuit with local gates"""
    params = []
    qiskit_circuit = qiskit.QuantumCircuit(2)
    qiskit_circuit.x(0)
    qiskit_circuit.x(1)
    qiskit_descriptor = qleet.utils.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=params, cost_function=None
    )

    qiskit_entg_capability = EntanglementCapability(qiskit_descriptor, samples=100)
    entg = qiskit_entg_capability.entanglement_capability("meyer-wallach")
    assert np.isclose(entg, 0)


def test_entanglement_non_local():
    """Test entanglement capability of a parameterized circuit with non-local gates"""
    params = [qiskit.circuit.Parameter(r"$θ_1$"), qiskit.circuit.Parameter(r"$θ_2$")]
    qiskit_circuit = qiskit.QuantumCircuit(2)
    qiskit_circuit.rx(params[0], 0)
    qiskit_circuit.cx(0, 1)
    qiskit_circuit.rx(params[1], 1)
    qiskit_descriptor = qleet.utils.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=params, cost_function=None
    )

    qiskit_entg_capability = EntanglementCapability(qiskit_descriptor, samples=100)
    entg = qiskit_entg_capability.entanglement_capability("meyer-wallach")
    assert entg > 0
