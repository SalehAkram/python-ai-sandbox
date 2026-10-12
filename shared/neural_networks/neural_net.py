"""Small fully-connected neural network used as an evolvable controller."""

from __future__ import annotations

from pathlib import Path
import numpy as np
from shared.neural_networks.base import AbstractNeuralNetwork


class NeuralNetwork(AbstractNeuralNetwork):
    """An 8-16-4 MLP whose parameters form an evolvable genome."""

    def __init__(self, input_size: int, hidden_size: int, output_size: int, rng=None):
        rng = rng or np.random.default_rng()
        self.input_size, self.hidden_size, self.output_size = input_size, hidden_size, output_size
        self.wih = rng.normal(0, np.sqrt(2 / input_size), (hidden_size, input_size))
        self.who = rng.normal(0, np.sqrt(2 / hidden_size), (output_size, hidden_size))
        self.bias_hidden = np.zeros((hidden_size, 1))
        self.bias_output = np.zeros((output_size, 1))

    def activation_function(self, x):
        return np.tanh(x)

    def feedforward(self, inputs):
        values = np.asarray(inputs, dtype=float).reshape(-1, 1)
        if values.shape[0] != self.input_size:
            raise ValueError(f"expected {self.input_size} inputs, got {values.shape[0]}")
        hidden = self.activation_function(self.wih @ values + self.bias_hidden)
        return self.who @ hidden + self.bias_output

    def clone(self):
        clone = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        for name in ("wih", "who", "bias_hidden", "bias_output"):
            setattr(clone, name, getattr(self, name).copy())
        return clone

    def crossover(self, other, rng):
        child = self.clone()
        for name in ("wih", "who", "bias_hidden", "bias_output"):
            left, right = getattr(self, name), getattr(other, name)
            setattr(child, name, np.where(rng.random(left.shape) < 0.5, left, right))
        return child

    def mutate(self, rate, scale, rng):
        for name in ("wih", "who", "bias_hidden", "bias_output"):
            values = getattr(self, name)
            values += (rng.random(values.shape) < rate) * rng.normal(0, scale, values.shape)

    def save(self, path: str | Path):
        np.savez_compressed(path, input_size=self.input_size, hidden_size=self.hidden_size,
                            output_size=self.output_size, wih=self.wih, who=self.who,
                            bias_hidden=self.bias_hidden, bias_output=self.bias_output)

    @classmethod
    def load(cls, path: str | Path):
        with np.load(path) as data:
            network = cls(int(data["input_size"]), int(data["hidden_size"]), int(data["output_size"]))
            for name in ("wih", "who", "bias_hidden", "bias_output"):
                setattr(network, name, data[name].copy())
        return network

    # Accessors retained for compatibility with the original prototype.
    def get_wih(self): return self.wih
    def get_who(self): return self.who
    def get_bias_hidden(self): return self.bias_hidden
    def get_bias_output(self): return self.bias_output
