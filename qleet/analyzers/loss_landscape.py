import numpy as np
import tqdm.auto as tqdm
import plotly.graph_objects as pg

from ..simulators.pqc_trainer import PQCSimulatedTrainer
from ..interface.metric_spec import MetricSpecifier


class LossLandscapePlotter:

    def __init__(self, solver: PQCSimulatedTrainer, metric: MetricSpecifier, dim=2):
        self.n = len(solver.circuit.parameters)
        self.metric = metric
        self.solver = solver
        self.dim = dim
        self.axes = self.__random_subspace(dim=self.dim)

    def __random_subspace(self, dim):
        axes = []
        for _i in range(dim):
            axis = np.random.random(self.n)
            for other_axis in axes:
                projection = np.dot(axis, other_axis)
                axis = axis - projection * other_axis
            axis = axis / np.sum(axis)
            axes.append(axis)
        return np.stack(axes, axis=0)

    def scan(self, points, distance, origin):
        chained_range = [
            np.linspace(-distance, distance, points) for _i in range(self.dim)
        ]
        coords = np.meshgrid(*chained_range)
        coords = np.reshape(np.stack(coords, axis=-1), (-1, self.dim))
        values = np.zeros(len(coords), dtype=np.float)
        with tqdm.trange(len(coords)) as iterator:
            iterator.set_description("Contour Plot Scan")
            for i in iterator:
                # TODO: Incorporate state vector and density matrix modes for higher speed
                values[i] = self.metric.from_circuit(circuit_descriptor=self.solver.circuit,
                                                     parameters=coords[i] @ self.axes + origin,
                                                     mode='samples')
        return values, coords

    def plot(self, mode="surface", points=25, distance=np.pi):
        assert mode in ["line", "contour", "surface"]
        if mode == "contour":
            assert (
                self.dim == 2
            ), "Contour plots can only be drawn with 2-dimensional axes"
            origin = self.solver.model.trainable_variables[0]
            data, _coords = self.scan(points, distance, origin)
            data = np.reshape(data, (points, points))
            scan_range = np.linspace(-distance, +distance, points)
            fig = pg.Figure(data=pg.Contour(z=data, x=scan_range, y=scan_range))
            return fig
        elif mode == "surface":
            assert (
                self.dim == 2
            ), "Contour plots can only be drawn with 2-dimensional axes"
            origin = self.solver.model.trainable_variables[0]
            data, _coords = self.scan(points, distance, origin)
            data = np.reshape(data, (points, points))
            scan_range = np.linspace(-distance, +distance, points)
            fig = pg.Figure(data=pg.Surface(z=data, x=scan_range, y=scan_range))
            return fig
        else:
            raise NotImplementedError("This plotting mode has not been implemented yet")
