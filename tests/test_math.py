# 文件: tests/test_math.py

import pytest

# 一个简单的加法函数
def add(x, y):
    return x + y

# 测试用例 1: 测试加法功能是否正确 (这个会通过)
def test_addition():
    print("\n正在测试加法...")
    assert add(2, 3) == 5

# 测试用例 2: 测试一个预期会失败的场景 (这个会失败)
def test_subtraction_fails():
    print("\n正在测试一个错误的减法...")
    assert 5 - 3 == 1  # 故意写错，正确应该是 2

# 测试用例 3: 测试可能引发异常的场景 (这个会通过)
def test_division_by_zero():
    print("\n正在测试除零异常...")
    with pytest.raises(ZeroDivisionError):
        result = 1 / 0
