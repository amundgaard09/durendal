"""The first iteration of the Amundworks XO Neural Network series."""

import math
import random
import typing

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
    return 1 / (1 + math.exp(-x))

def DerivativeReLU(x: float) -> float:
    """Returns the derivative of the ReLU activation function."""
    return 1 if x > 0 else 0
def DerivativeSigmoid(x: float) -> float:
    """Returns the derivative of the sigmoid activation function."""
    s = Sigmoid(x)
    return s * (1 - s)

def Slope(x1: float, y1: float, x2: float, y2: float) -> float:
    """Returns the slope of the line between two points."""
    if x2 - x1 == 0:
        raise ValueError("Cannot calculate slope for vertical line")
    return (y2 - y1) / (x2 - x1)
def MSE(ActualValue: float, PredictedValue: float):
    """_Mean Squared Error Function_
    Args:
        PredictedValue (float): The error value that the neural net predicts will be a good match for the training data.
        ActualValue (float): The error value that actual"""
    return (PredictedValue - ActualValue)**2
def MSEGradient(ActualValue: float, PredictedValue: float):
    return 2*(PredictedValue - ActualValue)

class Neuron:
    """_Neuron class for individual neurons in the network, containing weights, bias, activation function, and methods for forward and backward passes._"""
    
    def __init__(self, NInputs: int,  Activation: typing.Callable[[float], float], DerivativeActivation: typing.Callable[[float], float]):
        """Neuron Initialization with random weights and bias."""
        self.Weights = [random.uniform(-1, 1) for _ in range(NInputs)]
        self.Bias = random.uniform(-1, 1)
        self.Activation = Activation
        self.DerivativeActivation = DerivativeActivation
        
    def Forward(self, Input: list) -> float:  
        """Forward pass for the neuron."""           
        self.Input = Input
        self.Z = DotProduct(Input, self.Weights) + self.Bias
        self.Output = self.Activation(self.Z)
        return self.Output
            
    def Backward(self, dLoss_dOut: float, LearningRate: float):
        """_Backward pass for the neuron._
        Args:
            dLoss_dOut (float): The Gradient of Loss with respects to the output of this neuron
            LearningRate (float): The Learning Rate (aka rate of change) in the weights and biases of the neuron.
            Delta (float): 
        """
        Delta = dLoss_dOut * self.DerivativeActivation(self.Z)
        
        for idx in range(len(self.Weights)):
            self.Weights[idx] -= LearningRate * Delta * self.Input[idx]
        
        self.Bias -= LearningRate * Delta
        return [Delta * Weight for Weight in self.Weights]
    
class Layer:
    """_Layer class for NN Layers, containing multiple neurons and handling forward and backward passes for the layer._"""
    def __init__(self, InputCount, NeuronCount, Activation: typing.Callable[[float], float], DerivativeActivation: typing.Callable[[float], float]):
        self.Activation = Activation
        self.DerivativeActivation = DerivativeActivation
        self.Nodes = [Neuron(InputCount, Activation, DerivativeActivation) for _ in range(NeuronCount)]
        
    def Forward(self, Input: list[float]) -> list[float]:
        """_Forward pass for the layer._

        Args:
            Input (list[float]): A vectorlist of input values to the layer, comprised of individual outputs from neurons of the previous layer.
        
        Returns:  
            Output (list[float]): A vectorlist of output values from the layer, comprised of individual outputs from neurons of the current layer. 
        """
        Output = []
        for node in self.Nodes:
            Output.append(node.Forward(Input))
        return Output
        
    def Backward(self, dLoss_dOutList: list[float], LearningRate: float) -> list[float]:
        """_Backward Pass for Layers_
        Args:
            dLoss_dOutList (list): The Gradient of Loss with respects to each output of the neurons in this layer.
            LearningRate (float): The Learning Rate (aka rate of change) in the weights and biases of the neuron.
        Returns:
            dLoss_dInput (list): The Gradient of Loss with respects to input for the next layer backwards.
        """
        dLoss_dInput = [0.0] * len(self.Nodes[0].Input)
        
        for Neuron, dLoss_dOut in zip(self.Nodes, dLoss_dOutList):
            NeuronGradients = Neuron.Backward(dLoss_dOut, LearningRate)
            
            for idx, Gradient in enumerate(NeuronGradients):
                dLoss_dInput[idx] += Gradient
                
        return dLoss_dInput
        
