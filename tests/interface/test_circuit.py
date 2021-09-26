import cirq
import pytest
import qiskit
import sympy

import qleet


def test_cirq_constructor():
    cirq_circuit = cirq.Circuit(
        [
            cirq.H(cirq.LineQubit(0)),
            cirq.H(cirq.LineQubit(1)),
            cirq.H(cirq.LineQubit(2)),
            cirq.CX(cirq.LineQubit(2), cirq.LineQubit(1)),
        ]
    )
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )
    assert cirq_circuit == cirq_descriptor.cirq_circuit


def test_qiskit_constructor():
    qiskit_circuit = qiskit.QuantumCircuit(3)
    qiskit_circuit.h(0)
    qiskit_circuit.h(1)
    qiskit_circuit.h(2)
    qiskit_circuit.cx(2, 1)

    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=[], cost_function=cirq.PauliSum()
    )
    assert qiskit_circuit == qiskit_descriptor.qiskit_circuit


def test_cirq_qiskit_conversion():
    cirq_circuit = cirq.Circuit(
        [
            cirq.H(cirq.NamedQubit("q_0")),
            cirq.H(cirq.NamedQubit("q_1")),
            cirq.H(cirq.NamedQubit("q_2")),
            cirq.CX(cirq.NamedQubit("q_2"), cirq.NamedQubit("q_1")),
        ]
    )
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )
    assert cirq_circuit == cirq_descriptor.cirq_circuit

    qiskit_circuit = qiskit.QuantumCircuit(3)
    qiskit_circuit.h(0)
    qiskit_circuit.h(1)
    qiskit_circuit.h(2)
    qiskit_circuit.cx(2, 1)

    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=[], cost_function=cirq.PauliSum()
    )
    assert qiskit_circuit.qasm() == cirq_descriptor.qiskit_circuit.qasm()
    assert cirq_circuit == qiskit_descriptor.cirq_circuit


@pytest.mark.xfail
def test_cirq_to_qiskit_parametrized():
    params = sympy.symbols("param:%d" % 2)
    cirq_circuit = cirq.Circuit(
        [
            cirq.rx(params[0]).on(cirq.NamedQubit("q_0")),
            cirq.CX(cirq.NamedQubit("q_0"), cirq.NamedQubit("q_1")),
            cirq.rx(params[1]).on(cirq.NamedQubit("q_1")),
        ]
    )
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=params, cost_function=cirq.PauliSum()
    )
    qiskit_circuit = cirq_descriptor.qiskit_circuit
    assert qiskit_circuit.parameters is not None
