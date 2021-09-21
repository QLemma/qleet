import qleet


def test_trainer():
    circuit_descriptor = qleet.utils.circuit.CircuitDescriptor(
        circuit=qleet.circuits.qaoa_maxcut.qaoa_circuit,
        params=qleet.circuits.qaoa_maxcut.params,
        cost_function=qleet.circuits.qaoa_maxcut.qaoa_cost,
    )
    pqc_trainer = qleet.simulators.pqc_trainer.PQCSimulatedTrainer(
        circuit=circuit_descriptor
    )
    pqc_trainer.train()
