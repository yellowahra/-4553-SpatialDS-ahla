"""
@author - Ahla Cho
@date -  mm/dd/yyyy
@description - This program does ..... and write more than one line .....

@resources - I found code and methods at https://docs.python.org/2/library/csv.html,
                https://docs.python.org/2/tutorial/inputoutput.html.....
"""
import csv
import json

nodes =[]   #two list
edges =[]
geometry={} #dictionary

with open('nodes.csv', 'rb') as csvfile:
    rows= csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in rows:
        nodes.append(row)

with open('edges.csv', 'rb') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in rows:
         edges.append(row)

f= open('nodegeometry.json', 'r')

for line in f:
    #geometry.append(json.loads(line))
    #all id
    line=json.loads(line)
    print line['id']
    geometry[line['id']]= line['geometry']

#print nodes
print len(geometry[str(250691)])
print 'Your Name'
print len(nodes)
print len(edges)

#print geometry
