from Utils.value_object import ValueObject


class DatePeriod(ValueObject):
    def __init__(self, d1, d2):
        pass

    def get_duration(self):
        return (self.d2 - self.d1).days
