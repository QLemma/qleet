import itertools

import numpy as np
import networkx as nx
import sympy
import cirq

graph = nx.gnm_random_graph(n=10, m=40)
p = 4
qubits = cirq.GridQubit.rect(1, graph.number_of_nodes())
params = sympy.symbols("q0:%d" % (2 * p))

qaoa_circuit = cirq.Circuit()
for qubit in qubits:
    qaoa_circuit.append(cirq.H(qubit))
for i in range(p):
    # Cost Hamiltonian
    for edge in graph.edges():
        qaoa_circuit += cirq.CNOT(qubits[edge[0]], qubits[edge[1]])
        qaoa_circuit += cirq.rz(params[2 * i]).on(qubits[edge[1]])
        qaoa_circuit += cirq.CNOT(qubits[edge[0]], qubits[edge[1]])
    # Mixing Hamiltonian
    for j in range(len(qubits)):
        qaoa_circuit += cirq.rx(2 * params[2 * i + 1]).on(qubits[j])

qaoa_cost = 0
for edge in graph.edges():
    qaoa_cost += cirq.PauliString(
        1 / 2 * cirq.Z(qubits[edge[0]]) * cirq.Z(qubits[edge[1]])
    )


def solve_classically(self):
    """Solve the combinatorial problem using a full, exponentially sized search
    :return: Value of the max the cut
    """
    subsets_list = itertools.chain.from_iterable(
        itertools.combinations(self.graph.nodes(), r)
        for r in range(self.graph.number_of_nodes() + 1)
    )
    max_cut = [
        nx.algorithms.cuts.cut_size(self.graph, assignment)
        for assignment in subsets_list
    ]
    return np.max(max_cut)
