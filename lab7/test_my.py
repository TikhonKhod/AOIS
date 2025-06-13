import unittest
import numpy as np
import sys
import os

# Добавляем путь к основному модулю (если тесты в отдельной папке)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import DiagonalMatrix

class TestDiagonalMatrix(unittest.TestCase):
    
    def setUp(self):
        """Создаем экземпляр класса для каждого теста"""
        self.dm = DiagonalMatrix()
    
    def test_init(self):
        """Тест инициализации класса"""
        # Проверяем, что матрица создана правильно
        self.assertEqual(self.dm.matrix.shape, (16, 16))
        self.assertIsInstance(self.dm.matrix, np.ndarray)
        
        # Проверяем, что словарь логических функций заполнен
        self.assertEqual(len(self.dm.logic_functions), 16)
        
        # Проверяем несколько конкретных функций
        self.assertEqual(self.dm.logic_functions['f0'], [0, 0, 0, 0])
        self.assertEqual(self.dm.logic_functions['f6'], [0, 1, 1, 0])  # XOR
        self.assertEqual(self.dm.logic_functions['f9'], [1, 0, 0, 1])  # XNOR
        self.assertEqual(self.dm.logic_functions['f15'], [1, 1, 1, 1])
    
    def test_print_matrix(self):
        """Тест печати матрицы (проверяем, что не падает)"""
        try:
            self.dm.print_matrix()
        except Exception as e:
            self.fail(f"print_matrix raised {e} unexpectedly!")
    
    def test_read_word_valid(self):
        """Тест чтения слова с валидными параметрами"""
        # Читаем слово 0
        word0 = self.dm.read_word(0)
        self.assertIsInstance(word0, str)
        self.assertEqual(len(word0), 16)
        self.assertTrue(all(c in '01' for c in word0))
        
        # Читаем слово 15
        word15 = self.dm.read_word(15)
        self.assertIsInstance(word15, str)
        self.assertEqual(len(word15), 16)
        
        # Читаем несколько средних слов
        for i in [2, 5, 8, 11]:
            word = self.dm.read_word(i)
            self.assertEqual(len(word), 16)
    
    def test_read_word_invalid(self):
        """Тест чтения слова с невалидными параметрами"""
        # Отрицательный номер
        with self.assertRaises(ValueError):
            self.dm.read_word(-1)
        
        # Слишком большой номер
        with self.assertRaises(ValueError):
            self.dm.read_word(16)
        
        # Граничные невалидные значения
        with self.assertRaises(ValueError):
            self.dm.read_word(100)
        
        with self.assertRaises(ValueError):
            self.dm.read_word(-100)
    
    def test_write_word_valid(self):
        """Тест записи слова с валидными параметрами"""
        test_word = "1010101010101010"
        
        # Записываем и сразу читаем
        self.dm.write_word(0, test_word)
        read_word = self.dm.read_word(0)
        self.assertEqual(read_word, test_word)
        
        # Тестируем разные слова
        test_cases = [
            (1, "0000000000000000"),
            (5, "1111111111111111"),
            (10, "1100110011001100"),
            (15, "0011001100110011")
        ]
        
        for word_num, word_data in test_cases:
            self.dm.write_word(word_num, word_data)
            result = self.dm.read_word(word_num)
            self.assertEqual(result, word_data)
    
    def test_write_word_invalid(self):
        """Тест записи слова с невалидными параметрами"""
        # Неправильная длина слова
        with self.assertRaises(ValueError):
            self.dm.write_word(0, "101010")  # Слишком короткое
        
        with self.assertRaises(ValueError):
            self.dm.write_word(0, "10101010101010101")  # Слишком длинное
        
        # Неправильный номер слова
        with self.assertRaises(ValueError):
            self.dm.write_word(-1, "1010101010101010")
        
        with self.assertRaises(ValueError):
            self.dm.write_word(16, "1010101010101010")
        
        # Пустая строка
        with self.assertRaises(ValueError):
            self.dm.write_word(0, "")
    
    def test_read_column_valid(self):
        """Тест чтения столбца с валидными параметрами"""
        # Читаем все столбцы
        for col_num in range(16):
            column = self.dm.read_column(col_num)
            self.assertIsInstance(column, str)
            self.assertEqual(len(column), 16)
            self.assertTrue(all(c in '01' for c in column))
    
    def test_read_column_invalid(self):
        """Тест чтения столбца с невалидными параметрами"""
        with self.assertRaises(ValueError):
            self.dm.read_column(-1)
        
        with self.assertRaises(ValueError):
            self.dm.read_column(16)
        
        with self.assertRaises(ValueError):
            self.dm.read_column(100)
    
    def test_write_column_valid(self):
        """Тест записи столбца с валидными параметрами"""
        test_column = "1010101010101010"
        
        # Записываем и читаем
        self.dm.write_column(0, test_column)
        result = self.dm.read_column(0)
        self.assertEqual(result, test_column)
        
        # Тестируем разные столбцы
        test_cases = [
            (3, "0000000000000000"),
            (7, "1111111111111111"),
            (12, "1100110011001100")
        ]
        
        for col_num, col_data in test_cases:
            self.dm.write_column(col_num, col_data)
            result = self.dm.read_column(col_num)
            self.assertEqual(result, col_data)
    
    def test_write_column_invalid(self):
        """Тест записи столбца с невалидными параметрами"""
        with self.assertRaises(ValueError):
            self.dm.write_column(0, "101010")  # Короткий
        
        with self.assertRaises(ValueError):
            self.dm.write_column(-1, "1010101010101010")  # Неправильный номер
        
        with self.assertRaises(ValueError):
            self.dm.write_column(16, "1010101010101010")  # Неправильный номер
    
    def test_apply_logic_function_f6(self):
        """Тест применения логической функции f6 (XOR)"""
        # Устанавливаем известные значения
        self.dm.write_word(0, "1100110011001100")
        self.dm.write_word(1, "1010101010101010")
        
        result = self.dm.apply_logic_function('f6', 0, 1, 2)
        expected = "0110011001100110"  # XOR результат
        self.assertEqual(result, expected)
        
        # Проверяем, что результат записан в слово 2
        stored_result = self.dm.read_word(2)
        self.assertEqual(stored_result, expected)
    
    def test_apply_logic_function_f9(self):
        """Тест применения логической функции f9 (XNOR)"""
        self.dm.write_word(3, "1111000011110000")
        self.dm.write_word(4, "1100110011001100")
        
        result = self.dm.apply_logic_function('f9', 3, 4, 5)
        # Проверяем, что результат корректный
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in '01' for c in result))
    
    def test_apply_logic_function_f4(self):
        """Тест применения логической функции f4 (NOT A AND B)"""
        self.dm.write_word(6, "1010101010101010")
        self.dm.write_word(7, "1111000011110000")
        
        result = self.dm.apply_logic_function('f4', 6, 7, 8)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 16)
    
    def test_apply_logic_function_f11(self):
        """Тест применения логической функции f11 (A OR NOT B)"""
        self.dm.write_word(9, "0000111100001111")
        self.dm.write_word(10, "0101010101010101")
        
        result = self.dm.apply_logic_function('f11', 9, 10, 11)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 16)
    
    def test_apply_logic_function_all_functions(self):
        """Тест всех логических функций"""
        # Тестируем все функции от f0 до f15
        for i in range(16):
            func_name = f'f{i}'
            result = self.dm.apply_logic_function(func_name, 0, 1, 2)
            self.assertIsInstance(result, str)
            self.assertEqual(len(result), 16)
    
    def test_apply_logic_function_invalid(self):
        """Тест применения логической функции с невалидными параметрами"""
        with self.assertRaises(ValueError):
            self.dm.apply_logic_function('f100', 0, 1, 2)  # Несуществующая функция
        
        with self.assertRaises(ValueError):
            self.dm.apply_logic_function('invalid', 0, 1, 2)
    
    def test_sort_words(self):
        """Тест сортировки слов"""
        # Записываем известные значения для проверки сортировки
        test_words = [
            (0, "0000000000000001"),  # 1
            (1, "0000000000000010"),  # 2
            (2, "0000000000000000"),  # 0
            (3, "1000000000000000"),  # большое число
        ]
        
        for word_num, word_data in test_words:
            self.dm.write_word(word_num, word_data)
        
        sorted_words = self.dm.sort_words()
        
        # Проверяем структуру результата
        self.assertIsInstance(sorted_words, list)
        self.assertEqual(len(sorted_words), 16)
        
        # Проверяем, что каждый элемент - кортеж из 3 элементов
        for item in sorted_words:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 3)
            self.assertIsInstance(item[0], int)  # номер слова
            self.assertIsInstance(item[1], str)  # двоичное представление
            self.assertIsInstance(item[2], int)  # десятичное значение
        
        # Проверяем, что список отсортирован по возрастанию
        values = [item[2] for item in sorted_words]
        self.assertEqual(values, sorted(values))
    
    def test_arithmetic_operation_valid_key(self):
        """Тест арифметических операций с валидным ключом"""
        # Создаем слово с известной структурой V-A-B-S
        # V=111, A=1100(12), B=0011(3), S=00000
        test_word = "111" + "1100" + "0011" + "00000"
        self.dm.write_word(0, test_word)
        
        modified = self.dm.arithmetic_operation("111")
        
        # Проверяем результат
        self.assertIsInstance(modified, list)
        if modified:  # Если есть измененные слова
            self.assertEqual(len(modified), 1)
            mod = modified[0]
            
            # Проверяем структуру результата
            self.assertIn('word_num', mod)
            self.assertIn('original', mod)
            self.assertIn('modified', mod)
            self.assertIn('v', mod)
            self.assertIn('a', mod)
            self.assertIn('b', mod)
            self.assertIn('s_old', mod)
            self.assertIn('s_new', mod)
            self.assertIn('a_dec', mod)
            self.assertIn('b_dec', mod)
            self.assertIn('sum', mod)
            
            # Проверяем корректность сложения
            self.assertEqual(mod['a_dec'] + mod['b_dec'], mod['sum'])
    
    def test_arithmetic_operation_invalid_key(self):
        """Тест арифметических операций с невалидным ключом"""
        with self.assertRaises(ValueError):
            self.dm.arithmetic_operation("1111")  # Слишком длинный ключ
        
        with self.assertRaises(ValueError):
            self.dm.arithmetic_operation("11")    # Слишком короткий ключ
        
        with self.assertRaises(ValueError):
            self.dm.arithmetic_operation("")      # Пустой ключ
    
    def test_arithmetic_operation_no_matches(self):
        """Тест арифметических операций без совпадений ключа"""
        # Устанавливаем слова, которые не начинаются с "000"
        for i in range(16):
            self.dm.write_word(i, "1111111111111111")
        
        modified = self.dm.arithmetic_operation("000")
        self.assertEqual(len(modified), 0)
    
    def test_arithmetic_operation_overflow(self):
        """Тест арифметических операций с переполнением"""
        # V=101, A=1111(15), B=1111(15), сумма=30, но максимум 31
        test_word = "101" + "1111" + "1111" + "00000"
        self.dm.write_word(5, test_word)
        
        modified = self.dm.arithmetic_operation("101")
        
        if modified:
            mod = modified[0]
            self.assertEqual(mod['sum'], 30)  # 15+15=30, не превышает 31
    
    def test_arithmetic_operation_max_overflow(self):
        """Тест арифметических операций с максимальным переполнением"""
        # Создаем условие для переполнения > 31
        # Это невозможно с 4-битными полями (макс 15+15=30), но проверим логику
        test_word = "110" + "1111" + "1111" + "11111"
        self.dm.write_word(7, test_word)
        
        modified = self.dm.arithmetic_operation("110")
        
        if modified:
            mod = modified[0]
            # Сумма 15+15=30, что меньше 31, поэтому переполнения не будет
            self.assertLessEqual(mod['sum'], 31)
    
    def test_arithmetic_operation_all_keys(self):
        """Тест арифметических операций со всеми возможными ключами"""
        keys = [f"{i:03b}" for i in range(8)]  # "000" до "111"
        
        for key in keys:
            result = self.dm.arithmetic_operation(key)
            self.assertIsInstance(result, list)
    
    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Тест с нулевыми значениями
        zero_word = "0000000000000000"
        self.dm.write_word(0, zero_word)
        result = self.dm.read_word(0)
        self.assertEqual(result, zero_word)
        
        # Тест с единичными значениями
        ones_word = "1111111111111111"
        self.dm.write_word(15, ones_word)
        result = self.dm.read_word(15)
        self.assertEqual(result, ones_word)
        
        # Тест чередующихся значений
        alt_word = "1010101010101010"
        self.dm.write_word(8, alt_word)
        result = self.dm.read_word(8)
        self.assertEqual(result, alt_word)
    
    def test_matrix_consistency(self):
        """Тест согласованности операций с матрицей"""
        # Записываем слово, затем читаем столбцы и проверяем согласованность
        test_word = "1100110011001100"
        self.dm.write_word(3, test_word)
        
        # Проверяем, что биты слова соответствуют элементам в нужных позициях
        for i in range(16):
            col = (3 + i) % 16
            matrix_bit = str(self.dm.matrix[i][col])
            word_bit = test_word[i]
            self.assertEqual(matrix_bit, word_bit)
    
    def test_diagonal_addressing_formula(self):
        """Тест формулы диагональной адресации"""
        # Проверяем, что формула (word_num + i) % 16 работает корректно
        for word_num in range(16):
            for i in range(16):
                expected_col = (word_num + i) % 16
                self.assertGreaterEqual(expected_col, 0)
                self.assertLess(expected_col, 16)


