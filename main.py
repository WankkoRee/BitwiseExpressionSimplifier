from __future__ import annotations


class BitwiseOperation(object):
    def setNegate(self) -> None:
        raise Exception

    def setNegateL(self) -> BitwiseOperation:
        self.setNegate()
        return self

    def getNegate(self) -> bool:
        return False

    def copy(self) -> BitwiseOperation:
        raise Exception


class BitwiseExpression(BitwiseOperation):
    def __init__(self, left: BitwiseOperation, operator: str, right: BitwiseOperation):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right
        self._simplified = False

        if operator == '&':
            if type(left) is BitwiseNumber and left.bit == 1:  # 1 & x == x
                self._simplified = True
                self._simplify = right
            elif type(right) is BitwiseNumber and right.bit == 1:  # x & 1 == x
                self._simplified = True
                self._simplify = left
            elif type(left) is BitwiseNumber and left.bit == 0:  # 0 & x == 0
                self._simplified = True
                self._simplify = left
            elif type(right) is BitwiseNumber and right.bit == 0:  # x & 0 == 0
                self._simplified = True
                self._simplify = right
            elif type(left) is BitwiseExpression and type(right) is not BitwiseExpression:
                left_set: set[BitwiseOperation] = left.getContinuousHashSet(operator)
                if right in left_set:  # (x & y & ...) & x == (x & y & ...)
                    self._simplified = True
                    self._simplify = left
                elif right.copy().setNegateL() in left_set:  # (x & y & ...) & ~x == 0
                    self._simplified = True
                    self._simplify = BitwiseNumber(0)
            elif type(left) is not BitwiseExpression and type(right) is BitwiseExpression:
                right_set: set[BitwiseOperation] = right.getContinuousHashSet(operator)
                if left in right_set:  # x & (x & y & ...) == (x & y & ...)
                    self._simplified = True
                    self._simplify = right
                elif left.copy().setNegateL() in right_set:  # ~x & (x & y & ...) == 0
                    self._simplified = True
                    self._simplify = BitwiseNumber(0)
            elif type(left) is BitwiseExpression and type(right) is BitwiseExpression:
                left_set: set[BitwiseOperation] = left.getContinuousHashSet(operator)
                right_set: set[BitwiseOperation] = right.getContinuousHashSet(operator)
                left_negated_set: set[BitwiseOperation] = set(i.copy().setNegateL() for i in left_set)
                right_negated_set: set[BitwiseOperation] = set(i.copy().setNegateL() for i in right_set)
                if len(left_set & right_negated_set) > 0:  # (x & y & ...) & (~y & z & ...) == 0
                    self._simplified = True
                    self._simplify = BitwiseNumber(0)
                elif len(left_negated_set & right_set) > 0:  # (x & ~y & ...) & (y & z & ...) == 0
                    self._simplified = True
                    self._simplify = BitwiseNumber(0)
                elif len(left_set & right_set) > 0:  # (x & y & ...) & (y & z & ...) == (x & y & ...) & (z & ...)
                    for same_operation in left_set & right_set:
                        if type(self.right) is BitwiseExpression:
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.right == same_operation:
                            self._simplified = True
                            self._simplify = left
                            self.right = None
                        else:
                            raise Exception
            elif left == right:  # x & x == x
                self._simplified = True
                self._simplify = left
            elif left == right.copy().setNegateL():  # x & ~x == 0
                self._simplified = True
                self._simplify = BitwiseNumber(0)
            else:
                ...
        elif operator == '|':
            if type(left) is BitwiseNumber and left.bit == 1:  # 1 | x == 1
                self._simplified = True
                self._simplify = left
            elif type(right) is BitwiseNumber and right.bit == 1:  # x | 1 == 1
                self._simplified = True
                self._simplify = right
            elif type(left) is BitwiseNumber and left.bit == 0:  # 0 | x == x
                self._simplified = True
                self._simplify = right
            elif type(right) is BitwiseNumber and right.bit == 0:  # x | 0 == x
                self._simplified = True
                self._simplify = left
            elif type(left) is BitwiseExpression and type(right) is not BitwiseExpression:
                left_set: set[BitwiseOperation] = left.getContinuousHashSet(operator)
                if right in left_set:  # (x | y | ...) | x == (x | y | ...)
                    self._simplified = True
                    self._simplify = left
                elif right.copy().setNegateL() in left_set:  # (x | y | ...) | ~x == 1
                    self._simplified = True
                    self._simplify = BitwiseNumber(1)
            elif type(left) is not BitwiseExpression and type(right) is BitwiseExpression:
                right_set: set[BitwiseOperation] = right.getContinuousHashSet(operator)
                if left in right_set:  # x | (x | y | ...) == (x | y | ...)
                    self._simplified = True
                    self._simplify = right
                elif left.copy().setNegateL() in right_set:  # ~x | (x | y | ...) == 1
                    self._simplified = True
                    self._simplify = BitwiseNumber(1)
            elif type(left) is BitwiseExpression and type(right) is BitwiseExpression:
                left_set: set[BitwiseOperation] = left.getContinuousHashSet(operator)
                right_set: set[BitwiseOperation] = right.getContinuousHashSet(operator)
                left_negated_set: set[BitwiseOperation] = set(i.copy().setNegateL() for i in left_set)
                right_negated_set: set[BitwiseOperation] = set(i.copy().setNegateL() for i in right_set)
                if len(left_set & right_negated_set) > 0:  # (x | y | ...) | (~y | z | ...) == 1
                    self._simplified = True
                    self._simplify = BitwiseNumber(1)
                elif len(left_negated_set & right_set) > 0:  # (x | ~y | ...) | (y | z | ...) == 1
                    self._simplified = True
                    self._simplify = BitwiseNumber(1)
                elif len(left_set & right_set) > 0:  # (x | y | ...) | (y | z | ...) == (x | y | ...) | (z | ...)
                    for same_operation in left_set & right_set:
                        if type(self.right) is BitwiseExpression:
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.right == same_operation:
                            self._simplified = True
                            self._simplify = left
                            self.right = None
                        else:
                            raise Exception
            elif left == right:  # x | x == x
                self._simplified = True
                self._simplify = left
            elif left == right.copy().setNegateL():  # x | ~x == 1
                self._simplified = True
                self._simplify = BitwiseNumber(1)
            else:
                ...
        elif operator == '^':
            if type(left) is BitwiseNumber and left.bit == 0:  # 0 ^ x == x
                self._simplified = True
                self._simplify = right
            elif type(right) is BitwiseNumber and right.bit == 0:  # x ^ 0 == x
                self._simplified = True
                self._simplify = left
            elif type(left) is BitwiseNumber and left.bit == 1:  # 1 ^ x == ~x
                self._simplified = True
                right.setNegate()
                self._simplify = right
            elif type(right) is BitwiseNumber and right.bit == 1:  # x ^ 1 == ~x
                self._simplified = True
                left.setNegate()
                self._simplify = left
            elif type(left) is BitwiseExpression and type(right) is not BitwiseExpression:
                left_set: set[BitwiseOperation] = left.getContinuousHashSet(operator)
                if right in left_set:  # (x ^ y ^ ...) ^ x == (y ^ ...)
                    self._simplified = True
                    self._simplify = left.removeContinuousOperation(operator, right)
                elif right.copy().setNegateL() in left_set:  # (x ^ y ^ ...) ^ ~x == ~(y ^ ...)
                    self._simplified = True
                    self._simplify = left.removeContinuousOperation(operator, right.copy().setNegateL()).setNegateL()
            elif type(left) is not BitwiseExpression and type(right) is BitwiseExpression:
                right_set: set[BitwiseOperation] = right.getContinuousHashSet(operator)
                if left in right_set:  # x ^ (x ^ y ^ ...) == (y ^ ...)
                    self._simplified = True
                    self._simplify = right.removeContinuousOperation(operator, left)
                elif left.copy().setNegateL() in right_set:  # ~x ^ (x ^ y ^ ...) == ~(y ^ ...)
                    self._simplified = True
                    self._simplify = right.removeContinuousOperation(operator, left.copy().setNegateL()).setNegateL()
            elif type(left) is BitwiseExpression and type(right) is BitwiseExpression:
                left_set: set[BitwiseOperation] = left.getContinuousHashSet(operator)
                right_set: set[BitwiseOperation] = right.getContinuousHashSet(operator)
                left_negated_set: set[BitwiseOperation] = set(i.copy().setNegateL() for i in left_set)
                right_negated_set: set[BitwiseOperation] = set(i.copy().setNegateL() for i in right_set)
                if len(left_set & right_negated_set) > 0:  # (x ^ y ^ ...) ^ (~y ^ z ^ ...) == ~((x ^ ...) ^ ( z ^ ...))
                    for same_operation in left_set & right_negated_set:
                        if type(self.left) is BitwiseExpression and type(self.right) is BitwiseExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = self.right.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                        elif self.left == same_operation and type(self.right) is BitwiseExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.left = None
                        elif type(self.left) is BitwiseExpression and self.right == same_operation.copy().setNegateL():
                            self._simplified = True
                            self._simplify = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = None
                        else:
                            raise Exception
                    if not self._simplified:
                        self.setNegate()
                    else:
                        self._simplify.setNegate()
                elif len(left_negated_set & right_set) > 0:  # (x ^ ~y ^ ...) ^ (y ^ z ^ ...) ==  ~((x ^ ...) ^ ( z ^ ...))
                    for same_operation in left_negated_set & right_set:
                        if type(self.left) is BitwiseExpression and type(self.right) is BitwiseExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.left == same_operation.copy().setNegateL() and type(self.right) is BitwiseExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation)
                            self.left = None
                        elif type(self.left) is BitwiseExpression and self.right == same_operation:
                            self._simplified = True
                            self._simplify = self.left.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.right = None
                        else:
                            raise Exception
                    if not self._simplified:
                        self.setNegate()
                    else:
                        self._simplify.setNegate()
                elif len(left_set & right_set) > 0:  # (x ^ y ^ ...) ^ (y ^ z ^ ...) == (x ^ ...) ^ (z ^ ...)
                    for same_operation in left_set & right_set:
                        if type(self.left) is BitwiseExpression and type(self.right) is BitwiseExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.left == same_operation and type(self.right) is BitwiseExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation)
                            self.left = None
                        elif type(self.left) is BitwiseExpression and self.right == same_operation:
                            self._simplified = True
                            self._simplify = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = None
                        else:
                            raise Exception
            elif left == right:  # x ^ x == 0
                self._simplified = True
                self._simplify = BitwiseNumber(0)
            elif left == right.copy().setNegateL():  # x ^ ~x == 1
                self._simplified = True
                self._simplify = BitwiseNumber(1)
            else:
                ...
        elif operator == '⊙':
            if type(left) is BitwiseNumber and left.bit == 1:  # 1 ⊙ x == x
                self._simplified = True
                self._simplify = right
            elif type(right) is BitwiseNumber and right.bit == 1:  # x ⊙ 1 == x
                self._simplified = True
                self._simplify = left
            elif type(left) is BitwiseNumber and left.bit == 0:  # 0 ⊙ x == ~x
                self._simplified = True
                right.setNegate()
                self._simplify = right
            elif type(right) is BitwiseNumber and right.bit == 0:  # x ⊙ 0 == ~x
                self._simplified = True
                left.setNegate()
                self._simplify = left
            elif type(left) is BitwiseExpression and type(right) is not BitwiseExpression:
                left_set: set[BitwiseOperation] = left.getContinuousHashSet(operator)
                if right in left_set:  # (x ⊙ y ⊙ ...) ⊙ x == (y ⊙ ...)
                    self._simplified = True
                    self._simplify = left.removeContinuousOperation(operator, right)
                elif right.copy().setNegateL() in left_set:  # (x ⊙ y ⊙ ...) ⊙ ~x == ~(y ⊙ ...)
                    self._simplified = True
                    self._simplify = left.removeContinuousOperation(operator, right.copy().setNegateL()).setNegateL()
            elif type(left) is not BitwiseExpression and type(right) is BitwiseExpression:
                right_set: set[BitwiseOperation] = right.getContinuousHashSet(operator)
                if left in right_set:  # x ⊙ (x ⊙ y ⊙ ...) == (y ⊙ ...)
                    self._simplified = True
                    self._simplify = right.removeContinuousOperation(operator, left)
                elif left.copy().setNegateL() in right_set:  # ~x ⊙ (x ⊙ y ⊙ ...) == ~(y ⊙ ...)
                    self._simplified = True
                    self._simplify = right.removeContinuousOperation(operator, left.copy().setNegateL()).setNegateL()
            elif type(left) is BitwiseExpression and type(right) is BitwiseExpression:
                left_set: set[BitwiseOperation] = left.getContinuousHashSet(operator)
                right_set: set[BitwiseOperation] = right.getContinuousHashSet(operator)
                left_negated_set: set[BitwiseOperation] = set(i.copy().setNegateL() for i in left_set)
                right_negated_set: set[BitwiseOperation] = set(i.copy().setNegateL() for i in right_set)
                if len(left_set & right_negated_set) > 0:  # (x ⊙ y ⊙ ...) ⊙ (~y ⊙ z ⊙ ...) == ~((x ⊙ ...) ⊙ ( z ⊙ ...))
                    for same_operation in left_set & right_negated_set:
                        if type(self.left) is BitwiseExpression and type(self.right) is BitwiseExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = self.right.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                        elif self.left == same_operation and type(self.right) is BitwiseExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.left = None
                        elif type(self.left) is BitwiseExpression and self.right == same_operation.copy().setNegateL():
                            self._simplified = True
                            self._simplify = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = None
                        else:
                            raise Exception
                    if not self._simplified:
                        self.setNegate()
                    else:
                        self._simplify.setNegate()
                elif len(left_negated_set & right_set) > 0:  # (x ⊙ ~y ⊙ ...) ⊙ (y ⊙ z ⊙ ...) ==  ~((x ⊙ ...) ⊙ ( z ⊙ ...))
                    for same_operation in left_negated_set & right_set:
                        if type(self.left) is BitwiseExpression and type(self.right) is BitwiseExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.left == same_operation.copy().setNegateL() and type(self.right) is BitwiseExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation)
                            self.left = None
                        elif type(self.left) is BitwiseExpression and self.right == same_operation:
                            self._simplified = True
                            self._simplify = self.left.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.right = None
                        else:
                            raise Exception
                    if not self._simplified:
                        self.setNegate()
                    else:
                        self._simplify.setNegate()
                elif len(left_set & right_set) > 0:  # (x ⊙ y ⊙ ...) ⊙ (y ⊙ z ⊙ ...) == (x ⊙ ...) ⊙ (z ⊙ ...)
                    for same_operation in left_set & right_set:
                        if type(self.left) is BitwiseExpression and type(self.right) is BitwiseExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.left == same_operation and type(self.right) is BitwiseExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation)
                            self.left = None
                        elif type(self.left) is BitwiseExpression and self.right == same_operation:
                            self._simplified = True
                            self._simplify = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = None
                        else:
                            raise Exception
            elif left == right:  # x ⊙ x == 1
                self._simplified = True
                self._simplify = BitwiseNumber(1)
            elif left == right.copy().setNegateL():  # x ⊙ ~x == 0
                self._simplified = True
                self._simplify = BitwiseNumber(0)
            else:
                ...

    def __str__(self) -> str:
        return (str(self.left) if type(self.left) is not BitwiseExpression else f"({self.left})")\
               + f" {self.operator} "\
               + (str(self.right) if type(self.right) is not BitwiseExpression else f"({self.right})")

    def __eq__(self, other) -> bool:
        if type(other) is BitwiseExpression:
            return (self.left == other.left and self.operator == other.operator and self.right == other.right)\
                   or (self.left == other.right and self.operator == other.operator and self.left == other.right)
        return False

    def __hash__(self) -> int:
        return hash(self.operator)

    def getResult(self) -> BitwiseOperation:
        if self._simplified:
            return self._simplify
        else:
            return self

    def getContinuousHashSet(self, operator: str) -> set[BitwiseOperation]:
        """根据运算符提取连续同运算表达式中的所有运算数的 hash 集合"""
        if self.operator == operator:
            result: set[BitwiseOperation] = set()
            if type(self.left) == BitwiseExpression:
                result.update(self.left.getContinuousHashSet(operator))
            else:
                result.add(self.left)
            if type(self.right) == BitwiseExpression:
                result.update(self.right.getContinuousHashSet(operator))
            else:
                result.add(self.right)
            return result
        else:
            return {self}

    def removeContinuousOperation(self, operator: str, operation: BitwiseOperation) -> BitwiseOperation:
        if self.operator == operator:
            if self.left == operation:
                return self.right
            elif self.right == operation:
                return self.left
            elif type(self.left) == BitwiseExpression and operation in self.left.getContinuousHashSet(operator):
                self.left = self.left.removeContinuousOperation(operator, operation)
                return self
            elif type(self.right) == BitwiseExpression and operation in self.right.getContinuousHashSet(operator):
                self.right = self.right.removeContinuousOperation(operator, operation)
                return self
            else:
                raise Exception

    def setNegate(self) -> None:
        if self.operator == '&':
            self.left.setNegate()
            self.operator = '|'
            self.right.setNegate()
        elif self.operator == '|':
            self.left.setNegate()
            self.operator = '&'
            self.right.setNegate()
        elif self.operator == '^':
            self.left.setNegate()
            self.operator = '⊙'
            self.right.setNegate()
        elif self.operator == '⊙':
            self.left.setNegate()
            self.operator = '^'
            self.right.setNegate()

    def copy(self) -> BitwiseExpression:
        return BitwiseExpression(self.left.copy(), self.operator, self.right.copy())


