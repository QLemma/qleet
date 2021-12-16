import pytest

import cirq
import qiskit
import pyquil

import sympy

import qleet

# cirq template circuit
cirq_circuit = cirq.Circuit(
    [
        cirq.H(cirq.LineQubit(0)),
        cirq.H(cirq.LineQubit(1)),
        cirq.H(cirq.LineQubit(2)),
        cirq.CX(cirq.LineQubit(2), cirq.LineQubit(1)),
    ]
)

# cirq template circuit from qasm
cirq_circuit_qasm = cirq.Circuit(
    [
        cirq.H(cirq.NamedQubit("q_0")),
        cirq.H(cirq.NamedQubit("q_1")),
        cirq.H(cirq.NamedQubit("q_2")),
        cirq.CX(cirq.NamedQubit("q_2"), cirq.NamedQubit("q_1")),
    ]
)


# qiskit template circuit
qiskit_circuit = qiskit.QuantumCircuit(3)
qiskit_circuit.h(0)
qiskit_circuit.h(1)
qiskit_circuit.h(2)
qiskit_circuit.cx(2, 1)


# pyuil template circuit
pyquil_circuit = pyquil.Program()
pyquil_circuit += pyquil.gates.H(0)
pyquil_circuit += pyquil.gates.H(1)
pyquil_circuit += pyquil.gates.H(2)
pyquil_circuit += pyquil.gates.CNOT(2, 1)


def test_cirq_constructor():
    """Tests circuit descriptor for cirq circuits"""
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )
    assert cirq_circuit == cirq_descriptor.cirq_circuit


def test_qiskit_constructor():
    """Tests circuit descriptor for qiskit circuits"""
    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=qiskit.quantum_info.PauliList(["III"]),
    )
    assert qiskit_circuit == qiskit_descriptor.qiskit_circuit


def test_pyquil_constructor():
    """Tests circuit descriptor for pyquil circuits"""
    pyquil_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )
    assert pyquil_circuit == pyquil_descriptor.pyquil_circuit


def test_cirq_pyquil_conversion():
    """Tests circuit conversions for cirq and pyquil circuits"""
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )

    pyquil_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )

    assert cirq_circuit == pyquil_descriptor.cirq_circuit
    assert pyquil_circuit == cirq_descriptor.pyquil_circuit


def test_qiskit_pyquil_conversion():
    """Tests circuit conversions for pyquil and qiskit circuits"""
    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=qiskit.quantum_info.PauliList(["III"]),
    )

    pyquil_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )

    assert qiskit_circuit == pyquil_descriptor.qiskit_circuit
    assert pyquil_circuit == qiskit_descriptor.pyquil_circuit


def test_cirq_qiskit_conversion():
    """Tests circuit conversions for cirq and qiskit circuits"""
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit,
        params=[],
        cost_function=None,
    )

    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=None,
    )

    print(
        qiskit_descriptor.qiskit_circuit.qasm(),
        repr(cirq_circuit),
        repr(qiskit_descriptor.cirq_circuit),
    )

    assert qiskit_circuit == cirq_descriptor.qiskit_circuit
    assert cirq_circuit_qasm == qiskit_descriptor.cirq_circuit


def test_circuit_descriptor_from_qasm():
    """Tests circuit descriptor's from_qasm functionality"""

    qasm_str = qiskit_circuit.qasm()
    qiskit_descriptor_qasm = qleet.interface.circuit.CircuitDescriptor.from_qasm(
        qasm_str, [], qiskit.quantum_info.PauliList(["III"]), "qiskit"
    )
    pyquil_descriptor_qasm = qleet.interface.circuit.CircuitDescriptor.from_qasm(
        qasm_str, [], pyquil.paulis.PauliSum([]), "pyquil"
    )
    cirq_descriptor_qasm = qleet.interface.circuit.CircuitDescriptor.from_qasm(
        qasm_str, [], cirq.PauliSum(), "cirq"
    )

    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=qiskit.quantum_info.PauliList(["III"]),
    )
    pyquil_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit_qasm, params=[], cost_function=cirq.PauliSum()
    )

    assert qiskit_descriptor == qiskit_descriptor_qasm
    assert pyquil_descriptor == pyquil_descriptor_qasm
    assert cirq_descriptor == cirq_descriptor_qasm


