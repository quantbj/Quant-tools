from numpy import nan

field_index = { 'bondFuture': {'ignore_fx_index': 17, 'discount_curve_index': 4},           #
                'cap': {'ignore_fx_index': 17, 'discount_curve_index': 26},                 #
                'cash': {'ignore_fx_index': 5, 'discount_curve_index': nan},          #
                'cashFlow': {'ignore_fx_index': 4, 'discount_curve_index': 2},              # Note: List of cfs in column #2 
                'creditDefaultSwap': {'ignore_fx_index': 25, 'discount_curve_index': 9},    #
                'equity': {'ignore_fx_index': 11, 'discount_curve_index': nan},             #
                'floor': {'ignore_fx_index': 17, 'discount_curve_index': 26},               #
                'fxOption': {'ignore_fx_index': 15, 'discount_curve_index': nan},           #
                'genericBond': {'ignore_fx_index': 124, 'discount_curve_index': 124},       #
                'swaption': {'ignore_fx_index': 23, 'discount_curve_index': 54}             #
               }