class BitwiseNumber(BitwiseOperation):
    def __init__(self, number: int):
        super().__init__()
        if number == 0:
            self.bit = 0
        elif number == 1:
            self.bit = 1
        else:
            raise Exception

    def __str__(self) -> str:
        return str(self.bit)

    def __eq__(self, other) -> bool:
        if type(other) is BitwiseNumber:
            return self.bit == other.bit
        return False

    def __hash__(self) -> int:
        return hash(self.bit)

    def setNegate(self) -> None:
        self.bit = 1 - self.bit

    def copy(self) -> BitwiseNumber:
        return BitwiseNumber(self.bit)


class BitwiseKnownNumber(BitwiseOperation):
    def __init__(self, name: str, index: int):
        super().__init__()
        self.name = name
        self.index = index
        self._negate = False

    def __str__(self) -> str:
        return f"{'~' if self._negate else ''}{self.name}[{self.index}]"

    def __eq__(self, other) -> bool:
        if type(other) is BitwiseKnownNumber:
            return self.name == other.name and self.index == other.index and self._negate == other.getNegate()
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def setNegate(self) -> None:
        self._negate = not self._negate

    def getNegate(self) -> bool:
        return self._negate

    def copy(self) -> BitwiseKnownNumber:
        rtn = BitwiseKnownNumber(self.name, self.index)
        if self.getNegate():
            rtn.setNegate()
        return rtn


