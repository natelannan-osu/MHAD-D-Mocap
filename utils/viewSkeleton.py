import numpy as np
import scipy.io as spio
import sys
import argparse, textwrap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
from celluloid import Camera
import ast



def unpack(skeletonFile, joints):
    if skeletonFile.endswith('.mat'):
        mat = spio.loadmat(skeletonFile, squeeze_me=True)
        matrices = np.array(list(mat.keys()))
        skel = mat[matrices[3]]
    elif skeletonFile.endswith('.npz'):
        skel = np.squeeze(np.load(skeletonFile)['data'])
    else:
        sys.exit('file not mat or npz')
    if len(skel.shape) != 3:
        if len(skel.shape) != 2:
            print(skel.shape)
            sys.exit('skeleton file shape not supported')
        else:
            check = skel.shape.count(joints*3)
            if check == 0:
                sys.exit('there is no dimension which is jointNum*3 size in this ' \
                         '2 dimensional array.  make sure the number of joints ' \
                         'is correct.')
            elif check > 1:
                sys.exit('skeleton file has frames and joint dimentions which ' \
                         'are both 3*jointNum.  no way to differentiate which ' \
                         'dimension is frames and which is joints.')
            else:
                if skel.shape[0]//joints != 3:
                    skel = np.reshape(skel, (skel.shape[0],skel.shape[1]//3, 3))
                elif skel.shape[1]//joints != 3:
                    skel = np.reshape(skel, (skel.shape[0]//3,3,skel.shape[1]))
                
    jInd = skel.shape.index(joints)
    xyzInd = skel.shape.index(3)
    frInd = [i for i in range(3) if i not in [jInd, xyzInd]][0]
    skel = np.transpose(skel, (frInd, jInd, xyzInd))
    return skel
        

def plotSkel(skel1, skel2, joints, frStr, parents, view, video, noGrid, multicolor, joints2=0, parents2 = []):
    plt.style.use('seaborn')
    if joints2 == 0:
        joints2 = joints
    if parents2 == []:
        parents2 = parents
    if frStr == 'all':
        frames = [0, skel1.shape[0]]
    else:
        frames = [int(x) for x in frStr.split(':')]

    fig = plt.figure(1)
    camera = Camera(fig)
    ax = fig.add_subplot(111,projection='3d')
    ax.view_init(azim=view[0], elev=view[1])
    if noGrid:
        # Hide grid lines
        ax.grid(False)

        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    if len(parents) != joints:
        sys.exit('parent list is not same length as joints')
    if len(parents2) != joints2:
        sys.exit('parent2 list is not same length as joints2')

    if multicolor:
        colorMap1 = np.array(['k', u'#008000', u'#000080', u'#800000', u'#800080', u'#808000'])
        colorMap2 = np.array(['k', u'#008000', u'#000080', u'#800000', u'#800080', u'#808000'])
    else:
        colorMap1 = np.array(['b', 'b', 'b', 'b', 'b', 'b'])
        colorMap2 = np.array(['r', 'r', 'r', 'r', 'r', 'r'])
        
    if joints == 22:
        jCats1 = np.array([0,1,2,2,2,2,3,3,3,3,1,1,1,1,4,4,4,4,5,5,5,5])
        bCats1 = np.array([0,2,2,2,2,3,3,3,3,1,1,1,1,4,4,4,4,5,5,5,5])
    elif joints ==21:
        #jCats1 = np.array([1,2,2,2,2,3,3,3,3,1,1,1,1,4,4,4,4,5,5,5,5])
        jCats1 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        bCats1 = np.array([2,2,2,2,3,3,3,3,1,1,1,1,4,4,4,4,5,5,5,5])
    elif joints == 17:
        jCats1 = np.array([0,1,2,2,2,2,3,3,3,3,1,4,4,4,5,5,5])
        bCats1 = np.array([0,2,2,2,2,3,3,3,3,1,4,4,4,5,5,5])
    elif joints == 16:
        #jCats1 = np.array([1,2,2,2,2,3,3,3,3,1,4,4,4,5,5,5])
        jCats1 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        bCats1 = np.array([2,2,2,2,3,3,3,3,1,4,4,4,5,5,5])
    elif joints == 6:
        jCats1 = np.array([0,0,0,0,0,0])
        bCats1 = np.array([2,2,1,3,3]) 
    else:
        sys.exit('Skeleton 1: Color map for arbitrary skeleton shape is not currently supported.')
        
    if joints2 == 22:
        jCats2 = np.array([0,1,2,2,2,2,3,3,3,3,1,1,1,1,4,4,4,4,5,5,5,5])
        bCats2 = np.array([0,2,2,2,2,3,3,3,3,1,1,1,1,4,4,4,4,5,5,5,5])
    elif joints2 ==21:
        jCats2 = np.array([1,2,2,2,2,3,3,3,3,1,1,1,1,4,4,4,4,5,5,5,5])
        bCats2 = np.array([2,2,2,2,3,3,3,3,1,1,1,1,4,4,4,4,5,5,5,5])
    elif joints2 == 17:
        jCats2 = np.array([0,1,2,2,2,2,3,3,3,3,1,4,4,4,5,5,5])
        bCats2 = np.array([0,2,2,2,2,3,3,3,3,1,4,4,4,5,5,5])
    elif joints2 == 16:
        jCats2 = np.array([1,2,2,2,2,3,3,3,3,1,4,4,4,5,5,5])
        bCats2 = np.array([2,2,2,2,3,3,3,3,1,4,4,4,5,5,5])
    elif joints == 6:
        jCats1 = np.array([0,0,0,0,0,0])
        bCats1 = np.array([2,2,1,3,3])
    else:
        sys.exit('Skeleton 2: Color map for arbitrary skeleton shape is not currently supported.')

    for t in range(frames[0], frames[1]):
        
        for joint in range(joints):
            if joints != 17 and joints != 22:
                startJoint = 0
            else:
                startJoint = 1
            if joint > startJoint:
                ax.plot([skel1[t,parents[joint],0], skel1[t,joint,0]],
                        [skel1[t,parents[joint],1], skel1[t,joint,1]],
                        [skel1[t,parents[joint],2], skel1[t,joint,2]],
                        color=colorMap1[bCats1[joint-1]], linewidth=3.0)
        
        if skel2.size !=0:
            for joint2 in range(joints2):
                if joints2 != 17 and joints2 != 22:
                    startJoint = 0
                else:
                    startJoint = 1
                if joint2 > startJoint:
                    ax.plot([skel2[t,parents2[joint2],0], skel2[t,joint2,0]],
                            [skel2[t,parents2[joint2],1], skel2[t,joint2,1]],
                            [skel2[t,parents2[joint2],2], skel2[t,joint2,2]],
                            color=colorMap2[bCats2[joint2-1]], linewidth=3.0)
        ax.scatter(skel1[t,:,0], skel1[t,:,1], skel1[t,:,2], color=colorMap1[jCats1], alpha=1)#, marker = '.', s=320)
        if skel2.size != 0:
            ax.scatter(skel2[t,:,0], skel2[t,:,1], skel2[t,:,2], color=colorMap2[jCats2])
        camera.snap()
    animation = camera.animate()
    if video != '':
        animation.save(video)
    plt.show()





if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-s", type=str, help=textwrap.dedent('skeleton file.  can be .npz or ' \
                                                             '.mat and in cartesian coordinate form' \
                                                             'or condensed'))
    parser.add_argument("-f", type=str, default = 'all', help=textwrap.dedent('frames to display.  use form start:end or "all". default = all'))
    parser.add_argument("-j", type=int, default = 17, help=textwrap.dedent('number of joints.  default=17'))
    parser.add_argument("-m", type=str, default = '', help=textwrap.dedent('secondary skeleton file.  ' \
                                                                           'will display secondary skeleton \n' \
                                                                           'in the same manner as first ' \
                                                                           'skeleton on the same plot.'))
    parser.add_argument("-k", type=int, default = 0, help=textwrap.dedent('number of joints for secondary skeleton.  default=0'))
    parser.add_argument("-p", type=str, default = '[-1,0,1,2,3,4,1,6,7,8,1,10,11,12,10,14,15]',
                        help=textwrap.dedent('parent list for joints.  defines bone structure for skeleton. \n' \
                                             'for 16 joints:  [-1,0,1,2,3,0,5,6,7,0,9,10,11,9,13,14]\n' \
                                             'for 17 joints(default):  [-1,0,1,2,3,4,1,6,7,8,1,10,11,12,10,14,15]\n' \
                                             'for 21 joints:  [-1,0,1,2,3,0,5,6,7,0,9,10,11,11,13,14,15,11,17,18,19]\n' \
                                             'for 22 joints:  [-1,0,1,2,3,4,1,6,7,8,1,10,11,12,12,14,15,16,12,18,19,20]\n'))
    parser.add_argument("-q", type=str, default = '[]',
                        help=textwrap.dedent('parent list for joints2.  defines bone structure for skeleton2.  default = []\n' \
                                             'for 16 joints:  [-1,0,1,2,3,0,5,6,7,0,9,10,11,9,13,14]\n' \
                                             'for 17 joints:  [-1,0,1,2,3,4,1,6,7,8,1,10,11,12,10,14,15]\n' \
                                             'for 21 joints:  [-1,0,1,2,3,0,5,6,7,0,9,10,11,11,13,14,15,11,17,18,19]\n' \
                                             'for 22 joints:  [-1,0,1,2,3,4,1,6,7,8,1,10,11,12,12,14,15,16,12,18,19,20]\n'))
    parser.add_argument("-v", type=str, default = '', help=textwrap.dedent('name of mp4 file to save.  if empty, no file ' \
                                                                           'will be saved.  default is empty'))
    parser.add_argument("-g", action='store_true', help=textwrap.dedent('Hide grid'))
    parser.add_argument("-c", action='store_true', help=textwrap.dedent('use multicolor skeleton'))
    args = parser.parse_args()
    parents = ast.literal_eval(args.p)
    parents2 = ast.literal_eval(args.q)

    sk1 = np.array([])
    sk2 = np.array([])
    sk1 = unpack(args.s, args.j)
    if args.k == 0:
        args.k = args.j
    if args.q == '[]':
        args.q = args.p
    if args.m:
        sk2 = unpack(args.m, args.k)

    view=[-90,90]  #Y down
    #view=[0,0]  #Z down
    plotSkel(sk1, sk2, args.j, args.f, parents, view, args.v, args.g, args.c, joints2 = args.k, parents2 = parents2)
    
