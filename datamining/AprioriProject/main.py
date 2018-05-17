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

#print(df.head())
apr = Apriori(df, info, 0.1, 0.1, 6)

rules = apr.getAssociationRules()

i = 0
for rule in rules:
    print('#{} {}'.format(i, rule))
    i+=1