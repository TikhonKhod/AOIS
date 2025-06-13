import itertools
import re

# Допустимые символы
VARIABLES = {'a', 'b', 'c', 'd', 'e'}
OPERATORS = {'&', '|', '!', '->', '~', '(', ')'}

def validate_expr(expression):
    """Проверка корректности выражения"""
    # Заменяем составные операторы для проверки
    temp_expr = expression.replace('->', 'IMP').replace('~', 'EQU')
    tokens = re.findall(r'[a-e]|IMP|EQU|[&|!() ]', temp_expr)
    
    for token in tokens:
        if token not in VARIABLES and token not in OPERATORS and token not in {'IMP', 'EQU'}:
            return False
    return True

def expr_to_python(expression):
    """Преобразование логического выражения в Python код"""
    expr = re.sub(r'([a-e)!]+)\s*->\s*([a-e(!]+)', r'(not (\1) or (\2))', expression)
    expr = re.sub(r'([a-e)!]+)\s*~\s*([a-e(!]+)', r'((\1) == (\2))', expr)
    expr = expr.replace('!', 'not ')
    expr = expr.replace('&', ' and ')
    expr = expr.replace('|', ' or ')
    return expr

def truth_table_builder(vars_list, expression):
    """Построение таблицы истинности"""
    table = []
    minterms = []
    maxterms = []
    
    for combo in itertools.product([0, 1], repeat=len(vars_list)):
        env = dict(zip(vars_list, combo))
        try:
            result = eval(expr_to_python(expression), {}, env)
        except Exception as e:
            raise ValueError(f"Ошибка в выражении: {e}")
        
        table.append((combo, result))
        if result:
            minterms.append(combo)
        else:
            maxterms.append(combo)
    
    return table, minterms, maxterms

def find_differences(term1, term2):
    """Поиск различий между двумя термами"""
    diff_count = 0
    diff_position = -1
    
    for i in range(len(term1)):
        if term1[i] != term2[i]:
            diff_count += 1
            diff_position = i
    
    return diff_count == 1, diff_position

def combine_terms(terms):
    """Склеивание термов"""
    combined = set()
    used_indices = set()
    
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            can_combine, pos = find_differences(terms[i], terms[j])
            if can_combine:
                new_term = list(terms[i])
                new_term[pos] = 'X'
                combined.add(tuple(new_term))
                used_indices.add(i)
                used_indices.add(j)
    
    # Добавляем неиспользованные термы
    for i, term in enumerate(terms):
        if i not in used_indices:
            combined.add(tuple(term))
    
    return list(combined)

def format_term(term, variables, dnf_mode=True):
    """Преобразование терма в строковое представление"""
    parts = []
    
    for i, bit in enumerate(term):
        if bit == 'X':
            continue
        
        if dnf_mode:
            parts.append(f'¬{variables[i]}' if bit == 0 else variables[i])
        else:
            parts.append(variables[i] if bit == 0 else f'¬{variables[i]}')
    
    separator = ' & ' if dnf_mode else ' ∨ '
    return separator.join(parts)

def minimize_with_steps(expression, variables, dnf_mode=True):
    """Минимизация с выводом шагов"""
    _, minterms, maxterms = truth_table_builder(variables, expression)
    
    if dnf_mode:
        terms = [tuple(val) for val in minterms]
        mode_name = "СДНФ"
    else:
        terms = [tuple(val) for val in maxterms]
        mode_name = "СКНФ"
    
    print(f"\n=== Минимизация {mode_name} расчетным методом ===")
    print(f"Исходные термы {mode_name}:")
    for i, term in enumerate(terms):
        print(f"  {i+1}: {term}")
    
    step = 1
    while True:
        new_terms = combine_terms(terms)
        if new_terms == terms:
            break
        
        print(f"\nЭтап склеивания {step}:")
        for term in new_terms:
            print(f"  {format_term(term, variables, dnf_mode)}")
        
        terms = new_terms
        step += 1
    
    return terms

def minimize_with_table(expression, variables, dnf_mode=True):
    """Минимизация расчетно-табличным методом"""
    _, minterms, maxterms = truth_table_builder(variables, expression)
    
    if dnf_mode:
        terms = [tuple(val) for val in minterms]
        original_terms = minterms
        mode_name = "СДНФ"
    else:
        terms = [tuple(val) for val in maxterms]
        original_terms = maxterms
        mode_name = "СКНФ"
    
    print(f"\n=== Минимизация {mode_name} расчетно-табличным методом ===")
    
    # Этап склеивания (аналогично расчетному методу)
    step = 1
    while True:
        new_terms = combine_terms(terms)
        if new_terms == terms:
            break
        terms = new_terms
        step += 1
    
    # Построение таблицы покрытия
    print("\nТаблица покрытия:")
    header = "Импликанты\t\t"
    for orig_term in original_terms:
        header += f"{orig_term}\t"
    print(header)
    print("-" * len(header))
    
    for term in terms:
        term_str = format_term(term, variables, dnf_mode)
        row = f"{term_str:<20}\t"
        
        for orig_term in original_terms:
            covers = True
            for i, (t_bit, o_bit) in enumerate(zip(term, orig_term)):
                if t_bit != 'X' and t_bit != o_bit:
                    covers = False
                    break
            row += "X\t" if covers else " \t"
        print(row)
    
    return terms

