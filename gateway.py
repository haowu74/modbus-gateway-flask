from unit import Unit

class Gateway:
    def __init__(self, file):
        self.file = file

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit_id):
        self.unit = list(filter(lambda x: x.unit != unit_id, self.units))

    def load_from_file(self, file):
        pass

    def save_to_file(self, file):
        pass

    def clear(self):
        self.units.clear()

    def writeRegister(self, address, register, value):
        pass

    def trigger(self, unit, lock=True):
        pass

