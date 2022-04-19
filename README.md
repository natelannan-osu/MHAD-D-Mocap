# MHAD-D-Mocap
This repository holds the D-Mocap data which extends the MHAD dataset.

Data exists in two directories:
* Front-Facing - D-Mocap data derived from the front-facing MHAD depth images with time synchronized optical mocap frames.
* Rear-Facing - D-Mocap data derived from the rear-facing MHAD depth images with time synchronized optical mocap frames.

A utils directory includes simple python scripts for doing useful things:
* matToNpz.py - converting a matlab .mat file to a numpy .npz
* npzToMat.py - converting a numpy .npz file to a matlab .mat file
* viewSkeleton.py - simple tool to plot frames of a human motion file
* yToZDown.py - convert a y-down file to z-down

If you use this dataset please reference the folowing paper:

@InProceedings{lannan,
author = {Lannan, Nate and Zhou, Le and Fan, Guoliang},
title = {A Multiview Depth-based Motion Capture Benchmark Dataset for Human Motion Denoising and Enhancement Research},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR) Workshops},
month = {June},
year = {2022}
}
