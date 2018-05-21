# -*- coding:utf-8 -*-
import math
import copy

'''
Node类
用于表示A*搜索的中间状态
'''
class Node(object):
    def __init__(self, graph, depth=0):
        self.graph = graph # 3*3 表格，保存当前的状态
        self.depth = depth # depth是从初始状态移动到当前状态移动的部署，即g(n)
    
    def print_graph(self):
        # 打印当前状态的棋盘布局
        for i in range(3):
            print "%s|%s|%s" % (str(self.graph[i][0]), str(self.graph[i][1]), str(self.graph[i][2]))
            if i != 2:
                print "- - -"

# 计算曼哈顿距离
def manhattan_distance(point_x, point_y):
    return math.fabs(point_x[0] - point_y[0]) + math.fabs(point_x[1] - point_y[1])

# 启发式函数
def h(status):
    h = 0
    # 计算status布局下每一个数值到其最终所在位置的曼哈顿距离
    for i in range(3):
        for j in range(3):
            num = status[i][j]
            if num == 0:
                continue
            standard_pos = (
                (num-1) // 3,
                (num-1) % 3
            )# 数字num的标准位置坐标
            h += manhattan_distance((i,j), standard_pos)
    return h

# 计算获取相邻状态
def get_neibors(node):
    neibors = []
    status = node.graph
    # 先定位空格所在位置
    for i in range(3):
        for j in range(3):
            if status[i][j] == 0:
                space_pos = (i,j)
    # 枚举四个可能方向的向量
    directions = (
        [0,1], [0,-1], [1,0], [-1,0]
    )
    for direction in directions:
        neibor_x = space_pos[0] + direction[0]
        neibor_y = space_pos[1] + direction[1]
        # 保证没有越界
        if neibor_x in range(3) and neibor_y in range(3):
            new_status = copy.deepcopy(status) # 注意这里一定要用深拷贝
            # 移动
            new_status[space_pos[0]][space_pos[1]] = new_status[neibor_x][neibor_y]
            new_status[neibor_x][neibor_y] = 0
            neibors.append(Node(new_status, node.depth + 1))
    
    return neibors

def solve(initial_node):
    if h(initial_node.graph) == 0:
        print 'arrived final status'
        initial_node.print_graph()
        return
    close = [initial_node]
    open = get_neibors(initial_node)
    # 终止搜索的两个条件：close中包含终点，或open为空
    while len(open) > 0:
        min_h = 999999
        next_index = -1
        for i in range(len(open)):
            # 选取h最小的
            next = open[i]
            print 'searching depth = ' + str(next.depth)
            next.print_graph()
            temp_h = h(next.graph)
            if temp_h < min_h:
                min_h = temp_h
                next_index = i
        if next_index >= 0:
            if min_h == 0:
                close.append(open[next_index])
                print 'final status arrived'
                return
            close.append(open[next_index])
            open = get_neibors(open[next_index])

if __name__ == "__main__":
    inital_status = [
        [1,2,3],
        [4,5,0],
        [7,6,8]
    ]
    initial_node = Node(inital_status, 0)
    solve(initial_node)