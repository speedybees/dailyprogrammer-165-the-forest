from collections import OrderedDict

class Statistics(object):
    def __init__(self):
        self.stats = {}

    def log(self, statistic, amount):
        if self.stats.has_key(statistic):
            self.stats[statistic] += amount
        else:
            self.stats[statistic] = amount

    def clear(self):
        self.stats.clear()

    def keys(self):
        return self.stats.keys()

    def __getitem__(self, statistic):
        if self.stats.has_key(statistic):
            return self.stats[statistic]
        else:
            return 0

class StatisticsBatch(object):
    def __init__(self):
        self.statistics = OrderedDict()

    def add_groups(self, *args):
        for group_name in args:
            self.statistics[group_name] = Statistics()

    def log_all(self, statistic, amount):
        for group_name in self.statistics:
            self.statistics[group_name].log(statistic, amount)

    def keys(self):
        return self.statistics.keys()

    def __getitem__(self, group_name):
        return self.statistics[group_name]
