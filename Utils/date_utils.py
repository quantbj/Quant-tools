from Utils.value_object import ValueObject


class DatePeriod(ValueObject):
    def __init__(self, d1, d2):
        pass

    def get_duration(self):
        return (self.d2 - self.d1).days

class DayCountConvention():
    def dcf(self, date_period):
        raise(NotImplementedError)
        
class Act360(DayCountConvention):
    def dcf(self, date_period):
        return date_period.get_duration()/360.0
        
ACT360 = Act360()