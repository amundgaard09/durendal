""" Second Iteration - XO Neural Net Series | Matrix-Based Neuronless Neural Net"""

import tensorflow as tf
import numpy as np
import typing

# Missing components for a complete neural network:

# 1. Implement the Backward() method in NeuralNetwork class     .
#    - Calculate loss gradient from target output               .
#    - Propagate gradients backward through all layers          .
#    - Use chain rule to compute dA for each layer              .
#
# 2. Add a loss function (e.g., Mean Squared Error)             DONE (MSE)
#    - Measures difference between predicted and target output  DONE (MSE)
#    - Returns scalar loss value                                DONE (MSE)
#
# 3. Add a derivative of loss function                          DONE (BinaryCrossEntropy from TensorFlow)
#    - Needed for backpropagation to start                      DONE (BinaryCrossEntropy from TensorFlow)
#
# 4. Implement a training loop/method                           .
#    - Takes training data and labels                           .
#    - Calls Forward() then Backward() repeatedly               .
#    - Tracks loss over epochs                                  .
#
# 5. Add a method to make predictions on new data               .
#    - Calls Forward() and returns predictions                  .
#    - Optional: add argmax for classification tasks            .
#
# 6. Add data preprocessing/loading                             .
#    - Convert input data to numpy arrays                       DONE (ConvertToNPArray())
#    - Normalize/scale input features if needed                 .
#
# 7. Add evaluation metrics                                     DONE (MSE, MAE, RMSE)
#    - Accuracy, precision, recall for classification           DONE (MSE, MAE, RMSE)
#    - Or MAE, RMSE for regression                              DONE (MSE, MAE, RMSE)

def DotProduct(listA: list, listB: list) -> float:
    """Returns the dot product of two lists of the same length."""
    
    if len(listA) != len(listB):
        raise ValueError("Lists must be of the same length")
    
    return sum(x * y for x, y in zip(listA, listB))

def ReLU(x: float) -> float:
    """Returns the ReLU activation of x."""
    return max(0, x)
def Sigmoid(x: float) -> float:
    """Returns the sigmoid activation of x."""
    return 1 / (1 + np.exp(-x))

def DerivativeReLU(x: float) -> float:
    """Returns the derivative of the ReLU activation function."""
    return 1 if x > 0 else 0
def DerivativeSigmoid(x: float) -> float:
    """Returns the derivative of the sigmoid activation function."""
    s = Sigmoid(x)
    return s * (1 - s)

def ConvertToNPArray(ArrayLike) -> np.ndarray:
    return np.array(ArrayLike)

def MAE(Actual: list, Prediction: list) -> float:
    if len(Prediction) != len(Actual):
        return None
    
    return (sum((np.abs(Actual[i] - Prediction[i])) for i in range(len(Actual)))) / len(Actual)
def MSE(Actual: list, Prediction: list) -> float:
    return (sum(np.mean((Actual[i] - Prediction[i])**2) for i in range(len(Actual)))) / len(Actual)
def RMSE(Actual: list, Prediction: list) -> float:
    return np.sqrt(sum(np.mean((Actual[i] - Prediction[i])**2) for i in range(len(Actual))))

