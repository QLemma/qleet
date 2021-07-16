from typing_extensions import final
import numpy as np
import tqdm.auto as tqdm
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

import plotly.express as px

from ..circuits.maxcut import QAOAMaxCutSolver


class OptimizationPathPlotter:

    def __init__(self, mode="tSNE"):
        assert mode in ["tSNE", "PCA"], "Mode of Dimentionality Reduction is not implemented, use PCA or tSNE."
        self.trial, self.counter = 0, 0
        self.data = []
        self.runs = []
        self.item = []
        self.dimentionality_reduction = TSNE if mode == "tSNE" else PCA

    def log(self, solver: QAOAMaxCutSolver, loss):
        self.data.append(solver.model.trainable_variables[0].numpy())
        self.runs.append(self.trial)
        self.item.append(self.counter)
        self.counter += 1

    def plot(self):
        raw_params = np.stack(self.data)
        final_params = self.dimentionality_reduction(n_components=2).fit_transform(raw_params)
        max_number_of_runs = max(self.item)
        size_values = [5 if size > max_number_of_runs - 5 else 1 for size in self.item]
        fig = px.scatter(x=final_params[:, 0], y=final_params[:, 1], color=self.runs, size=size_values)
        fig.show()

    def next(self):
        self.trial += 1
        self.counter = 0
