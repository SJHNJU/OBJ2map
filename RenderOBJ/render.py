import os
import argparse
import sys

from crop_img import *
from idx_to_path import *

###
# Render cropped face model into RGB picture
# Usage: python render.py -pidx ${pidx} -eidx ${eidx}
# Input: people index; expression index
#
# Output: Rendered RGB picture of human face 
#
# Author: Jiahui She
#
# Date: 2019/07/16
#
###


parser = argparse.ArgumentParser()
parser.add_argument('-pidx',type=int)
parser.add_argument('-eidx',type=int)
args = parser.parse_args()

# Configure model path here
model_path, img_save_dir, img_save_path = idx_to_path(args.pidx, args.eidx)

if not os.path.exists(model_path):
    print(model_path+' do not exists')
    sys.exit(0)

print('Rendering '+model_path)
import trimesh
import pyrender
import scipy.misc

fuze_trimesh = trimesh.load(model_path)
mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
scene = pyrender.Scene()
scene.add(mesh)

# yfov: vertical field of view
# aspectRatio: to make things look smaller when they are farther
camera = pyrender.PerspectiveCamera(yfov=np.pi/4, aspectRatio=1.0)


# the point where the viewpoint is
# you need to get higher->larger in Z to look the whole face.
camera_pose = np.array([
    [1.0,  0.0, 0.0, 0.0],
    [0.0,  1.0, 0.0, 0.0],
    [0.0,  0.0, 1.0, 300.0],
    [0.0,  0.0, 0.0, 1.0],
 ])

scene.add(camera, pose=camera_pose)

dl = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=8.0)
scene.add(dl, pose=camera_pose)


r = pyrender.OffscreenRenderer(400, 400)
color, depth = r.render(scene)

crop_color = crop_img(color)

if not os.path.exists(img_save_dir):
    os.mkdir(img_save_dir)

scipy.misc.imsave(img_save_path, crop_color)

print(model_path+ ' is rendered')

sys.exit(0)