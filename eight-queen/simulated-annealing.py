# -*- coding:utf-8 -*-
import math
import random

'''
八皇后问题：模拟退火法求解
用一个一维的数组status保存8个皇后的位置信息
因为每一列一定有且只有一个皇后（否则冲突），有status[i] = j 表示第i列的皇后在第j行
'''

def get_temprature(t):
    '''
    温度随时间t(迭代次数)变化的函数
    '''
    return 36 / math.sqrt(t)

def get_accept_prob(delta_e, t):
    '''
    选择劣解的概率，e^(delta_e/T)
    delta_e为代价差（后继状态 - 当前状态）
    '''
    return math.pow(math.e, delta_e / get_temprature(t))

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

# 计算t时刻status布局下的后继状态
def simulated_annealing(status, t):
    neibor_dict = {}
    
    # 枚举所有相邻状态
    for col in range(len(status)):
        for row in range(len(status)):
            if status[col] == row:
                continue
            status_copy = list(status)
            status_copy[col] = row
            neibor_dict[(col,row)] = get_conflict_queen_num(status_copy)
    
    current_confict_num = get_conflict_queen_num(status)

    # 从所有相邻状态中随机挑选一个状态作为后继
    target_next = random.randint(0, len(neibor_dict) - 1)
    count = 0
    for k,v in neibor_dict.iteritems():
        if count == target_next: # 被选中的后继状态
            delta_e = current_confict_num - v
            if delta_e > 0:
                status[k[0]] = k[1]
                return status
            elif random.random() < get_accept_prob(delta_e, t):
                # 一定概率接受劣解
                status[k[0]] = k[1]
                return status
        else:
            count += 1
            continue
    return status

def solve(status):
    for t in range(1000000):
        status = simulated_annealing(status, t)
        if get_conflict_queen_num(status) == 0:
            print 'solved: ' + str(status)
            break
        print 't = ' + str(t) + ', status: ' + str(status)

if __name__ == "__main__":
    status = [0,1,2,3,4,5,6,7] # 初始布局
    solve(status)
