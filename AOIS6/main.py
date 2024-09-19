class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        # Преобразуем первые две буквы в индекс
        index = 0
        if len(key) >= 2:
            index = (ord(key[0]) - ord('А')) * 32 + (ord(key[1]) - ord('А'))
        return index % self.size

    def insert(self, key, value):
        index = self._hash(key)
        original_index = index
        step = 1

        while self.table[index] is not None:
            if self.table[index][0] == key:
                # Обновляем значение, если ключ уже существует
                self.table[index] = (key, value)
                return
            # Квадратичное разрешение коллизий
            index = (original_index + step ** 2) % self.size
            step += 1

        self.table[index] = (key, value)

    def get(self, key):
        index = self._hash(key)
        original_index = index
        step = 1

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            # Квадратичное разрешение коллизий
            index = (original_index + step ** 2) % self.size
            step += 1

        return None

    def delete(self, key):
        index = self._hash(key)
        original_index = index
        step = 1

        while self.table[index] is not None:
            if self.table[index][0] == key:
                # Удаляем элемент, заменяя его специальной меткой
                self.table[index] = ("<deleted>", None)
                return True
            # Квадратичное разрешение коллизий
            index = (original_index + step ** 2) % self.size
            step += 1

        return False
