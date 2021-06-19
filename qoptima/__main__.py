import numpy as np
import plotly.graph_objects as pg

import itertools
import tqdm

from .qaoa.maxcut import QAOACircuitMaxCut

if __name__ == '__main__':
    x = QAOACircuitMaxCut(QAOACircuitMaxCut.generate_random_graph(8), 1)
    grid_size = 25  # Set the grid size = number of points in the interval [0, 2π).
    exp_values = np.empty((grid_size, grid_size))
    par_values_beta = np.empty((grid_size, grid_size))
    par_values_gamma = np.empty((grid_size, grid_size))
    for (i, gamma_value), (j, beta_value) in tqdm.tqdm(
            itertools.product(
                enumerate(np.linspace(0, 2 * np.pi, grid_size)),
                enumerate(np.linspace(0, 2 * np.pi, grid_size))),
            total=grid_size*grid_size):
        exp_values[i][j] = x({x.params[0]: gamma_value, x.params[1]: beta_value})
        par_values_gamma[i][j] = gamma_value
        par_values_beta[i][j] = beta_value

    fig = pg.Figure(data=[pg.Surface(x=par_values_gamma, y=par_values_beta, z=exp_values)])
    fig.update_layout(title='Potential Energy Surface',
                      scene=dict(
                          xaxis=dict(title='Gamma (Hamiltonian Parameter)'),
                          yaxis=dict(title='Beta (Mixer Parameter)'),
                          zaxis=dict(title='Cost Function'),
                      ),
                      autosize=False,
                      width=1200, height=800,
                      margin=dict(l=65, r=50, b=65, t=90))
    fig.show()
