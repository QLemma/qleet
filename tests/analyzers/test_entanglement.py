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
@pytest.mark.parametrize("metric", ["meyer-wallach", "scott"])
@pytest.mark.parametrize("samples", [50, 100])
def test_entanglement(params, noise_model, metric, samples):
    """Test entangling power of a quantum circuit"""
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
    qiskit_entanglement_capability = (
        qleet.analyzers.entanglement.EntanglementCapability(
            qiskit_descriptor, noise_model=noise_model, samples=samples
        )
    )
    entanglement = qiskit_entanglement_capability.entanglement_capability(metric)
    if not isinstance(entanglement, list):
        entanglement = [entanglement]
    for entmeas in entanglement:
        assert 0 <= entmeas <= 1


@pytest.mark.parametrize(
    ("noise_model", "metric", "msg_match"),
    [
        (
            cirqNoiseModel.from_noise_model_like(cirq.depolarize(p=0.0)),
            "meyer-wallach",
            "Circuit and noise model must correspond to the same",
        ),
        (
            qiskitNoiseModel(),
            "abc",
            "Invalid measure provided",
        ),
    ],
)
def test_exception_entanglement(noise_model, metric, msg_match):
    """Test exceptions while evaluating entangling power of a quantum circuit"""

    qiskit_circuit = qiskit.QuantumCircuit(2)
    qiskit_circuit.h(0)
    qiskit_circuit.cx(0, 1)

    qiskit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qiskit_circuit, params=[], cost_function=None
    )

    with pytest.raises(ValueError, match=msg_match):

        qiskit_entanglement_capability = (
            qleet.analyzers.entanglement.EntanglementCapability(
                qiskit_descriptor, noise_model=noise_model, samples=100
            )
        )
        qiskit_entanglement_capability.entanglement_capability(metric)
