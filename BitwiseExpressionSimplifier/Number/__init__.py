from __future__ import annotations

from ..Bitwise import *

__all__ = ["NOperation", "NExpression", "NNumber", "NKnownNumber"]


class NOperation(object):
    def __init__(self):
        self.length = 0
        self.bitwise: list[BOperation] = []

    def __str__(self) -> str:
        return "[" + ", ".join(str(i) for i in self.bitwise[::-1]) + "]"

    def __repr__(self):
        return self.__str__()

    def getNumber(self):
        raise Exception

    def setNegate(self) -> None:
        for i in range(self.length):
            self.bitwise[i].setNegate()

    def leftOffset(self, length: int) -> None:
        """<<"""
        for _ in range(length):
            # bitwise 存储方式为 [0:length] ，所以左移对 list 是执行右移操作
            self.bitwise.pop(self.length - 1)  # 高位溢出
            self.bitwise.insert(0, BNumber(0))  # 低位补 0

    def rightOffset(self, length: int) -> None:
        """>>"""
        for _ in range(length):
            # bitwise 存储方式为 [0:length] ，所以右移对list是执行左移操作
            self.bitwise.pop(0)  # 低位溢出
            self.bitwise.append(BNumber(0))  # 高位补 0

    def copy(self):
        raise Exception


class NExpression(NOperation):
    def __init__(self, left: NOperation, operator, right: NOperation, length: int):
        super().__init__()
        self.length = length
        self._left = left
        self._operator = operator
        self._right = right

        for i in range(self.length):
            self.bitwise.append(BExpression(left.bitwise[i], operator, right.bitwise[i]).getResult())

    def copy(self):
        rtn = NExpression(self._left, self._operator, self._right, self.length)
        for i in range(self.length):
            rtn.bitwise[i] = self.bitwise[i].copy()
        return rtn


class NNumber(NOperation):
    def __init__(self, number: int, length: int):
        super().__init__()
        self.length = length
        self._number = number

        x = self._number
        p = self.length - 1
        # bitwise 存储方式为 [0:length] ，所以除二取余法是正向存储
        while x > 0 and p >= 0:  # 除二取余
            self.bitwise.append(BNumber(x % 2))
            x //= 2
            p -= 1
        while p >= 0:  # 高位补 0
            self.bitwise.append(BNumber(0))
            p -= 1

    def getNumber(self) -> int:
        return self._number

    def copy(self):
        rtn = NNumber(self._number, self.length)
        for i in range(self.length):
            rtn.bitwise[i] = self.bitwise[i].copy()
        return rtn


class NKnownNumber(NOperation):
    def __init__(self, name: str, length: int):
        super().__init__()
        self.length = length
        self._name = name

        # bitwise 存储方式为 [0:length] ，所以下标是正向存储
        for i in range(self.length):
            self.bitwise.append(BKnownNumber(name, i))

    def copy(self):
        rtn = NKnownNumber(self._name, self.length)
        for i in range(self.length):
            rtn.bitwise[i] = self.bitwise[i].copy()
        return rtn
