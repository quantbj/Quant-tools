class Ccy:
    def __init__(self):
        raise NotImplementedError()
    def get_discount_curve(self):
        raise NotImplementedError()

    
class EUR(Ccy):
    pass