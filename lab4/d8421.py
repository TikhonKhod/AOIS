from sympy import symbols, SOPform

# Определяем переменные
W, X, Y, Z = symbols('W X Y Z')

# On-set и don't-care для каждой выходной функции
on_sets = {'A': [], 'B': [], 'C': [], 'D': []}
dc_set = []
for dec in range(16):
    bits = ((dec >> 3) & 1, (dec >> 2) & 1, (dec >> 1) & 1, dec & 1)
    if dec <= 9:
        out = dec + 5
        out_bits = ((out >> 3) & 1, (out >> 2) & 1, (out >> 1) & 1, out & 1)
        if out_bits[0]: on_sets['A'].append(bits)
        if out_bits[1]: on_sets['B'].append(bits)
        if out_bits[2]: on_sets['C'].append(bits)
        if out_bits[3]: on_sets['D'].append(bits)
    else:
        dc_set.append(bits)

# Минимизируем SOP с don't-care
A_expr = SOPform([W, X, Y, Z], on_sets['A'], dc_set)
B_expr = SOPform([W, X, Y, Z], on_sets['B'], dc_set)
C_expr = SOPform([W, X, Y, Z], on_sets['C'], dc_set)
D_expr = SOPform([W, X, Y, Z], on_sets['D'], dc_set)

if __name__ == '__main__':
    print("Минимизированные СДНФ преобразователя Д8421→Д8421+5:")
    print(f"A = {A_expr}")
    print(f"B = {B_expr}")
    print(f"C = {C_expr}")
    print(f"D = {D_expr}")

    print("\nПроверка преобразования для всех входов 0–9:")
    for dec in range(10):
        bits_in = ((dec >> 3) & 1, (dec >> 2) & 1, (dec >> 1) & 1, dec & 1)
        subs_map = {W: bits_in[0], X: bits_in[1], Y: bits_in[2], Z: bits_in[3]}
        bits_out = (
            int(bool(A_expr.subs(subs_map))),
            int(bool(B_expr.subs(subs_map))),
            int(bool(C_expr.subs(subs_map))),
            int(bool(D_expr.subs(subs_map)))
        )
        print(f"{dec:>2} -> {dec+5:>2} (bits {bits_out})")