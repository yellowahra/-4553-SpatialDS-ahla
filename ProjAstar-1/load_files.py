"""
@author - Ahla Cho
@date -  11/18/2015
@program5 -part1
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
    #print line['id']
    geometry[line['id']]= line['geometry']
geo = json.loads(geometry[str(250691)]) #get point from the given line
#print nodes
print "Ahla Cho"
print "Program 5- part 1"
print "Read 'nodes.csv' " + str(len(nodes))
print "Read 'edges.csv' " + str(len(edges))
print "Nodes 250691 contains " + str(len(geo))+ " points."
print "Geometry follows: "
print geometry[str(250691)]

#print geometry
