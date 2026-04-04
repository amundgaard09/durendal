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

### PERFORMANCE METRICS

def MAE(Actual: list, Prediction: list) -> float:
    if len(Prediction) != len(Actual):
        return None
    return (sum((np.abs(Actual[i] - Prediction[i])) for i in range(len(Actual)))) / len(Actual)
def MSE(Actual: list, Prediction: list) -> float:
    if len(Prediction) != len(Actual):
        return None
    return (sum(np.mean((Actual[i] - Prediction[i])**2) for i in range(len(Actual)))) / len(Actual)
def RMSE(Actual: list, Prediction: list) -> float:
    if len(Prediction) != len(Actual):
        return None
    return np.sqrt(MSE(Actual, Prediction))

### DATA PROCESSING

def ConvertToNPArray(ArrayLike) -> np.ndarray:
    return np.array(ArrayLike)

