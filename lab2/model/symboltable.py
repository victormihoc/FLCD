class SymbolTable:
    def __init__(self, capacity=58):
        self.capacity = capacity
        self.table = [[] for _ in range(self.capacity)]
        self.keys = []

    def hash(self, key):
        ascii_sum = 0
        for char in key:
            ascii_sum += ord(char)
        return ascii_sum % self.capacity

    def get(self, key):
        idx = self.hash(key)
        for _ in range(self.capacity):
            if len(self.table[idx]) != 0:
                return self.table[idx]

    def put(self, key, value):
        idx = self.hash(key)
        if key not in self.keys:
            self.table[idx].append(value)
            self.keys.append(key)
            return idx
        return -1

    def search(self, key):
        idx = self.hash(key)
        return key in self.table[idx]

    def get_table(self):
        return self.table

    def __getitem__(self, item):
        return self.get(item)

    def get_keys(self):
        return self.keys
