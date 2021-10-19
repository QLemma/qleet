import qleet

import networkx as nx
from matplotlib import pyplot as plt
import pytest


@pytest.mark.parametrize("ensemble_size", [3, 5])
def test_plot_histogram(ensemble_size):
    graph = nx.gnm_random_graph(n=10, m=40)
    qaoa = qleet.examples.qaoa_maxcut.QAOACircuitMaxCut(graph, p=2)
    circuit = qleet.interface.circuit.CircuitDescriptor(
        qaoa.qaoa_circuit, qaoa.params, qaoa.qaoa_cost
    )
    plot = qleet.analyzers.histogram.ParameterHistograms(
        circuit, ensemble_size=ensemble_size, epochs_chart=(0, 1, 5, 10)
    )
    ax = plot.plot()
    assert ax is not None
