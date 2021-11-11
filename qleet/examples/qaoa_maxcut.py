"""Implements an example of QAOA for Max Cut.
Allows the user to analyze QAOA with easy setup.
"""

import itertools
import typing

import numpy as np
import networkx as nx
import sympy
import cirq

from ..interface.metric_spec import MetricSpecifier


class QAOACircuitMaxCut:
    """The class to specify a QAOA circuit and metric for computing Max Cut of a graph."""

    def __init__(self, graph: nx.Graph = None, p: int = 2):
        """Constructor for the QAOA problem for Max Cut computation
        :type graph: nx.Graph
        :param graph: The graph for which we want to compute the max-cut
        :type p: int
        :param p: The number of blocks of the QAOA circuit
        """
        self._graph = nx.gnm_random_graph(n=6, m=15) if graph is None else graph
        self._qubits = cirq.GridQubit.rect(1, self._graph.number_of_nodes())
        self.params = sympy.symbols("q0:%d" % (2 * p))

        self.qaoa_circuit = cirq.Circuit()
        for qubit in self._qubits:
            self.qaoa_circuit.append(cirq.H(qubit))
        for i in range(p):
            # Cost Hamiltonian
            for edge in self._graph.edges():
                self.qaoa_circuit += cirq.CNOT(
                    self._qubits[edge[0]], self._qubits[edge[1]]
                )
                self.qaoa_circuit += cirq.rz(self.params[2 * i]).on(
                    self._qubits[edge[1]]
                )
                self.qaoa_circuit += cirq.CNOT(
                    self._qubits[edge[0]], self._qubits[edge[1]]
                )
            # Mixing Hamiltonian
            for j in range(len(self._qubits)):
                self.qaoa_circuit += cirq.rx(2 * self.params[2 * i + 1]).on(
                    self._qubits[j]
                )

        self.qaoa_cost: cirq.PauliSum = cirq.PauliSum()
        for edge in self._graph.edges():
            self.qaoa_cost += cirq.PauliString(
                1 / 2 * cirq.Z(self._qubits[edge[0]]) * cirq.Z(self._qubits[edge[1]])
            )

    def solve_classically(self):
        """Solve the combinatorial problem using a full, exponentially sized search
        :return: Value of the max the cut
        :rtype: float
        """
        subsets_list = itertools.chain.from_iterable(
            itertools.combinations(self._graph.nodes(), r)
            for r in range(self._graph.number_of_nodes() + 1)
        )
        max_cut = [
            nx.algorithms.cuts.cut_size(self._graph, assignment)
            for assignment in subsets_list
        ]
        return np.max(max_cut)


class MaxCutMetric(MetricSpecifier):
    """The metric for the Max Cut problem, generates using a classical process."""

    def __init__(self, graph):
        """Constructs the class which can be called to generate the metric.
        :type: networkx.Graph
        :param graph: The graph for which we are computing the max-cut
        """
        super().__init__("samples")
        self.graph = graph

    def from_samples_vector(self, samples_vector: np.ndarray) -> float:
        """Computes the vector from the samples vector output from the quantum circuit.
        :type samples_vector: np.array, 2-D matrix of size (num_samples, n)
        :param samples_vector: `num_samples` measurements each of size `n`, as a 2-D matrix
        :returns: The value of the max-cut
        :rtype: float
        """
        return typing.cast(
            float,
            np.mean(
                [
                    nx.algorithms.cuts.cut_size(self.graph, np.where(cut)[0])
                    for cut in samples_vector
                ]
            ),
        )

    def from_density_matrix(self, density_matrix: np.ndarray) -> float:
        """Computes the vector from the samples vector output from the quantum circuit.
        :type density_matrix: np.array, 2-D matrix of size (2^n, 2^n)
        :param density_matrix: The 2-D density matrix to generate the output metric
        :returns: The value of the max-cut
        :rtype: float
        :raises NotImplemetedError: Computing from density-matrix is not implemented yet
        """
        raise NotImplementedError

    def from_state_vector(self, state_vector: np.ndarray) -> float:
        """Computes the vector from the samples vector output from the quantum circuit.
        :type state_vector: np.array, 2-D matrix of size (2^n,)
        :param state_vector: The 2-D state vector to generate the output metric
        :returns: The value of the max-cut
        :rtype: float
        :raises NotImplemetedError: Computing from density-matrix is not implemented yet
        """
        raise NotImplementedError
