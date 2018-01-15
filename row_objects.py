
from datetime import date as datetime_date


class RevenueRow(object):

    def __init__(self, name, date, visits, revenue):
        assert type(name) == str
        assert type(date) == datetime_date
        assert type(visits) == int
        assert type(revenue) in (float, int)
        self.name = name
        self.date = date
        self.visits = visits
        self.revenue = revenue

    def __str__(self):
        return ','.join(
            '{}:{}'.format(key, value) for key, value in self.__dict__.items()
        )

    def __repr__(self):
        return self.__str__()


class CostRow(object):

    def __init__(self, name, date, raws, cost):
        assert type(name) == str
        assert type(date) == datetime_date
        assert type(raws) == int
        assert type(cost) in (float, int)
        self.name = name
        self.date = date
        self.raws = raws
        self.cost = cost

    def __str__(self):
        return ','.join(
            '{}:{}'.format(key, value) for key, value in self.__dict__.items()
        )

    def __repr__(self):
        return self.__str__()