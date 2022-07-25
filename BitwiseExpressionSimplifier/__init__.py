from __future__ import annotations

from .util import list2NOperation
from .Number import *

__all__ = ["toNOperation"]


def toNOperation(expression: str, length: int, known_bitwise: set[str] = None, known_operation: dict[str, NOperation] = None):
    exp_arr = []
    if known_bitwise is None:
        known_bitwise = set()
    if known_operation is None:
        known_operation = {}
    while expression != "":
        if expression[0] == ' ':
            expression = expression[1:]
        elif expression[0] == '('\
                or expression[0] == ')'\
                or expression[0] == '&'\
                or expression[0] == '|'\
                or expression[0] == '^'\
                or expression[0] == '~':
            exp_arr.append(expression[0])
            expression = expression[1:]
        elif expression[:2] == '<<' or expression[:2] == '>>':
            exp_arr.append(expression[:2])
            expression = expression[2:]
        elif expression[0].isdigit():
            if len(expression) > 1 and expression[1].isdigit():
                p = 2
                n = len(expression)
                while p < n and expression[p].isdigit():
                    p += 1
                exp_arr.append(expression[:p])
                expression = expression[p:]
            elif len(expression) > 0 and expression[:2] == '0b':
                p = 2
                n = len(expression)
                while p < n and expression[p] in {'0', '1'}:
                    p += 1
                exp_arr.append(expression[:p])
                expression = expression[p:]
            elif len(expression) > 0 and expression[:2] == '0x':
                p = 2
                n = len(expression)
                while p < n and expression[p] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'}:
                    p += 1
                exp_arr.append(expression[:p])
                expression = expression[p:]
            else:
                exp_arr.append(expression[0])
                expression = expression[1:]
        else:
            is_known_bitwise = False
            is_known_operation = False
            for key in known_bitwise:
                if expression.startswith(key):
                    right = expression[len(key):]
                    if len(right) > 0 and (right[0].isalpha() or right[0].isdigit() or right[0] == '_'):
                        continue
                    exp_arr.append(NKnownNumber(key, length))
                    expression = right
                    is_known_bitwise = True
                    break
            if not is_known_bitwise:
                for key in known_operation.keys():
                    if expression.startswith(key):
                        right = expression[len(key):]
                        if len(right) > 0 and (right[0].isalpha() or right[0].isdigit() or right[0] == '_'):
                            continue
                        assert known_operation[key].length == length
                        exp_arr.append(known_operation[key])
                        expression = right
                        is_known_bitwise = True
                        break
            if not is_known_bitwise and not is_known_operation:
                raise Exception("拆分错误", f"未知的表达式: {expression}")
    return list2NOperation(exp_arr, length)