def test_circuit_descriptor_comparision():
    """Tests circuit descriptor comparision"""

    qasm_str = qiskit_circuit.qasm()
    qiskit_descriptor_qasm = qleet.interface.circuit.CircuitDescriptor.from_qasm(
        qasm_str, [], qiskit.quantum_info.PauliList(["III"]), "qiskit"
    )

    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=qiskit.quantum_info.PauliList(["III"]),
    )

    assert qiskit_descriptor == qiskit_descriptor_qasm
    assert str(qiskit_descriptor)[:-16] == str(qiskit_descriptor_qasm)[:-16]
    assert repr(qiskit_descriptor)[:-20] == repr(qiskit_descriptor_qasm)[:-20]

    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )
    pyquil_decriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )

    assert qiskit_descriptor.__eq__(qiskit_descriptor_qasm)
    assert not qiskit_descriptor.__eq__(cirq_descriptor)
    assert not qiskit_descriptor.__eq__(pyquil_decriptor)
    assert not qiskit_descriptor.__eq__(None)


def test_circuit_descriptor_parameters():
    """Tests circuit descriptor's backend parameters"""
    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=qiskit.quantum_info.PauliList(["III"]),
    )
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )
    pyquil_decriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )

    assert cirq_descriptor.parameters == qiskit_descriptor.parameters
    assert pyquil_decriptor.parameters == qiskit_descriptor.parameters

    assert len(cirq_descriptor) == len(qiskit_descriptor)
    assert len(pyquil_decriptor) == len(qiskit_descriptor)


def test_circuit_descriptor_num_qubits():
    """Tests circuit descriptor's  number of qubits"""
    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=qiskit.quantum_info.PauliList(["III"]),
    )
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )
    pyquil_decriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )

    assert cirq_descriptor.num_qubits == qiskit_descriptor.num_qubits
    assert pyquil_decriptor.num_qubits == qiskit_descriptor.num_qubits


def test_circuit_descriptor_backend():
    """Tests circuit descriptor's backend property"""
    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=qiskit.quantum_info.PauliList(["III"]),
    )
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )
    pyquil_decriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )

    assert qiskit_descriptor.default_backend == "qiskit"
    assert cirq_descriptor.default_backend == "cirq"
    assert pyquil_decriptor.default_backend == "pyquil"


def test_circuit_cost():
    """Tests circuit descriptor's cost property and exceptions"""

    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit,
        params=[],
        cost_function=qiskit.quantum_info.PauliList(["III"]),
    )
    cirq_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=cirq_circuit, params=[], cost_function=cirq.PauliSum()
    )
    pyquil_decriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=pyquil_circuit, params=[], cost_function=pyquil.paulis.PauliSum([])
    )

    assert cirq_descriptor.cirq_cost is not None

    with pytest.raises(
        NotImplementedError, match="Qiskit PauliString support is not implemented"
    ):
        assert qiskit_descriptor.cirq_cost is not None

    with pytest.raises(
        NotImplementedError, match="PyQuil PauliString support is not implemented"
    ):
        assert pyquil_decriptor.cirq_cost is not None


def test_exceptions_circuit_descriptor():
    """Tests exceptions related to circuit descriptor"""
    circuit_descriptor = qleet.interface.circuit.CircuitDescriptor(None, [], None)

    with pytest.raises(ValueError, match="Unsupported framework of circuit"):
        assert circuit_descriptor.default_backend is not None

    with pytest.raises(
        ValueError, match="Expected a circuit object in cirq, qiskit or pyquil"
    ):
        assert circuit_descriptor.qiskit_circuit is not None

    with pytest.raises(
        ValueError, match="Expected a circuit object in cirq, qiskit or pyquil"
    ):
        assert circuit_descriptor.cirq_circuit is not None

    with pytest.raises(
        ValueError, match="Expected a circuit object in cirq, qiskit or pyquil"
    ):
        assert circuit_descriptor.pyquil_circuit is not None

    with pytest.raises(ValueError, match="Unsupported framework of circuit"):
        assert circuit_descriptor.num_qubits is not None

    with pytest.raises(ValueError, match="Cost object should be a Pauli-Sum object"):
        assert circuit_descriptor.cirq_cost is not None
