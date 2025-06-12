import pytest

from main import (
    get_bin_representations,
    two_comp_to_int,
    add_in_twos,
    subtract_in_twos,
    multiply_bin,
    divide_bin,
    float_to_ieee754_manual,
    ieee754_to_float_manual,
    add_floats_ieee,
    format_binary_output,
)

def test_get_bin_representations_positive():
    # для положительных чисел direct==ones==twos
    d, o, t = get_bin_representations(5, bits=8)
    assert d == '00000101'
    assert o == '00000101'
    assert t == '00000101'

def test_get_bin_representations_negative():
    # -5: прямой код 1+magnitude_bits, обратный и дополнительный считаются от positive_repr
    direct, ones, twos = get_bin_representations(-5, bits=8)
    # magnitude_bits для 5: '0000101'
    assert direct == '1' + '0000101'
    # positive_repr для 5: '00000101', ones = инверсия, twos = ones+1
    assert ones == '11111010'
    assert twos == '11111011'

def test_two_comp_to_int():
    assert two_comp_to_int('00001010') == 10
    assert two_comp_to_int('11110110') == -10
    # можно передать список битов
    assert two_comp_to_int(['1','1','1','1','0','1','1','0']) == -10

def test_add_in_twos_simple():
    val, bits = add_in_twos(7, 3, width=8)
    assert val == 10
    assert bits == '00001010'

def test_add_in_twos_overflow():
    # 127 + 1 = -128 в 8-битном доп. коде
    val, bits = add_in_twos(127, 1, width=8)
    assert val == -128
    assert bits == '10000000'

def test_subtract_in_twos():
    # 5 - 8 = -3
    val, bits = subtract_in_twos(5, 8, width=8)
    assert val == -3
    # проверим, что это действительно -3 в доп. коде: 253
    assert bits == format((256 - 3) & 0xFF, '08b')

def test_multiply_bin_positive():
    b, val = multiply_bin(6, 7, width=8)
    assert val == 42
    assert b == format(42, '08b')

def test_multiply_bin_negative():
    b, val = multiply_bin(-3, 4, width=8)
    assert val == -12
    # прямой код: знак 1 + magnitude_bits(12)
    assert b == '1' + format(12, '07b')

def test_divide_bin_simple():
    b, val = divide_bin(10, 2, frac_bits=5, width=8)
    assert val == 5.0
    # целая часть 00001010 // 2 = 5 -> '00000101', дробь нулевая
    assert b.startswith('00000101.')

def test_divide_bin_fractional():
    b, val = divide_bin(7, 2, frac_bits=5, width=8)
    assert pytest.approx(val, rel=1e-5) == 3.5
    # проверка первых бит дробной части (0.5 -> .10000)
    assert b.endswith('.10000')

def test_divide_bin_zero_division():
    with pytest.raises(ZeroDivisionError):
        divide_bin(5, 0)

def test_float_to_ieee754_manual_and_back():
    for x in [0.0, 1.0, -2.5, 3.1415926]:
        bits = float_to_ieee754_manual(x)
        assert len(bits) == 32
        # пропускаем бесконечность и NaN
        if x != 0.0 and abs(x) < float('inf'):
            back = ieee754_to_float_manual(bits)
            assert pytest.approx(back, rel=1e-6) == x

def test_ieee754_to_float_manual_errors():
    with pytest.raises(ValueError):
        ieee754_to_float_manual('01')  # слишком короткая строка

def test_add_floats_ieee_positive():
    val, bits = add_floats_ieee(1.5, 2.25)
    assert pytest.approx(val, rel=1e-6) == 3.75
    assert len(bits) == 32

def test_add_floats_ieee_negative_error():
    with pytest.raises(ValueError):
        add_floats_ieee(-1.0, 2.0)

def test_format_binary_output():
    assert format_binary_output('10110011') == '[1 0110011]'
    assert format_binary_output('0') == '[0 ]'

if __name__ == "__main__":
    pytest.main()
