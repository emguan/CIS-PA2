'''
Calculated expected C given calbody and calreadings data.

Usage: 
python -m scripts.calibrate_expected --calbody ./data/pa1-unknown-k-calbody.txt --calreadings ./data/pa1-unknown-k-calreadings.txt --output pa1-unknown-k-output-1.txt

Author: Emily Guan
'''

import argparse
import os
import numpy as np

from utils.helpers import arr_to_points
from utils.read_write import read_calbody, read_calreadings, write_expected_C_txt
from utils.math_package import Transformations, Points, Rotations
from utils.registration import rigid_transformation

'''
Main executing function of file, takes in calibration bodies and frames, and makes predicted C.

Based off of Professor Taylor's slides
'''
def calibrate(d, a, c,
              D_frames: list[np.ndarray],
              A_frames: list[np.ndarray]) :
o


    return C_pred

"""
Calculate mean error (euclidean and RMS) vs ground truth C from calreadings.
"""
def print_error(C_frames, C_pred):

    per_frame_means = []
    per_frame_rms   = []

    for i, (Cp, Cgt) in enumerate(zip(C_pred, C_frames)):
        diffs = Cp - Cgt
        dists = np.linalg.norm(diffs, axis=1)  #euclidean error
        per_frame_means.append(dists.mean())
        per_frame_rms.append(np.sqrt(np.mean(dists**2))) #RMS error
        print(f"Frame {i:03d}: mean_err = {dists.mean():.6f} mm   rms = {np.sqrt(np.mean(dists**2)):.6f} mm")

    overall_mean = float(np.mean(per_frame_means))
    overall_rms  = float(np.mean(per_frame_rms))
    print(f"overall mean error = {overall_mean:.6f} mm")
    print(f"overall RMS error  = {overall_rms:.6f} mm")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute expected C marker positions per frame (PA1 Part 4).")
    parser.add_argument("--calbody", required=True, help="Path to name-calbody.txt")
    parser.add_argument("--calreadings", required=True, help="Path to name-calreadings.txt")
    parser.add_argument("--output", default=None, help="Optional path to write results (txt)")
    args = parser.parse_args()

    # read calibration
    d_cal, a_cal, c_cal, ND, NA, NC = read_calbody(args.calbody)

    # read frames
    D_frames, A_frames, C_frames, Nframes = read_calreadings(args.calreadings, ND, NA, NC)

    d = np.array([[p.x, p.y, p.z] for p in d_cal], dtype=float)
    a = np.array([[p.x, p.y, p.z] for p in a_cal], dtype=float)
    c = np.array([[p.x, p.y, p.z] for p in c_cal], dtype=float)

    D_frames = [np.array([[p.x, p.y, p.z] for p in frame], dtype=float) for frame in D_frames]
    A_frames = [np.array([[p.x, p.y, p.z] for p in frame], dtype=float) for frame in A_frames]
    C_frames = [np.array([[p.x, p.y, p.z] for p in frame], dtype=float) for frame in C_frames]

    # predict C
    C_pred = calibrate(d, a, c, D_frames, A_frames)
    print_error(C_frames, C_pred)

    #write
    out_path = args.output
    write_expected_C_txt(out_path, C_pred)