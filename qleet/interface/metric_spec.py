import abc

import numpy as np
import tensorflow_quantum as tfq

from ..interface.circuit import CircuitDescriptor


class MetricSpecifier(abc.ABC):

    def __init__(self, default_call_mode='samples'):
        self.__mode_to_function_map = {'samples': self.from_samples_vector,
                                       'state_vector': self.from_state_vector,
                                       'density_matrix': self.from_density_matrix}
        assert default_call_mode in ['samples', 'state_vector', 'density_matrix']
        self.default_call_mode = default_call_mode
        self.default_call_function = self.__mode_to_function_map[default_call_mode]

    def from_circuit(self, circuit_descriptor: CircuitDescriptor, parameters, mode='samples'):
        if mode == 'samples':
            samples = sample_solutions(circuit=circuit_descriptor.cirq_circuit,
                                       param_symbols=circuit_descriptor.parameters,
                                       param_values=parameters)
            return self.from_samples_vector(samples)
        elif mode == 'state_vector':
            raise NotImplementedError
        elif mode == 'density_matrix':
            raise NotImplementedError
        else:
            raise ValueError('Provided mode should be one of [samples, state_vector, density_matrix]')

    @abc.abstractmethod
    def from_state_vector(self, state_vector: np.ndarray) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def from_density_matrix(self, density_matrix: np.ndarray) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def from_samples_vector(self, samples_vector: np.ndarray) -> float:
        raise NotImplementedError


def sample_solutions(circuit, param_symbols, param_values, samples=1000):
    """
    Get the computed cuts for a given ansatz
    :param circuit: Circuit to be sampled
    :param param_symbols: The symbols of model parameters (betas and gammas) to sample at, 1-D vector
    :param param_values: The value of model parameters (betas and gammas) to sample at, 1-D vector
    :param samples: Number of times to sample the resulting quantum state
    :return: 2-D matrix, n_samples rows of boolean vectors showing the cut
    """
    output = tfq.layers.Sample()(
        circuit,
        symbol_names=param_symbols,
        symbol_values=[param_values],
        repetitions=samples,
    )
    return output.numpy()[0]
