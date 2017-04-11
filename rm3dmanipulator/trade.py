from numpy import nan, isnan    
from constants import field_index

class GenericTrade:
    def __init__(self, trade_data):
        self.trade_data = list(trade_data)
        self.trade_type = self.trade_data[0]
        self.ignore_fx_index = field_index[self.trade_type]['ignore_fx_index']
        self.discount_curve_index = field_index[self.trade_type]['discount_curve_index']

    def set_ignore_fx(self, flag):
        self.trade_data[self.ignore_fx_index] = flag
    
    def set_discount_curve(self, curve):
        if not isnan(self.discount_curve_index):
            if self.trade_type == 'cashFlow':
                cf_list = self.trade_data[self.discount_curve_index].split('|')
                cf_list[3::4] = [curve] * int(len(cf_list)/4)
                self.trade_data[self.discount_curve_index] = '|'.join(cf_list)
            else:
                self.trade_data[self.discount_curve_index] = curve
    
    def get_serialized(self):
        return self.trade_data