class NumberOperation(object):
    def __init__(self):
        self.length = 0
        self.bitwise: list[BitwiseOperation] = []

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
            self.bitwise.insert(0, BitwiseNumber(0))  # 低位补 0

    def rightOffset(self, length: int) -> None:
        """>>"""
        for _ in range(length):
            # bitwise 存储方式为 [0:length] ，所以右移对list是执行左移操作
            self.bitwise.pop(0)  # 低位溢出
            self.bitwise.append(BitwiseNumber(0))  # 高位补 0


class NumberExpression(NumberOperation):
    def __init__(self, left: NumberOperation, operator, right: NumberOperation, length: int):
        super().__init__()
        self.length = length
        self._left = left
        self._operator = operator
        self._right = right

        for i in range(self.length):
            self.bitwise.insert(0, BitwiseExpression(left.bitwise[i], operator, right.bitwise[i]).getResult())

    def __str__(self) -> str:
        return (str(self._left) if type(self._left) is not NumberExpression else f"({self._left})") \
               + f" {self._operator} " \
               + (str(self._right) if type(self._right) is not NumberExpression else f"({self._right})")


class NumberNumber(NumberOperation):
    def __init__(self, number: int, length: int):
        super().__init__()
        self.length = length
        self._number = number

        x = self._number
        p = self.length - 1
        # bitwise 存储方式为 [0:length] ，所以除二取余法是正向存储
        while x > 0 and p >= 0:  # 除二取余
            self.bitwise.append(BitwiseNumber(x % 2))
            x //= 2
            p -= 1
        while p >= 0:  # 高位补 0
            self.bitwise.append(BitwiseNumber(0))
            p -= 1

    def __str__(self) -> str:
        return hex(self._number)

    def getNumber(self) -> int:
        return self._number


