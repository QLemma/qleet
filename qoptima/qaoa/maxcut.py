import numpy as np
import networkx as nx
import sympy

from matplotlib import pyplot as plt

import cirq, cirq.contrib.svg


class QAOACircuitMaxCut:

    def __init__(self, graph, p):
        self.graph = graph
        self.p = p
        self.qubits, self.circuit, self.params = self.make_circuit()
        self.sim = cirq.Simulator()

    def draw_graph(self, assignment=None):
        nx.draw_circular(
            self.graph,
            node_color=None if assignment is None else ["Red" if node else "Blue" for node in assignment],
            node_size=1000,
            with_labels=True,
            width=[w['weight'] for (u, v, w) in self.graph.edges(data=True)])
        plt.show()

    def draw_circuit(self):
        print(self.circuit)

    @staticmethod
    def generate_random_graph(num_nodes):
        working_graph = nx.Graph()
        for qubit in range(num_nodes):
            working_graph.add_node(qubit)
        for qubit in range(num_nodes):
            for neighbor in range(num_nodes):
                if qubit != neighbor:
                    working_graph.add_edge(qubit, neighbor, weight=np.random.randint(0, 500) / 100)
        return working_graph

    def make_circuit(self):
        qaoa_qubits = cirq.GridQubit.rect(1, self.graph.number_of_nodes())
        qaoa_circuit = cirq.Circuit()

        # Create Mixer ground state
        qaoa_circuit.append([cirq.H.on_each(qaoa_qubits)], strategy=cirq.InsertStrategy.EARLIEST)

        qaoa_parameters = []
        for step in range(1, self.p + 1):
            gamma_i = sympy.Symbol("gamma{}_p={}".format(step, self.p))
            beta_i = sympy.Symbol("beta{}_p={}".format(step, self.p))
            qaoa_parameters.append(gamma_i)
            qaoa_parameters.append(beta_i)
            # Apply Ising hamiltonian
            for u, v, w in self.graph.edges(data=True):
                qaoa_circuit.append(cirq.ZZ(qaoa_qubits[u], qaoa_qubits[v]) ** (gamma_i * w['weight']),
                                    strategy=cirq.InsertStrategy.EARLIEST)
            # Apply Driver Hamiltonian
            qaoa_circuit.append(cirq.Moment(cirq.rx(beta_i)(u) for u in qaoa_qubits))

        # Measure all the qubits in the end
        for qubit in qaoa_qubits:
            qaoa_circuit.append(cirq.measure(qubit), strategy=cirq.InsertStrategy.EARLIEST)

        return qaoa_qubits, qaoa_circuit, qaoa_parameters

    def compute_cost(self, sample):
        """Estimate the cost function of the QAOA on the given graph using the
        provided computational basis bit-strings."""
        cost_value = 0.0

        # Loop over edge pairs and compute contribution.
        for u, v, w in self.graph.edges(data=True):
            u_sample = sample[str(self.qubits[u])]
            v_sample = sample[str(self.qubits[v])]

            # Determine if it was a +1 or -1 eigenvalue.
            u_signs = (-1)**u_sample
            v_signs = (-1)**v_sample
            term_signs = u_signs * v_signs

            # Add scaled term to total cost.
            term_val = np.mean(term_signs) * w['weight']
            cost_value += term_val

        return -cost_value

    def run_circuit(self, params):
        samples = self.sim.sample(
            self.circuit,
            params=params,
            repetitions=20000
        )
        return samples

    def __call__(self, params):
        return self.compute_cost(self.run_circuit(params))
