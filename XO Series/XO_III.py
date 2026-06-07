"""
Third Iteration - XO Neural Net Series

Matrix-Based MNIST Classification Neural Net
"""

import time, keras, numpy as np
from durapy import unicogni

ACTIVATIONS = {
    "relu":    (lambda Z: np.maximum(0, Z), lambda Z: (Z > 0).astype(float)),
    "linear":  (lambda Z: Z,                lambda Z: np.ones_like(Z)),
    "sigmoid": (unicogni.sigmoid,                   unicogni.d_sigmoid),
    "softmax": (unicogni.softmax,                   None) # Softmax derivative is handled differently in backpropagation, so we set it to None here.
}

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
    
    def Forward(self, input_arr: np.ndarray) -> np.ndarray:
        """_Forward pass for the entire network._

        Args:
            Input (list[float]): An array of input values to the network, where each value corresponds to the input of an input neuron.
            
        Returns:
            Output (list[float]): An array of output values from the network, where each value corresponds to the output of an output neuron.
        """
        x = input_arr
        for layer in self.Layers:
            x = layer.Forward(x)
        return x  
    
    def Backward(self, out_target: np.ndarray):
        """
        Backward pass for the entire network. Computes gradients and updates weights and biases based on the target output.

        Args:
            TargetOutput (np.ndarray): The expected output values for the given input, used to calculate the loss and update the network's parameters during backpropagation.
            OutputPrediction (np.ndarray): The predicted output values from the network's forward pass, used to calculate the loss and update the network's parameters during backpropagation.
        """
        out_pred: np.ndarray = self.Layers[-1].Output
        batch_size = out_target.shape[0] if out_target.ndim > 1 else 1
        initial_GOL = (unicogni.softmax(out_pred) - out_target) / batch_size 
        
        for layer in reversed(self.Layers):
            initial_GOL = layer.Backward(initial_GOL, self.LearningRate)
    
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
                
                EpochLoss += unicogni.cross_entropy_loss(y_batch, self.Layers[-1].Output)
                
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

X_train, Y_train, X_test, Y_test = np.array(X_train), np.array(Y_train), np.array(X_test), np.array(Y_test)

#reshaping and normalizing
X_train = np.reshape(X_train, (X_train.shape[0], -1))
X_test = np.reshape(X_test, (X_test.shape[0], -1))
X_train = X_train / 255.0
X_test = X_test / 255.0

#one-hot encoding of labels
train_labels = np.zeros((Y_train.size, Y_train.max() + 1))
test_labels = np.zeros((Y_test.size, Y_test.max() + 1))

train_rows = np.arange(Y_train.size)
test_rows = np.arange(Y_test.size)

train_labels[train_rows, Y_train] = 1
test_labels[test_rows, Y_test] = 1

X = X_train
Y = train_labels

#### -- TRAINING LOOP -- ####

epochs = 200 
start_time = time.time()

BATCHSIZE = 128
MNISTNET.Train(X, Y, epochs=epochs)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"\nTotal Training Time: {elapsed_time:.2f} seconds")
print(f"Time per Epoch: {elapsed_time/epochs:.4f} seconds")

correct_preds = np.zeros(10, dtype=int)

raw_preds = MNISTNET.Predict(X_test)
preds = np.argmax(raw_preds, axis=1)
test_label_idxs = np.argmax(test_labels, axis=1)

bool_arr = test_label_idxs == preds

correct_precentage = np.sum(bool_arr) / len(bool_arr) * 100
correct_preds = np.bincount(test_label_idxs[bool_arr], minlength=10)

for digit in range(10):
    print(f"Digit {digit}: {correct_preds[digit]}/{np.sum(test_labels[:, digit])} correct")

print(f"\nOverall Accuracy: {correct_precentage:.2f}%")
