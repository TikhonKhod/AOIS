from sympy import symbols, SOPform, And, Or

# Определяем переменные
A, B, Cin = symbols('A B Cin')

# Формируем список минтермов для функций S и Cout (каноническая СДНФ)
minterms_S = []
minterms_Cout = []
for a in (0, 1):
    for b in (0, 1):
        for c in (0, 1):
            S_bit = (a ^ b) ^ c
            Cout_bit = (a & b) or (a & c) or (b & c)
            if S_bit:
                minterms_S.append((a, b, c))
            if Cout_bit:
                minterms_Cout.append((a, b, c))

# Построение канонической СДНФ через OR от всех минтермов
def canonical_sdnf(vars_list, minterms):
    return Or(*[
        And(*[var if bit else ~var for var, bit in zip(vars_list, term)])
        for term in minterms
    ])

S_canonical = canonical_sdnf([A, B, Cin], minterms_S)
Cout_canonical = canonical_sdnf([A, B, Cin], minterms_Cout)

# Минимизация (минимизированная СФНФ)
S_min = SOPform([A, B, Cin], minterms_S)
Cout_min = SOPform([A, B, Cin], minterms_Cout)

if __name__ == '__main__':
    print("Каноническая СДНФ функций сумматора ОДС-3:")
    print(f"S_canonical   = {S_canonical}")
    print(f"Cout_canonical = {Cout_canonical}\n")
    print("Минимизированные СФНФ функций сумматора ОДС-3:")
    print(f"S_min         = {S_min}")
    print(f"Cout_min      = {Cout_min}\n")

    # Функция вычисления сумматора
    def odc3(a: int, b: int, cin: int) -> tuple[int, int]:
        if a not in (0, 1) or b not in (0, 1) or cin not in (0, 1):
            raise ValueError("Входы должны быть 0 или 1")
        subs = {A: a, B: b, Cin: cin}
        return int(bool(S_min.subs(subs))), int(bool(Cout_min.subs(subs)))

    # Проверка таблицы истинности
    print("Проверка таблицы истинности: a b cin -> S Cout")
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                s, co = odc3(a, b, c)
                print(a, b, c, '->', s, co)
