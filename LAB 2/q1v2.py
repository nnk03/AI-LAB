# 

import pandas as pd
import numpy as np
import re
import random as rnd

# file = open('./speeches.txt','r')
# file = open('./text.txt','r')
# file = open('./text2.txt','r')
file = open('./text3.txt','r')

# 1a
text = file.read()
# reading the file
text = text.lower()
# converting all words to lowercase
words = text.split()
# converting text to a list containing words
words = [word.strip('$.,/!@#$%^&*()-=_+[]{}1234567890 ') for word in words]
# removing all special characters given in the argument
words = [word.replace("'s",'') for word in words]
# deleting all apostrophes
words = [word.strip('\'\"') for word in words if word!='' and word!='re']
# removing all single quotes and double quotes
words = [word for word in words if word.isalpha()]

uniqueWordList = []
# initializing uniqueWordList as empty list
for word in words:
  if word not in uniqueWordList:
    uniqueWordList.append(word)
    # we append only if the word is not in uniqueWordList

freqList = [
  words.count(word) for word in uniqueWordList
]
# table = {
#   'words':uniqueWordList,
#   'freq': freqList
# }
# print(pd.DataFrame(table))
# frequency list of each word

# print(words)
# print(uniqueWordList)
# print(freqList)








# 1b

numUniqueWords = len(uniqueWordList)

nnmatrix = []
# initializing matrix to empty list

for i in range(numUniqueWords):
  rowToBeAppended = []
  # initialising an empty row
  for j in range(numUniqueWords):
    ith_word = uniqueWordList[i]
    jth_word = uniqueWordList[j]
    count = 0
    # starting count from 0
    for x in range(len(words)):
      if x<len(words)-1 and words[x] == ith_word and words[x+1] == jth_word:
        count += 1
        # finding frequency of occurrence of jth_word after ith_word
    rowToBeAppended.append(count)
  nnmatrix.append(rowToBeAppended)

# print(nnmatrix)
# print('[')
# for row in nnmatrix:
#   print(row)
# print(']')

def findFreqList():
  word = str(input())
  if word not in uniqueWordList:
    print('word not found')
  else:
    index = uniqueWordList.index(word)
    return nnmatrix[index]
for row in nnmatrix:
  print(row)
print()

row = findFreqList()
print(row)


# 1c

textLength = 0
word = rnd.choices(uniqueWordList,k=1)[0]
print(word,end=' ')
textLength+=1


# it has to be 5000
while textLength < 20:
  index = uniqueWordList.index(word)
  freq_dist_row = nnmatrix[index]
  word = rnd.choices(uniqueWordList,weights=freq_dist_row,k=1)[0]
  print(word,end=' ')
  textLength+=1
print()


file.close()