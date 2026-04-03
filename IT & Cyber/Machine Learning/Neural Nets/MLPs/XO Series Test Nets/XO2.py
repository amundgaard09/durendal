""" Second Iteration - XO Neural Net Series | Matrix-Based Neural Net"""

import numpy as np
import typing
import time

def _sigmoid(Z):
    return 1 / (1 + np.exp(-Z))
     
def _dsigmoid(Z):
    s = _sigmoid(Z)
    return s * (1 - s)

ACTIVATIONS = {
    "relu":    (lambda Z: np.maximum(0, Z),  lambda Z: (Z > 0).astype(float)),
    "sigmoid": (_sigmoid,                     _dsigmoid),
}

def MAE(Actual: np.ndarray, Prediction: np.ndarray) -> float:
    if Actual.shape != Prediction.shape:
        raise ValueError("Actual and Prediction must have the same shape")
    return np.mean(np.abs(Actual - Prediction))
def MSE(Actual: np.ndarray, Prediction: np.ndarray) -> float:
    if Actual.shape != Prediction.shape:
        raise ValueError("Actual and Prediction must have the same shape")
    return np.mean((Actual - Prediction) ** 2)
def RMSE(Actual: np.ndarray, Prediction: np.ndarray) -> float:
    return np.sqrt(MSE(Actual, Prediction))

class DenseLayer:
    def __init__(self, NInputs: int, NOutputs: int, activation: str):
        self.WeightMatrix = np.random.uniform(-1, 1, (NInputs, NOutputs))
        self.Bias         = np.random.uniform(-1, 1, NOutputs)
        self.act, self.dact = ACTIVATIONS[activation]

    def Forward(self, Input: np.ndarray) -> np.ndarray:
        self.Input = Input
        self.Z     = Input @ self.WeightMatrix + self.Bias
        self.Output = self.act(self.Z)
        return self.Output

    def Backward(self, dA: np.ndarray, LearningRate: float):
        dZ = dA * self.dact(self.Z)
        X   = self.Input if self.Input.ndim > 1 else self.Input.reshape(1, -1)
        dZm = dZ  if dZ.ndim  > 1 else dZ.reshape(1, -1)
        dW  = X.T @ dZm / X.shape[0]
        dB = dZm.mean(axis=0)
        dIn = dZm @ self.WeightMatrix.T
        self.WeightMatrix -= LearningRate * dW
        self.Bias         -= LearningRate * dB
        return dIn.reshape(self.Input.shape)

class NeuralNetwork:
    def __init__(
        self, 
        InputNeuronCount: int, 
        DenseLayerCount: int, 
        DenseLayerNeuronCount: int, 
        OutputNeuronCount: int,
        ActivationFunctionsPerLayer: list[str], 
        LearningRate: float
    ):
        
        self.InputNeuronCount = InputNeuronCount
        self.DenseLayerCount = DenseLayerCount
        self.OutputNeuronCount = OutputNeuronCount
        self.LearningRate = LearningRate
        self.Layers: list[DenseLayer] = []
 
        PreviousNeuronCount = InputNeuronCount
        
        for idx in range(DenseLayerCount):
            layer = DenseLayer(
                PreviousNeuronCount, 
                DenseLayerNeuronCount, 
                ActivationFunctionsPerLayer[idx]
            )
            self.Layers.append(layer)
            PreviousNeuronCount = DenseLayerNeuronCount

        # Output layer
        self.Layers.append(DenseLayer(PreviousNeuronCount, OutputNeuronCount, ActivationFunctionsPerLayer[-1]))
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
        n = TargetOutput.shape[0] if TargetOutput.ndim > 1 else 1
        dA = 2 * (OutputPrediction - TargetOutput) / n
        
        for layer in reversed(self.Layers):
            dA = layer.Backward(dA, self.LearningRate)
    def Train(self, X: np.ndarray, y: np.ndarray, epochs: int):
        """Training loop for the network.
        
        Args:
            X (np.ndarray): Input data.
            y (np.ndarray): Target labels.
            epochs (int): Number of training epochs.
        """
        for epoch in range(epochs):
            prediction = self.Forward(X)
            self.Backward(y)
            if (epoch + 1) % 1000 == 0:
                loss = MSE(y, self.Layers[-1].Output)  # post-update loss
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss:.6f}")       
    def Predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions on new data.
        
        Args:
            X (np.ndarray): Input data.
        
        Returns:
            np.ndarray: Predictions.
        """
        return self.Forward(X) 
    @staticmethod
    def NormalizeData(X: np.ndarray) -> np.ndarray:
        mean = np.mean(X, axis=0)
        std  = np.std(X, axis=0)
        std  = np.where(std == 0, 1, std)   # avoid div/0
        return (X - mean) / std

NEURALNET = NeuralNetwork(
    InputNeuronCount=3,
    DenseLayerCount=2,
    DenseLayerNeuronCount=4,
    OutputNeuronCount=2,
    ActivationFunctionsPerLayer=["relu", "relu", "sigmoid"],
    LearningRate=0.01
)

# TRAINING DATA | 3 Input Neurons, 2 Output Neurons | 8 Training Examples | Binary Classification Task
X = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
Y = np.array([[0, 0], [0, 1], [0, 1], [0, 0], [0, 1], [0, 0], [0, 0], [1, 1]])

Epochs = int(1e5)
StartTime = time.time()

NEURALNET.Train(X, Y, epochs=Epochs)

Endtime = time.time()
ElapsedTime = Endtime - StartTime

print(f"\nTotal Training Time: {ElapsedTime:.2f} seconds")
print(f"Time per Epoch: {ElapsedTime/Epochs:.4f} seconds")

# VERIFYING TRAINING DATA PREDICTIONS
for i in range(len(X)):
    pred = NEURALNET.Predict(X[i])
    print(f"Input: {X[i]}, Target: {Y[i]}, Prediction: {pred}")
    if np.array_equal(np.round(pred), Y[i]):
        print("\033[92m -- Correct Prediction! -- \033[0m")
    else:
        print("\033[91m -- Incorrect Prediction! -- \033[0m")

