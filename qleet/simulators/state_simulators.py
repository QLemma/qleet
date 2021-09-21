import typing

import numpy as np
import qiskit

import qleet


class StateSimulator:
    def __init__(
        self,
        circuit: qleet.utils.circuit.CircuitDescriptor,
        noise_model: typing.Optional[dict] = None,
    ):
        self.circuit = circuit
        self.noise_model = noise_model

    def simulate(
        self,
        param_resolver: typing.Dict[qiskit.circuit.Parameter, float],
        shots: int = 1024,
    ) -> np.ndarray:
        if self.circuit.default_backend == "qiskit":
            circuit = qiskit.QuantumCircuit.copy(
                self.circuit.qiskit_circuit
            ).bind_parameters(param_resolver)
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
        if self.circuit.default_backend == "cirq":
            raise NotImplementedError("Simulator for ")
