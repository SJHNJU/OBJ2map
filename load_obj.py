import os
import numpy as np


# 输入：(str) OBJ文件里的一行
# 输出：(str) 该行的报头(v/vt/f)
def find_header(l):
    h = ''
    for c in range(0, len(l)):
        if l[c] != ' ':
            h += l[c]
        else:
            return h    


# 输入：(str) 报头为v的一行
# 输出：(float, float, float) 该点的xyz空间坐标
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


# 输入：(str) 文件名
# 输出：(int, int, int) v, vt, f在文件里的行号
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


# 输入：(str) 报头为f的一行
# 输出：(int, int, int) 该面片引用的角点索引
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




# 输入：(str) 文件名
# 输出：(numpy) 角点的数量x3 角点的XYZ坐标
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



# 输入：(str) 文件名
# 输出：(numpy) 大小：面的数量x3；从文件里第一个面开始所有面的顶点索引
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




# 输入：(str) 文件名
# 输出：(numpy, numpy) 大小：点的数量x3；从文件里第一个点开始所有点的xyz坐标
#                     大小：面的数量x3；从文件里第一个面开始所有面的顶点索引
def load_obj(filename):
    return get_node_xyz_as_np(filename), get_v_idx_in_f(filename)
