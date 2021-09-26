import typing

import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as pg

from .loss_landscape import LossLandscapePlotter
from ..interface.metas import MetaLogger


class OptimizationPathPlotter(MetaLogger):
    def __init__(self, mode="tSNE"):
        super().__init__()
        assert mode in [
            "tSNE",
            "PCA",
        ], "Mode of Dimensionality Reduction is not implemented, use PCA or tSNE."
        self.dimensionality_reduction = TSNE if mode == "tSNE" else PCA

    def log(self, solver, _loss):
        self.data.append(solver.model.trainable_variables[0].numpy())
        self.runs.append(self.trial)
        self.item.append(self.counter)
        self.counter += 1

    def plot(self):
        raw_params = np.stack(self.data)
        final_params = self.dimensionality_reduction(n_components=2).fit_transform(
            raw_params
        )
        max_number_of_runs = max(self.item)
        size_values = [5 if size > max_number_of_runs - 5 else 1 for size in self.item]
        fig = px.scatter(
            x=final_params[:, 0],
            y=final_params[:, 1],
            color=self.runs,
            size=size_values,
        )
        return fig


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
