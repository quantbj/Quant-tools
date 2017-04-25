from Utils.value_object import ValueObject
from Utils.date_utils import ACT360

class IRIndex(ValueObject):
    def __init__(self, dcc):
        pass
    
EURIBOR6M = IRIndex(ACT360)
