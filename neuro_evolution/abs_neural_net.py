from abc import ABC, abstractmethod


class AbstractNeuralNetwork(ABC):

    @abstractmethod
    def activation_function(self, x):
        pass

    @abstractmethod
    def feedforward(self, inputs):
        pass
