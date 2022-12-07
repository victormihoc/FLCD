class PIF:
    def __init__(self):
        self.data = []

    def add(self, token, st_pos):
        if token not in self.data:
            self.data.append([token, st_pos])

    def get_data(self):
        return self.data

