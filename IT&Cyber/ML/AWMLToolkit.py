"""The complete AmundWorks toolkit for ML - Version I - Written by Simon Stordal Amundgård"""

import math
import numpy as np

### CALCULATIONS

def DotProduct(listA: list, listB: list) -> float:
    """Returns the dot product of two lists of the same length."""
    
    if len(listA) != len(listB):
        raise ValueError("Lists must be of the same length")
    
    return sum(x * y for x, y in zip(listA, listB))

### ACTIVATION FUNCTIONS

def ReLU(x: float) -> float:
    """Returns the ReLU activation of x."""
    return max(0, x)
def sigmoid(x: float) -> float:
    """Returns the sigmoid activation of x."""
    return 1 / (1 + math.exp(-x))
def dReLU(x: float) -> float:
    """Returns the derivative of the ReLU activation function."""
    return 1 if x > 0 else 0
def dsigmoid(x: float) -> float:
    """Returns the derivative of the sigmoid activation function."""
    s = sigmoid(x)
    return s * (1 - s)

def _softmax(Z: np.ndarray) -> np.ndarray:
    """Softmax activation function for multi-class classification. Converts raw scores (logits) into probabilities."""
    expZ = np.exp(Z - np.max(Z, axis=-1, keepdims=True))
    return expZ / np.sum(expZ, axis=-1, keepdims=True)

### PERFORMANCE METRICS

def mae(Actual: list, Prediction: list) -> float:
    if len(Prediction) != len(Actual):
        return None
    return (sum((np.abs(Actual[i] - Prediction[i])) for i in range(len(Actual)))) / len(Actual)
def mse(Actual: list, Prediction: list) -> float:
    if len(Prediction) != len(Actual):
        return None
    return (sum(np.mean((Actual[i] - Prediction[i])**2) for i in range(len(Actual)))) / len(Actual)
def rmse(Actual: list, Prediction: list) -> float:
    if len(Prediction) != len(Actual):
        return None
    return np.sqrt(mse(Actual, Prediction))

def crossEntropyLoss(Actual: np.ndarray, Prediction: np.ndarray) -> float:
    """Cross-entropy loss function for multi-class classification."""
    ArrayLength = Actual.shape[0]
    SoftmaxedPrediction = _softmax(Prediction) # Ensure predictions are probabilities.
    ClippedPrediction = np.clip(SoftmaxedPrediction, 1e-15, 1 - 1e-15) # Avoid log of zero = -inf.
    log_likelihood = -np.log(ClippedPrediction[range(ArrayLength), Actual.argmax(axis=1)])
    return np.sum(log_likelihood) / ArrayLength

### DATA PROCESSING

