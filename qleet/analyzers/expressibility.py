import itertools
import matplotlib.pyplot as plt
import numpy as np
from qiskit import execute, Aer
from qiskit.providers.aer.noise import NoiseModel
from qiskit.quantum_info import state_fidelity
from scipy.spatial.distance import jensenshannon


class Expressibility:
    """Calculates expressibility of a parameterized quantum circuit"""

    def __init__(self, circuit, circuit_params, noise_model=None, samples=1000):
        """Constructor the the Expressibility analyzer
        :param circuit (template(uparams, cparams, **kwargs)): circuit template with arguments
            for parameterized single-qubit gates and two-qubit gates parameters.
        :param circuit_params: [(layers, num_qubits, single-qubit operations),
            (layers, num_qubits, two-qubit operations)] list of shapes of the parameter
            object in the circuit (unitary and controlled layer).
        :param noise_model:  (dict, NoiseModel) initialization noise-model dictionary for
            generating noise model
        :param samples: number of samples for the experiment
        """
        # TODO add support for the circuit parser  # pylint: disable=W0511
        self.circuit = circuit

        if isinstance(circuit_params, list):
            self.param_shape = circuit_params

        if noise_model is not None:
            if isinstance(noise_model, dict):
                try:
                    self.noise_model = NoiseModel.from_dict(noise_model)
                except:  # pylint: disable=W0702
                    # TODO support for cirq's noise models # pylint: disable=W0511
                    self.noise_model = None
            elif isinstance(noise_model, NoiseModel):
                self.noise_model = noise_model
        else:
            self.noise_model = None
        self.num_samples = samples
        self.plot_data = None

    @staticmethod
    def kl_divergence(prob_a, prob_b):
        """Returns KL divergence between two probabilities"""
        prob_a[prob_a == 0] = 1e-10
        return np.sum(np.where(prob_a != 0, prob_a * np.log(prob_a / prob_b), 0))

    @staticmethod
    def gen_params(samples, params):
        """Generate parameters for the calculation of expressibility
        Args:
            samples (int): number of samples considered for the expressibility calculation
            params (list(tuple)): shape of the parameters for the parameterized quantum circuit
        Return
            theta (np.ndarray): first list of parameters for the parameterized quantum circuit
            phi (np.ndarray): second list of parameters for the parameterized quantum circuit
        """
        theta = [np.random.uniform(0, 2 * np.pi, (samples, *param)) for param in params]
        phi = [np.random.uniform(0, 2 * np.pi, (samples, *param)) for param in params]
        return theta, phi

    def circuit_ouput(self, circuit, shots=1024):
        """Returns output for the given circuit"""
        if self.noise_model is not None:
            circuit.snapshot("final", snapshot_type="density_matrix")
            result = execute(
                circuit,
                Aer.get_backend("qasm_simulator"),
                shots=shots,
                noise_model=self.noise_model,
                backend_options={"method": "density_matrix"},
            ).result()
            result_data = result.data(0)["snapshots"]["density_matrix"]["final"][0][
                "value"
            ]
        else:
            circuit.snapshot("final", snapshot_type="statevector")
            result = execute(
                circuit, Aer.get_backend("aer_simulator_statevector")
            ).result()
            result_data = result.data(0)["snapshots"]["statevector"]["final"][0]
        return result_data

    def prob_haar(self):
        """Returns probability density function of fidelities for Haar Random States"""
        fidelity = np.linspace(0, 1, self.num_samples)
        print(self.param_shape)
        num_qubits = self.param_shape[0][1]
        return (2 ** num_qubits - 1) * (1 - fidelity + 1e-8) ** (2 ** num_qubits - 2)

    def prob_pqc(self, shots: int = 1024) -> np.ndarray:
        """Return probability density function of fidelities for PQC
        Args:
            shots (int): number of shots for circuit execution
        Return:
            fidelities (np.ndarray): np.ndarray of fidelities
        """
        thetas, phis = self.gen_params(self.num_samples, self.param_shape)
        theta, phi = thetas[0], phis[0]
        try:
            ctheta, cphi = thetas[1], phis[1]
        except IndexError:
            ctheta, cphi = [None] * self.num_samples, [None] * self.num_samples

        th_circ = [
            self.circuit_ouput(self.circuit(th, cth), shots)  # pylint: disable=E1121
            for th, cth in zip(theta, ctheta)
        ]
        ph_circ = [
            self.circuit_ouput(self.circuit(ph, cph), shots)  # pylint: disable=E1121
            for ph, cph in zip(phi, cphi)
        ]
        fidelity = np.array(
            [
                state_fidelity(rhoa, rhob)
                for rhoa, rhob in itertools.product(th_circ, ph_circ)
            ]
        )
        return np.array(fidelity)

    def expressibility(self, measure: str = "kld", shots: int = 1024) -> float:
        """Returns expressibility for the circuit
        :param measure: specification for the measure used in the expressibility calculation
                           "kld" for KL divergence and "jsd" Jensen-Shannon divergence.
        :param shots: number of shots for circuit execution
        :returns pqc_expressibility: float, expressibility value
        """
        haar = self.prob_haar()
        haar_prob = haar / float(haar.sum())

        fidelity = self.prob_pqc(shots)
        pqc_hist, bin_edges = np.histogram(
            fidelity, self.num_samples, range=(0, 1), density=True
        )
        pqc_prob = pqc_hist / float(pqc_hist.sum())

        if measure == "kld":
            pqc_expressibility = self.kl_divergence(pqc_prob, haar_prob)
        elif measure == "jsd":
            pqc_expressibility = jensenshannon(pqc_prob, haar_prob, 2.0)

        self.plot_data = (pqc_prob, pqc_prob, bin_edges, pqc_expressibility)

        return pqc_expressibility

    def plot(self, figsize=(6, 4), dpi=300, **kwargs):
        """Returns plot for expressibility visualization"""
        if self.plot_data is None:
            raise "Perform expressibility calculation first"

        haar_prob, pqc_prob, bin_edges, expr = self.plot_data
        bin_middles = (bin_edges[1:] + bin_edges[:-1]) / 2.0
        bin_width = bin_edges[1] - bin_edges[0]

        fig = plt.figure(figsize=figsize, dpi=dpi, **kwargs)
        plt.bar(bin_middles, haar_prob, width=bin_width, label="Haar")
        plt.bar(bin_middles, pqc_prob, width=bin_width, label="PQC", alpha=0.6)
        plt.xlim((-0.05, 1.05))
        plt.ylim(bottom=0.0, top=max(max(pqc_prob), max((haar_prob))) + 0.01)
        plt.grid(True)
        plt.title(f"Expressibility: {np.round(expr,5)}")
        plt.xlabel("Fidelity")
        plt.ylabel("Probability")
        plt.legend()

        return fig
