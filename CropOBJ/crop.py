import os
import numpy as np
import argparse

from idx_to_path import *

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
# Usage: python crop.py -pidx ${pidx} -eidx ${eidx}
# Input: people index; expression index
#
# Output: face part model in OBJ format
#
# Author: SJH
#
# Date: 19/07/14
#


def find_header(l):
    h = ''
    for c in range(0, len(l)):
        if l[c] != ' ':
            h += l[c]
        else:
            return h    

def v_xyz(l):
    seg1 = ''
    seg2 = ''
    seg3 = ''
    blankId = []
    for c in range(0, len(l)):
        if l[c] == ' ':
            blankId.append(c)
    
    for c in range(blankId[0]+1, blankId[1]):
        seg1 += l[c]
    for c in range(blankId[1]+1, blankId[2]):
        seg2 += l[c]
    for c in range(blankId[2]+1, len(l)-1):
        seg3 += l[c]
    return float(seg1), float(seg2), float(seg3)

# return the x,y,z coordinate of v
def vt_xyz(l):
    seg1 = ''
    seg2 = ''
    blankId = []
    for c in range(0, len(l)):
        if l[c] == ' ':
            blankId.append(c)
    
    for c in range(blankId[0]+1, blankId[1]):
        seg1 += l[c]
    for c in range(blankId[1]+1, blankId[2]):
        seg2 += l[c]
    return float(seg1), float(seg2)

def get_idx(seg):
    idx = ''
    for c in range(0, len(seg)):
        if seg[c] != '/':
            idx += seg[c]
        else:
            return int(idx)

def face_v_index(l):
    seg1 = ''
    seg2 = ''
    seg3 = ''
    blankId = []
    slashId = []
    for c in range(0, len(l)):
        if l[c] == ' ':
            blankId.append(c)
        if l[c] == '/':
            slashId.append(c)

    for c in range(blankId[0]+1, slashId[0]):
        seg1 += l[c]
    for c in range(blankId[1]+1, slashId[1]):
        seg2 += l[c]
    for c in range(blankId[2]+1, slashId[2]):
        seg3 += l[c]
    
    return int(seg1), int(seg2), int(seg3)


# return the start line idx of v, vt, f
def get_v_vt_f_startIdx(file_name):
    v_startIdx, cntv = 0, 0
    vt_startIdx, cntvt = 0, 0
    f_startIdx, cntf = 0, 0
    with open(file_name) as f:
        ls = f.readlines()
        for l_idx in range(0, len(ls)):
            h = find_header(ls[l_idx])
            if h == 'v' and cntv == 0:
                v_startIdx = l_idx
                cntv = 1
            if h == 'vt' and cntvt == 0:
                vt_startIdx = l_idx
                cntvt = 1
            if h == 'f' and cntf == 0:
                f_startIdx = l_idx
                cntf = 1
    return v_startIdx+1, vt_startIdx+1, f_startIdx+1


# get vertex coordinate in numpy format
def get_node_xyz_as_np(file_name):
    v_s, vt_s, _ = get_v_vt_f_startIdx(file_name)
    rows = vt_s - v_s
    node_xyz = np.zeros([rows, 3])
    with open(file_name) as f:
        lines = f.readlines()
        for line_idx in range(1, vt_s):
            line = lines[line_idx]
            h = find_header(line)
            if h == 'v':
                x, y, z = v_xyz(line)
                node_xyz[line_idx-1, 0] = x
                node_xyz[line_idx-1, 1] = y
                node_xyz[line_idx-1, 2] = z
            
    return node_xyz

# return face in numpy, which is the index of v of each face
def get_v_idx_in_f(file_name):
    _, _, f_s = get_v_vt_f_startIdx(file_name)
    with open(file_name) as f:
        lines = f.readlines()
        face = np.zeros([len(lines)+2-f_s, 3], int)
        for line_idx in range(f_s-1, len(lines)):
            v1, v2, v3 = face_v_index(lines[line_idx])
            face[line_idx +1 - f_s, 0] = v1
            face[line_idx +1 - f_s, 1] = v2
            face[line_idx +1 - f_s, 2] = v3

    return face


def dis_between_node(node1, node2):
    tmp = node1 - node2
    tmp = tmp * tmp
    dis = sum(tmp)
    dis = dis ** 0.5
    return dis

def find_nose_tip(node_xyz):
    max_z = node_xyz[:, 2].max()
    row = np.where(node_xyz[:, 2] == max_z)[0]
    row = row[0]

    nose_tip = node_xyz[row, :]
    return nose_tip, row

# return selected node's index in OBJ file
def find_node_in_radius(node_xyz, nose_tip, radius, file_name):
    v_s, _, _ = get_v_vt_f_startIdx(file_name)
    rows, _ = node_xyz.shape[0], node_xyz.shape[1]
    selected_node_idx = []
    for row in range(0, rows):
        node = node_xyz[row, :]
        dis = dis_between_node(nose_tip, node)
        if dis < radius:
            selected_node_idx.append(row+v_s-1)

    return selected_node_idx


def get_selected_face_idx(file_name, selected_node_idx):
    _, _, f_s = get_v_vt_f_startIdx(file_name)
    print('getting face')
    face = get_v_idx_in_f(file_name)
    print('Got face nodes, selecting face')

    face_row, _ = np.where(face == selected_node_idx[0])

    print(len(selected_node_idx))
    for i in range(0, len(selected_node_idx)):
        node_idx = selected_node_idx[i]
        this_face_row, _ = np.where(face == node_idx)

        if i % 1000 == 0:
            print(i)
        face_row = np.union1d(face_row,this_face_row)
    
    print('faces are selected')
    face_row += f_s - 1

    return list(face_row)



if __name__ == '__main__':
    for pidx in range(102, 121):
        for eidx in range(1, 21):
            # Configure model path here
            file_name, file_save_name = idx_to_path(pidx, eidx)
            if os.path.exists(file_name):
                print('Cropping '+file_name+' ...')

                with open(file_name) as f:
                    lines =  f.readlines()

                    node_xyz = get_node_xyz_as_np(file_name)
                    
                    # delete some bad part
                    new_node_xyz = node_xyz.copy()
                    new_node_xyz[new_node_xyz[:, 1] < -100] = 0
                    new_node_xyz[new_node_xyz[:, 1] > 150] = 0
                    new_node_xyz[new_node_xyz[:, 0] > 95] = 0

                    nose_tip, _ = find_nose_tip(new_node_xyz)

                    print('selecting nodes')
                    selected_node_idx = find_node_in_radius(node_xyz, nose_tip, 90, file_name)

                    print('selecting faces')
                    face_idx = get_selected_face_idx(file_name, selected_node_idx)
                    v_s, vt_s, f_s = get_v_vt_f_startIdx(file_name)

                    print('writing v and vt')
                    with open(file_save_name, 'a+') as new_f:
                        for line_idx in range(0, f_s-1):
                            l = lines[line_idx]
                            new_f.write(l)
                    
                    print('writing face')
                    with open(file_save_name, 'a+') as new_f:
                        for f_idx in face_idx:  
                            line = lines[f_idx]
                            new_f.write(line)
            else:
                print(file_name+' not exist')
                
                        