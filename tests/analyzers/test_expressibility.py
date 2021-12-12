import pytest
import numpy as np

import cirq
import qiskit

from qiskit.providers.aer.noise import NoiseModel as qiskitNoiseModel
from cirq.devices.noise_model import NoiseModel as cirqNoiseModel

import qleet


@pytest.mark.parametrize(
    "params",
    [[], [qiskit.circuit.Parameter(r"$θ_1$"), qiskit.circuit.Parameter(r"$θ_2$")]],
)
@pytest.mark.parametrize("noise_model", [None, qiskitNoiseModel()])
@pytest.mark.parametrize("metric", ["kld", "jsd"])
@pytest.mark.parametrize("samples", [50, 100])
def test_expressibility(params, noise_model, metric, samples):
    """Test expressibility of a quantum circuit"""
    qiskit_circuit = qiskit.QuantumCircuit(2)
    if not params:
        qiskit_circuit.h(0)
    else:
        qiskit_circuit.rx(params[0], 0)
        qiskit_circuit.rz(params[1], 0)
    qiskit_circuit.cx(0, 1)
    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=params, cost_function=None
    )
    qiskit_expressibility = qleet.analyzers.expressibility.Expressibility(
        qiskit_descriptor, noise_model=noise_model, samples=samples
    )
    expr = qiskit_expressibility.expressibility(metric)
    assert expr > 0

    if metric == "jsd":
        assert expr < 1
        if not params:
            assert np.isclose(expr, 1)

    assert qiskit_expressibility.plot()


@pytest.mark.parametrize(
    ("noise_model", "metric", "plot", "msg_match"),
    [
        (
            cirqNoiseModel.from_noise_model_like(cirq.depolarize(p=0.0)),
            "kld",
            False,
            "Circuit and noise model must correspond to the same",
        ),
        (
            qiskitNoiseModel(),
            "abc",
            False,
            "Invalid measure provided",
        ),
        (
            qiskitNoiseModel(),
            "jsd",
            True,
            "Perform expressibility calculation first",
        ),
    ],
)
def test_exceptions_expressibility(noise_model, metric, plot, msg_match):
    """Test exceptions while evaluating expressibility of a quantum circuit"""

    qiskit_circuit = qiskit.QuantumCircuit(2)
    qiskit_circuit.h(0)
    qiskit_circuit.cx(0, 1)

    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=[], cost_function=None
    )

    with pytest.raises(ValueError, match=msg_match):
        qiskit_expressibility = qleet.analyzers.expressibility.Expressibility(
            qiskit_descriptor, noise_model=noise_model, samples=100
        )
        if plot:
            qiskit_expressibility.plot()
        qiskit_expressibility.expressibility(metric)
