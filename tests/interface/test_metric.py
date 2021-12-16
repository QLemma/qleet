import numpy as np
import networkx as nx
import pytest

import qleet


def test_metric():
    graph = nx.gnm_random_graph(n=10, m=40)
    qaoa = qleet.examples.qaoa_maxcut.QAOACircuitMaxCut(graph, p=1)
    circuit = qleet.interface.circuit.CircuitDescriptor(
        qaoa.qaoa_circuit, qaoa.params, qaoa.qaoa_cost
    )
    metric = qleet.examples.qaoa_maxcut.MaxCutMetric(graph)

    with pytest.raises(NotImplementedError):
        metric.from_circuit(
            circuit_descriptor=circuit,
            parameters=np.random.random(size=len(circuit.parameters)),
            mode="state_vector",
        )
    with pytest.raises(NotImplementedError):
        metric.from_circuit(
            circuit_descriptor=circuit,
            parameters=np.random.random(size=len(circuit.parameters)),
            mode="density_matrix",
        )
    with pytest.raises(ValueError):
        metric.from_circuit(
            circuit_descriptor=circuit,
            parameters=np.random.random(size=len(circuit.parameters)),
            mode="something_else",
        )
