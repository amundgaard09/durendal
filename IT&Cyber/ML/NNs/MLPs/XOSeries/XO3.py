""" Third Iteration - XO Neural Net Series | Matrix-Based Image Classification Neural Net"""

### XO4 -> CUDA OPTIMALIZATION

import keras
import numpy as np
import time

def _sigmoid(Z: np.ndarray) -> np.ndarray:
    """Sigmoid activation function for binary classification. Converts raw scores (logits) into probabilities."""
    return 1 / (1 + np.exp(-Z))    
def _dsigmoid(Z: np.ndarray) -> np.ndarray:
    """Derivative of the sigmoid function. Note: This is a simplified version and may not be suitable for all use cases."""
    s = _sigmoid(Z)
    return s * (1 - s)
def _softmax(Z: np.ndarray) -> np.ndarray:
    """Softmax activation function for multi-class classification. Converts raw scores (logits) into probabilities between 0 and 1."""
    expZ = np.exp(Z - np.max(Z, axis=-1, keepdims=True))
    return expZ / np.sum(expZ, axis=-1, keepdims=True)

ACTIVATIONS = {
    "relu":    (lambda Z: np.maximum(0, Z), lambda Z: (Z > 0).astype(float)),
    "linear":  (lambda Z: Z,                lambda Z: np.ones_like(Z)),
    "sigmoid": (_sigmoid,                   _dsigmoid),
    "softmax": (_softmax,                   None) # Softmax derivative is handled differently in backpropagation, so we set it to None here.
}

def _crossEntropyLoss(Actual: np.ndarray, Prediction: np.ndarray) -> float:
    """Cross-entropy loss function for multi-class classification."""
    ArrayLength = Actual.shape[0]
    SoftmaxedPrediction = _softmax(Prediction) # Ensure predictions are probabilities.
    ClippedPrediction = np.clip(SoftmaxedPrediction, 1e-15, 1 - 1e-15) # Avoid log of zero = -inf.
    log_likelihood = -np.log(ClippedPrediction[range(ArrayLength), Actual.argmax(axis=1)])
    return np.sum(log_likelihood) / ArrayLength

class DenseLayer:
    def __init__(self, NInputs: int, NOutputs: int, Activation: str):
        """Initializes a dense layer with given input and output sizes and activation function."""
        self.Weights: np.ndarray = np.random.randn(NInputs, NOutputs) * np.sqrt(2.0 / NInputs) # He Initialization for weights.
        self.Bias:    np.ndarray = np.zeros(NOutputs)                                          # New bias array filled with zeros.
        self.Activation, self.DerivativeActivation = ACTIVATIONS[Activation]
    
    def Forward(self, Input: np.ndarray) -> np.ndarray:
        """Forward pass for the layer. Computes the output based on the input and current weights and biases."""
        self.Input = Input
        self.Z = Input @ self.Weights + self.Bias # Z ->      Post transformation - Pre activation.
        self.Output = self.Activation(self.Z)
        return self.Output
    
    ### GOL / dX > Gradient of Loss. ### Reshaping > "Verification" of array dimensions ### .T > Transposing ###
    def Backward(self, dA: np.ndarray, LearningRate: float) -> np.ndarray:
        """Backward pass for the layer. Calculates gradients and updates weights and biases."""
        dZ: np.ndarray = dA * self.DerivativeActivation(self.Z)                               # dA -> Output GOL. dZ -> Z GOL.
        X:  np.ndarray = self.Input if self.Input.ndim > 1 else self.Input.reshape(1, -1)     # X  -> Reshaped input.
        dZ: np.ndarray = dZ         if dZ.ndim         > 1 else dZ.reshape(1, -1)             # dZ -> Reshaped dZ.
        dW: np.ndarray = X.T @ dZ / X.shape[0]                                                # dW -> Weight GOL. Batch averaged. X.T @ dZm computes the sum of gradients for each weight across the batch, and dividing by X.shape[0] gives the average.
        dB: np.ndarray = dZ.mean(axis=0)                                                      # dB -> Bias   GOL, Batch averaged.
        dI: np.ndarray = dZ @ self.Weights.T                                                  # dI -> Input  GOL. For backpropagation to previous layers. 

        self.Weights -= LearningRate * dW
        self.Bias    -= LearningRate * dB
        
        return dI.reshape(self.Input.shape)
    
