import pandas as pd
from pprint import pprint
from datamining.util.AssociationRule import AssociationRule
from datamining.util.RuleHandSize import RuleHandSize
from itertools import combinations
import itertools

df = pd.read_csv('input.csv', sep=',')

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

    def confidence(self, tuparr) -> float:
        try:
            colValues = tuparr[1:]
            colValue = tuparr[0]

            return self.support(colValues) / self.support(colValue)
        except:
            return 0

    def support(self, tupArr) -> float:
        equal = 0
        for line in self.df.iterrows():
            localEqual = 0
            for element in tupArr:
                print(element)
                templine = int(line[1][element[0]])
                tempitem = int(element[1])


                if templine == tempitem:
                    localEqual += 1
            if localEqual == len(tupArr):
                equal += 1

        return equal / self.rows

    def permutate(self, arr, elements):
        return list(itertools.permutations(arr, elements))

    def combineItemsets(self, itemset1, itemset2):
        answer = []
        for item1 in itemset1:
            for item2 in itemset2:
                answer.append([item1, item2])
        return answer

    def apriori2(self):
        firstItemset = []
        firstItemset2 = []
        processBuffer = []


        for column, elem in self.tbDescriptor.items():
            for delimiter, value in elem['groups'].items():
                firstItemset.append((column, int(delimiter)))

        for element in firstItemset:
            support = self.support([element])

            print(support)

            if support > self.minsup:
                firstItemset2.append(element)
                processBuffer.append(element)
                self.results.append(
                    AssociationRule([RuleHandSize(element[0], element[1])], RuleHandSize(element[0], element[1]), support, 0)
                )

        for i in range(2, self.groups):
            print('i = {}'.format(i))
            combinations = self.combineItemsets(processBuffer, firstItemset2)
            combinations = self.removeWrongRules(combinations)
            print(combinations)

            permutated = []
            for item in combinations:
                print(item)
                permutated.append(self.permutate(item, i))

            for item in permutated:
                sup = self.support(item)
                conf = self.confidence(item)









        '''
            if combs == []:
                break

            with open('out.txt', 'a') as file:
                for element in combs:
                    file.write('{}\n'.format(element))


            for element in combs:

                aconf = self.confidence(element[:-1], [element[-1]])
                asup = self.support(element)
                #print('CONF: {:.2f}, SUP: {:.2f} - ELEM {}'.format(aconf, asup, element))

                if asup > self.minsup and aconf > self.minconf:
                    #print('element: {} - s: {}, c: {}'.format(element, asup, aconf))
                    buffers[writeBuffer].append(element)
                    rules = []

                    for temp in element[:-1]:
                        rules.append(RuleHandSize(temp[0], temp[1]))


                    self.results.append(
                        AssociationRule(rules, RuleHandSize(element[-1][0], element[-1][1]),
                                        asup, 0))





    '''








    def getAssociationRules(self):
        #self.executeApriori()
        self.apriori2()
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

    def toupleArrHasEqual(self, arr, pos):
        values = []
        for element in arr:
            if element[pos] in values:
                return True
            values.append(element[pos])
        return False


    def removeWrongRules(self, combs):
        answ = []
        for item in combs:
            if not self.toupleArrHasEqual(item, 0):
                answ.append(item)
        return answ







