import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

import pytest

import qleet


@pytest.mark.parametrize("ensemble_size", [3, 5])
def test_plot_histogram(ensemble_size):
    graph = nx.gnm_random_graph(n=10, m=40)
    qaoa = qleet.QAOACircuitMaxCut(graph, p=2)
    circuit = qleet.CircuitDescriptor(qaoa.qaoa_circuit, qaoa.params, qaoa.qaoa_cost)
    epochs_chart = (0, 1, 5, 10)
    plot = qleet.ParameterHistograms(
        circuit, ensemble_size=2, epochs_chart=epochs_chart
    )
    ax = plot.plot()
    assert isinstance(ax, np.ndarray), "Array of plots wasn't returned by the plotter."
    assert ax.shape == (
        len(circuit.parameters),
        len(epochs_chart),
    ), "The shape of the plot returned is not correct."
    for subplot in np.reshape(ax, -1):
        assert isinstance(
            subplot, plt.Axes
        ), "Matplotlib figure axes were not returned by the plotter."
    for _group, data in plot._histograms.items():
        data = np.array(data)
        assert not np.any(
            np.isclose(np.var(data, axis=0), 0)
        ), "The parameters stayed the same after training, check logging."