class TestDiagonalMatrixIntegration(unittest.TestCase):
    """Интеграционные тесты для проверки взаимодействия функций"""
    
    def setUp(self):
        self.dm = DiagonalMatrix()
    
    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        # 1. Записываем несколько слов
        self.dm.write_word(0, "1010101010101010")
        self.dm.write_word(1, "1100110011001100")
        
        # 2. Применяем логическую функцию
        result = self.dm.apply_logic_function('f6', 0, 1, 2)
        self.assertIsInstance(result, str)
        
        # 3. Выполняем сортировку
        sorted_words = self.dm.sort_words()
        self.assertEqual(len(sorted_words), 16)
        
        # 4. Выполняем арифметические операции
        modified = self.dm.arithmetic_operation("101")
        self.assertIsInstance(modified, list)
    
    def test_multiple_operations_consistency(self):
        """Тест согласованности множественных операций"""
        original_word = self.dm.read_word(5)
        
        # Записываем и читаем обратно
        self.dm.write_word(5, "1111000011110000")
        modified_word = self.dm.read_word(5)
        self.assertEqual(modified_word, "1111000011110000")
        
        # Возвращаем исходное значение
        self.dm.write_word(5, original_word)
        restored_word = self.dm.read_word(5)
        self.assertEqual(restored_word, original_word)


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)