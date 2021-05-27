"""Wildcard Expansion"""

import re
import os
import pickle
import sys



def processresult(word , wlist):
  result = word + ": "
  for tup in wlist:
    result = result + "<" + tup[0] + "," + str(tup[1]) + ">,"
  result = result + ";"
  return result


path = os.getcwd()
os.chdir(path)


with open('ECTInvertedIndex.pkl', 'rb') as f:
    Index = pickle.load(f)

results = open("RESULTS1_20CS60R45.txt" , "w")

qfile = sys.argv[1]

Queries = open(qfile).readlines()
Queries = [query[:-1] for query in Queries]

for query in Queries:
  p = query.find('*') 
  if p>=0 :
    regex = "^" + query[:p] + "." + query[p:] + "$"
    for word in Index.keys():
      match = re.search(regex , word)
      if match:
        res = processresult(word , Index[word])
        results.write(res)
  
  else :
    for word in Index.keys():
      if word == query:
        res = processresult(word , Index[word])
        results.write(res)

results.close()