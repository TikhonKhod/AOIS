def main():
    print("Двоичный счетчик накапливающего типа на 8 состояний")
    print("T-триггеры, базис НЕ И-ИЛИ")
    
    # Таблица переходов
    print("\nТаблица переходов:")
    print("Q2 Q1 Q0 | Q2+ Q1+ Q0+ | T2 T1 T0")
    
    # Списки минтермов для каждой функции
    T2_minterms = []
    T1_minterms = []  
    T0_minterms = []
    
    for i in range(8):
        # Текущее состояние
        q2 = (i >> 2) & 1
        q1 = (i >> 1) & 1  
        q0 = i & 1
        
        # Следующее состояние (i+1) mod 8
        next_i = (i + 1) % 8
        q2_next = (next_i >> 2) & 1
        q1_next = (next_i >> 1) & 1
        q0_next = next_i & 1
        
        # Функции возбуждения T = Q XOR Q+
        t2 = q2 ^ q2_next
        t1 = q1 ^ q1_next
        t0 = q0 ^ q0_next
        
        print(f" {q2}  {q1}  {q0}  |  {q2_next}   {q1_next}   {q0_next}  |  {t2}  {t1}  {t0}")
        
        # Собираем минтермы
        if t2 == 1:
            T2_minterms.append((q2, q1, q0))
        if t1 == 1:
            T1_minterms.append((q2, q1, q0))
        if t0 == 1:
            T0_minterms.append((q2, q1, q0))
    
    print(f"\nМинтермы T2: {T2_minterms}")
    print(f"Минтермы T1: {T1_minterms}")
    print(f"Минтермы T0: {T0_minterms}")
    
    # Строим СДНФ вручную
    def build_sop(minterms, var_names):
        if not minterms:
            return "0"
        
        terms = []
        for minterm in minterms:
            term_parts = []
            for i, bit in enumerate(minterm):
                if bit == 1:
                    term_parts.append(var_names[i])
                else:
                    term_parts.append("¬" + var_names[i])
            terms.append("(" + " ∧ ".join(term_parts) + ")")
        
        return " ∨ ".join(terms)
    
    var_names = ["Q2", "Q1", "Q0"]
    
    print("\nИсходные СДНФ:")
    T2_sop = build_sop(T2_minterms, var_names)
    T1_sop = build_sop(T1_minterms, var_names)  
    T0_sop = build_sop(T0_minterms, var_names)
    
    print(f"T2 = {T2_sop}")
    print(f"T1 = {T1_sop}")
    print(f"T0 = {T0_sop}")
    
    # Простая минимизация вручную (анализ минтермов)
    print("\nМинимизация:")
    
    # T2: минтермы (1,0,0), (1,0,1), (1,1,0), (1,1,1) = Q2(¬Q1¬Q0 ∨ ¬Q1Q0 ∨ Q1¬Q0 ∨ Q1Q0) = Q2
    if T2_minterms:
        print("T2: все минтермы содержат Q2=1, остальные биты меняются")
        print("T2 = Q2")
    
    # T1: минтермы (0,1,0), (0,1,1), (1,0,0), (1,0,1) 
    if T1_minterms:
        print("T1: минтермы (0,1,0), (0,1,1) дают ¬Q2∧Q1")
        print("     минтермы (1,0,0), (1,0,1) дают Q2∧¬Q1")  
        print("T1 = ¬Q2∧Q1 ∨ Q2∧¬Q1 = Q2⊕Q1")
    
    # T0: все нечетные состояния
    if T0_minterms:
        print("T0: все минтермы имеют разные Q2,Q1 но всегда срабатывает")
        print("T0 = 1")
    
    print("\nМинимизированные функции:")
    print("T2 = Q2")
    print("T1 = Q2⊕Q1") 
    print("T0 = 1")
    
    # Преобразование в базис НЕ И-ИЛИ
    print("\nПреобразование в базис НЕ И-ИЛИ:")
    print("T2 = Q2")
    print("T1 = Q2⊕Q1 = (Q2∧¬Q1) ∨ (¬Q2∧Q1)")
    print("T0 = 1")
    
    # Проверка
    print("\nПроверка:")
    print("Состояние | T2 T1 T0 | Следующее")
    for i in range(8):
        q2 = (i >> 2) & 1
        q1 = (i >> 1) & 1
        q0 = i & 1
        
        # Вычисляем T по минимизированным функциям
        t2 = q2
        t1 = (q2 and not q1) or (not q2 and q1)  # XOR
        t0 = 1
        
        # Следующее состояние
        next_q2 = q2 ^ t2
        next_q1 = q1 ^ t1  
        next_q0 = q0 ^ t0
        
        next_state = next_q2*4 + next_q1*2 + next_q0
        print(f"   {i}     |  {t2}  {int(t1)}  {t0}  |    {next_state}")

if __name__ == '__main__':
    main()