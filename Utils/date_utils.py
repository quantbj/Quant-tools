from Utils.value_object import ValueObject


class DatePeriod():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_duration(self):
        return (self.end - self.start).days


class DayCountConvention():
    def dcf(self, date_period):
        raise(NotImplementedError)


class Act360(DayCountConvention):
    def dcf(self, date_period):
        return date_period.get_duration() / 360.0


ACT360 = Act360()
