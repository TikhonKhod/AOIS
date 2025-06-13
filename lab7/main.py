import numpy as np

class DiagonalMatrix:
    def __init__(self):
        self.matrix = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        
        # Таблица логических функций
        self.logic_functions = {
            'f0': [0, 0, 0, 0],   # 0
            'f1': [0, 0, 0, 1],   # AND
            'f2': [0, 0, 1, 0],   # A AND NOT B
            'f3': [0, 0, 1, 1],   # A
            'f4': [0, 1, 0, 0],   # NOT A AND B
            'f5': [0, 1, 0, 1],   # B
            'f6': [0, 1, 1, 0],   # XOR
            'f7': [0, 1, 1, 1],   # OR
            'f8': [1, 0, 0, 0],   # NOR
            'f9': [1, 0, 0, 1],   # XNOR (эквивалентность)
            'f10': [1, 0, 1, 0],  # NOT B
            'f11': [1, 0, 1, 1],  # A OR NOT B
            'f12': [1, 1, 0, 0],  # NOT A
            'f13': [1, 1, 0, 1],  # NOT A OR B
            'f14': [1, 1, 1, 0],  # NAND
            'f15': [1, 1, 1, 1]   # 1
        }
    
    def print_matrix(self):
        """Печать текущего состояния матрицы"""
        print("Текущая матрица:")
        for i, row in enumerate(self.matrix):
            print(f"Ряд {i:2d}: {' '.join(map(str, row))}")
        print()
    
    def read_word(self, word_num):
        """
        Считывание слова по номеру (диагональная адресация)
        Слово j располагается в столбцах с позициями (j+i) % 16 для строк i
        """
        if word_num < 0 or word_num >= 16:
            raise ValueError("Номер слова должен быть от 0 до 15")
        
        word = ""
        for i in range(16):
            col = (word_num + i) % 16
            word += str(self.matrix[i][col])
        
        return word
    
    def write_word(self, word_num, word_data):
        """Запись слова по номеру"""
        if word_num < 0 or word_num >= 16:
            raise ValueError("Номер слова должен быть от 0 до 15")
        if len(word_data) != 16:
            raise ValueError("Длина слова должна быть 16 бит")
        
        for i in range(16):
            col = (word_num + i) % 16
            self.matrix[i][col] = int(word_data[i])
    
    def read_column(self, col_num):
        """Считывание адресного столбца"""
        if col_num < 0 or col_num >= 16:
            raise ValueError("Номер столбца должен быть от 0 до 15")
        
        column = ""
        for i in range(16):
            column += str(self.matrix[i][col_num])
        
        return column
    
    def write_column(self, col_num, col_data):
        """Запись адресного столбца"""
        if col_num < 0 or col_num >= 16:
            raise ValueError("Номер столбца должен быть от 0 до 15")
        if len(col_data) != 16:
            raise ValueError("Длина столбца должна быть 16 бит")
        
        for i in range(16):
            self.matrix[i][col_num] = int(col_data[i])
    
    def apply_logic_function(self, func_name, word1_num, word2_num, result_word_num):
        """
        Применение логической функции к двум словам
        Результат записывается в указанное слово
        """
        if func_name not in self.logic_functions:
            raise ValueError(f"Неизвестная функция: {func_name}")
        
        word1 = self.read_word(word1_num)
        word2 = self.read_word(word2_num)
        func = self.logic_functions[func_name]
        
        result = ""
        for i in range(16):
            bit1 = int(word1[i])
            bit2 = int(word2[i])
            index = bit1 * 2 + bit2
            result += str(func[index])
        
        self.write_word(result_word_num, result)
        return result
    
    def sort_words(self):
        """
        Упорядоченная выборка (сортировка слов)
        Сортируем слова по их двоичному значению
        """
        words_with_indices = []
        
        # Собираем все слова с их индексами
        for i in range(16):
            word = self.read_word(i)
            decimal_value = int(word, 2)  # Преобразуем в десятичное число
            words_with_indices.append((i, word, decimal_value))
        
        # Сортируем по значению
        words_with_indices.sort(key=lambda x: x[2])
        
        return words_with_indices
    
    def arithmetic_operation(self, v_key):
        """
        Сложение полей Aj и Bj в словах Sj, у которых Vj совпадает с заданным V
        Структура слова: V(3 бита) + A(4 бита) + B(4 бита) + S(5 бит)
        """
        if len(v_key) != 3:
            raise ValueError("Ключ V должен быть 3 бита")
        
        modified_words = []
        
        for word_num in range(16):
            word = self.read_word(word_num)
            
            # Разбираем слово на поля
            v_field = word[:3]
            a_field = word[3:7]
            b_field = word[7:11]
            s_field = word[11:16]
            
            # Проверяем совпадение ключа
            if v_field == v_key:
                # Складываем A и B
                a_value = int(a_field, 2)
                b_value = int(b_field, 2)
                sum_value = a_value + b_value
                
                # Ограничиваем результат 5 битами (максимум 31)
                if sum_value > 31:
                    sum_value = 31
                
                # Преобразуем обратно в двоичную строку
                new_s_field = format(sum_value, '05b')
                
                # Формируем новое слово
                new_word = v_field + a_field + b_field + new_s_field
                
                # Записываем обратно
                self.write_word(word_num, new_word)
                
                modified_words.append({
                    'word_num': word_num,
                    'original': word,
                    'modified': new_word,
                    'v': v_field,
                    'a': a_field,
                    'b': b_field,
                    's_old': s_field,
                    's_new': new_s_field,
                    'a_dec': a_value,
                    'b_dec': b_value,
                    'sum': sum_value
                })
        
        return modified_words

