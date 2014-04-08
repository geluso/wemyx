## This is my first commit.

## This will begin the GitHub version of this project.


#!/usr/local/bin/python3.3

from string import *
import csv
csv.field_size_limit(int(9999999))

x = 1

altsList = []
altsFile = open('data/USen/doubList.txt')
for line in altsFile:
    if line != 0:
        altsList.append(line[:-1])
#print(altsList)

def dicWordLookup(pWord, totalVs, rSyls):
    if (rSyls <= totalVs):
        tName = str(totalVs)
        rName = str(rSyls)
        if totalVs < 10:
            tName = '0'+tName
        if rSyls < 10:
            rName = '0'+rName
        try:
            print('t'+tName, 'r'+rName)
            dicFile = csv.reader(open('data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))
            for line in dicFile:
                ##print('line:', line)
                keyChain = line[0].split('^')
                if pWord in keyChain:
                    matchBox = line[1].split('^')
                    if pWord in matchBox:
                        matchBox.remove(pWord)
                    return matchBox
        except IOError:
            print('FILE NOT FOUND')

while x != 0:
    pWord = str(input('Word to rhyme: '))
    totalVs = int(input('How many syllables in result? ("0" returns all results): '))
    rSyls = int(input('How many syllables must match in results ("0" returns the same length as word): '))
    matchBox = []
    if pWord in altsList:
        doubInt = int(0)
        while pWord in altsList:
            try:
                doubWord = pWord+'('+str(doubInt)+')'
                print(pWord, (doubInt+1))
                if totalVs == 0:
                    while totalVs < 10:
                        totalVs+=1
                        matchBox = dicWordLookup(doubWord, totalVs, rSyls)
                        print(matchBox)
                    totalVs = 0
                else:
                    matchBox = dicWordLookup(doubWord, totalVs, rSyls)
                    print(matchBox)
                    doubWord = doubWord[:-3]
                    doubInt+=1
                    if (len(matchBox) == 0) and (doubInt > 1):
                        break
                if (len(matchBox) == 0) and (doubInt > 1):
                    break
            except TypeError:
                if (doubInt > 1):
                    break
                else:
                    doubWord = doubWord[:-3] 
                    doubInt+=1
                    continue
        
    else:
        print(pWord)
        if totalVs == 0:
            while totalVs < 10:
                totalVs+=1
                matchBox = dicWordLookup(pWord, totalVs, rSyls)
                print(matchBox)
        else:
            matchBox = dicWordLookup(pWord, totalVs, rSyls)
            print(matchBox)
