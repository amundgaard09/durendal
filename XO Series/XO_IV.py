"""
XO Neural Net Series Revision IV
"""

USE_GPU = False

if USE_GPU:
    import cupy as xp # type: ignore # type
else:
    import numpy as xp

from durapy import unicogni

ACTIVATIONS = {
    "relu":    (lambda Z: xp.maximum(0, Z), lambda Z: (Z > 0).astype(float)),
    "linear":  (lambda Z: Z,                lambda Z: xp.ones_like(Z)),
    "sigmoid": (unicogni.sigmoid,                   unicogni.d_sigmoid),
    "softmax": (unicogni.softmax,                   None) # Softmax derivative is handled differently in backpropagation, so we set it to None here.
}

class Denselayer:
    def __init__(self, n_inputs: int, n_outputs: int, act: str):
        """Initializes a dense layer with given input and output sizes and activation function."""
        self.weight_matrix: xp.ndarray = xp.random.randn(n_inputs, n_outputs) * xp.sqrt(2.0 / n_inputs) # He Initialization for weights.
        self.bias_vec:      xp.ndarray = xp.zeros(n_outputs)                                            # New bias array filled with zeros.
        self.act, self.d_act = ACTIVATIONS.get(act, "relu")
    
    def Forward(self, input: xp.ndarray) -> xp.ndarray:
        """Forward pass for the layer. Computes the output based on the input and current weights and biases."""
        self.input = input
        self.Z = input @ self.weight_matrix + self.bias_vec
        self.output = self.act(self.Z)
        return self.output
    
    def Backward(self, dA: xp.ndarray, learning_rate: float) -> xp.ndarray:
        """Backward pass for the layer. Calculates gradients and updates weights and biases."""
        dZ: xp.ndarray = dA * self.d_act(self.Z)                                              # dA -> Output GOL. dZ -> Z GOL.
        X:  xp.ndarray = self.input if self.input.ndim > 1 else self.input.reshape(1, -1)     # X  -> Reshaped input.
        dZ: xp.ndarray = dZ         if dZ.ndim         > 1 else dZ.reshape(1, -1)             # dZ -> Reshaped dZ.
        dW: xp.ndarray = X.T @ dZ / X.shape[0]                                                # dW -> Weight GOL. Batch averaged. X.T @ dZm computes the sum of gradients for each weight across the batch, and dividing by X.shape[0] gives the average.
        dB: xp.ndarray = dZ.mean(axis=0)                                                      # dB -> Bias   GOL, Batch averaged.
        dI: xp.ndarray = dZ @ self.weight_matrix.T                                            # dI -> Input  GOL. For backpropagation to previous layers. 

        self.weight_matrix -= learning_rate * dW
        self.bias_vec -= learning_rate * dB
        
        return dI.reshape(self.input.shape)
    
class Sequential:
    def __init__(
        self, 
        input_neuron_count: int, 
        layer_count: int, 
        layer_neuron_count: int, 
        output_neuron_count: int,
        act_per_layer: list[str], 
        learning_rate: float
    ):
        
        self.input_neuron_count = input_neuron_count
        self.layer_count = layer_count
        self.output_neuron_count = output_neuron_count
        self.learning_rate = learning_rate
        self.layers: list[Denselayer] = []
 
        prev_neuron_count = input_neuron_count
        
        for idx in range(layer_count):
            layer = Denselayer(
                prev_neuron_count, 
                layer_neuron_count, 
                act_per_layer[idx]
            )
            self.layers.append(layer)
            prev_neuron_count = layer_neuron_count

        # Output layer
        self.layers.append(Denselayer(prev_neuron_count, output_neuron_count, act_per_layer[-1]))
    
    def Forward(self, input: xp.ndarray) -> xp.ndarray:
        """Forward pass for the entire network."""
        
        x = input
        for layer in self.layers:
            x = layer.Forward(x)
        return x  
    
    def Backward(self, out_target: xp.ndarray):
        """
        Backward pass for the entire network. Computes gradients and updates weights and biases based on the target output.

        Args
        ----
            out_target (np.ndarray): The expected output values for the given input, used to calculate the loss and update the network's parameters during backpropagation.
        Vars
        ----
            out_pred (np.ndarray): The predicted output values from the network's forward pass, used to calculate the loss and update the network's parameters during backpropagation.
        """
        out_pred: xp.ndarray = self.layers[-1].output
        batch_size = out_target.shape[0] if out_target.ndim > 1 else 1
        loss_gradient = (unicogni.softmax(out_pred) - out_target) / batch_size 
        
        for layer in reversed(self.layers):
            loss_gradient = layer.Backward(loss_gradient, self.learning_rate)
    
    def Train(self, x: xp.ndarray, y: xp.ndarray, epochs: int, batch_size: int):
        """Training loop for the network.
        
        Args:
            X (np.ndarray): Input data.
            y (np.ndarray): Target labels.
            epochs (int): Number of training epochs.
        """
        last_loss = float('inf')
        
        BATCHCOUNT = x.shape[0] // batch_size 
        
        for epoch in range(epochs):
            
            shuffle_indices = xp.random.permutation(x.shape[0])
            x = x[shuffle_indices]
            y = y[shuffle_indices]
            
            epoch_loss = 0.0
            
            for batches in range(0, x.shape[0], batch_size):
                X_batch = x[batches:batches+batch_size]
                y_batch = y[batches:batches+batch_size]
                
                self.Forward(X_batch)
                self.Backward(y_batch)
                
                epoch_loss += unicogni.cross_entropy_loss(y_batch, self.layers[-1].output)
                
            epoch_loss /= (x.shape[0] / BATCHCOUNT)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss:.6f} {"\033[92m ### \033[0m" if epoch_loss < last_loss else "\033[91m ### \033[0m"}")
            last_loss = epoch_loss     
    
    def Predict(self, X: xp.ndarray) -> xp.ndarray:
        """Make predictions on new data.
        
        Args:
            X (np.ndarray): Input data.
        
        Returns:
            np.ndarray: Predictions.
        """
        return self.Forward(X) 
    
    @staticmethod
    def NormalizeData(X: xp.ndarray) -> xp.ndarray:
        mean = xp.mean(X, axis=0)
        std  = xp.std(X, axis=0)
        std  = xp.where(std == 0, 1, std)
        return (X - mean) / std