from __future__ import annotations

__all__ = ["BOperation", "BExpression", "BNumber", "BKnownNumber"]


class BOperation(object):
    def setNegate(self) -> None:
        raise Exception

    def setNegateL(self) -> BOperation:
        self.setNegate()
        return self

    def getNegate(self) -> bool:
        return False

    def copy(self) -> BOperation:
        raise Exception


class BExpression(BOperation):
    def __init__(self, left: BOperation, operator: str, right: BOperation):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right
        self._simplified = False

        if operator == '&':
            if type(left) is BNumber and left.bit == 1:  # 1 & x == x
                self._simplified = True
                self._simplify = right
            elif type(right) is BNumber and right.bit == 1:  # x & 1 == x
                self._simplified = True
                self._simplify = left
            elif type(left) is BNumber and left.bit == 0:  # 0 & x == 0
                self._simplified = True
                self._simplify = left
            elif type(right) is BNumber and right.bit == 0:  # x & 0 == 0
                self._simplified = True
                self._simplify = right
            elif type(left) is BExpression and type(right) is not BExpression:
                left_set: set[BOperation] = left.getContinuousHashSet(operator)
                if right in left_set:  # (x & y & ...) & x == (x & y & ...)
                    self._simplified = True
                    self._simplify = left
                elif right.copy().setNegateL() in left_set:  # (x & y & ...) & ~x == 0
                    self._simplified = True
                    self._simplify = BNumber(0)
            elif type(left) is not BExpression and type(right) is BExpression:
                right_set: set[BOperation] = right.getContinuousHashSet(operator)
                if left in right_set:  # x & (x & y & ...) == (x & y & ...)
                    self._simplified = True
                    self._simplify = right
                elif left.copy().setNegateL() in right_set:  # ~x & (x & y & ...) == 0
                    self._simplified = True
                    self._simplify = BNumber(0)
            elif type(left) is BExpression and type(right) is BExpression:
                left_set: set[BOperation] = left.getContinuousHashSet(operator)
                right_set: set[BOperation] = right.getContinuousHashSet(operator)
                left_negated_set: set[BOperation] = set(i.copy().setNegateL() for i in left_set)
                right_negated_set: set[BOperation] = set(i.copy().setNegateL() for i in right_set)
                if len(left_set & right_negated_set) > 0:  # (x & y & ...) & (~y & z & ...) == 0
                    self._simplified = True
                    self._simplify = BNumber(0)
                elif len(left_negated_set & right_set) > 0:  # (x & ~y & ...) & (y & z & ...) == 0
                    self._simplified = True
                    self._simplify = BNumber(0)
                elif len(left_set & right_set) > 0:  # (x & y & ...) & (y & z & ...) == (x & y & ...) & (z & ...)
                    for same_operation in left_set & right_set:
                        if type(self.right) is BExpression:
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
                self._simplify = BNumber(0)
            else:
                ...
        elif operator == '|':
            if type(left) is BNumber and left.bit == 1:  # 1 | x == 1
                self._simplified = True
                self._simplify = left
            elif type(right) is BNumber and right.bit == 1:  # x | 1 == 1
                self._simplified = True
                self._simplify = right
            elif type(left) is BNumber and left.bit == 0:  # 0 | x == x
                self._simplified = True
                self._simplify = right
            elif type(right) is BNumber and right.bit == 0:  # x | 0 == x
                self._simplified = True
                self._simplify = left
            elif type(left) is BExpression and type(right) is not BExpression:
                left_set: set[BOperation] = left.getContinuousHashSet(operator)
                if right in left_set:  # (x | y | ...) | x == (x | y | ...)
                    self._simplified = True
                    self._simplify = left
                elif right.copy().setNegateL() in left_set:  # (x | y | ...) | ~x == 1
                    self._simplified = True
                    self._simplify = BNumber(1)
            elif type(left) is not BExpression and type(right) is BExpression:
                right_set: set[BOperation] = right.getContinuousHashSet(operator)
                if left in right_set:  # x | (x | y | ...) == (x | y | ...)
                    self._simplified = True
                    self._simplify = right
                elif left.copy().setNegateL() in right_set:  # ~x | (x | y | ...) == 1
                    self._simplified = True
                    self._simplify = BNumber(1)
            elif type(left) is BExpression and type(right) is BExpression:
                left_set: set[BOperation] = left.getContinuousHashSet(operator)
                right_set: set[BOperation] = right.getContinuousHashSet(operator)
                left_negated_set: set[BOperation] = set(i.copy().setNegateL() for i in left_set)
                right_negated_set: set[BOperation] = set(i.copy().setNegateL() for i in right_set)
                if len(left_set & right_negated_set) > 0:  # (x | y | ...) | (~y | z | ...) == 1
                    self._simplified = True
                    self._simplify = BNumber(1)
                elif len(left_negated_set & right_set) > 0:  # (x | ~y | ...) | (y | z | ...) == 1
                    self._simplified = True
                    self._simplify = BNumber(1)
                elif len(left_set & right_set) > 0:  # (x | y | ...) | (y | z | ...) == (x | y | ...) | (z | ...)
                    for same_operation in left_set & right_set:
                        if type(self.right) is BExpression:
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
                self._simplify = BNumber(1)
            else:
                ...
        elif operator == '^':
            if type(left) is BNumber and left.bit == 0:  # 0 ^ x == x
                self._simplified = True
                self._simplify = right
            elif type(right) is BNumber and right.bit == 0:  # x ^ 0 == x
                self._simplified = True
                self._simplify = left
            elif type(left) is BNumber and left.bit == 1:  # 1 ^ x == ~x
                self._simplified = True
                right.setNegate()
                self._simplify = right
            elif type(right) is BNumber and right.bit == 1:  # x ^ 1 == ~x
                self._simplified = True
                left.setNegate()
                self._simplify = left
            elif type(left) is BExpression and type(right) is not BExpression:
                left_set: set[BOperation] = left.getContinuousHashSet(operator)
                if right in left_set:  # (x ^ y ^ ...) ^ x == (y ^ ...)
                    self._simplified = True
                    self._simplify = left.removeContinuousOperation(operator, right)
                elif right.copy().setNegateL() in left_set:  # (x ^ y ^ ...) ^ ~x == ~(y ^ ...)
                    self._simplified = True
                    self._simplify = left.removeContinuousOperation(operator, right.copy().setNegateL()).setNegateL()
            elif type(left) is not BExpression and type(right) is BExpression:
                right_set: set[BOperation] = right.getContinuousHashSet(operator)
                if left in right_set:  # x ^ (x ^ y ^ ...) == (y ^ ...)
                    self._simplified = True
                    self._simplify = right.removeContinuousOperation(operator, left)
                elif left.copy().setNegateL() in right_set:  # ~x ^ (x ^ y ^ ...) == ~(y ^ ...)
                    self._simplified = True
                    self._simplify = right.removeContinuousOperation(operator, left.copy().setNegateL()).setNegateL()
            elif type(left) is BExpression and type(right) is BExpression:
                left_set: set[BOperation] = left.getContinuousHashSet(operator)
                right_set: set[BOperation] = right.getContinuousHashSet(operator)
                left_negated_set: set[BOperation] = set(i.copy().setNegateL() for i in left_set)
                right_negated_set: set[BOperation] = set(i.copy().setNegateL() for i in right_set)
                if len(left_set & right_negated_set) > 0:  # (x ^ y ^ ...) ^ (~y ^ z ^ ...) == ~((x ^ ...) ^ ( z ^ ...))
                    for same_operation in left_set & right_negated_set:
                        if type(self.left) is BExpression and type(self.right) is BExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = self.right.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                        elif self.left == same_operation and type(self.right) is BExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.left = None
                        elif type(self.left) is BExpression and self.right == same_operation.copy().setNegateL():
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
                        if type(self.left) is BExpression and type(self.right) is BExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.left == same_operation.copy().setNegateL() and type(self.right) is BExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation)
                            self.left = None
                        elif type(self.left) is BExpression and self.right == same_operation:
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
                        if type(self.left) is BExpression and type(self.right) is BExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.left == same_operation and type(self.right) is BExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation)
                            self.left = None
                        elif type(self.left) is BExpression and self.right == same_operation:
                            self._simplified = True
                            self._simplify = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = None
                        else:
                            raise Exception
            elif left == right:  # x ^ x == 0
                self._simplified = True
                self._simplify = BNumber(0)
            elif left == right.copy().setNegateL():  # x ^ ~x == 1
                self._simplified = True
                self._simplify = BNumber(1)
            else:
                ...
        elif operator == '⊙':
            if type(left) is BNumber and left.bit == 1:  # 1 ⊙ x == x
                self._simplified = True
                self._simplify = right
            elif type(right) is BNumber and right.bit == 1:  # x ⊙ 1 == x
                self._simplified = True
                self._simplify = left
            elif type(left) is BNumber and left.bit == 0:  # 0 ⊙ x == ~x
                self._simplified = True
                right.setNegate()
                self._simplify = right
            elif type(right) is BNumber and right.bit == 0:  # x ⊙ 0 == ~x
                self._simplified = True
                left.setNegate()
                self._simplify = left
            elif type(left) is BExpression and type(right) is not BExpression:
                left_set: set[BOperation] = left.getContinuousHashSet(operator)
                if right in left_set:  # (x ⊙ y ⊙ ...) ⊙ x == (y ⊙ ...)
                    self._simplified = True
                    self._simplify = left.removeContinuousOperation(operator, right)
                elif right.copy().setNegateL() in left_set:  # (x ⊙ y ⊙ ...) ⊙ ~x == ~(y ⊙ ...)
                    self._simplified = True
                    self._simplify = left.removeContinuousOperation(operator, right.copy().setNegateL()).setNegateL()
            elif type(left) is not BExpression and type(right) is BExpression:
                right_set: set[BOperation] = right.getContinuousHashSet(operator)
                if left in right_set:  # x ⊙ (x ⊙ y ⊙ ...) == (y ⊙ ...)
                    self._simplified = True
                    self._simplify = right.removeContinuousOperation(operator, left)
                elif left.copy().setNegateL() in right_set:  # ~x ⊙ (x ⊙ y ⊙ ...) == ~(y ⊙ ...)
                    self._simplified = True
                    self._simplify = right.removeContinuousOperation(operator, left.copy().setNegateL()).setNegateL()
            elif type(left) is BExpression and type(right) is BExpression:
                left_set: set[BOperation] = left.getContinuousHashSet(operator)
                right_set: set[BOperation] = right.getContinuousHashSet(operator)
                left_negated_set: set[BOperation] = set(i.copy().setNegateL() for i in left_set)
                right_negated_set: set[BOperation] = set(i.copy().setNegateL() for i in right_set)
                if len(left_set & right_negated_set) > 0:  # (x ⊙ y ⊙ ...) ⊙ (~y ⊙ z ⊙ ...) == ~((x ⊙ ...) ⊙ ( z ⊙ ...))
                    for same_operation in left_set & right_negated_set:
                        if type(self.left) is BExpression and type(self.right) is BExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = self.right.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                        elif self.left == same_operation and type(self.right) is BExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.left = None
                        elif type(self.left) is BExpression and self.right == same_operation.copy().setNegateL():
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
                        if type(self.left) is BExpression and type(self.right) is BExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation.copy().setNegateL())
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.left == same_operation.copy().setNegateL() and type(self.right) is BExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation)
                            self.left = None
                        elif type(self.left) is BExpression and self.right == same_operation:
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
                        if type(self.left) is BExpression and type(self.right) is BExpression:
                            self.left = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = self.right.removeContinuousOperation(operator, same_operation)
                        elif self.left == same_operation and type(self.right) is BExpression:
                            self._simplified = True
                            self._simplify = self.right.removeContinuousOperation(operator, same_operation)
                            self.left = None
                        elif type(self.left) is BExpression and self.right == same_operation:
                            self._simplified = True
                            self._simplify = self.left.removeContinuousOperation(operator, same_operation)
                            self.right = None
                        else:
                            raise Exception
            elif left == right:  # x ⊙ x == 1
                self._simplified = True
                self._simplify = BNumber(1)
            elif left == right.copy().setNegateL():  # x ⊙ ~x == 0
                self._simplified = True
                self._simplify = BNumber(0)
            else:
                ...

    def __str__(self) -> str:
        return (str(self.left) if type(self.left) is not BExpression else f"({self.left})")\
               + f" {self.operator} "\
               + (str(self.right) if type(self.right) is not BExpression else f"({self.right})")

    def __eq__(self, other) -> bool:
        if type(other) is BExpression:
            return (self.left == other.left and self.operator == other.operator and self.right == other.right)\
                   or (self.left == other.right and self.operator == other.operator and self.left == other.right)
        return False

    def __hash__(self) -> int:
        return hash(self.operator)

    def getResult(self) -> BOperation:
        if self._simplified:
            return self._simplify
        else:
            return self

    def getContinuousHashSet(self, operator: str) -> set[BOperation]:
        """根据运算符提取连续同运算表达式中的所有运算数的 hash 集合"""
        if self.operator == operator:
            result: set[BOperation] = set()
            if type(self.left) == BExpression:
                result.update(self.left.getContinuousHashSet(operator))
            else:
                result.add(self.left)
            if type(self.right) == BExpression:
                result.update(self.right.getContinuousHashSet(operator))
            else:
                result.add(self.right)
            return result
        else:
            return {self}

    def removeContinuousOperation(self, operator: str, operation: BOperation) -> BOperation:
        if self.operator == operator:
            if self.left == operation:
                return self.right
            elif self.right == operation:
                return self.left
            elif type(self.left) == BExpression and operation in self.left.getContinuousHashSet(operator):
                self.left = self.left.removeContinuousOperation(operator, operation)
                return self
            elif type(self.right) == BExpression and operation in self.right.getContinuousHashSet(operator):
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

    def copy(self) -> BExpression:
        return BExpression(self.left.copy(), self.operator, self.right.copy())


class BNumber(BOperation):
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
        if type(other) is BNumber:
            return self.bit == other.bit
        return False

    def __hash__(self) -> int:
        return hash(self.bit)

    def setNegate(self) -> None:
        self.bit = 1 - self.bit

    def copy(self) -> BNumber:
        return BNumber(self.bit)


class BKnownNumber(BOperation):
    def __init__(self, name: str, index: int):
        super().__init__()
        self.name = name
        self.index = index
        self._negate = False

    def __str__(self) -> str:
        return f"{'~' if self._negate else ''}{self.name}[{self.index}]"

    def __eq__(self, other) -> bool:
        if type(other) is BKnownNumber:
            return self.name == other.name and self.index == other.index and self._negate == other.getNegate()
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def setNegate(self) -> None:
        self._negate = not self._negate

    def getNegate(self) -> bool:
        return self._negate

    def copy(self) -> BKnownNumber:
        rtn = BKnownNumber(self.name, self.index)
        if self.getNegate():
            rtn.setNegate()
        return rtn
