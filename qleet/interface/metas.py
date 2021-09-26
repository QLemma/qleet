import typing
from abc import abstractmethod, ABC

if typing.TYPE_CHECKING:
    from ..simulators.pqc_trainer import PQCSimulatedTrainer


class MetaLogger(ABC):
    def __init__(self):
        self.trial, self.counter = 0, 0
        self.data = []
        self.runs = []
        self.item = []

    @abstractmethod
    def log(self, solver, loss):
        raise NotImplementedError

    @abstractmethod
    def plot(self):
        raise NotImplementedError

    def next(self):
        self.trial += 1
        self.counter = 0


class MetaExplorer(ABC):
    def __init__(self):
        pass


class AnalyzerList:
    def __init__(self, *args: typing.Union[MetaLogger, MetaExplorer]):
        self._analyzers: typing.Tuple[
            typing.Union[MetaLogger, MetaExplorer]
        ] = typing.cast(typing.Tuple[typing.Union[MetaLogger, MetaExplorer]], args)

    def __str__(self) -> str:
        return "\n".join(str(self._analyzers))

    def log(self, solver: "PQCSimulatedTrainer", loss: float) -> None:
        for analyzer in self._analyzers:
            if isinstance(analyzer, MetaLogger):
                analyzer.log(solver, loss)

    def next(self) -> None:
        for analyzer in self._analyzers:
            if isinstance(analyzer, MetaLogger):
                analyzer.next()

    def __getitem__(self, item: int) -> typing.Union[MetaLogger, MetaExplorer]:
        return self._analyzers[item]

    def __iter__(self) -> typing.Iterable[typing.Union[MetaLogger, MetaExplorer]]:
        return self._analyzers
