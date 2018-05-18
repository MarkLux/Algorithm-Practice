# -*- coding:utf-8 -*-
import random

'''
八皇后问题：爬山法求解
用一个一维的数组status保存8个皇后的位置信息
因为每一列一定有且只有一个皇后（否则冲突），有status[i] = j 表示第i列的皇后在第j行
'''

# 判断status布局下存在冲突的皇后对数
def get_conflict_queen_num(status):
    num = 0
    for i in range(len(status)):
        for j in range(i + 1, len(status)):
            if status[i] == status[j]:
                # 在同一行，不用判断同一列的情况
                num += 1
            offset = j - i
            if abs(status[i] - status[j]) == offset:
                # 在对角线上的情况，利用正方形 长 = 宽 的性质
                num += 1
    return num

# 使用爬山法选择status相邻所有状态中皇后冲突对数最小的状态
def hill_climbing(status):
    neibor_dict = {}
    '''
    邻居状态的枚举说明：
    考虑每一列的皇后仅在该列上移动，根据规则，皇后可以移动到该列的任意一个位置
    对于一个特定的局面，其所有的相邻状态即是将8列的所有皇后可移动的位置全部枚举一遍
    '''
    for col in range(len(status)):
        for row in range(len(status)):
            if status[col] == row:
                continue # 相当于该列的皇后没有移动
            status_copy = list(status) # 创建一个副本用于保存当前的邻居状态
            status_copy[col] = row # 将col列的皇后移动到row列
            neibor_dict[(col,row)] = get_conflict_queen_num(status_copy) # 保存所有邻居状态的皇后冲突对数    

    best_moves = [] # 保存最佳后继状态
    current_conflict_queen_num = get_conflict_queen_num(status)

    for k,v in neibor_dict.iteritems():
        if v < current_conflict_queen_num:
            current_conflict_queen_num = v # 找到所有后继中冲突对数最小的值
    for k,v in neibor_dict.iteritems():
        if v == current_conflict_queen_num:
            best_moves.append(k) # 将可能的最佳后继记录下来
    
    if len(best_moves) > 0:
        # 如果有多个可能的最佳后继，随机从中选择一个
        x = random.randint(0, len(best_moves) - 1)
        col = best_moves[x][0]
        row = best_moves[x][1]
        status[col] = row
    
    return status

# 使用爬山法求得满足八皇后问题的一个解，并输出每一次爬山选择的结果，直至没有冲突为止
def slove(status):
    while get_conflict_queen_num(status) > 0:
        status = hill_climbing(status)
        print "current climb: " + str(status)
        print "current conflict queen pairs: " + str(get_conflict_queen_num(status))

    print "answer :" + str(status)

if __name__ == "__main__":
    status = [0,1,2,3,4,5,6,7] # 初始布局
    slove(status)
    '''
    注意，爬山法并不保证能够找到解，很有可能在某个局部最优解处陷入死循环
    '''