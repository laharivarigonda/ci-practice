from calculator import add, multiply, subtract, division


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(4, 3) == 12


def test_division():
    assert division(20, 2) == 10
