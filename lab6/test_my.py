import unittest
from main import BiologyHashTable  # Предполагается, что класс находится в файле biology_hash_table.py

class TestBiologyHashTable(unittest.TestCase):
    def setUp(self):
        # Используем небольшую таблицу для удобства тестирования
        self.table = BiologyHashTable(table_size=5, start_addr=100)

    def test_compute_numeric_value_valid(self):
        self.assertEqual(self.table.compute_numeric_value("AB"), 1)
        self.assertEqual(self.table.compute_numeric_value("BA"), 26)
        self.assertEqual(self.table.compute_numeric_value("ZZ"), 25 * 26 + 25)

    def test_compute_numeric_value_lowercase(self):
        self.assertEqual(self.table.compute_numeric_value("ab"), 1)

    def test_compute_numeric_value_invalid_length(self):
        with self.assertRaises(ValueError):
            self.table.compute_numeric_value("A")

    def test_compute_numeric_value_non_english(self):
        with self.assertRaises(ValueError):
            self.table.compute_numeric_value("АБ")  # Некорректные символы

    def test_generate_hash_address(self):
        hash_addr, v_val = self.table.generate_hash_address("AB")
        expected_v = 1
        expected_addr = (expected_v % self.table.table_size) + self.table.start_addr
        self.assertEqual(hash_addr, expected_addr)
        self.assertEqual(v_val, expected_v)

    def test_add_entry_no_collision(self):
        result = self.table.add_entry("DNA", "Дезоксирибонуклеиновая кислота")
        self.assertTrue(result)
        entry = self.table.find_entry("DNA")
        self.assertEqual(entry, "Дезоксирибонуклеиновая кислота")
        self.assertEqual(self.table.collision_count, 0)

    def test_add_entry_collision(self):
        small_table = BiologyHashTable(table_size=2, start_addr=100)
        # "AB" -> V = 1, index = 1 % 2 = 1
        small_table.add_entry("AB", "First")
        # "BA" -> V = 26, index = 0 % 2 = 0 -> пробинг до первого свободного
        small_table.add_entry("BA", "Second")
        self.assertEqual(small_table.entries[1].data_info, "First")
        self.assertEqual(small_table.entries[0].data_info, "Second")
        self.assertEqual(small_table.collision_count, 1)

    def test_add_entry_update_existing(self):
        self.table.add_entry("DNA", "Старое описание")
        result = self.table.add_entry("DNA", "Новое описание")
        self.assertTrue(result)
        entry = self.table.find_entry("DNA")
        self.assertEqual(entry, "Новое описание")

    def test_add_entry_use_deleted(self):
        self.table.add_entry("RNA", "Рибонуклеиновая кислота")
        self.table.remove_entry("RNA")
        result = self.table.add_entry("RNA", "Обновленная РНК")
        self.assertTrue(result)
        entry = self.table.find_entry("RNA")
        self.assertEqual(entry, "Обновленная РНК")
        self.assertFalse(self.table.entries[self.table.find_entry("RNA").__dict__['key_id'] == "RNA"].deleted_flag)

    def test_add_entry_overflow(self):
        for i in range(self.table.table_size):
            self.table.add_entry(f"T{i}", f"Desc {i}")
        with self.assertRaises(Exception):
            self.table.add_entry("Overflow", "Too many entries")

    def test_find_entry_exists(self):
        self.table.add_entry("DNA", "ДНК")
        result = self.table.find_entry("DNA")
        self.assertEqual(result, "ДНК")

    def test_find_entry_not_exists(self):
        result = self.table.find_entry("RNA")
        self.assertIsNone(result)

    def test_find_entry_after_deletion(self):
        self.table.add_entry("DNA", "ДНК")
        self.table.remove_entry("DNA")
        result = self.table.find_entry("DNA")
        self.assertIsNone(result)

    def test_remove_entry_success(self):
        self.table.add_entry("DNA", "ДНК")
        result = self.table.remove_entry("DNA")
        self.assertTrue(result)
        entry = self.table.find_entry("DNA")
        self.assertIsNone(entry)
        idx = (self.table.generate_hash_address("DNA")[0] - self.table.start_addr)
        entry = self.table.entries[idx]
        self.assertTrue(entry.deleted_flag)
        self.assertFalse(entry.occupied_flag)

    def test_remove_entry_not_exists(self):
        result = self.table.remove_entry("RNA")
        self.assertFalse(result)

    def test_update_load_factor(self):
        self.assertEqual(self.table.load_factor, 0)
        self.table.add_entry("DNA", "ДНК")
        self.assertEqual(self.table.load_factor, 1 / self.table.table_size)
        self.table.remove_entry("DNA")
        self.assertEqual(self.table.load_factor, 0)

    def test_table_entry_initialization(self):
        entry = self.table.TableEntry("TERM", "Data")
        self.assertEqual(entry.key_id, "TERM")
        self.assertTrue(entry.occupied_flag)
        self.assertFalse(entry.collision_flag)
        self.assertTrue(entry.terminal_flag)
        self.assertFalse(entry.link_flag)
        self.assertFalse(entry.deleted_flag)
        self.assertEqual(entry.data_info, "Data")

    def test_show_table_contents(self):
        try:
            self.table.show_table_contents()
        except Exception as e:
            self.fail(f"show_table_contents() raised {e} unexpectedly!")

    def test_show_hash_calculations(self):
        try:
            self.table.show_hash_calculations("DNA")
        except Exception as e:
            self.fail(f"show_hash_calculations() raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()