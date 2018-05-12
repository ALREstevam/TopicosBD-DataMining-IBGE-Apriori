import pandas as pd
import math
import numpy as np
from pprint import pprint
import json
from datamining.util.FileRenamer import FileRenamer as Fr

inputFileName = "in.csv"
jsonInfoFile = 'info.json'
outputFileName = "out.csv"

df = pd.read_csv(inputFileName, sep=';', decimal=",")

print('HEAD')
print(df.head())

print('TYPES')
print(df.dtypes)


def getNumberOfIntervals(df, columnName):
    if np.issubdtype(df[columnName].dtype, np.number):
        stdDeviation = df[columnName].std()
        max = df[columnName].max()
        min = df[columnName].min()

        result = math.floor((max-min) / stdDeviation)
        if result <= 1:
            result += 1

        return result
    else:
        return 0

def getIntervalLayout(df, columnName, lastMax):
    intervalAmount = getNumberOfIntervals(df, columnName)
    intervalList = {}

    if intervalAmount != 0:
        lastMax = int(lastMax)
        beginCount = lastMax + (10 - (lastMax % 10))

        max = df[columnName].max()
        min = df[columnName].min()
        stdDeviation = df[columnName].std()

        for i in range(intervalAmount):
            intervalList[beginCount + i] = {'max': min + (i+1) * stdDeviation}

        intervalList = {str(key): value for key, value in intervalList.items()}


        return intervalList
    return None


def generateStructuredTableInfo(df):
    answ = []
    lastMax = -1
    for columnName in df:
        column = df[columnName]
        if np.issubdtype(column.dtype, np.number):
            mean = float(column.mean())
            variance = float(column.var())
            stdDeviation = float(column.std())
            maxValue = float(column.max())
            minValue = float(column.min())

            interval = getIntervalLayout(df, column.name, lastMax)
            lastMax = max(list(interval.keys()))
            temp = {column.name: {"max": maxValue,"min": minValue,"mean": mean,"stddev": stdDeviation,"variance": variance,"groups": interval }}
            #pprint(temp)
            answ.append(temp)
    return answ


content = generateStructuredTableInfo(df)
with open('data.json', 'w', encoding='utf8') as outfile:
    json.dump(content, outfile)


cols = list(df.columns)

for column in cols:
    if not np.issubdtype(df[column].dtype, np.number):
        cols.remove(column)

for col in cols:
    #colInfo = content[col]

    col_zscore = col + '_zscore'
    df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0) #computes the z-score

    #for key, value in colInfo['groups'].values():
    #    pass



df.to_csv(Fr(inputFileName).appendNameAtEnd('_zscored'))