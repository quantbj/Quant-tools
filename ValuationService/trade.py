from Utils.value_object import ValueObject


class CompoundTrade(ValueObject):
    def __init__(self, constituent_list):
        pass

    def present_value(self, env):
        pv = 0.0
        for c in self.constituent_list:
            pv = pv + c.present_value(env)

        return pv


class FutureCashFlowTrade(CompoundTrade):
    pass


class IRCapTrade(CompoundTrade):
    pass
