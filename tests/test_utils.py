from main import calculate_discount
import pytest

def test_discount_normal():
    assert calculate_discount(100, 10) == 90.00

def test_discount_zero():
    assert calculate_discount(50, 0) == 50.00

def test_discount_full():
    assert calculate_discount(80, 100) == 0.00

def test_discount_rounding():
    assert calculate_discount(99.99, 15) == 84.99

def test_invalid_discount_low():
    with pytest.raises(ValueError):
        calculate_discount(100, -5)

def test_invalid_discount_high():
    with pytest.raises(ValueError):
        calculate_discount(100, 150)
