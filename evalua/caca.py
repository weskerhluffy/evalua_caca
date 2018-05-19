#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
'''
Created on 18/05/2018

@author: ernesto
'''
# XXX: https://www.hackerrank.com/contests/cs1300-odd-2014/challenges/evaluate-expression/problem

from operator import add, sub, mul, truediv
import numbers

bt = type('()')
ot = type(add)


def evaluate_ops(s, p):
    if p == 1:
        ops = [add, sub]
    else:
        ops = [mul, truediv]
        
    if p == 1:
        s1 = []
        while s and type(s[-1]) != bt:
            s1.append(s.pop())
    else:
        s1 = s
    r = s1.pop()    
    while s1 and type(s1[-1]) == ot and s1[-1] in ops:
        if len(s1) > 1 and isnumber(s1[-2]) :
            n2 = r
            op = s1.pop()
            n1 = s1.pop()
            if p == 1:
                r = op(n2, n1)
            else:
                if n2:
                    r = op(n1, n2)
                else:
                    r = None
                    break
        else:
            r = None
            break
    
    if p == 1:
        if s1:
            r = None
    else:
        if s1 and not((type(s1[-1]) == ot and s1[-1] in [add, sub]) or (type(s1[-1]) == bt and s1[-1] == '(')):
            r = None
        
    if not isnumber(r):
        r = None
    return r


# XXX: https://stackoverflow.com/questions/4187185/how-can-i-check-if-my-python-object-is-a-number
def isnumber(n):
    r = isinstance(n, numbers.Number)
#    print("{} es num {}".format(n, r))
    return r


def build_tokens(s):
    i = 0
    t = []
    e = False
    ops = {'+':add, '-':sub, '*':mul, '/':truediv}
    while i < len(s):
        if s[i] in '()':
            t.append(s[i])
            if s[i] == '(' and i + 3 < len(s) and s[i + 1] in ['+', '-'] and s[i + 2].isdigit():
                j = i + 2
                while j < len(s) and s[j].isdigit():
                    j += 1
                n = int(s[i + 2:j])
                if s[i + 1] == '-':
                    n *= -1
                t.append(n)
                i=j
            else:
                i += 1
        else:
            if s[i] in ops:
                t.append(ops[s[i]])
                i += 1
            else:
                if s[i].isdigit():
                    j = i + 1
                    while j < len(s) and s[j].isdigit():
                        j += 1
                    t.append(int(s[i:j]))
                    i = j
                else:
                    if s[i] == ' ':
                        i += 1
                    else:
                        e = True
                        break
    if e:
        t = None
    return t


def evaluate_tokens(t):
    s = []
    r = None
    e = False
    for ct in t:
        tt = type(ct)
        if (tt not in [bt, ot]) and not isnumber(ct):
            e = True
            break
#        print("ct {} tt {} s {}".format(ct, tt, s))
        if isnumber(ct):
            s.append(ct)
            r = evaluate_ops(s, 2)
            if r is not None:
                s.append(r)
            else:
                e = True
                break
            
        if tt == bt:
            if ct == '(':
                if not s or type(s[-1]) == ot or (type(s[-1]) == bt and s[-1] == '('):
                    s.append(ct)
                else:
                    e = True
                    break
            else:
                if ct == ')':
                    r = None
                    if isnumber(s[-1]) :
                        r = evaluate_ops(s, 1)
                    
                    if e or r is None or not isnumber(r) or not s or type(s[-1]) != bt or s[-1] != '(':
                        e = True
                        break
                    s.pop()
                    s.append(r)
                    r = evaluate_ops(s, 2)
                    if r is None:
                        e = True
                        break
                    s.append(r)
#                    print("w1 {}".format(r))
                else:
                    e = True
                    break
        if tt == ot:
            if len(s) > 0 and isnumber(s[-1]) :
                s.append(ct)
            else:
                e = True
                break
                        
#    print(s)
    if e:
        r = None
    else:
        if s:
            r = evaluate_ops(s, 1)
        if s:
            r = None
    return r 


def main():
    t = build_tokens(input().strip())
#    print(t)
    if t :
        rn = evaluate_tokens(t)
        if rn is None:
            r = "ERROR"
        else:
            if isinstance(rn, int):
                r = rn
            else:
                r = int(rn) if rn.is_integer() else rn
    else:
        r = "ERROR"
    print(r)


main()
