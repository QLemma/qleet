import qleet


def test_trainer():
    qaoa_maxcut = qleet.circuits.qaoa_maxcut.QAOACircuitMaxCut()
    circuit_descriptor = qleet.utils.circuit.CircuitDescriptor(
        circuit=qaoa_maxcut.qaoa_circuit,
        params=qaoa_maxcut.params,
        cost_function=qaoa_maxcut.qaoa_cost,
    )
    pqc_trainer = qleet.simulators.pqc_trainer.PQCSimulatedTrainer(
        circuit=circuit_descriptor
    )
    pqc_trainer.train()
