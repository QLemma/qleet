import numpy as np
import qiskit

import qleet


def test_entanglement_local():
    """Test entanglement capability of a circuit with local gates"""
    params = []
    qiskit_circuit = qiskit.QuantumCircuit(2)
    qiskit_circuit.x(0)
    qiskit_circuit.x(1)
    qiskit_descriptor = qleet.utils.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=params, cost_function=None
    )

    qiskit_entanglement_capability = (
        qleet.analyzers.entanglement.EntanglementCapability(
            qiskit_descriptor, samples=100
        )
    )
    entanglement = qiskit_entanglement_capability.entanglement_capability(
        "meyer-wallach"
    )
    assert np.isclose(entanglement, 0)


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

    qiskit_entanglement_capability = (
        qleet.analyzers.entanglement.EntanglementCapability(
            qiskit_descriptor, samples=100
        )
    )
    entanglement = qiskit_entanglement_capability.entanglement_capability(
        "meyer-wallach"
    )
    assert entanglement > 0
