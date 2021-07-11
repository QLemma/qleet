import networkx as nx

from .circuits.maxcut import QAOAMaxCutSolver, train
from .plotter.landscape import LossLandscapePlotter

if __name__ == '__main__':
    qaoa = QAOAMaxCutSolver(nx.random_regular_graph(n=6, d=3), p=8)
    train(qaoa, epochs=5000)
    plot = LossLandscapePlotter(qaoa, dim=2)
    plot.plot('surface')

    qaoa = QAOAMaxCutSolver(nx.random_regular_graph(n=6, d=3), p=2)
    train(qaoa, epochs=5000)
    plot = LossLandscapePlotter(qaoa, dim=2)
    plot.plot('surface')
