class AbstractTrade:
    def __init__(self, data_dict):
        self.data_dict = data_dict
        
    def present_value(self, env):
        raise NotImplementedError()
        
    def required_curves(self):
        raise NotImplementedError()

class FutureCashFlowTrade(AbstractTrade):
    def __init__(self, data_dict):
        super().__init__(data_dict)
        assert('cash_flows' in self.data_dict)
        
    def present_value(self, env):
        pv = 0.0
        for c in self.data_dict['cash_flows']:
            pv = pv + c.present_value(env)
        
        return pv
