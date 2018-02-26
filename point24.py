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


def do_one_cal(a, b, sa, sb, op_num):
    if (op_num == 0):
        return a + b, '(' + sa + '+' + sb + ')'
    elif op_num == 2:
        return a - b, '(' + sa + '-' + sb + ')'
    elif op_num == 1:
        return a * b, '(' + sa + '*' + sb + ')'
    elif op_num == 3:
        if (b == 0):
            return 0, None
        return 1.0 * a / b, '(' + sa + '/' + sb + ')'


def dfs(numberList, ret, s, sum):
    if (len(numberList) == 0):
        if abs(sum - 24) < 1e-10:
            ret += [s[1:-1]]
        return
    for i in range(len(numberList)):
        for j in range(4):
            last = numberList[0:i] + numberList[i + 1:len(numberList)]
            sum2, s2 = do_one_cal(sum, numberList[i], s, str(numberList[i]), j)
            if (s2 == None):
                continue
            dfs(last, ret, s2, sum2)
            sum2, s2 = do_one_cal(numberList[i], sum, str(numberList[i]), s, j)
            if (s2 == None):
                continue
            dfs(last, ret, s2, sum2)


def del2fromnumberList(numberList, i, j):
    ii = i
    jj = j
    if (ii > jj):
        ii = j
        jj = i
    last = numberList[0:ii] + numberList[ii + 1:jj] + numberList[jj + 1:len(numberList)]  # get the remind numbers
    return last


def cal24bysteps(numberList):
    ret = []
    for i in range(len(numberList)):
        for j in range(len(numberList)):
            if (i == j):
                continue
            last = del2fromnumberList(numberList, i, j)
            for op1 in range(4):
                sm, s = do_one_cal(numberList[i], numberList[j], str(numberList[i]), str(numberList[j]), op1)
                if (s == None):
                    continue;
                dfs(last, ret, s, sm)
    return ret


def cal24by2items(numberList):
    ret = []
    for i in range(len(numberList)):
        for j in range(len(numberList)):
            if (i == j):
                continue
            last = del2fromnumberList(numberList, i, j)
            for op1 in range(4):
                if (op1 <= 1) and (i > j):
                    continue
                l, ls = do_one_cal(numberList[i], numberList[j], str(numberList[i]), str(numberList[j]), op1)
                for op2 in range(4):
                    ma = 2
                    if (op2 <= 1): ma = 1
                    for k in range(ma):
                        q1 = k
                        q2 = k ^ 1
                        r, rs = do_one_cal(last[q1], last[q2], str(last[q1]), str(last[q2]), op2)
                        for op3 in range(4):
                            if ls == None or rs == None:
                                break
                            ans, anss = do_one_cal(l, r, ls, rs, op3)
                            if (anss == None):
                                continue
                            if abs(ans - 24) < 1e-10:
                                ret += [anss[1:-1]]
    return ret


def cal24(numberList):
    ret = []
    ret += cal24bysteps(numberList)
    ret += cal24by2items(numberList)
    ret = list(OrderedDict.fromkeys(ret))
    return ret


def cal24_maigo(numberList):
    # 检查非int参数，防止eval奇怪东西
    notNumberList = list(filter(lambda x: not isinstance(x, int), numberList))
    if(len(notNumberList)>0):
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
    exps_24point_reduce = cal24_maigo(numberList)  # maigo超碉去重二十四点
    my_24point = cal24(numberList)  # 我的简陋去重的24点
    print (exps_24point_reduce)
    print (my_24point)
    print(len(exps_24point_reduce), len(my_24point))
