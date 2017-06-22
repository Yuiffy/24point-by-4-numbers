from collections import OrderedDict

def do_one_cal(a,b,sa,sb,op_num):
    if(op_num==0):
        return a+b, '('+sa+'+'+sb+')'
    elif op_num==2:
        return a-b,  '('+sa+'-'+sb+')'
    elif op_num==1:
        return a*b,  '('+sa+'*'+sb+')'
    elif op_num==3:
        if(b==0):
            return 0,None
        return 1.0*a/b,  '('+sa+'/'+sb+')'

def dfs(numberList, ret, s, sum):
    if(len(numberList)==0):
        if abs(sum - 24) < 1e-10:
            ret+=[s[1:-1]]
        return
    for i in range(len(numberList)):
        for j in range(4):
            last = numberList[0:i]+numberList[i+1:len(numberList)]
            sum2,s2 = do_one_cal(sum, numberList[i], s, str(numberList[i]), j)
            if(s2==None):
                continue
            dfs(last, ret, s2, sum2)
            sum2,s2 = do_one_cal(numberList[i],sum,  str(numberList[i]),s, j)
            if(s2==None):
                continue
            dfs(last, ret, s2, sum2)

def del2fromnumberList(numberList,i,j):
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
            if(i==j):
                continue
            last = del2fromnumberList(numberList,i,j)
            for op1 in range(4):
                sm,s = do_one_cal(numberList[i],numberList[j],str(numberList[i]),str(numberList[j]),op1)
                if(s==None):
                    continue;
                dfs(last, ret, s, sm)
    return ret

def cal24by2items(numberList):
    ret = []
    for i in range(len(numberList)):
        for j in range(len(numberList)):
            if(i==j):
                continue
            last = del2fromnumberList(numberList, i, j)
            for op1 in range(4):
                if(op1<=1) and (i>j):
                    continue
                l,ls = do_one_cal(numberList[i],numberList[j],str(numberList[i]),str(numberList[j]),op1)
                for op2 in range(4):
                    ma = 2
                    if(op2<=1): ma=1
                    for k in range(ma):
                        q1 = k
                        q2 = k^1
                        r, rs = do_one_cal(last[q1], last[q2], str(last[q1]), str(last[q2]), op2)
                        for op3 in range(4):
                            if ls==None or rs==None:
                                break
                            ans, anss = do_one_cal(l,r,ls,rs,op3)
                            if(anss==None):
                                continue
                            if abs(ans - 24) < 1e-10:
                                ret+=[anss[1:-1]]
    return ret

def cal24(numberList):
    ret = []
    ret += cal24bysteps(numberList)
    ret += cal24by2items(numberList)
    ret = list(OrderedDict.fromkeys(ret))
    return ret

if __name__ == '__main__':
    numberList = map(int, raw_input().split())
    print numberList
    print cal24(numberList)
