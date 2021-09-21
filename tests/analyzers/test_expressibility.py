import pytest
import numpy as np

import qiskit
import cirq
import pyquil
from qiskit import QuantumCircuit

import qleet
from qleet.analyzers.expressibility import Expressibility


def test_expressibility_non_param():
    """Test expressibility of a non-parameterized circuit"""
    params = []
    qiskit_circuit = qiskit.QuantumCircuit(2)
    qiskit_circuit.h(0)
    qiskit_circuit.cx(0, 1)
    qiskit_descriptor = qleet.utils.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=params, cost_function=None
    )

    qiskit_expressibility = Expressibility(qiskit_descriptor, samples=100)
    expr = qiskit_expressibility.expressibility("jsd")
    assert np.isclose(expr, 1)


def test_expressibility_param():
    """Test expressibility of a parameterized circuit"""
    params = [qiskit.circuit.Parameter(r"$θ_1$"), qiskit.circuit.Parameter(r"$θ_2$")]
    qiskit_circuit = qiskit.QuantumCircuit(2)
    qiskit_circuit.rx(params[0], 0)
    qiskit_circuit.cx(0, 1)
    qiskit_circuit.rx(params[1], 1)
    qiskit_descriptor = qleet.utils.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=params, cost_function=None
    )

    qiskit_expressibility = Expressibility(qiskit_descriptor, samples=100)
    expr = qiskit_expressibility.expressibility("jsd")
    assert expr > 0
