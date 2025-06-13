class BiologyHashTable:
    def __init__(self, table_size=20, start_addr=100):
        self.table_size = table_size
        self.start_addr = start_addr
        self.entries = [None] * table_size
        self.load_factor = 0.0
        self.collision_count = 0
        
        self.english_chars = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
            'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
            'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
        }
    
    class TableEntry:
        """Структура записи хеш-таблицы с флажками"""
        def __init__(self, key_id="", data=""):
            self.key_id = key_id          # ID - ключевое слово
            self.collision_flag = False   # C - флажок коллизий
            self.occupied_flag = False    # U - флажок "занято"
            self.terminal_flag = True     # T - терминальный флажок
            self.link_flag = False        # L - флажок связи
            self.deleted_flag = False     # D - флажок удаления
            self.overflow_ptr = -1        # P0 - указатель переполнения
            self.data_info = data         # Pi - данные или указатель
    
    def compute_numeric_value(self, term):
        """Вычисляет числовое значение V для биологического термина"""
        if len(term) < 2:
            raise ValueError("Термин должен содержать минимум 2 символа")
        
        first_letter = term[0].upper()
        second_letter = term[1].upper()
        
        if first_letter not in self.english_chars or second_letter not in self.english_chars:
            raise ValueError("Термин должен начинаться с английских букв")
        
        # Используем основание 26 для английского алфавита
        numeric_val = self.english_chars[first_letter] * 26 + self.english_chars[second_letter]
        return numeric_val
    
    def generate_hash_address(self, term):
        """Генерирует хеш-адрес для биологического термина"""
        v_value = self.compute_numeric_value(term)
        hash_addr = (v_value % self.table_size) + self.start_addr
        return hash_addr, v_value
    
    def add_entry(self, biology_term, description):
        """Добавляет новую запись в хеш-таблицу"""
        hash_addr, v_val = self.generate_hash_address(biology_term)
        index = hash_addr - self.start_addr
        
        # Квадратичный пробинг для поиска свободного места
        probe_step = 0
        original_idx = index
        collision_occurred = False
        
        while True:
            current_idx = (original_idx + probe_step * probe_step) % self.table_size
            
            if self.entries[current_idx] is None:
                # Создаем новую запись
                new_entry = self.TableEntry(biology_term, description)
                new_entry.occupied_flag = True
                new_entry.collision_flag = collision_occurred
                self.entries[current_idx] = new_entry
                self._update_load_factor()
                return True
                
            elif self.entries[current_idx].deleted_flag:
                # Используем удаленную ячейку
                self.entries[current_idx].key_id = biology_term
                self.entries[current_idx].data_info = description
                self.entries[current_idx].deleted_flag = False
                self.entries[current_idx].occupied_flag = True
                self.entries[current_idx].collision_flag = collision_occurred
                return True
                
            elif self.entries[current_idx].key_id == biology_term:
                # Обновляем существующую запись
                self.entries[current_idx].data_info = description
                return True
            
            collision_occurred = True
            self.collision_count += 1
            probe_step += 1
            
            if probe_step >= self.table_size:
                raise Exception("Хеш-таблица переполнена - невозможно добавить запись")
    
    def find_entry(self, biology_term):
        """Поиск записи по биологическому термину"""
        hash_addr, v_val = self.generate_hash_address(biology_term)
        index = hash_addr - self.start_addr
        
        probe_step = 0
        original_idx = index
        
        while True:
            current_idx = (original_idx + probe_step * probe_step) % self.table_size
            
            if self.entries[current_idx] is None:
                return None
                
            entry = self.entries[current_idx]
            if not entry.deleted_flag and entry.key_id == biology_term:
                return entry.data_info
                
            probe_step += 1
            if probe_step >= self.table_size:
                return None
    
    def remove_entry(self, biology_term):
        """Удаляет запись из хеш-таблицы"""
        hash_addr, v_val = self.generate_hash_address(biology_term)
        index = hash_addr - self.start_addr
        
        probe_step = 0
        original_idx = index
        
        while True:
            current_idx = (original_idx + probe_step * probe_step) % self.table_size
            
            if self.entries[current_idx] is None:
                return False
                
            entry = self.entries[current_idx]
            if not entry.deleted_flag and entry.key_id == biology_term:
                entry.deleted_flag = True
                entry.occupied_flag = False
                self._update_load_factor()
                return True
                
            probe_step += 1
            if probe_step >= self.table_size:
                return False
    
    def _update_load_factor(self):
        """Обновляет коэффициент заполнения таблицы"""
        occupied_count = sum(1 for entry in self.entries 
                           if entry is not None and entry.occupied_flag and not entry.deleted_flag)
        self.load_factor = occupied_count / self.table_size
    
    def show_table_contents(self):
        """Отображает полное содержимое хеш-таблицы"""
        print("=" * 80)
        print("БИОЛОГИЧЕСКАЯ ХЕШ-ТАБЛИЦА")
        print("=" * 80)
        print(f"Размер таблицы: {self.table_size}")
        print(f"Базовый адрес: {self.start_addr}")
        print(f"Коэффициент заполнения: {self.load_factor:.2f}")
        print(f"Количество коллизий: {self.collision_count}")
        print("-" * 80)
        
        print(f"{'Индекс':<6} {'Адрес':<6} {'Термин':<15} {'C':<2} {'U':<2} {'T':<2} {'L':<2} {'D':<2} {'Описание':<25}")
        print("-" * 80)
        
        for i in range(self.table_size):
            addr = self.start_addr + i
            
            if self.entries[i] is None:
                print(f"{i:<6} {addr:<6} {'':15} {'':<2} {'':<2} {'':<2} {'':<2} {'':<2} {'':25}")
            else:
                entry = self.entries[i]
                c_flag = '1' if entry.collision_flag else '0'
                u_flag = '1' if entry.occupied_flag else '0'
                t_flag = '1' if entry.terminal_flag else '0'
                l_flag = '1' if entry.link_flag else '0'
                d_flag = '1' if entry.deleted_flag else '0'
                
                term_display = entry.key_id if not entry.deleted_flag else "УДАЛЕНО"
                desc_display = entry.data_info if not entry.deleted_flag else ""
                
                print(f"{i:<6} {addr:<6} {term_display:<15} {c_flag:<2} {u_flag:<2} {t_flag:<2} {l_flag:<2} {d_flag:<2} {desc_display:<25}")
    
    def show_hash_calculations(self, biology_term):
        """Показывает расчеты хеш-функции для термина"""
        try:
            v_value = self.compute_numeric_value(biology_term)
            hash_addr, _ = self.generate_hash_address(biology_term)
            
            print(f"\nРасчеты для термина '{biology_term}':")
            print(f"Первая буква '{biology_term[0]}' = {self.english_chars[biology_term[0].upper()]}")
            print(f"Вторая буква '{biology_term[1]}' = {self.english_chars[biology_term[1].upper()]}")
            print(f"V = {self.english_chars[biology_term[0].upper()]} * 26 + {self.english_chars[biology_term[1].upper()]} = {v_value}")
            print(f"Хеш-адрес = ({v_value} % {self.table_size}) + {self.start_addr} = {hash_addr}")
            
        except Exception as e:
            print(f"Ошибка при вычислении: {e}")


if __name__ == "__main__":
    bio_table = BiologyHashTable()
    bio_table.add_entry("DNA", "Дезоксирибонуклеиновая кислота")
    bio_table.show_table_contents()