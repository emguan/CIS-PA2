"""
Pivot Calibration (algorithm from Professor Taylor).

Author: Emily Guan
"""

import numpy as np

def pivot_calibration(R_list: list[np.ndarray], t_list: list[np.ndarray]):

    #solving Ax = b where A = R | -I, x = tip/post, b = -p
    
    pts = len(R_list)

    A = np.zeros((3*pts, 6), dtype=float)
    b = np.zeros((3*pts, 1), dtype=float)

    for i in range(pts):
        R = R_list[i]
        t = t_list[i]
        
        #horizontal concat of R|-I
        A[3*i:3*i+3, 0:3] = R 
        A[3*i:3*i+3, 3:6] = -np.eye(3)

        b[3*i:3*i+3, 0] = -t

    #least squares method courtsey of numpy: https://numpy.org/doc/2.3/reference/generated/numpy.linalg.lstsq.html
    x, res, rank, s = np.linalg.lstsq(A, b)

    b_tip = x[0:3, 0]
    b_post = x[3:6, 0]

    #to evaluate lstsq, you can use residuals, res from lstsq gives us sum of squared residuals, so we can reverse backwards to get residuals
    if res.size > 0:
        score = float(np.sqrt(res[0] / pts))
    
    else:
        # iff system is perfect fit
        score = float(np.sqrt(np.mean((A @ x - b)**2)))

    print(f"RES SCORE PIVOT: {score}")

    return b_tip, b_post, score