import csv,re
from collections import namedtuple

import re
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headers = [ re.sub('[^a-zA-Z_]', '_', h) for h in next(f_csv) ]
    print(headers)
    print(headers)
    Row = namedtuple('Row', headers)
    for r in f_csv:
        row = Row(*r)
        print(row)


