import pandas as pd
from pprint import pprint
from datamining.util.AssociationRule import AssociationRule
from datamining.util.RuleHandSize import RuleHandSize
from itertools import combinations

df = pd.read_csv('input.csv', sep=',')
#print(df.head())

class Apriori():
    def __init__(self, dataframe, descriptor, minsup, minconf, maxgroups):
        self.df = dataframe
        self.minsup = minsup
        self.minconf = minconf
        self.groups = maxgroups
        self.rows = self.df.shape[0]
        self.columns = self.df.shape[1]
        self.tbDescriptor = descriptor
        self.results = []

    def supportAsTouples(self, colValues):
        columns = []
        values = []
        for column, value in colValues:
            columns.append(column)
            values.append(value)
        return self.support(columns, values)

    def confidenceAsTouples(self, colValues, colValue):
        columns = []
        values = []

        for column, value in colValues:
            columns.append(column)
            values.append(value)
        return self.confidence(columns, values, colValue)

    def confidenceAsToupleArray(self, toupleArray):
        if len(toupleArray) < 3:
            return None
        endTp = toupleArray[-1]
        toupleArray = toupleArray[:-1]
        return self.confidenceAsTouples(toupleArray, endTp)


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
        support0 = self.support(columns, values)
        support1 = self.support([columnValueTouple[0]], [columnValueTouple[1]]) == 0
        if support1 == 0:
            return 0.0

        return support0/support1
        #return self.support(columns, values) / self.support([columnValueTouple[0]], [columnValueTouple[1]])

    def allsame(self, items):
        return all(x == items[0] for x in items)

    def executeApriori(self):
        firstSubset = {}

        for column in self.df:
            firstSubset[column] = []

        for column, elem in self.tbDescriptor.items():
            for strp, value in elem['groups'].items():
                support = self.support([column], [strp])
                if support > self.minsup:
                    firstSubset[column].append(strp)
                    self.results.append(AssociationRule([RuleHandSize(column, strp)], RuleHandSize(column, strp), support, 0))

        print(firstSubset)



        for groups in range(2, self.groups + 1):
            pass

    def getAssociationRules(self):
        self.executeApriori()
        return self.results

    def combine(self, arrayToComb, maxCombs, maxOnly = False):
        groups = [c for i in range(maxCombs + 1) for c in combinations(arrayToComb, i)]
        answ = []

        if len(groups) > 1:
            groups = groups[1:]

        if maxOnly == True:
            for element in groups:
                if len(element) == maxCombs:
                    answ.append(element)
            return answ
        else:
            return groups

    def someEqual(self, arr):
        for value1 in arr:
            for value2 in arr:
                if value1 == value2:
                    return False
        return True

    def someEqualToupleArr(self, arr, pos):
        for value1 in arr:
            for value2 in arr:
                print('{} == {}'.format(value1[pos], value2[pos]))
                if value1[pos] == value2[pos]:
                    return True
        return False


    def removeWrongRules(self, combs):
        answ = []
        for item in combs:
            if not self.someEqualToupleArr(item, 0):
                print(item)
                answ.append(item)
        return answ






#a = Apriori(df, 0, 0, 0)
#print(a.support(['a', 'b', 'c'], [6, 14, 104]))
#print(a.confidence(['a','b'], [6, 14], ('c', 104)))


