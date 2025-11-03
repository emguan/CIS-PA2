"""
Helper to turn array to Points object. Pretty self explanatory??

Author: Emily Guan
"""

import numpy as np

from utils.math_package import Points

def arr_to_points(X: np.ndarray) -> list[Points]:
    return [Points(x=float(x), y=float(y), z=float(z)) for x,y,z in X]