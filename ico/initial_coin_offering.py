class ICO:
    def __init__(self, name, close_date, dataYesNo, raised_money):
        self.name = name
        self.close_date = close_date
        self.funds = dataYesNo
        self.raised_money = raised_money

    def __lt__(self, other):
        if self.close_date is None:
            return False
        else:
            if other.close_date is None:
                return True
            else:
                return self.close_date > other.close_date

    def __str__(self):
        return str([self.name, self.close_date, self.funds, self.raised_money])

    def hasData(self):
        return self.funds

    # Funktion und parameter so benennen, dass auch Aussenstehende verstehen, um was es geht
    # money immer als Liste machen
    def addData(self, new_data):
        if isinstance(self.raised_money, list):
            self.raised_money.append(new_data)
        else:
            self.raised_money = [self.raised_money, new_data]
            self.funds = True
