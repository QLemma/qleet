import qleet
import networkx as nx
import numpy as np

import pytest


def test_logger():
    with pytest.raises(TypeError):
        logger = qleet.interface.metas.MetaLogger()
        assert logger is not None


def test_analyzer_list():
    graph = nx.gnm_random_graph(n=10, m=40)
    qaoa = qleet.examples.qaoa_maxcut.QAOACircuitMaxCut(graph, p=1)
    circuit = qleet.interface.circuit.CircuitDescriptor(
        qaoa.qaoa_circuit, qaoa.params, qaoa.qaoa_cost
    )
    solver = qleet.simulators.pqc_trainer.PQCSimulatedTrainer(circuit)
    metric = qleet.examples.qaoa_maxcut.MaxCutMetric(graph)

    logger_1 = qleet.analyzers.loss_landscape.LossLandscapePlotter(
        solver, metric, dim=2
    )
    logger_2 = qleet.analyzers.training_path.LossLandscapePathPlotter(logger_1)
    logger_3 = qleet.analyzers.training_path.OptimizationPathPlotter(mode="tSNE")

    trackers = qleet.interface.metas.AnalyzerList(logger_1, logger_2, logger_3)
    for i in range(5):
        trackers.log(solver, np.random.random(3))
        assert len(logger_2.data) == i + 1, "Logger 2 didn't log data"
        assert len(logger_3.data) == i + 1, "Logger 3 didn't log data"
    trackers.next()
    assert logger_2.trial == 1, "Logger 2's trials did not update after calling next"
    assert logger_3.trial == 1, "Logger 3's trials did not update after calling next"
    assert logger_2.counter == 0, "Logger 2's counter did not reset on calling next"
    assert logger_3.counter == 0, "Logger 3's counter did not reset on calling next"

    logger_list = [logger_1, logger_2, logger_3]
    for i, logger in enumerate(trackers):
        assert trackers[i] == logger, "Get item and iterations are not consistent"
        assert (
            logger_list[i] == logger
        ), "Input list and internal list are not consistent"
    assert str(trackers) == "\n".join(
        [str(x) for x in logger_list]
    ), "String representation is not correct"
