import networkx as nx

from .circuits.maxcut import QAOAMaxCutSolver, train
from .plotter.landscape import LossLandscapePlotter
from .plotter.training import OptimizationPathPlotter

if __name__ == '__main__':
    tracker = OptimizationPathPlotter(mode="tSNE")
    graph = nx.random_regular_graph(n=6, d=3)
    for i in range(5):
        qaoa = QAOAMaxCutSolver(graph, p=4)
        train(qaoa, epochs=1000, logger=tracker)
        tracker.next()
    tracker.plot()

    qaoa = QAOAMaxCutSolver(graph, p=4)
    train(qaoa, epochs=5000, logger=tracker)
    plot = LossLandscapePlotter(qaoa, dim=2)
    plot.plot('surface')
