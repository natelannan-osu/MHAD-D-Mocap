import sys
import numpy as np
import scipy.io as io
import argparse

#convert numpy .npz files to matlab .mat files
def parse_args():
    parser = argparse.ArgumentParser(description='simple npz to mat converter.  requirements - numpy, scipy')
    parser.add_argument('--npz', '-n', type=str, help='npz file to be converted.  Option required')
    parser.add_argument('--var', '-v', default='data', type=str, help='Name of variable to be converted in npz file.  default - data')
    parser.add_argument('--mat', '-m', default='', type=str, help='destination for resulting mat file.  without this option the .mat file will be named the same as the original npz file.')
    parser.add_argument('--matrix', '-x', default='convertedData', type=str, help='Name of matrix inside matlab.  defualt - convertedData')
    args = parser.parse_args()
    return args

args = parse_args()

if args.mat == '':
    args.mat = args.npz[:-3]+"mat"
    
data = np.load(args.npz)[args.var]
io.savemat(args.mat,{args.matrix:data})
