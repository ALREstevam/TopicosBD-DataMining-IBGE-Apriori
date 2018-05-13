import pandas as pd
import math
import numpy as np
from pprint import pprint
import json
from datamining.util.FileRenamer import FileRenamer as Fr
import operator

class DataCleaner:
    def __init__(self, inputFileName = "in.csv",jsonInfoFile = 'info.json', outputFileName = "out.csv", sep = ';', decimal = ','):
        self.inputFileName = inputFileName
        self.jsonInfoFile = jsonInfoFile
        self.outputFileName = outputFileName
        self.df = pd.read_csv(inputFileName, sep=sep, decimal=decimal)


    def getNumberOfIntervals(self, columnName):
        if np.issubdtype(self.df[columnName].dtype, np.number):
            stdDeviation = self.df[columnName].std()
            max = self.df[columnName].max()
            min = self.df[columnName].min()

            result = math.floor((max-min) / stdDeviation)
            if result <= 1:
                result += 1

            return result
        else:
            return 0

    def getIntervalLayout(self, columnName, lastMax):
        intervalAmount = self.getNumberOfIntervals(columnName)
        intervalList = {}

        if intervalAmount != 0:
            lastMax = int(lastMax)
            beginCount = lastMax + (10 - (lastMax % 10))

            maxv = self.df[columnName].max()
            minv = self.df[columnName].min()
            stdDeviation = self.df[columnName].std()

            for i in range(intervalAmount):
                intervalList[beginCount + i] = minv + (i+1) * stdDeviation

            intervalList = {str(key): value for key, value in intervalList.items()}
            return intervalList
        return None


    def generateStructuredTableInfo(self):
        answ = {}
        lastMax = -1
        for columnName in self.df:
            column = self.df[columnName]
            if np.issubdtype(column.dtype, np.number):
                mean = float(column.mean())
                variance = float(column.var())
                stdDeviation = float(column.std())
                maxValue = float(column.max())
                minValue = float(column.min())

                interval = self.getIntervalLayout(column.name, lastMax)
                lastMax = max(list(interval.keys()))
                temp = {"max": maxValue,"min": minValue,"mean": mean,"stddev": stdDeviation,"variance": variance,"groups": interval }
                #pprint(temp)
                answ[column.name] = temp
        return answ


    def tableInfoToJson(self):
        content = self.generateStructuredTableInfo()
        with open('data.json', 'w', encoding='utf8') as outfile:
            json.dump(content, outfile)

    def addZscoreNDumps(self):
        cols = list(self.df.columns)

        for column in cols:
            if not np.issubdtype(self.df[column].dtype, np.number):
                cols.remove(column)

        for col in cols:
            #colInfo = content[col]

            col_zscore = col + '_zscore'
            self.df[col_zscore] = (self.df[col] - self.df[col].mean())/self.df[col].std(ddof=0) #computes the z-score

            #for key, value in colInfo['groups'].values():
            #    pass

            self.df.to_csv(Fr(self.inputFileName).appendNameAtEnd('_zscored'))


    def stripeTable(self):
        content = self.generateStructuredTableInfo()
        newData = {}
        for row in self.df:
            group = content[row]['groups']

            newColumn = []
            for data in self.df[row]:
                sortedGroup = sorted(group.items(), key=operator.itemgetter(1))
                lastCount = 0
                for name, minvalue in sortedGroup:
                    if data < minvalue:
                        newColumn.append(name)
                        break

                    if lastCount == len(sortedGroup)-1:
                        newColumn.append(sortedGroup[-1][0])
                        break

                    lastCount += 1

            newData[row] = newColumn
            #print(newRow)
            #print(len(newRow))

        df2 = pd.DataFrame(newData)
        #print(df2)
        return df2









