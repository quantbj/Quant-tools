class RM3DReader:
    ids = [
        'cash',
        'cap',
        'floor',
        'bondFuture',
        'genericBond',
        'cashFlow',
        'creditDefaultSwap',
        'equity',
        'fxOption',
        'swaption']

    def __init__(self):
        pass

    def process(self, input_str):
        elem_raw = [l.split('\t') for l in input_str.split('\n')]
        elem_subset = [e for e in elem_raw if e[0] in self.ids]

        return(elem_subset)
