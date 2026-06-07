
USE_GPU = False

if USE_GPU:
    import cupy as xp # type: ignore # type
else:
    import numpy as xp


    