def main(): #pragma: no coverage
    dm = DiagonalMatrix()
    
    print("=== ЛАБОРАТОРНАЯ РАБОТА 7 - ВАРИАНТ 3 ===\n")
    
    # 1. Запись/считывание разрядных столбцов и слов по индексу
    print("1. ЗАПИСЬ/СЧИТЫВАНИЕ СЛОВ И СТОЛБЦОВ")
    print("-" * 50)
    
    # Считываем слово #2
    word2 = dm.read_word(2)
    print(f"Слово #2: {word2}")
    
    # Считываем адресный столбец #3
    col3 = dm.read_column(3)
    print(f"Столбец #3: {col3}")
    
    print()
    
    # 2. Логические функции f6 и f9, f4 и f11
    print("2. ЛОГИЧЕСКИЕ ФУНКЦИИ")
    print("-" * 50)
    
    # f6 (XOR) для слов 2 и 3, результат в слово 14
    print("Применяем f6 (XOR) к словам 2 и 3, результат в слово 14:")
    word2 = dm.read_word(2)
    word3 = dm.read_word(3)
    print(f"Слово 2: {word2}")
    print(f"Слово 3: {word3}")
    
    result_f6 = dm.apply_logic_function('f6', 2, 3, 14)
    print(f"f6 результат: {result_f6}")
    
    # f9 (XNOR) для слов 4 и 5, результат в слово 13
    print("\nПрименяем f9 (XNOR) к словам 4 и 5, результат в слово 13:")
    word4 = dm.read_word(4)
    word5 = dm.read_word(5)
    print(f"Слово 4: {word4}")
    print(f"Слово 5: {word5}")
    
    result_f9 = dm.apply_logic_function('f9', 4, 5, 13)
    print(f"f9 результат: {result_f9}")
    
    # f4 (NOT A AND B) для слов 6 и 7, результат в слово 12
    print("\nПрименяем f4 (NOT A AND B) к словам 6 и 7, результат в слово 12:")
    word6 = dm.read_word(6)
    word7 = dm.read_word(7)
    print(f"Слово 6: {word6}")
    print(f"Слово 7: {word7}")
    
    result_f4 = dm.apply_logic_function('f4', 6, 7, 12)
    print(f"f4 результат: {result_f4}")
    
    # f11 (A OR NOT B) для слов 8 и 9, результат в слово 11
    print("\nПрименяем f11 (A OR NOT B) к словам 8 и 9, результат в слово 11:")
    word8 = dm.read_word(8)
    word9 = dm.read_word(9)
    print(f"Слово 8: {word8}")
    print(f"Слово 9: {word9}")
    
    result_f11 = dm.apply_logic_function('f11', 8, 9, 11)
    print(f"f11 результат: {result_f11}")
    
    print()
    
    # 3. Упорядоченная выборка (сортировка)
    print("3. УПОРЯДОЧЕННАЯ ВЫБОРКА (СОРТИРОВКА)")
    print("-" * 50)
    
    sorted_words = dm.sort_words()
    print("Слова отсортированные по возрастанию их двоичного значения:")
    for i, (word_num, word, value) in enumerate(sorted_words):
        print(f"{i+1:2d}. Слово #{word_num}: {word} (десятичное: {value})")
    
    print()
    
    # 4. Арифметические операции
    print("4. АРИФМЕТИЧЕСКИЕ ОПЕРАЦИИ")
    print("-" * 50)
    
    # Ищем слова с ключом V = "111"
    print("Поиск слов с ключом V = '111' и сложение полей A и B:")
    modified = dm.arithmetic_operation("111")
    
    if modified:
        for mod in modified:
            print(f"Слово #{mod['word_num']}:")
            print(f"  Исходное: {mod['original']}")
            print(f"  Изменено: {mod['modified']}")
            print(f"  V={mod['v']}, A={mod['a']}({mod['a_dec']}), B={mod['b']}({mod['b_dec']})")
            print(f"  S: {mod['s_old']} -> {mod['s_new']} (сумма A+B = {mod['sum']})")
            print()
    else:
        print("Слов с указанным ключом не найдено")
    
    # Также проверим другие ключи
    for key in ["000", "001", "010", "011", "100", "101", "110"]:
        modified = dm.arithmetic_operation(key)
        if modified:
            print(f"Найдены слова с ключом V = '{key}': {len(modified)} шт.")
    
    print()
    print("5. ИТОГОВОЕ СОСТОЯНИЕ МАТРИЦЫ")
    print("-" * 50)
    dm.print_matrix()

if __name__ == "__main__":
    main()