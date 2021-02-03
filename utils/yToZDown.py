import numpy as np
import scipy.io as io
import argparse, textwrap

#convert npz matrices defined as Y down to Z down.

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-f", type=str,
    help=textwrap.dedent('npz file to convert to Z down.  This option is required'))
parser.add_argument("-v", type=str, default = 'data',
    help=textwrap.dedent('variable name in npz file to convert.  default - data'))                
parser.add_argument("-n", type=str, default="",
    help=textwrap.dedent('Name of destination file.'))
parser.add_argument("-m", action='store_true', 
    help=textwrap.dedent('convert output to mat.'))
parser.add_argument("-x", type=str, default="",
    help=textwrap.dedent('Name of Matlab matrix in file (ignored if -m option not used).'))
args = parser.parse_args()

if args.n == "":
    baseName = args.f[:-4]
    destination = baseName+"_zdown"
    if args.m:
        destination = destination+".mat"
    else:
        destination = destination+".npz"
else:
    destination = args.n


data = np.load(args.f)[args.v]
zDown = np.empty(data.shape)
zDown[:,:,0] = data[:,:,2]
zDown[:,:,1] = data[:,:,0]
zDown[:,:,2] = data[:,:,1]

if args.m:
    io.savemat(destination,{args.x:zDown})
else:
    np.savez_compressed(destination, data = zDown)
