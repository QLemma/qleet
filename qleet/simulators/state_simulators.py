import typing

import cirq
import numpy as np
import qiskit

import qleet


class StateSimulator:
    def __init__(
        self,
        circuit: qleet.utils.circuit.CircuitDescriptor,
        noise_model: typing.Optional[dict] = None,
    ):
        """
        Initialize the state simulator
        :param circuit: the target circuit to simulate
        :param noise_model: the noise model as dict or empty dict for density matrix simulations,
            None if performing state vector simulations
        """
        self.circuit = circuit
        self.noise_model = noise_model

    def simulate(
        self,
        param_resolver: typing.Dict[qiskit.circuit.Parameter, float],
        shots: int = 1024,
    ) -> np.ndarray:
        """
        Simulate to get the state vector or the density matrix
        :param param_resolver: a dictionary of all the symbols/parameters mapping to their values
        :param shots: number of times to run the qiskit density matrix simulator
        :returns: state vector or density matrix resulting from the simulation
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
            return result_data
        elif self.circuit.default_backend == "cirq":
            simulator = cirq.Simulator()
            result = simulator.simulate(self.circuit.cirq_circuit, param_resolver)
            if self.noise_model is None:
                return result.final_state_vector
            else:
                return result.density_matrix_of()
        else:
            raise NotImplementedError(
                "Parametrized circuit simulation is not implemented for this backend."
            )
