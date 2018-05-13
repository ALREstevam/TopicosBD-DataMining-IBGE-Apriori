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

apr = Apriori(df, info, 0.2, 0.2, 5)

rules = apr.getAssociationRules()

a = apr.confidenceAsToupleArray([('a', 1), ('b', 12), ('c', 22)])

combs = apr.combine([('a',1), ('a',2), ('b',10), ('b',11), ('c', 20)], 3, True)

print(apr.removeWrongRules(combs))


print(a)

for rule in rules:
    print(rule)