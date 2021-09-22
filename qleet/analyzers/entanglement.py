import itertools
import typing

from qiskit.providers.aer.noise import NoiseModel as qiskitNoiseModel
from cirq.devices.noise_model import NoiseModel as cirqNoiseModel
from pyquil.noise import NoiseModel as pyquilNoiseModel

from qiskit.quantum_info import partial_trace
from scipy.special import comb

import numpy as np

from qleet.utils.circuit import CircuitDescriptor
from qleet.simulators.circuit_simulators import CircuitSimulator

NOISE_MODELS = {
    "cirq": cirqNoiseModel,
    "pyquil": pyquilNoiseModel,
    "qiskit": qiskitNoiseModel,
}


class EntanglementCapability:
    """Calculates entangling capability of a parameterized quantum circuit"""

    def __init__(
        self,
        circuit: CircuitDescriptor,
        noise_model: typing.Union[
            cirqNoiseModel, qiskitNoiseModel, pyquilNoiseModel, None
        ] = None,
        samples: int = 1000,
    ):
        """Constructor for entanglement capability plotter

        :param circuit: input circuit as a CircuitDescriptor object
        :param noise_model:  (dict, NoiseModel) initialization noise-model dictionary for
            generating noise model
        :param samples: number of samples for the experiment
        :returns Entanglement object instance
        :raises ValueError: If circuit and noise model does not correspond to same framework
        """
        self.circuit = circuit

        if noise_model is not None:
            if isinstance(noise_model, NOISE_MODELS[circuit.default_backend]):
                self.noise_model = noise_model
            else:
                raise ValueError(
                    f"Circuit and noise model must correspond to the same \
                    framework but circuit:{circuit.default_backend} and \
                    noise_model:{type(noise_model)} were provided."
                )
        else:
            self.noise_model = None

        self.num_samples = samples
        self.entgcap = 0

    def gen_params(self) -> typing.Tuple[typing.List, typing.List]:
        """Generate parameters for the calculation of expressibility
        Args:
            samples (int): number of samples considered for the expressibility calculation
        Return
            theta (np.ndarray): first list of parameters for the parameterized quantum circuit
            phi (np.ndarray): second list of parameters for the parameterized quantum circuit
        """
        theta = [
            {p: 2 * np.random.random() * np.pi for p in self.circuit.parameters}
            for _ in range(self.num_samples)
        ]
        phi = [
            {p: 2 * np.random.random() * np.pi for p in self.circuit.parameters}
            for _ in range(self.num_samples)
        ]
        return theta, phi

    @staticmethod
    def scott_helper(state, perms):
        """Helper function for entanglement measure. It gives trace of the output state"""
        dems = np.linalg.matrix_power(
            [partial_trace(state, list(qb)).data for qb in perms], 2
        )
        trace = np.trace(dems, axis1=1, axis2=2)
        return np.sum(trace).real

    def meyer_wallach_measure(self, states, num_qubits):
        r"""Returns the meyer-wallach entanglement measure for the given circuit.

        .. math::
        Q = \frac{2}{|\vec{\theta}|}\sum_{\theta_{i}\in \vec{\theta}}\Bigg(1-
            \frac{1}{n}\sum_{k=1}^{n}Tr(\rho_{k}^{2}(\theta_{i}))\Bigg)

        """
        permutations = list(itertools.combinations(range(num_qubits), num_qubits - 1))
        ns = 2 * sum(
            [
                1 - 1 / num_qubits * self.scott_helper(state, permutations)
                for state in states
            ]
        )
        print(permutations)
        return ns.real

    def scott_measure(self, states, num_qubits):
        r"""Returns the scott entanglement measure for the given circuit.

        .. math::
        Q = \frac{1}{\lfloor N/2 \rfloor} \sum_{m=1}^{\lfloor N/2 \rfloor} Q_{m} \Rightarrow
            \frac{1}{\lfloor N/2 \rfloor |\vec{\theta}|} \sum_{m=1}^{\lfloor N/2 \rfloor}
            \frac{2^{m}}{2^{m}-1} \sum_{\theta_{i}\in \vec{\theta}}\Bigg( 1 -
            \frac{m! (N-m)!}{N!} \sum_{|S|=m} Tr(\rho_{S}^{2}(\theta_{i}))  \Bigg)
        """
        m = range(1, num_qubits // 2 + 1)
        permutations = [
            list(itertools.combinations(range(num_qubits), num_qubits - idx))
            for idx in m
        ]
        combs = [1 / comb(num_qubits, idx) for idx in m]
        contri = [2 ** idx / (2 ** idx - 1) for idx in m]
        ns = []

        for ind, perm in enumerate(permutations):
            ns.append(
                contri[ind]
                * sum(
                    [
                        1 - combs[ind] * self.scott_helper(state, perm)
                        for state in states
                    ]
                )
            )

        return np.array(ns)

    def entanglement_capability(
        self, measure: str = "meyer-wallach", shots: int = 1024
    ) -> float:
        """Returns entanglement measure for the given circuit
        :param measure: specification for the measure used in the entangling capability
                            calculation "meyer-wallach" for Meyer-Wallach measure and
                           "scott" for Scott measure.
        :param shots: number of shots for circuit execution
        :returns pqc_entangling_capability (float): entanglement measure value
        :raises ValueError: if invalid measure is specified
        """
        thetas, phis = self.gen_params()

        theta_circs = [
            CircuitSimulator(self.circuit, self.noise_model).simulate(theta, shots)
            for theta in thetas
        ]
        phi_circs = [
            CircuitSimulator(self.circuit, self.noise_model).simulate(phi, shots)
            for phi in phis
        ]

        num_qubits = self.circuit.num_qubits

        if measure == "meyer-wallach":
            pqc_entanglement_capability = self.meyer_wallach_measure(
                theta_circs + phi_circs, num_qubits
            ) / (2 * self.num_samples)
        elif measure == "scott":
            pqc_entanglement_capability = self.scott_measure(
                theta_circs + phi_circs, num_qubits
            ) / (2 * self.num_samples)
        else:
            raise ValueError(
                "Invalid measure provided, choose from 'meyer-wallach' or 'scott'"
            )

        self.entgcap = pqc_entanglement_capability
        return pqc_entanglement_capability
