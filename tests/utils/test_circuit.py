import cirq
import qiskit

from qleet.utils.circuit import CircuitDescriptor


def test_cirq_constructor():
    cirq_circuit = cirq.Circuit(
        [
            cirq.H(cirq.LineQubit(0)),
            cirq.H(cirq.LineQubit(1)),
            cirq.H(cirq.LineQubit(2)),
            cirq.CX(cirq.LineQubit(2), cirq.LineQubit(1)),
        ]
    )
    cirq_descriptor = CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=lambda x: 0
    )
    assert cirq_circuit == cirq_descriptor.cirq_circuit


def test_qiskit_constructor():
    qiskit_circuit = qiskit.QuantumCircuit(3)
    qiskit_circuit.h(0)
    qiskit_circuit.h(1)
    qiskit_circuit.h(2)
    qiskit_circuit.cx(2, 1)

    qiskit_descriptor = CircuitDescriptor(
        circuit=qiskit_circuit, params=[], cost_function=lambda x: 0
    )
    assert qiskit_circuit == qiskit_descriptor.qiskit_circuit


def test_cirq_qiskit_conversion():
    cirq_circuit = cirq.Circuit(
        [
            cirq.H(cirq.LineQubit(0)),
            cirq.H(cirq.LineQubit(1)),
            cirq.H(cirq.LineQubit(2)),
            cirq.CX(cirq.LineQubit(2), cirq.LineQubit(1)),
        ]
    )
    cirq_descriptor = CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=lambda x: 0
    )
    assert cirq_circuit == cirq_descriptor.cirq_circuit

    qiskit_circuit = qiskit.QuantumCircuit(3)
    qiskit_circuit.h(0)
    qiskit_circuit.h(1)
    qiskit_circuit.h(2)
    qiskit_circuit.cx(2, 1)

    qiskit_descriptor = CircuitDescriptor(
        circuit=qiskit_circuit, params=[], cost_function=lambda x: 0
    )
    assert qiskit_circuit.qasm() == cirq_descriptor.qiskit_circuit.qasm()
