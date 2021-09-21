import cirq
import numpy as np
import tqdm.auto as tqdm

import tensorflow as tf
import tensorflow_quantum as tfq

from qleet.utils.circuit import CircuitDescriptor


class PQCSimulatedTrainer:
    def __init__(self, circuit: CircuitDescriptor):
        self.optimizer = tf.keras.optimizers.Adam(lr=0.01)
        self.model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Input(shape=(), dtype=tf.dtypes.string),
                tfq.layers.PQC(
                    circuit.cirq_circuit,
                    circuit.cost_function,
                    differentiator=tfq.differentiators.Adjoint(),
                ),
            ]
        )
        self.circuit = circuit

    def train(self, epochs=100, _loggers=None):
        dummy_input = tfq.convert_to_tensor([cirq.Circuit()])
        with tqdm.trange(epochs) as iterator:
            iterator.set_description("QAOA Optimization Loop")
            for _epoch in iterator:
                with tf.GradientTape() as tape:
                    error = self.model(dummy_input)
                grads = tape.gradient(error, self.model.trainable_variables)
                self.optimizer.apply_gradients(
                    zip(grads, self.model.trainable_variables)
                )
                error = error.numpy()[0][0]
                iterator.set_postfix(error=error)
        return self.model

    def evaluate(self, n_samples: int = 1000):
        trained_parameters = self.model.trainable_variables[0]
        output = tfq.layers.Sample()(
            self.circuit.cirq_circuit,
            symbol_names=self.circuit.parameters,
            symbol_values=[trained_parameters],
            repetitions=n_samples,
        )
        samples = output.numpy()[0]
        loss_values = [self.circuit.cost_function(sample) for sample in samples]
        return np.mean(loss_values)
