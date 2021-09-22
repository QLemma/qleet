import typing

import cirq
import numpy as np
import qiskit

from qleet.interface.circuit import CircuitDescriptor


class CircuitSimulator:
    """The interface for users to execute their CircuitDescriptor objects"""

    def __init__(
        self,
        circuit: CircuitDescriptor,
        noise_model: typing.Optional[dict] = None,
    ):
        """Initialize the state simulator
        :param circuit: the target circuit to simulate
        :param noise_model: the noise model as dict or empty dict for density matrix simulations,
            None if performing state vector simulations
        """
        self.circuit = circuit
        self.noise_model = noise_model
        self._result = None

    @property
    def result(
        self,
    ) -> typing.Optional[np.ndarray]:
        """Get the results stored from the circuit simulator
        :return: stored result of the circuit simulation if it has been performed, else None.
        """
        return self._result

    def simulate(
        self,
        param_resolver: typing.Dict[qiskit.circuit.Parameter, float],
        shots: int = 1024,
    ) -> np.ndarray:
        """Simulate to get the state vector or the density matrix
        :param param_resolver: a dictionary of all the symbols/parameters mapping to their values
        :param shots: number of times to run the qiskit density matrix simulator
        :returns: state vector or density matrix resulting from the simulation
        :raises NotImplementedError: if circuit simulation is not supported for a backend
        """
        if self.circuit.default_backend == "qiskit":
            circuit = self.circuit.qiskit_circuit.bind_parameters(param_resolver)
            if self.noise_model is not None:
                circuit.snapshot("final", snapshot_type="density_matrix")
                result = qiskit.execute(
                    circuit,
                    qiskit.Aer.get_backend("qasm_simulator"),
                    shots=shots,
                    noise_model=self.noise_model,
                    backend_options={"method": "density_matrix"},
                ).result()
                result_data = result.data(0)["snapshots"]["density_matrix"]["final"][0][
                    "value"
                ]
            else:
                circuit.snapshot("final", snapshot_type="statevector")
                result = qiskit.execute(
                    circuit, qiskit.Aer.get_backend("aer_simulator_statevector")
                ).result()
                result_data = result.data(0)["snapshots"]["statevector"]["final"][0]

        elif self.circuit.default_backend == "cirq":
            simulator = cirq.Simulator()
            result = simulator.simulate(self.circuit.cirq_circuit, param_resolver)
            if self.noise_model is None:
                result_data = result.final_state_vector
            else:
                result_data = result.density_matrix_of()

        else:
            raise NotImplementedError(
                "Parametrized circuit simulation is not implemented for this backend."
            )

        self._result = result_data
        return result_data
