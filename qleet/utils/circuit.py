import typing

import numpy as np
import sympy

import cirq
import qiskit
import pyquil

from cirq.contrib.qasm_import import circuit_from_qasm
from cirq.contrib.quil_import import circuit_from_quil
import qiskit.quantum_info
import pyquil.paulis


def convert_to_cirq(
    circuit: typing.Union[qiskit.QuantumCircuit, cirq.Circuit, pyquil.Program]
) -> cirq.Circuit:
    """Converts any circuit to cirq
    :param circuit: input circuit in any framework
    :return: circuit in cirq
    :raises ValueError: if the circuit is not from one of the supported frameworks
    """
    if isinstance(circuit, cirq.Circuit):
        return circuit
    elif isinstance(circuit, qiskit.QuantumCircuit):
        return circuit_from_qasm(circuit.qasm())
    elif isinstance(circuit, pyquil.Program):
        return circuit_from_quil(str(circuit))
    else:
        raise ValueError(
            f"Expected a circuit object in cirq, qiskit or pyquil, got {type(circuit)}"
        )


def convert_to_qiskit(
    circuit: typing.Union[qiskit.QuantumCircuit, cirq.Circuit, pyquil.Program]
) -> qiskit.QuantumCircuit:
    """Converts any circuit to qiskit
    :param circuit: input circuit in any framework
    :raises ValueError: if the circuit is not from one of the supported frameworks
    :return: circuit in qiskit
    """
    if isinstance(circuit, cirq.Circuit):
        return qiskit.QuantumCircuit.from_qasm_str(circuit.to_qasm())
    elif isinstance(circuit, qiskit.QuantumCircuit):
        return circuit
    elif isinstance(circuit, pyquil.Program):
        raise convert_to_qiskit(convert_to_cirq(circuit))
    else:
        raise ValueError(
            f"Expected a circuit object in cirq, qiskit or pyquil, got {type(circuit)}"
        )


class CircuitDescriptor:
    """The interface for users to provide a circuit in any framework and visualize it in qLEET."""

    def __init__(
        self,
        circuit: typing.Union[qiskit.QuantumCircuit, cirq.Circuit, pyquil.Program],
        params: typing.List[typing.Union[sympy.Symbol, qiskit.circuit.Parameter]],
        cost_function: typing.Union[
            cirq.PauliSum, qiskit.quantum_info.PauliList, pyquil.paulis.PauliSum, None
        ] = None,
    ):
        self._circuit = circuit
        self._params = params
        self._cost = cost_function

    @property
    def default_backend(self):
        if isinstance(self._circuit, cirq.Circuit):
            return "cirq"
        elif isinstance(self._circuit, qiskit.QuantumCircuit):
            return "qiskit"
        elif isinstance(self._circuit, pyquil.Program):
            return "pyquil"
        else:
            raise ValueError("Unsupported framework of circuit")

    @classmethod
    def from_qasm(cls, qasm_str: str, params, cost_function):
        """Generate the descriptor from OpenQASM string
        :param qasm_str:OpenQASM string for each part of the circuit
        :param params: list of sympy symbols which act as parameters
        :param cost_function: pauli-string operator to implement cost function
        :return: The CircuitDescriptor object
        """
        cirq_circuit = circuit_from_qasm(qasm_str)
        return CircuitDescriptor(
            circuit=cirq_circuit, params=params, cost_function=cost_function
        )

    @property
    def parameters(
        self,
    ) -> typing.List[typing.Union[sympy.Symbol, qiskit.circuit.Parameter]]:
        """The list of sympy symbols to resolve as parameters, will be swept from 0 to 2*pi
        :return: list of parameters
        """
        return self._params

    @property
    def shape(self) -> int:
        """Number of parameters in the variational circuit
        :return: number of parameters in the circuit
        """
        return len(self.parameters)

    @property
    def cirq_circuit(self) -> cirq.Circuit:
        """Get the circuit in cirq
        :return: the cirq representation of the circuit
        """
        return convert_to_cirq(self._circuit)

    @property
    def qiskit_circuit(self) -> qiskit.QuantumCircuit:
        """Get the circuit in qiskit
        :return: the cirq representation of the circuit
        """
        return convert_to_qiskit(self._circuit)

    @property
    def num_qubits(self) -> qiskit.QuantumCircuit:
        """Get the number of qubits for a circuit
        :return: the number of qubits in the circuit
        :raises ValueError: if unsupported circuit framework is given
        """
        if isinstance(self._circuit, cirq.Circuit):
            return len(self._circuit.all_qubits())
        elif isinstance(self._circuit, qiskit.QuantumCircuit):
            return self._circuit.num_qubits
        elif isinstance(self._circuit, pyquil.Program):
            return len(self._circuit.get_qubits())
        else:
            raise ValueError("Unsupported framework of circuit")

    @property
    def cirq_cost(self) -> cirq.PauliSum:
        """Returns the cost function, which is a function that takes in the state vector or the
        density matrix and returns the loss value of the solution envisioned by the Quantum Circuit.
        :raises ValueError: if the circuit is not from one of the supported frameworks
        :raises NotImplementedError: Long as qiskit and pyquil ports of pauli-string aren't written
        :return: cost function
        TODO: Implement conversions into Cirq PauliSum
        """
        if isinstance(self._cost, cirq.PauliSum):
            return self._cost
        elif isinstance(self._cost, qiskit.quantum_info.PauliList):
            raise NotImplementedError("Qiskit PauliString support is not implemented")
        elif isinstance(self._cost, pyquil.paulis.PauliSum):
            raise NotImplementedError("PyQuil PauliString support is not implemented")
        else:
            raise ValueError("Cost object should be a Pauli-Sum object")

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, CircuitDescriptor):
            return (
                np.array_equal(self.parameters, other.parameters)
                and self.cirq_circuit == other.cirq_circuit
            )
        else:
            return False

    def __repr__(self) -> str:
        return f"qleet.CircuitDescriptor({repr(self._circuit)}, {repr(self._params)})"

    def __str__(self) -> str:
        return f"qleet.CircuitDescriptor({repr(self._circuit)})"
