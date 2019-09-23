#coding:utf-8
import os
import numpy as np
import argparse

from load_obj import *
from convert_to_ply import *
from load_path import *

# Crop face part from the whole OBJ model
# OBJ format:
#   v
#   v
#   ...
#   v
#   vt
#   ...
#   vt
#   f ${index of v which from 1}/${index of vt which from 1} ...
#   f
#   ...
#   f
#
# Output: face part model in OBJ format
#
# Author: SJH
#
# Date: 19/07/14
#

def dis_between_node(node1, node2):
    tmp = node1 - node2
    tmp = tmp * tmp
    dis = sum(tmp)
    dis = dis ** 0.5
    return dis


# 输入：(numpy) 点的xyz空间坐标
# 输出：(3x1numpy) 鼻尖点空间坐标
def find_nose_tip(node_xyz):
    max_z = node_xyz[:, 2].max()
    row = np.where(node_xyz[:, 2] == max_z)[0]
    row = row[0]

    nose_tip = node_xyz[row, :]
    return nose_tip


# return selected node's index in OBJ file
# 输入：(numpy, numpy, float, str)
# 输出: (list) 被选中的点在点集中的索引，从1开始
def find_node_in_radius(node_xyz, nose_tip, radius):
    rows, _ = node_xyz.shape[0], node_xyz.shape[1]
    selected_node_idx = []
    for row in range(0, rows):
        node = node_xyz[row, :]
        dis = dis_between_node(nose_tip, node)
        if dis < radius:
            selected_node_idx.append(row+1)

    return selected_node_idx



# 输入：(str, list) OBJ文件名，被选择的点的序号列表
# 输出：(list) 被选择的面在OBJ文件里的行号
def get_selected_face_idx(file_name, face, selected_node_idx):
    _, _, f_s = get_v_vt_f_startIdx(file_name)

    face_row, _ = np.where(face == selected_node_idx[0])

    for i in range(0, len(selected_node_idx)):
        node_idx = selected_node_idx[i]
        this_face_row, _ = np.where(face == node_idx)
        face_row = np.union1d(face_row,this_face_row)

        if i % 1000 == 0:
            print('Processing {0} nodes'.format(i))
        
    face_row += f_s

    return list(face_row)



if __name__ == '__main__':
    # Configure model path here
    parser = argparse.ArgumentParser()
    parser.add_argument('-pidx',type=int)
    parser.add_argument('-eidx',type=int)
    args = parser.parse_args()

    file_name, file_save_name, plyname = load_path(args.pidx, args.eidx)


    # 开始裁剪
    if os.path.exists(file_name):
        print('Cropping '+file_name+' ...')

        print('Loading model')
        node_xyz, face = load_obj(file_name)

        print('Ignoring bad part')
        new_node_xyz = node_xyz.copy()
        new_node_xyz[new_node_xyz[:, 1] < -100] = 0
        new_node_xyz[new_node_xyz[:, 1] > 150] = 0
        new_node_xyz[new_node_xyz[:, 0] > 95] = 0

        nose_tip = find_nose_tip(new_node_xyz)

        print('Selecting needed nodes')
        selected_node_idx = find_node_in_radius(node_xyz, nose_tip, 120)
        print('find {0} nodes in total'.format(len(selected_node_idx)))

        print('Save to ply file')
        convert_to_ply(node_xyz, selected_node_idx, plyname)

        print('Selecting needed faces')
        face_idx = get_selected_face_idx(file_name, face, selected_node_idx)
        

        v_s, vt_s, f_s = get_v_vt_f_startIdx(file_name)
        with open(file_name) as f:
            lines =  f.readlines()

        print('Writing v and vt')
        # 把面以前的所有数据全部写入文件，没有删除角点等
        with open(file_save_name, 'a+') as new_f:
            for line_idx in range(0, f_s-1):
                l = lines[line_idx]
                new_f.write(l)
        
        # 选择lines里面对应编号的面写入文件
        print('Writing face')
        with open(file_save_name, 'a+') as new_f:
            for f_idx in face_idx:  
                line = lines[f_idx-1]
                new_f.write(line)
    else:
        print(file_name + ' does not exist')
                