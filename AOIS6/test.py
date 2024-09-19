import unittest
from main import *


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.hash_table = HashTable(size=10)  # Измените размер для тестирования коллизий

    def test_insert_and_get(self):
        self.hash_table.insert("АБ", 100)
        self.assertEqual(self.hash_table.get("АБ"), 100)

    def test_update_value(self):
        self.hash_table.insert("АБ", 100)
        self.hash_table.insert("АБ", 200)
        self.assertEqual(self.hash_table.get("АБ"), 200)

    def test_collision_resolution(self):
        # Эти ключи должны вызвать коллизию
        self.hash_table.insert("АА", 1)
        self.hash_table.insert("БА", 2)
        self.assertEqual(self.hash_table.get("АА"), 1)
        self.assertEqual(self.hash_table.get("БА"), 2)

    def test_delete(self):
        self.hash_table.insert("АБ", 100)
        self.assertTrue(self.hash_table.delete("АБ"))
        self.assertIsNone(self.hash_table.get("АБ"))

    def test_delete_nonexistent(self):
        self.assertFalse(self.hash_table.delete("ВВ"))

    def test_insert_after_delete(self):
        self.hash_table.insert("АБ", 100)
        self.hash_table.delete("АБ")
        self.hash_table.insert("АБ", 200)
        self.assertEqual(self.hash_table.get("АБ"), 200)


if __name__ == "__main__":
    unittest.main()