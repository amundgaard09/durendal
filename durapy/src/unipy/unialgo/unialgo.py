"""
The `AWPC` `UniAlgo` module. 
This module contains a collection of mathematical algorithms that are used throughout the `AWPC` library, 
such as the Fibonacci sequence generator and Lovelace's algorithm for solving systems of linear equations.
"""

def fibonacci_list(ListLength: float) -> list[int]:
    """Fibonacci sequence generator that returns a list of the sequence up to the given length."""
    
    try:
        ListLength = int(ListLength)  
    except ValueError:
        raise ValueError("FibonacciInteger does not take floats or strings!")      
    
    fib0, fib1 = 0, 1
    FiboList = [fib0, fib1]
    
    if ListLength < 2:
        raise ValueError("FibonacciList does not take integers less than 2!")
    
    for _ in range(0, (ListLength - 2)):
        fib2 = fib0 + fib1
        fib0, fib1 = fib1, fib2
        FiboList.append(fib2)
        
    return FiboList   
def fibonacci_integer(FiboIndex: float) -> int:
    """Fibonacci integer generator that returns the Fibonacci integer at the given index.""" 
    
    try:
        FiboIndex = int(FiboIndex)  
    except ValueError:
        raise ValueError("FibonacciInteger does not take floats or strings!") 
    
    if FiboIndex < 2:
        raise ValueError("FibonacciInteger does not take integers less than 2!")
    
    if FiboIndex == 2:
        return 1  
      
    fib0, fib1, fib2 = 0, 1, 1
    
    for _ in range(0, (FiboIndex - 2)):
        fib2 = fib0 + fib1
        fib0, fib1 = fib1, fib2
        
    return fib2

def lovelace(a: float, b: float, c: float, d: float, e: float, f: float) -> tuple:
    """Lovelace's algorithm for solving systems of linear equations."""
    if a*e == b*d: 
        raise ValueError("The system has no unique solution.")
    
    Dx = c*e - b*f
    Dy = a*f - c*d
    x = Dx / (a*e - b*d)
    y = Dy / (a*e - b*d)
    return (x, y)
