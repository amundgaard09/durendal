from __future__ import annotations

"""
The DuraPy UniCogni Package for Machine Learning.
"""

USE_GPU = False  # Set to True on your NVIDIA machine

if USE_GPU:
    import cupy as xp # type: ignore # 'xp' stands for cross-platform (numpy/cupy)
else:
    import numpy as xp

import math
from ..unimath.linalg_dtypes import is_close
from ...commons.constants import E, PI
from ...commons.exceptions import MissingParameters

### TODO REFACTOR LIST TYPE TO NP.NDARRAY

### ACTIVATION FUNCTIONS

def relu(x: float) -> float:
    """Returns the Rectified Linear Unit activation of x."""
    return max(0.0, x)
def d_relu(x: float) -> float:
    """Returns the derivative of the Rectified Linear Unit activation function."""
    return 1.0 if x > 0 else 0.0

def leaky_relu(x: float) -> float:
    """Returns the Leaky ReLU activation of X."""
    return max(0.01 * x, x)
def d_leaky_relu(x: float) -> float:
    """Returns the derivative of the Leaky ReLU activation function."""
    return 1.0 if x > 0 else 0.01

def gelu(x: float) -> float: 
    """Gaussian Error Linear Unit using the tanh approximation."""
    return 0.5 * x * (1.0 + tanh(math.sqrt(2 / PI) * (x + 0.044715 * x**3)))
def d_gelu(x: float) -> float:
    """Derivative of GELU."""
    try:
        gauss = math.exp(-0.5 * x**2)
    except OverflowError:
        gauss = 0.0
    cdf = 0.5 * (1.0 + math.erf(x / math.sqrt(2)))
    pdf = (1.0 / math.sqrt(2 * PI)) * gauss
    return cdf + x * pdf

def silu(x: float) -> float:
    """Sigmoid Linear Unit."""
    return x * sigmoid(x)
def d_silu(x: float) -> float:
    """Derivative of the SiLU activation function."""
    s = sigmoid(x)
    return s * (1.0 + x * (1.0 - s))

def prelu(x: float, a: float) -> float:
    """Parametric ReLU."""
    return max(0.0, x) + a * min(0.0, x)
def d_prelu(x: float, a: float) -> float:
    """Derivative of PReLU with respect to x. Note: you will also need a gradient w.r.t 'a' during backprop!"""
    return 1.0 if x > 0 else a

def cdelu(x: float, alpha: float = 1.0) -> float:
    """Continuously Differentiable Exponential Linear Unit (CELU)."""
    return max(0.0, x) + min(0.0, alpha * (math.expm1(x / alpha)))
def d_cdelu(x: float, alpha: float = 1.0) -> float:
    """Derivative of the CELU activation function."""
    return 1.0 if x > 0 else math.exp(x / alpha)

def sigmoid(x: float) -> float:
    """Returns the Sigmoid activation of x with overflow protection."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    else:
        z = math.exp(x)
        return z / (1.0 + z)
def d_sigmoid(x: float) -> float:
    """Returns the derivative of the Sigmoid activation function."""
    s = sigmoid(x)
    return s * (1.0 - s)

def tanh(x: float) -> float:
    """Returns the Tanh activation of x using a numerically stable approach."""
    return math.tanh(x)
def d_tanh(x: float) -> float:
    """Returns the derivative of the Tanh activation function."""
    t = tanh(x)
    return 1.0 - t**2

def swish(x: float, β: float = 1.0) -> float:
    """Swish activation function."""
    return x * sigmoid(x * β)
def d_swish(x: float, β: float = 1.0) -> float:
    """Derivative of the Swish activation function."""
    s = sigmoid(x * β)
    return s + (β * x * s * (1.0 - s))

def mish(x: float) -> float: 
    """A self-regularized, smooth, non-monotonic activation function."""
    try:
        softplus = math.log1p(math.exp(x)) if x < 20 else x
    except OverflowError:
        softplus = x
    return x * tanh(softplus)
def d_mish(x: float) -> float:
    """Derivative of the Mish activation function."""
    try:
        ex = math.exp(x)
    except OverflowError:
        return 1.0  # Becomes linear at large positive values
    
    omega = 4.0 * (x + 1.0) + 4.0 * ex**2 + ex**3 + ex * (4.0 * x + 6.0)
    delta = 2.0 * ex + ex**2 + 2.0
    return (ex * omega) / (delta**2)

def softmax(Z: xp.ndarray) -> xp.ndarray:
    """Softmax activation function for multi-class classification. Converts raw scores (logits) into probabilities."""
    exp_z = xp.exp(Z - xp.max(Z, axis=-1, keepdims=True))
    return exp_z / xp.sum(exp_z, axis=-1, keepdims=True)

### PERFORMANCE METRICS

def mae(actual: xp.ndarray, pred: xp.ndarray) -> float:
    """Mean Absolute Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")
    
    return (sum((xp.abs(actual[i] - pred[i])) for i in range(len(actual)))) / len(actual)
def mse(actual: xp.ndarray, pred: xp.ndarray) -> float:
    """Mean Squared Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")
    
    return (sum(xp.mean((actual[i] - pred[i])**2) for i in range(len(actual)))) / len(actual)
def rmse(actual: xp.ndarray, pred: xp.ndarray) -> float:
    """Root Mean Squared Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")
    
    return xp.sqrt(mse(actual, pred))

def cross_entropy_loss(actual: xp.ndarray, pred: xp.ndarray) -> float:
    """Cross-entropy loss function for multi-class classification."""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")
    
    array_len = actual.shape[0]
    softmax_pred = softmax(pred)
    clipped_pred = xp.clip(softmax_pred, 1e-15, 1 - 1e-15)
    log_likelihood = -(xp.log(clipped_pred[range(array_len), actual.argmax(axis=1)]))
    return xp.sum(log_likelihood) / array_len



