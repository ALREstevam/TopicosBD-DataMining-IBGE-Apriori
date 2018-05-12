import copy
from pprint import pprint
row = []
rows = []



for i in range(100):
    row = []
    for j in range(20):
        row.append("{}".format(j+i))
    rows.append(row)

pprint(rows)