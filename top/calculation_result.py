class CalculationResult:
    def __init__(self, calculation_name, name_value_1=None, value_1=None, name_value_2=None, value_2=None,
                 name_value_dict=None):
        self.calculation_name = calculation_name
        self.name_value_1 = name_value_1
        self.name_value_2 = name_value_2
        self.value_1 = value_1
        self.value_2 = value_2
        self.name_value_dict: dict = name_value_dict
