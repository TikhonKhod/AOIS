def get_bin_representations(value: int, bits: int = 8):
    if value >= 0:
        bin_repr = format(value, f'0{bits}b')
        return bin_repr, bin_repr, bin_repr
    else:
        abs_value = abs(value)
        magnitude_bits = format(abs_value, f'0{bits-1}b')
        direct = '1' + magnitude_bits
        positive_repr = format(abs_value, f'0{bits}b')
        ones = ''.join('1' if b == '0' else '0' for b in positive_repr)
        ones_int = int(ones, 2)
        twos_int = (ones_int + 1) & ((1 << bits) - 1)
        twos = format(twos_int, f'0{bits}b')
        return direct, ones, twos

def two_comp_to_int(bits_list):
    if isinstance(bits_list, str):
        bits = bits_list
    else:
        bits = ''.join(str(b) for b in bits_list)
    
    if bits[0] == '0':
        return int(bits, 2)
    else:
        inverted = ''.join('1' if b == '0' else '0' for b in bits)
        magnitude = int(inverted, 2) + 1
        return -magnitude

def add_in_twos(a: int, b: int, width: int = 8):
    _, _, ta = get_bin_representations(a, width)
    _, _, tb = get_bin_representations(b, width)
    
    result_bits = []
    carry = 0
    
    for i in range(width-1, -1, -1):
        bit_sum = carry + int(ta[i]) + int(tb[i])
        result_bits.append(str(bit_sum & 1))
        carry = bit_sum >> 1
    
    result_bits.reverse()
    result_str = ''.join(result_bits)
    result_val = two_comp_to_int(result_str)
    
    return result_val, result_str

def subtract_in_twos(a: int, b: int, width: int = 8):
    return add_in_twos(a, -b, width)

def multiply_bin(a: int, b: int, width: int = 8):
    result_negative = (a < 0) ^ (b < 0)
    abs_a = abs(a)
    abs_b = abs(b)
    product = abs_a * abs_b
    
    if result_negative:
        magnitude_bits = format(product, f'0{width-1}b')
        if len(magnitude_bits) > width - 1:
            magnitude_bits = magnitude_bits[-(width-1):]
        result_bin = '1' + magnitude_bits
        result_val = -product
    else:
        result_bin = format(product, f'0{width}b')
        if len(result_bin) > width:
            result_bin = result_bin[-width:]
        result_val = product
    
    return result_bin, result_val

def divide_bin(a: int, b: int, frac_bits: int = 5, width: int = 8):
    if b == 0:
        raise ZeroDivisionError("Деление на ноль")
    
    result_negative = (a < 0) ^ (b < 0)
    abs_a = abs(a)
    abs_b = abs(b)
    
    quotient = abs_a // abs_b
    remainder = abs_a % abs_b
    
    if result_negative:
        int_bits = format(quotient, f'0{width-1}b')
        if len(int_bits) > width - 1:
            int_bits = int_bits[-(width-1):]
        sign_bit = '1'
    else:
        int_bits = format(quotient, f'0{width}b')
        if len(int_bits) > width:
            int_bits = int_bits[-width:]
        sign_bit = '0' if not result_negative else '1'
    
    frac_bits_list = []
    current_remainder = remainder
    
    for _ in range(frac_bits):
        current_remainder *= 2
        if current_remainder >= abs_b:
            frac_bits_list.append('1')
            current_remainder -= abs_b
        else:
            frac_bits_list.append('0')
    
    if result_negative and quotient > 0:
        binary_result = sign_bit + int_bits + '.' + ''.join(frac_bits_list)
    else:
        binary_result = int_bits + '.' + ''.join(frac_bits_list)
    
    decimal_result = quotient
    for i, bit in enumerate(frac_bits_list):
        if bit == '1':
            decimal_result += 2 ** (-(i + 1))
    
    if result_negative:
        decimal_result = -decimal_result
    
    return binary_result, round(decimal_result, frac_bits)

