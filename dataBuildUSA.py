#!/usr/local/bin/python3.3

from string import *
import csv
import nltk.corpus

csv.field_size_limit(int(9999999))

empDic = {}
vocDic = {}
conDic = {}
fonDic = {}

#  In this emp data, the '1' signifies the dominant stress, which may be confusing
#  since '2' is numerically greater but emphasized quieter, and the '0' remains
#  lesser in both cases...

fCons = 'B', 'D', 'G', 'JH', 'L', 'N', 'P', 'S', 'T', 'V', 'ZH', 'CH', 'DH', 'F', 'HH', 'K', 'M', 'NG', 'R', 'SH', 'TH', 'W', 'Z'
fVocs = 'AA', 'AH', 'AW', 'EH', 'EY', 'IH', 'OW', 'UH', 'AE', 'AO', 'AY', 'ER', 'IY', 'OY', 'UW'

print('opening dictionary...')
entries = nltk.corpus.cmudict.entries()

thisWord = str()
doubList = []
print('analyzing text...')
for all in entries:
    if thisWord == all[0]:
        doubList.append(thisWord)
    thisWord = all[0]

##doubFile = open('data/USen/doubList.txt', 'w+', encoding='utf-8')
##for all in doubList:
    doubFile.write(all+'\n')

doubTaggers = []
for all in entries:
    if all[0] in doubList:
        doubInt = int(0)
        while all[0]+'('+str(doubInt)+')' in doubTaggers:
            doubInt+=1
        thisWord = all[0]+'('+str(doubInt)+')'
        doubTaggers.append(thisWord)
    else:
        thisWord = all[0]
    theseEmps = str()
    theseVocs = str()
    theseCons = str()
    theseFono = str()
    for each in all[1]:
        if len(each) > 2:
            theseFono+=(each[:2]+'^')
        else:
            theseFono+=(each+'^')
        if '0' in each:
            theseEmps+='0'
        elif '1' in each:
            theseEmps+='1'
        elif '2' in each:
            theseEmps+='2'
        if each[:2] in fVocs:
            theseVocs+=(each[:2]+'^')
        else:
            theseCons+=(each+'^')
    empDic[thisWord] = theseEmps
    vocDic[thisWord] = theseVocs[:-1]
    conDic[thisWord] = theseCons[:-1]
    fonDic[thisWord] = theseFono[:-1]
    
print(len(doubList))

print('writing files...')

########
## Three emp files, depending on the desired use of secondary stress data.

# The prime preserves the numerals used in this dictionary:
dicFile = csv.writer(open('data/USen/empDic-USen-MAST.csv', 'w+', encoding='utf-8'))
for key, val in empDic.items():
    dicFile.writerow([key, val])

# The 'even' iteration considers the two stresses as equal.
dicFile = csv.writer(open('data/USen/empDic-USen-even.csv', 'w+', encoding='utf-8'))
for key, val in empDic.items():
    newVal = val.replace('2', '1')
    dicFile.writerow([key, newVal])

# The 'unik' iteration eliminates all but the primary stress.
dicFile = csv.writer(open('data/USen/empDic-USen-unik.csv', 'w+', encoding='utf-8'))
for key, val in empDic.items():
    newVal = val.replace('2', '0')
    dicFile.writerow([key, newVal])


# These record the consonants and vowels, each discrete unit separated with carrot ('^')
dicFile = csv.writer(open('data/USen/vocDic-USen-MAS.csv', 'w+', encoding='utf-8'))
for key, val in vocDic.items():
    dicFile.writerow([key, val])

dicFile = csv.writer(open('data/USen/conDic-USen-MAS.csv', 'w+', encoding='utf-8'))
for key, val in conDic.items():
    dicFile.writerow([key, val])   

dicFile = csv.writer(open('data/USen/fonDic-USen-MAS.csv', 'w+', encoding='utf-8'))
for key, val in fonDic.items():
    dicFile.writerow([key, val])

def dicsToLists(dic, newDic):
    for key, val in dic.items():
        newDic[key] = val.split('^')


print('program complete')