class NumberKnownNumber(NumberOperation):
    def __init__(self, name: str, length: int):
        super().__init__()
        self.length = length
        self._name = name

        # bitwise 存储方式为 [0:length] ，所以下标是正向存储
        for i in range(self.length):
            self.bitwise.append(BitwiseKnownNumber(name, i))

    def __str__(self) -> str:
        return self._name


def list2NumberOperation(expression: list, length: int) -> NumberOperation:
    # 0级优先，形态转换
    p = 0
    while p < len(expression):
        if type(expression[p]) is str and expression[p][0].isdigit():
            if expression[p].startswith('0b'):
                expression[p] = NumberNumber(int(expression[p], 2), length)
            elif expression[p].startswith('0x'):
                expression[p] = NumberNumber(int(expression[p], 16), length)
            else:
                expression[p] = NumberNumber(int(expression[p], 10), length)
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
            expression = expression[:p] + [list2NumberOperation(expression[p + 1:q - 1], length)] + expression[q:]
        p += 1
    # 2级优先，~
    p = 0
    while p < len(expression):
        if expression[p] == '~':
            if expression[p + 1] == '~':  # 抵消
                expression = expression[:p] + expression[p + 2:]
                continue
            elif isinstance(expression[p+1], NumberOperation):
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
            expression = expression[:p - 1] + [NumberExpression(expression[p - 1], '&', expression[p + 1], length)] + expression[p + 2:]
            continue
        p += 1
    # 9级优先，^
    p = 0
    while p < len(expression):
        if expression[p] == '^':
            expression = expression[:p - 1] + [NumberExpression(expression[p - 1], '^', expression[p + 1], length)] + expression[p + 2:]
            continue
        p += 1
    # 10级优先，|
    p = 0
    while p < len(expression):
        if expression[p] == '|':
            expression = expression[:p - 1] + [NumberExpression(expression[p - 1], '|', expression[p + 1], length)] + expression[p + 2:]
            continue
        p += 1
    assert len(expression) == 1
    return expression[0]


