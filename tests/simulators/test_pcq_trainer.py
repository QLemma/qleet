import qleet


def test_trainer():
    qaoa_maxcut = qleet.examples.qaoa_maxcut.QAOACircuitMaxCut()
    circuit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qaoa_maxcut.qaoa_circuit,
        params=qaoa_maxcut.params,
        cost_function=qaoa_maxcut.qaoa_cost,
    )
    pqc_trainer = qleet.simulators.pqc_trainer.PQCSimulatedTrainer(
        circuit=circuit_descriptor
    )
    pqc_trainer.train()


def test_evaluation():
    qaoa_maxcut = qleet.examples.qaoa_maxcut.QAOACircuitMaxCut()
    circuit_descriptor = qleet.interface.circuit.CircuitDescriptor(
        circuit=qaoa_maxcut.qaoa_circuit,
        params=qaoa_maxcut.params,
        cost_function=qaoa_maxcut.qaoa_cost,
    )
    pqc_trainer = qleet.simulators.pqc_trainer.PQCSimulatedTrainer(
        circuit=circuit_descriptor
    )
    logger = qleet.interface.metas.AnalyzerList(
        qleet.analyzers.training_path.OptimizationPathPlotter()
    )
    loss_1 = pqc_trainer.evaluate(1000)
    pqc_trainer.train(10000, loggers=logger)
    loss_2 = pqc_trainer.evaluate(1000)
    assert loss_1 >= loss_2, "Training worsened the output accuracy."
