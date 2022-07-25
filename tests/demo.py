from BitwiseExpressionSimplifier import toNOperation


if __name__ == '__main__':
    # 验证单位位运算的化简情况
    assert str(toNOperation("1 & ~1 | 1", 1).bitwise[0]) == '1'
    assert str(toNOperation("((((x))))", 1, {'x'}).bitwise[0]) == 'x[0]'
    assert str(toNOperation("1 & x", 1, {'x'}).bitwise[0]) == 'x[0]'
    assert str(toNOperation("x & 1", 1, {'x'}).bitwise[0]) == 'x[0]'
    assert str(toNOperation("0 & x", 1, {'x'}).bitwise[0]) == '0'
    assert str(toNOperation("x & 0", 1, {'x'}).bitwise[0]) == '0'
    assert str(toNOperation("x & y & x", 1, {'x', 'y'}).bitwise[0]) == 'x[0] & y[0]'
    assert str(toNOperation("x & (y & x)", 1, {'x', 'y'}).bitwise[0]) == 'y[0] & x[0]'
    assert str(toNOperation("(x & y) & (y & x)", 1, {'x', 'y'}).bitwise[0]) == 'x[0] & y[0]'
    assert str(toNOperation("(x & z & y) & (y & x)", 1, {'x', 'y', 'z'}).bitwise[0]) == '(x[0] & z[0]) & y[0]'
    assert str(toNOperation("(0 | x & 1) & x", 1, {'x'}).bitwise[0]) == 'x[0]'
    assert str(toNOperation("(1 | x & 0) & x", 1, {'x'}).bitwise[0]) == 'x[0]'
    assert str(toNOperation("x & ~x", 1, {'x'}).bitwise[0]) == '0'
    assert str(toNOperation("x & x", 1, {'x'}).bitwise[0]) == 'x[0]'
    assert str(toNOperation("x & y & (~x & y & z)", 1, {'x', 'y', 'z'}).bitwise[0]) == '0'
    assert str(toNOperation("~x & y & z & x", 1, {'x', 'y', 'z'}).bitwise[0]) == '0'
    assert str(toNOperation("(x ^ y) ^ (y ^ ~x)", 1, {'x', 'y', 'z'}).bitwise[0]) == '1'

    # 每字节中，新x高四位为原x高四位，新x低四位为原y高四位，新y高四位为原x低四位，新y低四位为原y低四位
    base = toNOperation("(x^(y>>4))&0xf0f0f0f", 32, {'x', 'y'})
    x = toNOperation("x^base", 32, {'x'}, {'base': base})
    y = toNOperation("y^(base<<4)", 32, {'y'}, {'base': base})
    assert ", ".join([str(i) for i in x.bitwise][::-1]) == 'x[31], x[30], x[29], x[28], y[31], y[30], y[29], y[28], x[23], x[22], x[21], x[20], y[23], y[22], y[21], y[20], x[15], x[14], x[13], x[12], y[15], y[14], y[13], y[12], x[7], x[6], x[5], x[4], y[7], y[6], y[5], y[4]'
    assert ", ".join([str(i) for i in y.bitwise][::-1]) == 'x[27], x[26], x[25], x[24], y[27], y[26], y[25], y[24], x[19], x[18], x[17], x[16], y[19], y[18], y[17], y[16], x[11], x[10], x[9], x[8], y[11], y[10], y[9], y[8], x[3], x[2], x[1], x[0], y[3], y[2], y[1], y[0]'
