import pandas as pd
from pprint import pprint

df = pd.read_csv('input.csv', sep=',')
#print(df.head())

class Apriori():
    def __init__(self, dataframe, jsonDescriptionPath, minsup, minconf, maxgroups):
        self.df = dataframe
        self.minsup = minsup
        self.minconf = minconf
        self.groups = maxgroups
        self.rows = self.df.shape[0]
        self.columns = self.df.shape[1]
        self.results = []

    def support(self, cols, values) -> float:
        equals = 0
        items = []
        for line in self.df.iterrows():
            items = []
            for col in cols:
                items.append(line[1][col])
            if items == values:
                equals += 1
        return equals / self.rows

    def confidence(self,columns, values, columnValueTouple) -> float:
        return self.support(columns, values) / self.support([columnValueTouple[0]], [columnValueTouple[1]])

    def allsame(self, items):
        return all(x == items[0] for x in items)






a = Apriori(df, 0, 0, 0)
print(a.support(['a', 'b', 'c'], [6, 14, 104]))
print(a.confidence(['a','b'], [6, 14], ('c', 104)))











