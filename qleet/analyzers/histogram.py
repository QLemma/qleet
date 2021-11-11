import typing

import sympy
from matplotlib import pyplot as plt
import seaborn as sns

from ..interface.metas import MetaExplorer
from ..interface.circuit import CircuitDescriptor
from ..simulators.pqc_trainer import PQCSimulatedTrainer


class ParameterHistograms(MetaExplorer):
    """Class to plot the histograms of parameters in the circuit."""

    def __init__(
        self,
        circuit: CircuitDescriptor,
        ensemble_size: int = 3,
        groups: typing.Optional[typing.Dict[str, typing.List[sympy.Symbol]]] = None,
        epochs_chart=(0, 10, 10),
    ) -> None:
        """Creates an explorer object which will plot the histogram.
        :param circuit: The Parametrized Quantum circuit
        :param groups: Groups of variables which can be analyzed together.
        """
        super().__init__()
        self.circuit = circuit
        # Generate an ensemble or runs
        self.ensemble_size = ensemble_size
        self.models = [
            PQCSimulatedTrainer(self.circuit) for _ in range(self.ensemble_size)
        ]
        self.epochs_chart = epochs_chart
        # Prepare the groups of variables which will be analyzed together
        if groups is not None:
            self.groups = groups
        else:
            self.groups = dict()
            for param in circuit.parameters:
                self.groups[param.name] = [param]
        # Prepare the array to store histograms resulting from simulation
        self._histograms: typing.Dict[str, typing.List[typing.List]] = {
            group: [[] for _ in self.epochs_chart] for group in self.groups.keys()
        }

    def simulate(self) -> None:
        """Simulates the circuit and generate the histogram data."""
        for epochs_idx, epochs_to_train in enumerate(self.epochs_chart):
            for model in self.models:
                model.train(n_samples=epochs_to_train)
            for group_name, group_symbols in self.groups.items():
                for model in self.models:
                    for variable in group_symbols:
                        self._histograms[group_name][epochs_idx].append(
                            self._get_symbol_value_from_model(model, variable)
                        )

    @staticmethod
    def _get_symbol_value_from_model(model: PQCSimulatedTrainer, symbol: sympy.Symbol):
        """Get the current value of the symbol in the PQC Trainer
        :param model: The model we want to find the symbol values from
        :param symbol: The sympy symbol we want to find the value of
        :return: The current value of the symbol, as a float
        """
        return model.pqc_layer.symbol_values()[symbol]

    def plot(self) -> plt.Axes:
        """Plot the parameter histogram for this circuit.
        :return: The axes with the completed plots
        """
        self.simulate()
        _fig, ax = plt.subplots(
            len(self.epochs_chart),
            len(self.groups),
            figsize=(len(self.groups) * 5, len(self.epochs_chart) * 5),
        )
        for group_idx, group_name in enumerate(self.groups.keys()):
            for epoch_idx in range(len(self.epochs_chart)):
                sns.kdeplot(
                    self._histograms[group_name][epoch_idx],
                    ax=ax[epoch_idx, group_idx],
                )
                ax[epoch_idx, group_idx].set_title(f"{group_name} @ epoch:{epoch_idx}")
                ax[epoch_idx, group_idx].set_xlabel(f"Parameter Values")
        return ax