class DenseLayer:
    """_DenseLayer class for the layers of the network, containing the weight matrix, bias vector, activation function, and methods for forward and backward passes._"""
    def __init__(
        self, 
        NInputs: int, 
        NOutputs: int, 
        Activation: typing.Callable[[float], float], 
        DerivativeActivation: typing.Callable[[float], float]
    ):
        """Neuron Initialization with random weights and bias."""
        self.WeightMatrix = np.random.uniform(-1,1,(NInputs, NOutputs))
        self.Bias = np.random.uniform(-1, 1, NOutputs)
        self.Activation = Activation
        self.DerivativeActivation = DerivativeActivation  
    def Forward(self, Input: np.ndarray) -> np.ndarray: 
        """Forward pass for the neuron."""
        self.Input = Input 
        self.Z = Input @ self.WeightMatrix + self.Bias
        self.Output = np.vectorize(self.Activation)(self.Z)
        return self.Output
    def Backward(self, dA: np.ndarray, LearningRate: float) -> np.ndarray:
        """Performs the backward pass for the dense layer.

        This function computes the gradients of the loss with respect to the
        layer's weights, bias, and input using backpropagation. It then updates
        the weights and bias using gradient descent.

        Parameters
        ----------
        dA : numpy.ndarray
            Gradient of the loss with respect to the layer's output
            (dLoss/dOutput). Shape: (NOutputs,).

        LearningRate : float
            Learning rate used for gradient descent weight updates.

        Returns
        -------
        numpy.ndarray
        Gradient of the loss with respect to the layer's input
        (dLoss/dInput). Shape: (NInputs,).

        Notes
        -----
        The backward pass follows these steps:

        1. Compute the gradient after the activation function:
            dZ = dA * Activation'(Z)

        2. Compute gradients for weights and bias:
            dW = outer(Input, dZ)
            dB = dZ

        3. Compute gradient to propagate to the previous layer:
            dInput = dZ @ WeightMatrix.T

        4. Update parameters using gradient descent:
            W = W - LearningRate * dW
            B = B - LearningRate * dB"""
            
        dZ = dA * np.vectorize(self.DerivativeActivation)(self.Z)

        dW = np.outer(self.Input, dZ)
        dB = dZ

        dInput = dZ @ self.WeightMatrix.T

        self.WeightMatrix -= LearningRate * dW
        self.Bias -= LearningRate * dB

        return dInput
class NeuralNetwork:
    def __init__(
        self, 
        InputNeuronCount: int, 
        DenseLayerCount: int, 
        DenseLayerNeuronCount: int, 
        OutputNeuronCount: int,
        ActivationFunctionsPerLayer: list[typing.Callable[[float], float]], 
        DerivativeActivationFunctionsPerLayer: list[typing.Callable[[float], float]],
        LearningRate: float
    ):
        
        self.InputNeuronCount = InputNeuronCount
        self.DenseLayerCount = DenseLayerCount
        self.OutputNeuronCount = OutputNeuronCount
        self.LearningRate = LearningRate
        self.Layers: list[DenseLayer] = []

        #Layers 
        PreviousNeuronCount = InputNeuronCount
        Counter = 0
        
        for _ in range(DenseLayerCount):
            layer = DenseLayer(
                PreviousNeuronCount, 
                DenseLayerNeuronCount, 
                ActivationFunctionsPerLayer[Counter], 
                DerivativeActivationFunctionsPerLayer[Counter]
            )
            self.Layers.append(layer)
            PreviousNeuronCount = DenseLayerNeuronCount
            Counter += 1

        # Output layer
        self.Layers.append(DenseLayer(PreviousNeuronCount, OutputNeuronCount, ActivationFunctionsPerLayer[len(ActivationFunctionsPerLayer)-1], DerivativeActivationFunctionsPerLayer[len(DerivativeActivationFunctionsPerLayer)-1]))
    def Forward(self, Input: np.ndarray) -> np.ndarray:
        """_Forward pass for the entire network._

        Args:
            Input (list[float]): A vectorlist of input values to the network, comprised of individual input values for each input neuron.
            
        Returns:
            Output (list[float]): A vectorlist of output values from the network, comprised of individual output values from each output neuron.
        """
        x = Input
        for layer in self.Layers:
            x = layer.Forward(x)
        return x  
    def Backward(self, TargetOutput: np.ndarray):
        """Backward pass for the entire network.
        
        Args:
            TargetOutput (np.ndarray): Target output values for backpropagation.
        """
        OutputPrediction = self.Layers[-1].Output
        dA = -(TargetOutput / OutputPrediction - (1 - TargetOutput) / (1 - OutputPrediction))
        
        for layer in reversed(self.Layers):
            dA = layer.Backward(dA, self.LearningRate)
        
MatrixNet = NeuralNetwork(
    InputNeuronCount = 2, 
    DenseLayerCount = 1, 
    DenseLayerNeuronCount = 8, 
    OutputNeuronCount = 1, 
    ActivationFunctionsPerLayer = [Sigmoid, Sigmoid], 
    DerivativeActivationFunctionsPerLayer = [DerivativeSigmoid, DerivativeSigmoid],
    LearningRate = 0.005
)

