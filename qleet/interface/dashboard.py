import networkx as nx

import dash
import dash_core_components as dash_core
import dash_html_components as dash_html

from qleet.interface.metas import AnalyzerList
from qleet.analyzers.loss_landscape import LossLandscapePlotter
from qleet.analyzers.training_path import OptimizationPathPlotter
from qleet.analyzers.training_path import LossLandscapePathPlotter


def launch_dashboard(trainer, plottable_metric):
    plot = LossLandscapePlotter(trainer, plottable_metric, dim=2)
    trainer.train(n_samples=50)
    fig_loss_surface = plot.plot("surface", points=5)

    trackers = AnalyzerList(
        LossLandscapePathPlotter(plot),
        OptimizationPathPlotter(mode="tSNE"),
    )
    for _i in range(5):
        trainer.train(loggers=trackers)
        trackers.next()

    # Make the app to plot all of this

    external_stylesheets = [
        "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
        "./app.css",
    ]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    fig_loss_traversal = trackers[0].plot()
    fig_training_trace = trackers[1].plot()

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
            dash_html.H1(children="Variational Quantum Circuit Analyzer"),
            dash_html.H3(children="Visualizing QAOA Landscapes and Plotting Paths."),
            dash_html.H2(children="tSNE of Optimization Path"),
            dash_core.Graph(id="training-path", figure=fig_training_trace),
            dash_html.H2(children="Loss Landscape along random 2-D subspace"),
            dash_core.Graph(
                id="loss-landscape",
                figure=fig_loss_surface,
            ),
            dash_html.H2(children="Traversal on the Loss Landscape above"),
            dash_core.Graph(
                id="loss-traversal",
                figure=fig_loss_traversal,
            ),
        ],
    )
    app.run_server(debug=False)


if __name__ == "__main__":
    from qleet.interface.circuit import CircuitDescriptor
    from qleet.simulators.pqc_trainer import PQCSimulatedTrainer
    from qleet.examples.qaoa_maxcut import QAOACircuitMaxCut, MaxCutMetric

    graph = nx.gnm_random_graph(n=10, m=40)
    qaoa = QAOACircuitMaxCut(graph, p=1)
    circuit = CircuitDescriptor(qaoa.qaoa_circuit, qaoa.params, qaoa.qaoa_cost)
    solver = PQCSimulatedTrainer(circuit)
    metric = MaxCutMetric(graph)
    launch_dashboard(solver, metric)
