import numpy as np
from neuro_evolution.abs_neural_net import AbstractNeuralNetwork
from scipy.special import expit as sigmoid


class NeuralNetwork(AbstractNeuralNetwork):

    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self._input_size = input_size
        self._hidden_size = hidden_size
        self._output_size = output_size

        # Initialize weights and biases randomly
        self._wih = np.random.rand(hidden_size, input_size)
        self._who = np.random.rand(output_size, hidden_size)
        self._bias_hidden = np.random.rand(hidden_size, 1)
        self._bias_output = np.random.rand(output_size, 1)

    def activation_function(self, x):
        return sigmoid(x)

    def feedforward(self, inputs):
        inputs = np.array(inputs, ndmin=2).T

        # Calculate hidden layer outputs
        hidden_inputs = np.dot(self._wih, inputs) + self._bias_hidden
        hidden_outputs = self.activation_function(hidden_inputs)

        # Calculate final outputs
        final_inputs = np.dot(self._who, hidden_outputs) + self._bias_output
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

    # Getter methods for weights and biases
    def get_wih(self):
        return self._wih

    def get_who(self):
        return self._who

    def get_bias_hidden(self):
        return self._bias_hidden

    def get_bias_output(self):
        return self._bias_output
