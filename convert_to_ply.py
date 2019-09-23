# 输入(numpy, list, 文件名) 全部顶点的空间坐标，被选择的顶点的索引（从1开始），ply文件名
# 输出（file）保存下的点云文件
def convert_to_ply(node_xyz, selected_node_idx, filename):
    num = len(selected_node_idx)

    lines = ['ply\n', 'format ascii 1.0\n', 'element vertex {0}\n'.format(num)]
    lines.append('property double x\n')
    lines.append('property double y\n')
    lines.append('property double z\n')
    lines.append('end_header\n')

    for i in range(0, num):
        xyz = node_xyz[selected_node_idx[i]-1, :]
        lines.append('{0} {1} {2}\n'.format(xyz[0], xyz[1], xyz[2]))

    with open(filename, 'a+') as f:
        for line in lines:  
            f.write(line)
