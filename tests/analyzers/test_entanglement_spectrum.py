import pytest
import numpy as np

import cirq
import qiskit

import matplotlib.pyplot as plt

from qiskit.providers.aer.noise import NoiseModel as qiskitNoiseModel
from cirq.devices.noise_model import NoiseModel as cirqNoiseModel

import qleet


@pytest.mark.parametrize(
    "params",
    [[], [qiskit.circuit.Parameter(r"$θ_1$"), qiskit.circuit.Parameter(r"$θ_2$")]],
)
@pytest.mark.parametrize("tapered_indices", [[0], [1]])
@pytest.mark.parametrize("noise_model", [None, qiskitNoiseModel()])
@pytest.mark.parametrize("metric", ["kld", "jsd"])
@pytest.mark.parametrize("samples", [50, 100])
def test_entanglement_spectrum(params, tapered_indices, noise_model, metric, samples):
    """Test entanglement spectrum of a quantum circuit"""
    qiskit_circuit = qiskit.QuantumCircuit(2)
    if not params:
        qiskit_circuit.h(0)
    else:
        qiskit_circuit.rx(params[0], 0)
        qiskit_circuit.rz(params[1], 0)
    qiskit_circuit.cx(0, 1)
    qiskit_descriptor = qleet.CircuitDescriptor(
        circuit=qiskit_circuit, params=params, cost_function=None
    )
    qiskit_entanglement_spectrum = (
        qleet.analyzers.entanglement_spectrum.EntanglementSpectrum(
            qiskit_descriptor,
            noise_model=noise_model,
            samples=samples,
            tapered_indices=tapered_indices,
        )
    )
    pqc_esd, mean_eigvals = qiskit_entanglement_spectrum.entanglement_spectrum(metric)
    assert pqc_esd > 0

    if metric == "jsd":
        assert pqc_esd < 1
        if not params:
            print(pqc_esd)
            assert np.isclose(pqc_esd, 1, rtol=0.01, atol=0.01)

    assert qiskit_entanglement_spectrum.plot(np.array([mean_eigvals]))
    plt.close("all")


@pytest.mark.parametrize(
    ("tapered_indices", "noise_model", "metric", "msg_match"),
    [
        (
            [],
            cirqNoiseModel.from_noise_model_like(cirq.depolarize(p=0.0)),
            "kld",
            "Circuit and noise model must correspond to the same",
        ),
        (
            [],
            qiskitNoiseModel(),
            "abc",
            "Invalid measure provided",
        ),
        (
            [1, 2],
            qiskitNoiseModel(),
            "jsd",
            "The provided tapered_indices must exactly have half",
        ),
    ],
)
def test_exceptions_entanglement_spectrum(
    tapered_indices, noise_model, metric, msg_match
):
    """Test exceptions while evaluating entanglement spectrum of a quantum circuit"""

    qiskit_circuit = qiskit.QuantumCircuit(2)
    qiskit_circuit.h(0)
    qiskit_circuit.cx(0, 1)

    qiskit_descriptor = qleet.CircuitDescriptor(
        circuit=qiskit_circuit, params=[], cost_function=None
    )

    with pytest.raises(ValueError, match=msg_match):
        qiskit_entanglement_spectrum = (
            qleet.analyzers.entanglement_spectrum.EntanglementSpectrum(
                qiskit_descriptor,
                noise_model=noise_model,
                samples=100,
                tapered_indices=tapered_indices,
            )
        )
        qiskit_entanglement_spectrum.entanglement_spectrum(metric)
