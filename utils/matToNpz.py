import numpy as np
import scipy.io as spio
import argparse, textwrap

#convert mat files to npz.
#If mat file contains multiple matrices, all will be converted with their own file based on the name of the matrix in matlab

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-f", type=str,
    help=textwrap.dedent('Matlab file to convert to npz.  This option is required'))
parser.add_argument("-n", type=str, default="",
    help=textwrap.dedent('Name of destination npz file.'))
parser.add_argument("-m", type=str, default="",
    help=textwrap.dedent('Name of Matlab matrix in file.'))
parser.add_argument("-d", type=str, default="",
    help=textwrap.dedent('Destination directory.'))
args = parser.parse_args()

if args.n == "":
    baseName = args.f[:-3]
    destination = args.d+'/'+baseName+"npz"
else:
    destination = args.d+'/'+args.n

mat = spio.loadmat(args.f, squeeze_me=True)
if args.m == "":
    matrices = np.array(list(mat.keys()))
    if matrices.shape == (4,):
        nparr = mat[matrices[3]]
        np.savez_compressed(destination, data = nparr)
    else:
        for matrix in matrices:
            if matrix != '__header__' and matrix != '__version__' and matrix != '__globals__':
                nparr = mat[matrix]
                destination = args.d+'/'+matrix+'.npz'
                np.savez_compressed(destination, data = nparr)
else:
    nparr = mat[args.m]
    np.savez_compressed(destination, data = nparr)