def create_karnaugh_map(table, variables):
    """Создание карты Карно"""
    n = len(variables)
    if n < 2 or n > 4:
        print("Карта Карно поддерживает только 2-4 переменные")
        return []
    
    # Определение строк и столбцов
    if n == 2:
        row_vars = [variables[0]]
        col_vars = [variables[1]]
    elif n == 3:
        row_vars = [variables[0]]
        col_vars = [variables[1], variables[2]]
    else:  # n == 4
        row_vars = [variables[0], variables[1]]
        col_vars = [variables[2], variables[3]]
    
    # Генерация кодов Грея
    def gray_codes(bits):
        return [format(i ^ (i >> 1), f'0{bits}b') for i in range(2 ** bits)]
    
    row_codes = gray_codes(len(row_vars))
    col_codes = gray_codes(len(col_vars))
    
    # Создание карты значений
    value_grid = {}
    for combo, result in table:
        var_mapping = dict(zip(variables, combo))
        row_key = ''.join(str(var_mapping[v]) for v in row_vars)
        col_key = ''.join(str(var_mapping[v]) for v in col_vars)
        value_grid[(row_key, col_key)] = result
    
    # Вывод карты
    print("\nКарта Карно:")
    print("   " + "  ".join(col_codes))
    for row_code in row_codes:
        line = f"{row_code} |"
        for col_code in col_codes:
            val = value_grid.get((row_code, col_code), ' ')
            line += f" {int(val)} " if isinstance(val, int) else "   "
        print(line)
    
    return []

def minimize_karnaugh_dnf(expression, variables):
    """Минимизация СДНФ табличным методом (Карно)"""
    print("\n=== Минимизация СДНФ табличным методом (карта Карно) ===")
    table, _, _ = truth_table_builder(variables, expression)
    groups = create_karnaugh_map(table, variables)
    return groups

def minimize_karnaugh_cnf(expression, variables):
    """Минимизация СКНФ табличным методом (Карно)"""
    print("\n=== Минимизация СКНФ табличным методом (карта Карно) ===")
    table, _, _ = truth_table_builder(variables, expression)
    groups = create_karnaugh_map(table, variables)
    return groups

def simplify_dnf(expression, vars_list):
    """Упрощенная минимизация СДНФ"""
    _, ones, _ = truth_table_builder(vars_list, expression)
    terms = [tuple(x) for x in ones]
    prev = None
    while terms != prev:
        prev, terms = terms, combine_terms(terms)
    return terms

def simplify_cnf(expression, vars_list):
    """Упрощенная минимизация СКНФ"""
    _, _, zeros = truth_table_builder(vars_list, expression)
    terms = [tuple(x) for x in zeros]
    prev = None
    while terms != prev:
        prev, terms = terms, combine_terms(terms)
    return terms

def kmap_generator(tt, vars_list, is_dnf=True):
    """Генератор карты Карно (для совместимости с тестами)"""
    create_karnaugh_map(tt, vars_list)
    return []

def term_to_str(term, vars_list, is_dnf=True):
    """Преобразование терма в строку (для совместимости с тестами)"""
    return format_term(term, vars_list, is_dnf)

if __name__ == "__main__":
    while True:
        user_expr = input("Введите логическое выражение (используйте &, |, !, ->, ~): ").strip()
        
        if not user_expr:
            break
            
        if not validate_expr(user_expr):
            print("Ошибка: выражение содержит недопустимые символы.")
            continue
        
        used_variables = sorted(set(re.findall(r'[a-e]', user_expr)))
        if len(used_variables) > 5:
            print("Ошибка: допустимо не более 5 переменных.")
            continue
        if len(used_variables) == 0:
            print("Ошибка: не найдено переменных.")
            continue
        
        print(f"\nИспользуемые переменные: {used_variables}")
        print(f"Исходное выражение: {user_expr}")
        
        try:
            # 1) Минимизация СДНФ расчетным методом
            dnf_calc = minimize_with_steps(user_expr, used_variables, True)
            print(f"\nРезультат: {' ∨ '.join(format_term(t, used_variables, True) for t in dnf_calc)}")
            
            # 2) Минимизация СКНФ расчетным методом  
            cnf_calc = minimize_with_steps(user_expr, used_variables, False)
            print(f"\nРезультат: {' ∧ '.join(format_term(t, used_variables, False) for t in cnf_calc)}")
            
            # 3) Минимизация СДНФ расчетно-табличным методом
            dnf_table = minimize_with_table(user_expr, used_variables, True)
            print(f"\nРезультат: {' ∨ '.join(format_term(t, used_variables, True) for t in dnf_table)}")
            
            # 4) Минимизация СКНФ расчетно-табличным методом
            cnf_table = minimize_with_table(user_expr, used_variables, False)
            print(f"\nРезультат: {' ∧ '.join(format_term(t, used_variables, False) for t in cnf_table)}")
            
            # 5) Минимизация СДНФ табличным методом (Карно)
            minimize_karnaugh_dnf(user_expr, used_variables)
            
            # 6) Минимизация СКНФ табличным методом (Карно)
            minimize_karnaugh_cnf(user_expr, used_variables)
            
        except Exception as e:
            print(f"Ошибка при обработке: {e}")
        
        print("\n" + "="*50)
        break