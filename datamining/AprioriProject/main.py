from datamining.AprioriProject.Apriori import Apriori
from datamining.cleanformat.CleanData import DataCleaner
from pprint import pprint
import json
import os
import csv
from datamining.util.MyTiming import MyTiming

csvFilePaht = "Base de Dados.csv"
t = MyTiming()


t.start_counting()
dc = DataCleaner(csvFilePaht, sep=',', decimal='.')
info = dc.generateStructuredTableInfo()


with open('tableData.json', 'w') as jsonFile:
    json.dump(info, jsonFile)

df = dc.stripeTable()
df.to_csv('cleaned.csv', index=False)

print(df.head())

t.stop_counting()

print('Cleaning duration: {}'.format(t.countElapsed()))
t.resetTimer()

t.start_counting()


minsup = 0.5
minconf = 0.5

if input('Execute Apriori on cleaned data? with minsup={} and minconf={} (y/n)'.format(minsup, minconf)) == 'n':
    exit(0)

apr = Apriori(df, info, minsup=minsup, minconf=minconf, maxgroups=5)

rules = apr.getAssociationRulesWithMax(20)
print(apr.getInfoText())

i = 0
for rule in rules:
    print('#{} {}'.format(i, rule))
    i+=1


t.stop_counting()
print('Apriori duration: {}'.format(t.countElapsed()))