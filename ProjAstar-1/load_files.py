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


print len(geometry[str(265957)])

#print len(nodes)
#print len(edges)

#print geometry
