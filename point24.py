# -*- coding: utf-8 -*-
from collections import OrderedDict


# 结点类
class Node:
    def __init__(self, ch=None, left=None, right=None, polar=0, id=0):
        self.ch = ch  # 变量或运算符
        self.left = left  # 左孩子
        self.right = right  # 右孩子
        self.polar = polar  # 极性，可取 0, 1, -1
        self.id = id  # 结点编号

    def __str__(self):  # 把树转换成算式
        if self.ch not in '+-*/':
            return self.ch  # 单变量不加括号
        left = str(self.left)  # 左子树转字符串
        right = str(self.right)  # 右子树转字符串
        if self.ch in '*/' and self.left.ch in '+-':
            left = '(' + left + ')'  # 左子树加括号
        if self.ch == '/' or self.ch in '*-' and self.right.ch in '+-':
            right = '(' + right + ')'  # 右子树加括号
        return left + ' ' + self.ch + ' ' + right  # 用根结点的运算符相连


# 考虑加减乘除，去重
def smart4(left, right):
    # 加法：两个孩子都不能是减号；左孩子还不能是加号；
    #       若右孩子是加号，则左孩子和右孩子的左孩子要满足单调性
    if left.ch not in '+-' and right.ch != '-' and (right.ch != '+' or left.id < right.left.id):
        polar = (0 if left.polar == 0 and right.polar == 0 else  # 无极性 + 无极性 = 无极性
                 1 if left.polar == 0 or right.polar == 0 else  # 有极性 + 无极性 = 正极性
                 right.polar)  # 有极性 + 有极性 = 右子树极性
        yield Node('+', left, right, polar)
    # 减法：两个孩子都不能是减号
    if left.ch != '-' and right.ch != '-':
        if left.polar == 0 and right.polar == 0:  # 无极性 - 无极性：
            yield Node('-', left, right, 1)  # 正过来减是正极性
            yield Node('-', right, left, -1)  # 反过来减是负极性
        else:
            if left.polar == 0:
                yield Node('-', right, left, -1)  # 有极性 - 无极性 = 负极性
                # （无极性 - 有极性 = 舍弃）
                # （有极性 - 有极性 = 舍弃）
            if right.polar == 0:
                yield Node('-', left, right, -1)  # 同上
    # 乘法：两个孩子都不能是除号；左孩子还不能是乘号；
    #       若右孩子是乘号，则左孩子和右孩子的左孩子要满足单调性
    if left.ch not in '*/' and right.ch != '/' and (right.ch != '*' or left.id < right.left.id):
        if left.polar == 0 or right.polar == 0:
            yield Node('*', left, right, left.polar + right.polar)  # 无极性 * 无极性 = 无极性
            # 有极性 * 无极性 = 有极性者的极性
        elif left.polar > 0:
            yield Node('*', left, right, right.polar)  # 正极性 * 有极性 = 右子树极性
            # （负极性 * 有极性 = 舍弃）
    # 除法：两个孩子都不能是除号
    if left.ch != '/' and right.ch != '/':
        if left.polar == 0 or right.polar == 0:
            yield Node('/', left, right, left.polar + right.polar)  # 无极性 * 无极性 = 无极性
            # 有极性 * 无极性 = 有极性者的极性
            yield Node('/', right, left, left.polar + right.polar)  # 同上
        else:
            if left.polar > 0:
                yield Node('/', left, right, right.polar)  # 正极性 / 有极性 = 右子树极性
                # （负极性 / 有极性 = 舍弃）
            if right.polar > 0:
                yield Node('/', right, left, left.polar)  # 同上


# 枚举由 n 个变量组成的算式
def enum(numberList, actions):
    def DFS(trees, minj):  # trees 为当前算式列表，minj 为第二棵子树的最小下标
        if len(trees) == 1:
            yield str(trees[0])  # 只剩一个算式，输出
            return
        for j in range(minj, len(trees)):  # 枚举第二棵子树
            for i in range(j):  # 枚举第一棵子树
                for node in actions(trees[i], trees[j]):  # 枚举运算符
                    node.id = trees[-1].id + 1  # 为新结点赋予 id
                    new_trees = [trees[k] for k in range(len(trees)) if k != i and k != j] + [node]
                    # 从集合中去掉两棵子树，并加入运算结果
                    new_minj = j - 1 if actions in [smart4] else 1
                    # 若 actions 函数去重，则此处也避免「独立运算顺序不唯一」造成的重复
                    for expression in DFS(new_trees, new_minj):  # 递归下去
                        yield expression

    n = len(numberList)
    trees = [Node(str(numberList[i]) + ".", id=i) for i in range(n)]  # 初始时有 n 个由单变量组成的算式
    return DFS(trees, 1)


def cal24(numberList):
    # 检查非int参数，防止eval奇怪东西
    notNumberList = list(filter(lambda x: not isinstance(x, int), numberList))
    if (len(notNumberList) > 0):
        print ('have not number param:', notNumberList)
        return []
    # 用去重的 actions 函数枚举算式
    smart_exps = list(enum(numberList, smart4))
    exps_24point = []
    for exp in smart_exps:
        try:
            ans = eval(exp)
            if (abs(ans - 24) < 1e-10):
                exps_24point += [exp]
        except:
            pass
    exps_24point_reduce = list(OrderedDict.fromkeys(exps_24point))  # 字符串去重
    exps_24point_reduce = map(lambda s: s.replace('.', ''), exps_24point_reduce)  # 删除小数点
    return exps_24point_reduce


if __name__ == '__main__':
    numberList = map(int, raw_input().split())
    print (numberList)
    the24point = cal24(numberList)
    print (the24point)
    print(len(the24point))
