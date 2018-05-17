import pandas as pd
from pprint import pprint
from datamining.util.AssociationRule import AssociationRule
from datamining.util.RuleHandSize import RuleHandSize
from itertools import combinations
import itertools
from datamining.util.ProgressBar import ProgressBar

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
        colValues = tuparr[1:]
        colValue = tuparr[0]

        sup1 = self.support(colValues)
        sup2 = self.support([colValue])
        return sup1 / sup2



    def support(self, tupArr) -> float:
        equal = 0
        for line in self.df.iterrows():
            localEqual = 0
            for element in tupArr:
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

    def combineItemsets2(self, itemsetComposed, itemsetSimple):
        answer = []
        for element in itemsetComposed:
            for item in itemsetSimple:
                lstelem = list(element)
                lstelem.append(item)
                answer.append(lstelem)
        return answer

    def apriori(self):
        with open('rules.txt', 'w') as file:
            file.write('')

        firstItemset = []
        firstItemset2 = []
        processBuffer = []


        for column, elem in self.tbDescriptor.items():
            for delimiter, value in elem['groups'].items():
                firstItemset.append((column, int(delimiter)))

        for element in firstItemset:
            support = self.support([element])

            if support > self.minsup:
                firstItemset2.append(element)
                processBuffer.append(element)
                self.results.append(
                    AssociationRule([RuleHandSize(element[0], element[1])], RuleHandSize(element[0], element[1]), support, 0)
                )

        for i in range(2, self.groups):
            if i > 2:
                combinations = self.combineItemsets2(processBuffer, firstItemset2)
            else:
                combinations = self.combineItemsets(processBuffer, firstItemset2)
            combinations = self.removeWrongRules(combinations)
            if combinations == []:
                break

            processBuffer = []


            print('\n\nPROCESSING RULES WITH {} ELEMENTS.'.format(i))
            pb = ProgressBar(len(combinations))
            for element in combinations:

                pb += 1

                sup = self.support(element)
                conf = self.confidence(element)

                rules = []
                for temp in element[:-1]:
                    rules.append(RuleHandSize(temp[0], temp[1]))

                if sup > self.minsup and conf > self.minconf:
                    processBuffer.append(element)

                    self.results.append(
                        AssociationRule(rules, RuleHandSize(element[-1][0], element[-1][1]),sup, conf))


        print('\n\n\n\n')

    def getAssociationRules(self):
        print('{:^50s}'.format('EXECUTING APRIORI ALGORITHM'))
        self.apriori()

        print('WRITING RESULTS TO A FILE')
        pb = ProgressBar(len(self.results))

        with open('rules.txt', 'w') as file:
            for rule in self.results:
                file.write('{}\n'.format(rule))
                pb+=1


        print('\n\n\n')
        print('RULES FOUND: {}'.format(len(self.results)))
        print('DONE.')
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







