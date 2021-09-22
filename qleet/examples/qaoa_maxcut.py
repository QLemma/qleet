import itertools

import numpy as np
import networkx as nx
import sympy
import cirq


class QAOACircuitMaxCut:
    def __init__(self, graph: nx.Graph = None, p: int = 2):
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
