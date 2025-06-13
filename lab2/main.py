import re
from itertools import product

class LogicFunctionAnalyzer:
    def __init__(self):
        self.variables = []
        self.truth_table = []
        
    def parse_function(self, func_str):
        """Парсинг логической функции и извлечение переменных"""
        # Замена символов на стандартные операторы Python
        func_str = func_str.replace('∨', '|').replace('∧', '&').replace('¬', '~')
        func_str = func_str.replace('->', '=>').replace('~', ' not ')
        func_str = func_str.replace('=>', ' <= ')  # импликация a->b эквивалентна ~a|b
        
        # Извлечение переменных
        variables = re.findall(r'[a-e]', func_str)
        self.variables = sorted(list(set(variables)))
        
        return func_str
    
    def evaluate_function(self, func_str, values_dict):
        """Вычисление значения функции для заданных значений переменных"""
        # Замена переменных на их значения
        for var, val in values_dict.items():
            func_str = func_str.replace(var, str(val))
        
        # Обработка импликации a <= b эквивалентна not a or b
        func_str = re.sub(r'(\d+)\s*<=\s*(\d+)', r'(not \1 or \2)', func_str)
        
        try:
            return eval(func_str)
        except:
            return False
    
    def build_truth_table(self, original_func):
        """Построение таблицы истинности"""
        func_str = self.parse_function(original_func)
        n = len(self.variables)
        
        print(f"\nТаблица истинности для функции: {original_func}")
        print("=" * 50)
        
        # Заголовок таблицы
        header = " | ".join(self.variables) + " | F"
        print(header)
        print("-" * len(header))
        
        self.truth_table = []
        
        # Генерация всех возможных комбинаций значений
        for combination in product([0, 1], repeat=n):
            values_dict = dict(zip(self.variables, combination))
            result = self.evaluate_function(func_str, values_dict)
            
            # Добавление в таблицу истинности
            row = list(combination) + [int(result)]
            self.truth_table.append(row)
            
            # Вывод строки таблицы
            row_str = " | ".join(map(str, combination)) + f" | {int(result)}"
            print(row_str)
    
    def get_minterms(self):
        """Получение минтермов (строки где F=1)"""
        minterms = []
        for i, row in enumerate(self.truth_table):
            if row[-1] == 1:  # Если функция равна 1
                minterms.append(i)
        return minterms
    
    def get_maxterms(self):
        """Получение макстермов (строки где F=0)"""
        maxterms = []
        for i, row in enumerate(self.truth_table):
            if row[-1] == 0:  # Если функция равна 0
                maxterms.append(i)
        return maxterms
    
    def build_sdnf(self):
        """Построение СДНФ"""
        minterms = self.get_minterms()
        if not minterms:
            return "0", []
        
        sdnf_terms = []
        
        for minterm_idx in minterms:
            term_parts = []
            for i, var in enumerate(self.variables):
                bit_value = (minterm_idx >> (len(self.variables) - 1 - i)) & 1
                if bit_value == 1:
                    term_parts.append(var)
                else:
                    term_parts.append(f"¬{var}")
            sdnf_terms.append(f"({' ∧ '.join(term_parts)})")
        
        sdnf = " ∨ ".join(sdnf_terms)
        return sdnf, minterms
    
    def build_sknf(self):
        """Построение СКНФ"""
        maxterms = self.get_maxterms()
        if not maxterms:
            return "1", []
        
        sknf_terms = []
        
        for maxterm_idx in maxterms:
            term_parts = []
            for i, var in enumerate(self.variables):
                bit_value = (maxterm_idx >> (len(self.variables) - 1 - i)) & 1
                if bit_value == 0:  # Для СКНФ инвертируем
                    term_parts.append(var)
                else:
                    term_parts.append(f"¬{var}")
            sknf_terms.append(f"({' ∨ '.join(term_parts)})")
        
        sknf = " ∧ ".join(sknf_terms)
        return sknf, maxterms
    
    def get_index_form(self):
        """Получение индексной формы функции"""
        binary_str = ""
        for row in self.truth_table:
            binary_str += str(row[-1])
        
        decimal_value = int(binary_str, 2)
        return decimal_value, binary_str
    
    def analyze_function(self, func_str):
        """Полный анализ логической функции"""
        print("АНАЛИЗ ЛОГИЧЕСКОЙ ФУНКЦИИ")
        print("=" * 50)
        
        # Построение таблицы истинности
        self.build_truth_table(func_str)
        
        # Построение СДНФ
        sdnf, minterms = self.build_sdnf()
        print(f"\nСовершенная дизъюнктивная нормальная форма (СДНФ):")
        print(sdnf)
        
        # Построение СКНФ
        sknf, maxterms = self.build_sknf()
        print(f"\nСовершенная конъюнктивная нормальная форма (СКНФ):")
        print(sknf)
        
        # Числовые формы
        print(f"\nЧисловые формы:")
        print(f"СДНФ: {tuple(minterms)} ∨")
        print(f"СКНФ: {tuple(maxterms)} ∧")
        
        # Индексная форма
        index_value, binary_form = self.get_index_form()
        print(f"\nИндексная форма:")
        print(f"{index_value} - {binary_form}")

def main(): # pragma: no cover
    analyzer = LogicFunctionAnalyzer()
    
    print("Программа для построения СДНФ и СКНФ")
    print("Поддерживаемые операции: & (И), | (ИЛИ), ! или ¬ (НЕ), -> (импликация)")
    print("Переменные: a, b, c, d, e")
    print("Пример: (a|b)&!c")
    print("-" * 50)
    
    while True:
        try:
            func_input = input("\nВведите логическую функцию (или 'quit' для выхода): ")
            
            if func_input.lower() == 'quit':
                break
                
            if not func_input.strip():
                continue
                
            analyzer.analyze_function(func_input)
            
        except Exception as e:
            print(f"Ошибка: {e}")
            print("Проверьте правильность введенной функции")

if __name__ == "__main__":
    # Пример использования
    analyzer = LogicFunctionAnalyzer()
    
    # Тестирование с примером из задания
    print("ПРИМЕР")
    analyzer.analyze_function("(a->b)&c")
    
    print("\n" + "="*70)
    
    # Интерактивный режим
    main()