def float_to_ieee754_manual(value: float):
    if value == 0.0:
        return '0' * 32
    
    sign = '1' if value < 0 else '0'
    value = abs(value)
    
    integer_part = int(value)
    fractional_part = value - integer_part
    
    if integer_part == 0:
        int_binary = '0'
    else:
        int_binary = bin(integer_part)[2:]
    
    frac_binary = ''
    while fractional_part > 0 and len(frac_binary) < 50:
        fractional_part *= 2
        if fractional_part >= 1:
            frac_binary += '1'
            fractional_part -= 1
        else:
            frac_binary += '0'
    
    if integer_part == 0:
        first_one = frac_binary.find('1')
        if first_one == -1:
            return '0' * 32
        exponent = -(first_one + 1)
        mantissa = frac_binary[first_one + 1:]
    else:
        exponent = len(int_binary) - 1
        mantissa = int_binary[1:] + frac_binary
    
    biased_exponent = exponent + 127
    
    if biased_exponent >= 255:
        return sign + '1' * 8 + '0' * 23
    elif biased_exponent <= 0:
        return sign + '0' * 31
    
    exp_binary = format(biased_exponent, '08b')
    
    if len(mantissa) > 23:
        mantissa = mantissa[:23]
    else:
        mantissa = mantissa.ljust(23, '0')
    
    return sign + exp_binary + mantissa

def ieee754_to_float_manual(bit_string: str):
    if len(bit_string) != 32:
        raise ValueError("Строка должна содержать 32 бита")
    
    sign_bit = bit_string[0]
    exponent_bits = bit_string[1:9]
    mantissa_bits = bit_string[9:32]
    
    sign = -1 if sign_bit == '1' else 1
    exponent = int(exponent_bits, 2)
    
    if exponent == 0:
        if mantissa_bits == '0' * 23:
            return 0.0
        else:
            return 0.0
    elif exponent == 255:
        return float('inf') * sign if mantissa_bits == '0' * 23 else float('nan')
    else:
        real_exponent = exponent - 127
        mantissa_value = 1.0
        for i, bit in enumerate(mantissa_bits):
            if bit == '1':
                mantissa_value += 2 ** (-(i + 1))
        
        return sign * mantissa_value * (2 ** real_exponent)

def add_floats_ieee(a: float, b: float):
    if a < 0 or b < 0:
        raise ValueError("Функция работает только с положительными числами")
    
    result = a + b
    ieee_bits = float_to_ieee754_manual(result)
    
    return result, ieee_bits

def format_binary_output(bits: str):
    return f"[{bits[0]} {bits[1:]}]"

# pragma: no cover
def interactive(): # pragma: no cover
    while True:
        try:
            x = int(input("Ввод числа №1\n"))
            break
        except ValueError:
            print("Ошибка ввода")
    
    print(f"Число введено: {x}")
    d1, o1, t1 = get_bin_representations(x, 8)
    print(f"Прямой код: {format_binary_output(d1)}")
    print(f"Обратный код: {format_binary_output(o1)}")
    print(f"Дополнительный код: {format_binary_output(t1)}")
    
    while True:
        try:
            y = int(input("Ввод числа №2\n"))
            break
        except ValueError:
            print("Ошибка ввода")
    
    print(f"Число введено: {y}")
    d2, o2, t2 = get_bin_representations(y, 8)
    print(f"Прямой код: {format_binary_output(d2)}")
    print(f"Обратный код: {format_binary_output(o2)}")
    print(f"Дополнительный код: {format_binary_output(t2)}")
    
    sum_val, sum_bin = add_in_twos(x, y, 8)
    print(f"Результат: {sum_val}")
    d_sum, o_sum, t_sum = get_bin_representations(sum_val, 8)
    print(f"Прямой код: {format_binary_output(d_sum)}")
    print(f"Обратный код: {format_binary_output(o_sum)}")
    print(f"Дополнительный код: {format_binary_output(t_sum)}")
    
    diff_val, diff_bin = subtract_in_twos(x, y, 8)
    print(f"Вычитание: {diff_val}")
    
    mult_bin, mult_val = multiply_bin(x, y, 8)
    print(f"Умножение: {mult_val}")
    
    try:
        div_bin, div_val = divide_bin(x, y, frac_bits=5, width=8)
        print(f"Деление: {div_val}")
    except ZeroDivisionError:
        print("Деление на ноль")
    
    while True:
        try:
            f1 = float(input("Первое положительное число: "))
            if f1 < 0:
                print("Число должно быть положительным")
                continue
            break
        except ValueError:
            print("Ошибка ввода")
    
    while True:
        try:
            f2 = float(input("Второе положительное число: "))
            if f2 < 0:
                print("Число должно быть положительным")
                continue
            break
        except ValueError:
            print("Ошибка ввода")
    
    try:
        sum_float, sum_ieee = add_floats_ieee(f1, f2)
        print(f"Сумма: {sum_float}")
        print(f"IEEE-754: {sum_ieee}")
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    interactive()