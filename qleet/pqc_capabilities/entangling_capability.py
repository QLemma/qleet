import itertools
import numpy as np
from qiskit import execute, Aer
from qiskit.providers.aer.noise import NoiseModel
from qiskit.quantum_info import partial_trace
from scipy.special import comb

class EntanglingCapability:
    """ Calculates entangling capability of a parameterized quantum circuit """
    def __init__(self, circuit, circuit_params, noise_model = None, samples = 1000):
        """
        Args:
            circuit (template(uparams, cparams, **kwargs)): circuit template with arguments
            for parameterized single-qubit gates and two-qubit gates parameters.
            circuit_params (list[tuples]): [(layers, num_qubits, single-qubit operations),
            (layers, num_qubits, two-qubit operations)] list of shapes of the parameter
            object in the circuit (unitary and controlled layer).
            initilization noise_model (dict, NoiseModel): dictionary for generating noise model
            samples (int): number of samples for the experiment

        Returns:
            Expressibility object instance
        """
        # TODO add support for the circuit parser  # pylint: disable=W0511
        self.circuit = circuit

        if isinstance(circuit_params, list):
            self.param_shape = circuit_params

        if noise_model is not None:
            if isinstance(noise_model, dict):
                try:
                    self.noise_model = NoiseModel.from_dict(noise_model)
                except: # pylint: disable=W0702
                    # TODO support for cirq's noise models # pylint: disable=W0511
                    self.noise_model = None
            elif isinstance(noise_model, NoiseModel):
                self.noise_model = noise_model
        else:
            self.noise_model = None
        self.num_samples = samples

    @staticmethod
    def gen_params(samples, params):
        """ Generate parameters for the calculation of entangling capability
        Args:
            samples (int): number of samples considered for the entangling capability calculation
            params (list(tuple)): shape of the parameters for the parameterized quantum circuit
        Return
            theta (np.ndarray): first list of parameters for the parameterized quantum circuit
            phi (np.ndarray): second list of parameters for the parameterized quantum circuit
        """
        theta = [np.random.uniform(0, 2*np.pi, (samples, *param)) for param in params]
        phi = [np.random.uniform(0, 2*np.pi, (samples, *param)) for param in params]
        return theta, phi

    @staticmethod
    def scott_helper(st, perms):
        """ Helper function for entanglement measure. It gives trace of the output state """
        dems = np.linalg.matrix_power([partial_trace(st, list(qb)).data for qb in perms], 2)
        trace = np.trace(dems, axis1=1, axis2=2)
        return np.sum(trace).real

    def meyer_wallach_measure(self, states, num_qubits):
        """
            Returns the meyer-wallach entanglement measure for the given circuit.

            r"$$ Q = \frac{2}{|\vec{\theta}|}\sum_{\theta_{i}\in \vec{\theta}}\Bigg(1-
                        \frac{1}{n}\sum_{k=1}^{n}Tr(\rho_{k}^{2}(\theta_{i}))\Bigg)$$ "

        """
        permutations = list(itertools.combinations(range(num_qubits), num_qubits-1))
        ns = 2 * sum([1 - self.scott_helper(st, permutations)/num_qubits for st in states])
        return ns.real

    def scott_measure(self, states, num_qubits):
        """
            Returns the scott entanglement measure for the given circuit.

            r"$$ Q = \frac{1}{\lfloor N/2 \rfloor} \sum_{m=1}^{\lfloor N/2 \rfloor} Q_{m} \Rightarrow
                     \frac{1}{\lfloor N/2 \rfloor |\vec{\theta}|} \sum_{m=1}^{\lfloor N/2 \rfloor}
                     \frac{2^{m}}{2^{m}-1} \sum_{\theta_{i}\in \vec{\theta}}\Bigg( 1 -
                     \frac{m! (N-m)!}{N!} \sum_{|S|=m} Tr(\rho_{S}^{2}(\theta_{i}))  \Bigg) $$"
        """
        m = range(1, num_qubits//2 + 1)
        permutations = [list(itertools.combinations(range(num_qubits), num_qubits-idx)) for idx in m]
        combs = [1/comb(num_qubits, idx) for idx in m]
        contri = [2**idx/(2**idx-1) for idx in m]
        ns = []

        for ind, perm in enumerate(permutations):
            ns.append(contri[ind] * sum([1 - combs[ind]*self.scott_helper(st, perm) for st in states]))

        return ns

    def circuit_ouput(self, circuit, shots=1024):
        """ Returns output for the given circuit """
        if self.noise_model is not None:
            circuit.snapshot('final', snapshot_type='density_matrix')
            result = execute(circuit, Aer.get_backend('qasm_simulator'), shots=shots,
            noise_model = self.noise_model, backend_options = {"method": "density_matrix"}).result()
            result_data = result.data(0)['snapshots']['density_matrix']['final'][0]['value']
        else:
            result = execute(circuit, Aer.get_backend('statevector_simulator')).result()
            result_data = result.get_statevector(circuit, decimals=5)
        return result_data

    def entangling_capability(self, measure: str = "meyer-wallach", shots: int = 1024) -> float:
        """ Returns entanglement measure for the given circuit
        Args:
            measure (str): specification for the measure used in the entangling capability
                            calculation "meyer-wallach" for Meyer-Wallach measure and
                           "scott" for Scott measure.
            shorts (int): number of shots for circuit execution
        Returns:
            pqc_entangling_capability (float): entanglement measure value
        """

        thetas, phis = self.gen_params(self.num_samples, self.param_shape)
        theta, phi = thetas[0], phis[0]
        try:
            ctheta, cphi = thetas[1], phis[1]
        except IndexError:
            ctheta, cphi = [None]*self.num_samples, [None]*self.num_samples

        th_circ = [self.circuit_ouput(self.circuit(th, cth), shots) # pylint: disable=E1121
                        for th, cth in zip(theta, ctheta)]
        ph_circ = [self.circuit_ouput(self.circuit(ph, cph), shots) # pylint: disable=E1121
                        for ph, cph in zip(phi, cphi)]

        num_qubits = self.param_shape[0][1]

        if measure == "meyer-wallach":
            pqc_entangling_capability = self.meyer_wallach_measure(th_circ+ph_circ,
                                                            num_qubits)/(2*self.num_samples)
        elif measure == "scott":
            pqc_entangling_capability = self.scott_measure(th_circ+ph_circ,
                                                            num_qubits)/(2*self.num_samples)

        return pqc_entangling_capability
