import pytest
import numpy as np
from qleet.pqc_property.entanglement_capability import EntanglementCapability
from qiskit import QuantumCircuit

class TestEntanglementCapability:
    """ Test entanglement capability functionality """

    def temp1(params, cparams=None):
        layers, num_qubits, depth = params.shape
        ansatz = QuantumCircuit(num_qubits)
        for idx in range(layers):
            if idx:
                ansatz.barrier()
            for ind in range(num_qubits):
                ansatz.rx(params[idx][ind][0], ind)
                ansatz.rz(params[idx][ind][1], ind)
        return ansatz

    def temp2(params, cparams=None):
        layers, num_qubits, depth = params.shape
        ansatz = QuantumCircuit(num_qubits)
        for idx in range(layers):
            if idx:
                ansatz.barrier()
            for ind in range(num_qubits):
                ansatz.rx(params[idx][ind][0], ind)
                ansatz.rz(params[idx][ind][1], ind)
            indexes = [[i, i-1] for i in reversed(range(1, num_qubits))]
            for ind in indexes:
                ansatz.cx(ind[0], ind[1])

        return ansatz

    @pytest.mark.parametrize("circuit", [temp1, temp2])
    def test_entanglement_circuits(self, circuit):
        """ Tests that the entanglement measures give correct output """
        ent_circ = EntanglementCapability(circuit, [(1, 4, 2)])
        res1, res2 = 0., 0.
        for measure in ["meyer-wallach", "scott"]:
            ent_res = ent_circ.entanglement_capability(measure)
            if not isinstance(ent_res, np.ndarray):
                res1 = ent_res
            else:
                res2 = ent_res[0]

        assert np.isclose(res1, res2, atol=0.3, rtol=0.3)

    @pytest.mark.parametrize("circuit", [temp1])
    @pytest.mark.parametrize("measure", ["meyer-wallach", "scott"])
    def test_entanglement_measures(self, circuit, measure):
        """ Tests that the entanglement measures give correct output """
        ent_circ = EntanglementCapability(circuit, [(1, 4, 2)])
        ent_res = ent_circ.entanglement_capability(measure)
        if not isinstance(ent_res, np.ndarray):
            res1 = ent_res
        else:
            res1 = ent_res[0]

        assert np.isclose(res1, 0.0, atol=0.3, rtol=0.3)
