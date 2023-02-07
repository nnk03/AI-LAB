import pandas as pd
import numpy as np
import re
import random as rnd

# 1a
file = open('./speeches.txt','r')
text = file.read()
# reading the file
text = text.lower()
# converting all words to lowercase
words = text.split()
# converting text to a list containing words
words = [word.strip('$.,/!@#$%^&*()-=_+[]{} ') for word in words]
# removing all special characters given in the argument
words = [word.replace("'s",'') for word in words]
# deleting all apostrophes
words = [word.strip('\'\"') for word in words if word!='']
# removing all single quotes and double quotes
# uniqueWordArray = np.array(str,ndmin=1)

# print(uniqueWordArray)
uniqueWordList = []
for word in words:
  if word not in uniqueWordList:
    uniqueWordList.append(word)
# print(uniqueWordList)
# print(len(uniqueWordList))

freqList = [words.count(word) for word in uniqueWordList]
wordFreqObject = {
  'Words':uniqueWordList,
  'Frequency': freqList
}
wordFreqTable = pd.DataFrame(wordFreqObject)
# print(wordFreqTable)


# wordFreqSeries = pd.Series(wordFreqObject['Frequency'],index=wordFreqObject['Words'])
# print(wordFreqSeries.to_string())


# 1b


numUniqueWords = len(uniqueWordList)
# i = 4
# j = 5
# ithword = uniqueWordList[i-1]
# jthword = uniqueWordList[j-1]

# freq_jthword_after_ithword = uniqueWordList[i-1:].count(jthword)
# print(ithword,jthword,freq_jthword_after_ithword)


def freq_j_after_i(i,j):
  ithword = uniqueWordList[i]
  jthword = uniqueWordList[j]
  freq_jthword_after_ithword = uniqueWordList[i:].count(jthword)
  return freq_jthword_after_ithword

# print(freq_j_after_i(45,123))

nnmatrix = [[freq_j_after_i(i,j) for j in range(numUniqueWords)] for i in range(numUniqueWords)]
# print(nnmatrix)


def findrow():
  word = str(input('Enter a word '))
  try:
    index = uniqueWordList.index(word)
    return nnmatrix[index]

  except Exception as e:
    print(e)


freqList = findrow()
print(freqList)


# 1c
randomIndex = rnd.randint(0,numUniqueWords-1)
randomWord = uniqueWordList[randomIndex]











file.close()