class NeuralNetwork:
    def __init__(
        self, 
        InputNeuronCount: int, 
        HiddenLayerCount: int, 
        HiddenLayerNeuronCount: int, 
        OutputNeuronCount: int, 
        ActivationFunctionsPerLayer: list[typing.Callable[[float], float]], 
        DerivativeActivationFunctionsPerLayer: list[typing.Callable[[float], float]],
        LearningRate: float
    ):
        
        self.InputCount = InputNeuronCount
        self.HiddenLayerCount = HiddenLayerCount
        self.OutputCount = OutputNeuronCount
        self.LearningRate = LearningRate
        
        self.Layers: list[Layer] = []

        # Hidden layers
        PreviousNeuronCount = InputNeuronCount
        Counter = 0
        for _ in range(HiddenLayerCount):
            layer = Layer(PreviousNeuronCount, HiddenLayerNeuronCount, ActivationFunctionsPerLayer[Counter], DerivativeActivationFunctionsPerLayer[Counter])
            self.Layers.append(layer)
            PreviousNeuronCount = HiddenLayerNeuronCount
            Counter += 1

        # Output layer
        self.Layers.append(Layer(PreviousNeuronCount, OutputNeuronCount, ActivationFunctionsPerLayer[len(ActivationFunctionsPerLayer)-1], DerivativeActivationFunctionsPerLayer[len(DerivativeActivationFunctionsPerLayer)-1]))

    def Forward(self, Input: list[float]) -> list[float]:
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
    
    def Backward(self, TargetOutput: list[float]):
        OutputLayer = self.Layers[-1]
        dLoss_dOut = []
        
        for Neuron, Target in zip(OutputLayer.Nodes, TargetOutput):
            dLoss_dOut.append(Neuron.Output - Target)
            
        for Layer in reversed(self.Layers):
            dLoss_dOut = Layer.Backward(dLoss_dOut, self.LearningRate)
        
# XOR
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y = [0, 1, 1, 0]

XORnet = NeuralNetwork(
    InputNeuronCount=2, 
    HiddenLayerCount=1, 
    HiddenLayerNeuronCount=8, 
    OutputNeuronCount=1, 
    ActivationFunctionsPerLayer = [Sigmoid, Sigmoid], 
    DerivativeActivationFunctionsPerLayer = [DerivativeSigmoid, DerivativeSigmoid],
    LearningRate=0.005
)       

while True:
    try:
        EpochCount = int(input("Epoch Count: "))
        SatisfactionThreshold = float(input("Satisfaction Threshold (standard: 0.001):"))
        break
    except ValueError:
        print("Invalid Variables!")
        continue

for Epoch in range(EpochCount):
    TotalLoss = 0
    for X_i, Y_i in zip(X, Y):
        Output = XORnet.Forward(X_i)[0]
        
        Loss = MSE(PredictedValue=Y_i, ActualValue=Output)
        TotalLoss += Loss
        
        XORnet.Backward([Y_i])
        
        if Epoch % 100 == 0:
            print(f"Epoch {Epoch}, Loss = {TotalLoss/4}")
            
    if TotalLoss <= SatisfactionThreshold:
        break

print("\nPredicted XOR outputs after training:")
CorrectPredictions = 0
Predictions = 0
for x_i, y_i in zip(X, Y):
    raw_output = XORnet.Forward(x_i)[0]
    predicted = 1 if raw_output > 0.5 else 0
    print(f"Input: {x_i}, Predicted: {predicted}, Actual: {y_i}, Raw output: {raw_output:.4f}")
    Predictions += 1
    if predicted == y_i:
        CorrectPredictions += 1
        
if CorrectPredictions == Predictions:
    print("\033[92m -- Successful Training! -- \033[0m")