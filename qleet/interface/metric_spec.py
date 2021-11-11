import abc
import typing

import numpy as np
import sympy
import tensorflow_quantum as tfq

from ..interface.circuit import CircuitDescriptor


class MetricSpecifier(abc.ABC):
    """Class to specify classical metrics which are a function of the sampled quantum state.
    Examples would be an arbitrary cost function, Mean Squared Error for some regression task,
    size of the max cut, etc.

    This is an abstract class, all metrics should be it's subclasses
    """

    def __init__(self, default_call_mode="samples") -> None:
        """Creates the metric specifier object.
        :param default_call_mode: Which function to use by default for computing metric
        """
        self.__mode_to_function_map = {
            "samples": self.from_samples_vector,
            "state_vector": self.from_state_vector,
            "density_matrix": self.from_density_matrix,
        }
        assert default_call_mode in ["samples", "state_vector", "density_matrix"]
        self.default_call_mode = default_call_mode
        self.default_call_function = self.__mode_to_function_map[default_call_mode]

    def from_circuit(
        self,
        circuit_descriptor: CircuitDescriptor,
        parameters: typing.Union[np.ndarray, typing.List],
        mode="samples",
    ) -> float:
        """Computes the value of the metric from the circuit, by using the default mode
        or metric computation.
        :param circuit_descriptor: The provided circuit
        :param parameters: List of values of the parameters to sample the circuit at
        :param mode: From what to compute the metric, samples, state_vector, or density_matrix
        :return: The value of the metric at those parameters
        :raises NotImplementedError: if required mode of evaluating metric wasn't implemented
        :raises ValueError: if the mode specified wasn't valid
        """
        if mode == "samples":
            samples = sample_solutions(
                circuit=circuit_descriptor.cirq_circuit,
                param_symbols=circuit_descriptor.parameters,
                param_values=parameters,
            )
            return self.from_samples_vector(samples)
        elif mode == "state_vector":
            raise NotImplementedError
        elif mode == "density_matrix":
            raise NotImplementedError
        else:
            raise ValueError(
                "Provided mode should be one of [samples, state_vector, density_matrix]"
            )

    @abc.abstractmethod
    def from_state_vector(self, state_vector: np.ndarray) -> float:
        """Returns the value of the loss function given the state vector of the state
        prepared from the circuit.
        :param state_vector: State vector of state prepared by circuit
        :return: value of the loss function
        """
        raise NotImplementedError

    @abc.abstractmethod
    def from_density_matrix(self, density_matrix: np.ndarray) -> float:
        """Returns the value of the loss function given the density matrix of the state
        prepared from the circuit using the noise model provided.
        :param density_matrix: Vector of samples drawn from the circuit
        :return: value of the loss function
        """
        raise NotImplementedError

    @abc.abstractmethod
    def from_samples_vector(self, samples_vector: np.ndarray) -> float:
        """Returns the value of the loss function from one set of measurements sampled from
        the circuit.
        :param samples_vector: Vector of samples drawn from the circuit
        :return: value of the loss function
        """
        raise NotImplementedError


def sample_solutions(
    circuit,
    param_symbols: typing.List[sympy.Symbol],
    param_values: typing.Iterable,
    samples: int = 1000,
) -> np.ndarray:
    """Get the computed cuts for a given ansatz
    :param circuit: Circuit to be sampled
    :param param_symbols: The symbols of model parameters
    :param param_values: The value of model parameters to sample at, 1-D vector
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
