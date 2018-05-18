'''
Created on 18/05/2018

@author: ernesto
'''
# XXX: https://www.hackerrank.com/contests/cs1300-odd-2014/challenges/evaluate-expression/problem

from operator import add, sub, mul, floordiv


def build_tokens(s):
    i = 0
    t = []
    e = False
    ops = {'+':add, '-':sub, '*':mul, '/':floordiv}
    while i < len(s):
        if s[i] in '()':
            t.append(s[i])
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
                        continue
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
    bt = type('()')
    ot = type(add)
    nt = type(1)
    for ct in t:
        tt = type(ct)
        if tt not in [bt, ot, nt]:
            e = True
            break
        print("ct {} tt {} s {}".format(ct, tt, s))
        if tt == nt:
            if not s or (type(s[-1]) == bt and s[-1] == '('):
                s.append(ct)
            else:
                if len(s) > 1 and type(s[-1]) == ot and type(s[-2]) == nt:
                    if s[-1] in [mul, floordiv]:
                        n2 = ct
                        op = s.pop()
                        n1 = s.pop()
                        r = op(n1, n2)
                        s.append(r)
#                        print("ap {}".format(r))
                    else:
                        s.append(ct)
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
                    while s and type(s[-1]) == nt:
                        r = s.pop()
                        print("mierda {} ot {} {}".format(r, s[-1], s[-1] in [add, sub]))
                        if s and type(s[-1]) != bt:
                            if len(s) > 1 and type(s[-1]) == ot and s[-1] in [add, sub] and type(s[-2]) == nt:
                                n2 = r
                                op = s.pop()
                                n1 = s.pop()
                                r = op(n1, n2)
                                s.append(r)
#                                print("w {}".format(r))
                            else:
                                e = True
                                break
                    if e or r is None or type(r) != nt or not s or type(s[-1]) != bt or s[-1] != '(':
                        e = True
                        break
                    s.pop()
                    while s and type(s[-1]) == ot and s[-1] in [mul, floordiv]:
                        if len(s) > 1 and type(s[-2]) == nt:
                            n2 = r
                            op = s.pop()
                            n1 = s.pop()
                            r = op(n1, n2)
                        else:
                            e = True
                            break
                    if e:
                        break
                    s.append(r)
#                    print("w1 {}".format(r))
                else:
                    e = True
                    break
        if tt == ot:
            if len(s) > 0 and type(s[-1]) == nt:
                s.append(ct)
            else:
                e = True
                break
                        
    print(s)
    if e:
        r = None
    return r


def main():
    t = build_tokens(input().strip())
    r = evaluate_tokens(t)
    print(r)


main()
