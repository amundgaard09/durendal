
from core.utilities.txtfiletools import log as dec_log
import functools
import time

def logger(func):
    """A decorator that logs function arguments, execution time, and errors."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dec_log(f"Starting {func.__name__} with args={args}, kwargs={kwargs} \n")
        
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            
            dec_log(f"Finished {func.__name__} in {duration:.4f}s. Result: {result} \n")
            return result
            
        except Exception as e:
            duration = time.perf_counter() - start_time
            
            dec_log(f"Failed {func.__name__} after {duration:.4f}s. Error: {e} \n")
            raise
            
    return wrapper

