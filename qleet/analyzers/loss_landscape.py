import typing
import numpy as np
import tqdm.auto as tqdm
import plotly.graph_objects as pg

from ..interface.metas import MetaLogger


class LossLandscapePlotter:
    def __init__(self, solver, dim=2):
        self.n = len(solver)
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
                values[i] = self.solver.compute_cost(coords[i] @ self.axes + origin)
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


class LossLandscapePathPlotter(MetaLogger):
    def __init__(self, base_plotter: LossLandscapePlotter):
        super().__init__()
        self.loss: typing.List[float] = []
        self.plotter = base_plotter

    def log(self, solver, loss: float):
        self.data.append(
            self.plotter.axes @ solver.model.trainable_variables[0].numpy()
        )
        self.loss.append(loss)
        self.runs.append(self.trial)
        self.item.append(self.counter)
        self.counter += 1

    def plot(self):
        data = np.array(self.data)
        loss = np.array(self.loss)
        max_number_of_runs = max(self.item)
        size_values = np.array(
            [12 if size > max_number_of_runs - 5 else 5 for size in self.item]
        )
        fig = pg.Figure(
            data=[
                pg.Scatter3d(
                    x=data[:, 0],
                    y=data[:, 1],
                    z=-loss,
                    mode="markers",
                    marker=dict(color=self.runs, size=size_values),
                )
            ]
        )
        return fig