class NeuralNetwork:
    def __init__(
        self, 
        InputNeuronCount: int, 
        DenseLayerCount: int, 
        DenseLayerNeuronCount: int, 
        OutputNeuronCount: int,
        ActivationsPerLayer: list[str], 
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
                ActivationsPerLayer[idx]
            )
            self.Layers.append(layer)
            PreviousNeuronCount = DenseLayerNeuronCount

        # Output layer
        self.Layers.append(DenseLayer(PreviousNeuronCount, OutputNeuronCount, ActivationsPerLayer[-1]))
    
    def Forward(self, Input: np.ndarray) -> np.ndarray:
        """_Forward pass for the entire network._

        Args:
            Input (list[float]): An array of input values to the network, where each value corresponds to the input of an input neuron.
            
        Returns:
            Output (list[float]): An array of output values from the network, where each value corresponds to the output of an output neuron.
        """
        x = Input
        for layer in self.Layers:
            x = layer.Forward(x)
        return x  
    
    def Backward(self, OutputTarget: np.ndarray):
        """Backward pass for the entire network. Computes gradients and updates weights and biases based on the target output.

        Args:
            TargetOutput (np.ndarray): The expected output values for the given input, used to calculate the loss and update the network's parameters during backpropagation.
            OutputPrediction (np.ndarray): The predicted output values from the network's forward pass, used to calculate the loss and update the network's parameters during backpropagation.
        """
        OutputPrediction: np.ndarray = self.Layers[-1].Output
        BatchSize = OutputTarget.shape[0] if OutputTarget.ndim > 1 else 1
        InitialGOL = (_softmax(OutputPrediction) - OutputTarget) / BatchSize 
        
        for layer in reversed(self.Layers):
            InitialGOL = layer.Backward(InitialGOL, self.LearningRate)
    
    def Train(self, X: np.ndarray, y: np.ndarray, epochs: int):
        """Training loop for the network.
        
        Args:
            X (np.ndarray): Input data.
            y (np.ndarray): Target labels.
            epochs (int): Number of training epochs.
        """
        lastloss = float('inf')
        
        BATCHCOUNT = X.shape[0] // BATCHSIZE 
        
        for epoch in range(epochs):
            
            shuffle_indices = np.random.permutation(X.shape[0])
            X = X[shuffle_indices]
            y = y[shuffle_indices]
            
            EpochLoss = 0.0
            
            for batches in range(0, X.shape[0], BATCHSIZE):
                X_batch = X[batches:batches+BATCHSIZE]
                y_batch = y[batches:batches+BATCHSIZE]
                
                self.Forward(X_batch)
                self.Backward(y_batch)
                
                EpochLoss += _crossEntropyLoss(y_batch, self.Layers[-1].Output)
                
            EpochLoss /= (X.shape[0] / BATCHCOUNT)
                
            Marker = "\033[92m ### \033[0m" if EpochLoss < lastloss else "\033[91m ### \033[0m"
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {EpochLoss:.6f} {Marker}")
            lastloss = EpochLoss     
    
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
        std  = np.where(std == 0, 1, std)
        return (X - mean) / std

MNISTNET = NeuralNetwork(
    InputNeuronCount=784,
    DenseLayerCount=2,
    DenseLayerNeuronCount=256,
    OutputNeuronCount=10,
    ActivationsPerLayer= ["relu", "relu", "linear"],
    LearningRate=0.1
)

#### -- DATA PREPROCESSING -- ####

#data set
((X_train, Y_train), (X_test,  Y_test)) = keras.datasets.mnist.load_data()

#reshaping and normalizing
X_train = np.reshape(X_train, (X_train.shape[0], -1))
X_test = np.reshape(X_test, (X_test.shape[0], -1))
X_train = X_train / 255.0
X_test = X_test / 255.0

#one-hot encoding of labels
TrainingLabels = np.zeros((Y_train.size, Y_train.max() + 1))
TestingLabels = np.zeros((Y_test.size, Y_test.max() + 1))

TrainingRows = np.arange(Y_train.size)
TestingRows = np.arange(Y_test.size)

TrainingLabels[TrainingRows, Y_train] = 1
TestingLabels[TestingRows, Y_test] = 1

X = X_train
Y = TrainingLabels

#### -- TRAINING LOOP -- ####

Epochs = 200 
StartTime = time.time()

BATCHSIZE = 128

MNISTNET.Train(X, Y, epochs=Epochs)

Endtime = time.time()
ElapsedTime = Endtime - StartTime

print(f"\nTotal Training Time: {ElapsedTime:.2f} seconds")
print(f"Time per Epoch: {ElapsedTime/Epochs:.4f} seconds")

CorrectPredictions = np.zeros(10, dtype=int)

RawPredictions = MNISTNET.Predict(X_test)
Predictions = np.argmax(RawPredictions, axis=1)
TestingLabelsIndices = np.argmax(TestingLabels, axis=1)

BoolArray = TestingLabelsIndices == Predictions

CorrectPrecentage = np.sum(BoolArray) / len(BoolArray) * 100
CorrectPredictions = np.bincount(TestingLabelsIndices[BoolArray], minlength=10)

for digit in range(10):
    print(f"Digit {digit}: {CorrectPredictions[digit]}/{np.sum(TestingLabels[:, digit])} correct")

print(f"\nOverall Accuracy: {CorrectPrecentage:.2f}%")
