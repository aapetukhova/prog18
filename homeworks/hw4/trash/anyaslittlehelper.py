##import csv
##import json
##
##
##def jsn():
##    with open('results.csv', 'r', encoding='utf-8') as csvfile:
##        filereader = csv.reader(csvfile, delimiter=';')
##        rows = list(filereader)
##    with open('file.json', 'x', encoding='utf-8') as f:
##        json.dump(rows, f)
##            
####            for row in filereader:
####                json.dump(row, jsonfile)
####                json.write('\n')
##
##jsn()




import csv
import os
import collections
import matplotlib
import matplotlib.pyplot as plt
# import seaborn 
from matplotlib import style
def plot(k, variable, title, xlabel, ylabel, iname):
    style.use('ggplot')
    s = []
    n = 0
    X = []
    Y = []
    with open('results.csv', 'r', encoding='utf-8') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';')
        for row in filereader:
            n += 1
            if row[k] != variable:
                s.append(row[k])
        counter = collections.Counter(s)
        for key, value in counter.items():
            X.append(key)
            Y.append(value)
    plt.scatter(X,Y)
    plt.title(title)
    plt.xlim(-0.5, len(X)-0.5)
    plt.ylim(0, n-1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(iname + '.png')

names = [['']]
for item in names:
    plot




    