def toNumberOperation(known_bitwise: set[str], expression: str, length: int = 32):
    exp_arr = []
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
            for key in known_bitwise:
                if expression.startswith(key):
                    right = expression[len(key):]
                    if len(right) > 0 and (right[0].isalpha() or right[0].isdigit() or right[0] == '_'):
                        continue
                    exp_arr.append(NumberKnownNumber(key, length))
                    expression = right
                    is_known_bitwise = True
                    break
            if not is_known_bitwise:
                raise Exception("拆分错误", f"未知的表达式: {expression}")
    return list2NumberOperation(exp_arr, length)


if __name__ == '__main__':
    assert str(toNumberOperation(set(), "1 & ~1 | 1", 1).bitwise[0]) == '1'
    assert str(toNumberOperation({'x'}, "((((x))))", 1).bitwise[0]) == 'x[0]'
    assert str(toNumberOperation({'x'}, "1 & x", 1).bitwise[0]) == 'x[0]'
    assert str(toNumberOperation({'x'}, "x & 1", 1).bitwise[0]) == 'x[0]'
    assert str(toNumberOperation({'x'}, "0 & x", 1).bitwise[0]) == '0'
    assert str(toNumberOperation({'x'}, "x & 0", 1).bitwise[0]) == '0'
    assert str(toNumberOperation({'x', 'y'}, "x & y & x", 1).bitwise[0]) == 'x[0] & y[0]'
    assert str(toNumberOperation({'x', 'y'}, "x & (y & x)", 1).bitwise[0]) == 'y[0] & x[0]'
    assert str(toNumberOperation({'x', 'y'}, "(x & y) & (y & x)", 1).bitwise[0]) == 'x[0] & y[0]'
    assert str(toNumberOperation({'x', 'y', 'z'}, "(x & z & y) & (y & x)", 1).bitwise[0]) == '(x[0] & z[0]) & y[0]'
    assert str(toNumberOperation({'x'}, "(0 | x & 1) & x", 1).bitwise[0]) == 'x[0]'
    assert str(toNumberOperation({'x'}, "(1 | x & 0) & x", 1).bitwise[0]) == 'x[0]'
    assert str(toNumberOperation({'x'}, "x & ~x", 1).bitwise[0]) == '0'
    assert str(toNumberOperation({'x'}, "x & x", 1).bitwise[0]) == 'x[0]'
    assert str(toNumberOperation({'x', 'y', 'z'}, "x & y & (~x & y & z)", 1).bitwise[0]) == '0'
    assert str(toNumberOperation({'x', 'y', 'z'}, "~x & y & z & x", 1).bitwise[0]) == '0'

    # nbop = toNumberOperation({'x', 'y'}, "(y^(x>>4))&0xF0F0F0F", 32)
