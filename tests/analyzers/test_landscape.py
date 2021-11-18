import numpy as np
import networkx as nx
import plotly.graph_objects as pg

import pytest

import qleet


graph = nx.gnm_random_graph(n=4, m=10)
qaoa = qleet.QAOACircuitMaxCut(graph, p=1)
circuit = qleet.CircuitDescriptor(qaoa.qaoa_circuit, qaoa.params, qaoa.qaoa_cost)
trainer = qleet.PQCSimulatedTrainer(circuit)
metric = qleet.MaxCutMetric(graph)
trainer.train(n_samples=50)
plot = qleet.LossLandscapePlotter(trainer, metric, dim=2)


def test_landscape_plotting_surface():
    fig = plot.plot()
    assert isinstance(
        fig, pg.Figure
    ), "The default landscape plot should be a plotly figure."


def test_landscape_scan():
    values, coords = plot.scan(
        points=5, distance=np.pi / 4, origin=trainer.model.trainable_variables[0]
    )
    assert values.shape == (25,)
    assert coords.shape == (25, 2)
    assert np.sum(values[25 // 2] > values) >= 25 // 2, (
        "More than half the values in the grid search are better than the trained optimal, "
        "something is wrong with the trainer or the grid search in the plotter."
    )
    assert np.sum(values[25 // 2] * 2.0 > values) >= 25, (
        "Double of optimal in grid search is worse then gradient search, something went wrong "
        "in training or grid search during plotting."
    )


def test_random_subspace():
    assert plot.axes.shape == (
        2,
        len(circuit.parameters),
    ), "The random subspace is of the wrong shape."
    for i in range(2):
        for j in range(i):
            assert np.isclose(
                np.dot(plot.axes[i], plot.axes[j]), 0
            ), "The basis vectors are not orthogonal"
    for i in range(2):
        assert np.isclose(
            np.linalg.norm(plot.axes[i]), 1
        ), "The basis vectors are not normalized"


def test_landscape_plotting_contour():
    fig = plot.plot(mode="contour")
    assert isinstance(fig, pg.Figure), "The contour plot should be a plotly figure."


def test_landscape_plotting_contour():
    with pytest.raises(
        NotImplementedError, match="This plotting mode has not been implemented yet"
    ):
        fig = plot.plot(mode="line")
