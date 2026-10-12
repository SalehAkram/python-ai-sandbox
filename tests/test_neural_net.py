import tempfile
import unittest
from pathlib import Path
import numpy as np
from shared.neural_networks.neural_net import NeuralNetwork


class NeuralNetworkTests(unittest.TestCase):
    def test_output_shape(self):
        network = NeuralNetwork(8, 16, 4, np.random.default_rng(1))
        self.assertEqual(network.feedforward(np.zeros(8)).shape, (4, 1))

    def test_save_load_round_trip(self):
        network = NeuralNetwork(8, 16, 4, np.random.default_rng(1))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brain.npz"
            network.save(path)
            loaded = NeuralNetwork.load(path)
        np.testing.assert_allclose(network.feedforward(np.arange(8)),
                                   loaded.feedforward(np.arange(8)))

    def test_mutation_changes_parameters(self):
        network = NeuralNetwork(8, 16, 4, np.random.default_rng(1))
        before = network.wih.copy()
        network.mutate(1.0, 0.2, np.random.default_rng(2))
        self.assertFalse(np.array_equal(before, network.wih))


if __name__ == "__main__": unittest.main()
