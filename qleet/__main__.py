import networkx as nx

import dash
import dash_core_components as dash_core
import dash_html_components as dash_html

from .circuits.maxcut import QAOAMaxCutSolver, train
from .plotter.landscape import LossLandscapePlotter
from .plotter.training import OptimizationPathPlotter, LossLandscapePathPlotter


if __name__ == '__main__':
    graph = nx.gnm_random_graph(n=10, m=40)

    qaoa = QAOAMaxCutSolver(graph, p=1)
    plot = LossLandscapePlotter(qaoa, dim=2)
    train(qaoa, epochs=5000)
    fig_loss_surface = plot.plot('surface', points=25)

    tracker_loss = LossLandscapePathPlotter(plot)
    tracker_path = OptimizationPathPlotter(mode="tSNE")
    for i in range(5):
        qaoa = QAOAMaxCutSolver(graph, p=1)
        train(qaoa, epochs=1000, loggers=[tracker_path, tracker_loss])
        tracker_path.next()
        tracker_loss.next()
    fig_training_trace = tracker_path.plot()
    fig_loss_traversal = tracker_loss.plot()

    # Make the app to plot all of this

    external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css", "./app.css"]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    fig_loss_surface.layout.update(
        height=800,
        width=1200,
    )
    fig_loss_traversal.layout.update(
        height=800,
        width=1200,
    )

    app.layout = dash_html.Div(
        className="container",
        id="mainApp",
        children=[
            dash_html.H1(children='Variational Quantum Circuit Analyzer'),
            dash_html.H3(children='Visualizing QAOA Landscapes and Plotting Paths.'),

            dash_html.H2(children='tSNE of Optimization Path'),
            dash_core.Graph(
                id='training-path',
                figure=fig_training_trace
            ),

            dash_html.H2(children='Loss Landscape along random 2-D subspace'),
            dash_core.Graph(
                id='loss-landscape',
                figure=fig_loss_surface,
            ),

            dash_html.H2(children='Traversal on the Loss Landscape above'),
            dash_core.Graph(
                id='loss-traversal',
                figure=fig_loss_traversal,
            )
        ]
    )
    app.run_server(debug=False)
