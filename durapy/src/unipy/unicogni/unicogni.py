"""
The DuraPy UniCogni Package for Machine Learning.
"""

USE_GPU = False  # Set to True on CUDA-compatible machine

if USE_GPU:
    import cupy as xp # type: ignore # 'xp' stands for cross-platform (numpy/cupy)
else:
    import numpy as xp

from scipy import special
from ...commons.constants import PI

### ACTIVATION FUNCTIONS

def relu(x: xp.ndarray) -> xp.ndarray:
    """Returns the Rectified Linear Unit activation of x."""
    return xp.maximum(0.0, x)
def d_relu(x: xp.ndarray) -> xp.ndarray:
    """Returns the derivative of the Rectified Linear Unit activation function."""
    return (x > 0).astype(xp.float32)

def leaky_relu(x: xp.ndarray) -> xp.ndarray:
    """Returns the Leaky ReLU activation of X."""
    return xp.maximum(0.01 * x, x)
def d_leaky_relu(x: xp.ndarray) -> xp.ndarray:
    """Returns the derivative of the Leaky ReLU activation function."""
    return xp.where(x > 0, 1.0, 0.01).astype(xp.float32)

def gelu(x: xp.ndarray) -> xp.ndarray:
    """Gaussian Error Linear Unit using the tanh approximation."""
    return 0.5 * x * (1.0 + tanh(xp.sqrt(2.0 / PI) * (x + 0.044715 * x**3)))
def d_gelu(x: xp.ndarray) -> xp.ndarray:
    """Derivative of GELU."""
    try:
        gauss = xp.exp(-0.5 * x**2)
    except OverflowError:
        gauss = 0.0
    cdf = 0.5 * (1.0 + special.erf(x / xp.sqrt(2)))
    pdf = (1.0 / xp.sqrt(2 * PI)) * gauss
    return cdf + x * pdf

def silu(x: xp.ndarray) -> xp.ndarray:
    """Sigmoid Linear Unit."""
    return x * sigmoid(x)
def d_silu(x: xp.ndarray) -> xp.ndarray:
    """Derivative of the SiLU activation function."""
    s = sigmoid(x)
    return s * (1.0 + x * (1.0 - s))

def prelu(x: xp.ndarray, a: float) -> xp.ndarray:
    """Parametric ReLU."""
    return xp.maximum(0.0, x) + a * xp.minimum(0.0, x)
def d_prelu(x: xp.ndarray, a: float) -> xp.ndarray:
    """Derivative of PReLU with respect to x. Note: you will also need a gradient w.r.t 'a' during backprop!"""
    return xp.where(x > 0, 1.0, a)

def cdelu(x: xp.ndarray, alpha: float = 1.0) -> xp.ndarray:
    """Continuously Differentiable Exponential Linear Unit (CELU)."""
    return xp.maximum(0.0, x) + xp.minimum(0.0, alpha * xp.expm1(x / alpha))
def d_cdelu(x: xp.ndarray, alpha: float = 1.0) -> xp.ndarray:
    """Derivative of the CELU activation function."""
    return xp.where(x > 0, 1.0, xp.exp(x / alpha))

def sigmoid(x: xp.ndarray) -> xp.ndarray:
    """Returns the Sigmoid activation of x with overflow protection."""
    return xp.where(x >= 0, 1.0 / (1.0 + xp.exp(-x)), xp.exp(x) / (1.0 + xp.exp(x)))
def d_sigmoid(x: xp.ndarray) -> xp.ndarray:
    """Returns the derivative of the Sigmoid activation function."""
    s = sigmoid(x)
    return s * (1.0 - s)

def tanh(x: xp.ndarray) -> xp.ndarray:
    """Returns the Tanh activation of x using a numerically stable approach."""
    return xp.tanh(x)
def d_tanh(x: xp.ndarray) -> xp.ndarray:
    """Returns the derivative of the Tanh activation function."""
    t = tanh(x)
    return 1.0 - t**2

def swish(x: xp.ndarray, β: float = 1.0) -> xp.ndarray:
    """Swish activation function."""
    return x * sigmoid(x * β)
def d_swish(x: xp.ndarray, β: float = 1.0) -> xp.ndarray:
    """Derivative of the Swish activation function."""
    s = sigmoid(x * β)
    return s + (β * x * s * (1.0 - s))

def mish(x: xp.ndarray) -> xp.ndarray:
    """A self-regularized, smooth, non-monotonic activation function."""
    softplus = xp.where(x < 20.0, xp.log1p(xp.exp(x)), x)
    return x * tanh(softplus)
def d_mish(x: xp.ndarray) -> xp.ndarray:
    """Derivative of the Mish activation function."""
    try:
        ex = xp.exp(x)
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
    
    return sum(xp.abs(actual - pred)) / len(actual)
def mse(actual: xp.ndarray, pred: xp.ndarray) -> float:
    """Mean Squared Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")
    
    return sum(xp.mean(actual - pred)**2) / len(actual)
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
    clipped_pred = xp.clip(softmax(pred), 1e-15, 1 - 1e-15)
    log_likelihood = -(xp.log(clipped_pred[range(array_len), actual.argmax(axis=1)]))
    return xp.sum(log_likelihood) / array_len



