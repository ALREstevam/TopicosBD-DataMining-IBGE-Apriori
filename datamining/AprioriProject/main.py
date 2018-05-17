from datamining.AprioriProject.Apriori import Apriori
from datamining.cleanformat.CleanData import DataCleaner
from pprint import pprint
import json

dc = DataCleaner('input.csv', sep=',', decimal='.')
info = dc.generateStructuredTableInfo()


with open('tableData.json', 'w') as jsonFile:
    json.dump(info, jsonFile)

df = dc.stripeTable()
df.to_csv('cleaned.csv', index=False)

print(df.head())
apr = Apriori(df, info, 0.2, 0.2, 7)


it1 = [('x', 1), ('y', 2), ('z', 3)]
it2 = [(('a', 1),('a', 2)), (('b', 2), ('b', 2)), (('c', 3), ('c', 4))]

#for item in apr.combineItemsets(it1, it2):
#    print(apr.removeWrongRules(item))

#c1 = apr.combine([1,2,3,4,5], 3, True)
#c2 = apr.permutate([1,2,3,4,5], 3)

#exit()

rules = apr.getAssociationRules()

i = 0
for rule in rules:
    print('#{} {}'.format(i, rule))
    i+=1