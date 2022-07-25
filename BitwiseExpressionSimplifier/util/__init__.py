from __future__ import annotations

from ..Number import *

__all__ = "list2NOperation"


def list2NOperation(expression: list, length: int) -> NOperation:
    # 0级优先，形态转换
    p = 0
    while p < len(expression):
        if type(expression[p]) is str and expression[p][0].isdigit():
            if expression[p].startswith('0b'):
                expression[p] = NNumber(int(expression[p], 2), length)
            elif expression[p].startswith('0x'):
                expression[p] = NNumber(int(expression[p], 16), length)
            else:
                expression[p] = NNumber(int(expression[p], 10), length)
        p += 1
    # 1级优先，( )
    p = 0
    while p < len(expression):
        if expression[p] == '(':
            balance = 1
            q = p + 1
            while q < len(expression) and balance > 0:
                if expression[q] == '(':
                    balance += 1
                elif expression[q] == ')':
                    balance -= 1
                q += 1
            if balance != 0:
                raise Exception("解析错误", "括号不平衡")
            expression = expression[:p] + [list2NOperation(expression[p + 1:q - 1], length)] + expression[q:]
        p += 1
    # 2级优先，~
    p = 0
    while p < len(expression):
        if expression[p] == '~':
            if expression[p + 1] == '~':  # 抵消
                expression = expression[:p] + expression[p + 2:]
                continue
            elif isinstance(expression[p+1], NOperation):
                expression[p + 1].setNegate()
                expression = expression[:p] + expression[p + 1:]
            else:
                raise Exception
        p += 1
    # 5级优先，<< >>
    p = 0
    while p < len(expression):
        if expression[p] == '>>':
            expression[p - 1].rightOffset(expression[p + 1].getNumber())
            expression = expression[:p] + expression[p + 2:]
            continue
        elif expression[p] == '<<':
            expression[p - 1].leftOffset(expression[p + 1].getNumber())
            expression = expression[:p] + expression[p + 2:]
            continue
        p += 1
    # 8级优先，&
    p = 0
    while p < len(expression):
        if expression[p] == '&':
            expression = expression[:p - 1] + [NExpression(expression[p - 1], '&', expression[p + 1], length)] + expression[p + 2:]
            continue
        p += 1
    # 9级优先，^
    p = 0
    while p < len(expression):
        if expression[p] == '^':
            expression = expression[:p - 1] + [NExpression(expression[p - 1], '^', expression[p + 1], length)] + expression[p + 2:]
            continue
        p += 1
    # 10级优先，|
    p = 0
    while p < len(expression):
        if expression[p] == '|':
            expression = expression[:p - 1] + [NExpression(expression[p - 1], '|', expression[p + 1], length)] + expression[p + 2:]
            continue
        p += 1
    assert len(expression) == 1
    return expression[0]
