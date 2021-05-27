import nltk
import pickle
import numpy as np
import os
import glob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import BracketParseCorpusReader
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import WhitespaceTokenizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words("english"))
stop_words = stop_words.union(",","(",")","[","]","{","}","#","@","!",":",";",".","?" , "-" , ":" , "%")

Index={}

#h e l l o   m y   n a  m   e      i  s     v  e  n  u       g  o  p  a  l
#0 1 2 3 4 5 6 7 8 9 10 11 12  13 14 15  16 17 18 19 20  21  22 23 24 25 26
Lemmatizer = WordNetLemmatizer()

path = os.getcwd()
os.chdir(path)

print(os.getcwd())
for file in glob.glob("ECTText/*.txt"):
  offset=0
  doc = open(file).read()
  docID = file[len("/ECTText/"):-len(".txt")]
  print(docID)
  tokens = word_tokenize(doc)
  for w in tokens:
      x = Lemmatizer.lemmatize(w)
      pos = doc[offset:].find(w) + offset
      offset = offset + len(w)
      while doc[offset]== ' ':
        offset = offset + 1

      if x not in stop_words and not x.isdigit():
        if x not in Index.keys():
          Index.update({x : []})
        Index[x].append( (docID , pos) )

picklefile = open('ECTInvertedIndex.pkl', 'wb')
pickle.dump(Index, picklefile)
picklefile.close()

