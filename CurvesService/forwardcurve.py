# class ForwardCurve():
#     def __init__(self, ccy, name):
#         self.ccy = ccy
#         self.name = name


class IRForwardCurve():
    def __init__(self, ccy, name):
        self.ccy = ccy
        self.name = name

    def __eq__(self, other):
        return ((self.ccy == other.ccy) and (self.name == other.name))


class FxForwardCurve():
    def __init__(self, ccy_domestic, ccy_foreign):
        self.ccy_domestic = ccy_domestic
        self.ccy_foreign = ccy_foreign

    def __eq__(self, other):
        return ((self.ccy_domestic == other.ccy_domestic)
                and (self.ccy_foreign == other.ccy_foreign))
