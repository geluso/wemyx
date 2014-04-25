#!/usr/local/bin/python3.3

from string import *
import csv
import nltk.corpus

csv.field_size_limit(int(9999999))

emps = {}
vocs = {}
cons = {}
fono = {}

empDic = {}
vocDic = {}
conDic = {}
fonDic = {}

rhyDic = {}

#  In this emp data, the '1' signifies the dominant stress, which may be confusing
#  since '2' is numerically greater but emphasized quieter, and the '0' remains
#  lesser in both cases...

fCons = 'B', 'D', 'G', 'JH', 'L', 'N', 'P', 'S', 'T', 'V', 'ZH', 'CH', 'DH', 'F', 'HH', 'K', 'M', 'NG', 'R', 'SH', 'TH', 'W', 'Z'
fVocs = 'AA', 'AH', 'AW', 'EH', 'EY', 'IH', 'OW', 'UH', 'AE', 'AO', 'AY', 'ER', 'IY', 'OY', 'UW'

print('input ranges:')
tVMin = int(input('totalVs min:'))
tVMax = int(input('totalVs max:'))
rSMin = int(input('rSyls min:'))
rSMax = int(input('rSyls max:'))

print('opening dictionary...')

entries = nltk.corpus.cmudict.entries()
superLexi = []

altsList = []
altsFile = open('data/USen/doubList.txt')
for line in altsFile:
    if line != 0:
        altsList.append(line[:-1])

print('len(altList):', len(altsList), '\nanalyzing text...')

for all in entries:
    thisWord = all[0]
    altNum = int(0)
    if thisWord in altsList:
        altWord = thisWord+'('+str(altNum)+')'
        while altWord in superLexi:
            altWord = thisWord+'('+str(altNum)+')'
            altNum+=1
        thisWord = altWord
        #print('thisWord:', thisWord)
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
            theseEmps+='0'
        if each[:2] in fVocs:
            theseVocs+=(each[:2]+'^')
        else:
            theseCons+=(each+'^')
    empDic[thisWord] = theseEmps
    vocDic[thisWord] = theseVocs[:-1]
    fonDic[thisWord] = theseFono[:-1]
    superLexi.append(thisWord)

    
print('preparing dics...')

def dicsToLists(dic, newDic):
    for key, val in dic.items():
        newDic[key] = val.split('^')

for key, val in empDic.items():
    emps[key] = val
dicsToLists(vocDic, vocs)
dicsToLists(fonDic, fono)

superPopList = []
print('starting rhyBuild...')

def rhymeBuilder(totalVs, rSyls):
    print('finding t'+str(totalVs)+'r'+str(rSyls))
    rhyDic = {}
    strikeList = []
    counter = int(0)
    for all in superLexi:
        superPopList.append(all) 
    while len(superPopList) > 0:
        pWord = superPopList.pop()
        keyEmps = emps[pWord]
        counter+=1
        if counter%1000 == 0:
            print('superPopList remaining:', len(superPopList))
            #print('@', counter, '('+pWord+')', '\nstrikeList sample:', strikeList[:20])
        if len(keyEmps) >= rSyls:
            matchList = str()
            keyList = str()
            keyEmps = emps[pWord]
            theseVocs = vocs[pWord]
            thisVocI = len(theseVocs)
            theseFono = fono[pWord]
            thisFonI = len(theseFono)
            phonLen = (len(theseFono) - 1)
            vocSpot = int(0)
            vCt = int(0) 
            while vCt <= rSyls:
                if theseFono[phonLen] in fVocs:
                    vCt+=1
                    ###print('.')
                if vCt < rSyls:
                    phonLen-=1
                    ###print(',')
            ###print('BREAK', phonLen)
            vocSpot = phonLen
            rhymeSlice = theseFono[vocSpot:]
            ###print('pWord:', pWord, '\nrhymeSlice:', rhymeSlice)
            for each in superPopList:
                theseEmps = emps[each]
                empLen = len(theseEmps)            
                if empLen >= rSyls:
                    testFono = fono[each]
                    rhyNum = len(rhymeSlice)
                    if len(testFono) >= rhyNum:
                        if (testFono[-rhyNum:] == rhymeSlice) and (keyEmps[-rSyls:] == theseEmps[-rSyls:]):
                            ###print('hit @', empLen, totalVs, '\nemps of '+each, emps[each], len(emps[each]))
                            ###print(pWord, each, rhymeSlice, testFono[-rhyNum:])
                            strikeList.append(each)
                            if empLen == totalVs:
                                matchList=matchList+each+'^'
                                keyList=keyList+each+'^'
                                #print('List1:', keyList, matchList)
                            else:
                                keyList=keyList+each+'^'
                                #print('List2:', keyList)
            for all in strikeList:
                try:
                    superPopList.remove(all)
                except ValueError:
                    continue
            strikeList = []
            
            if len(matchList) > 0:
                if len(emps[pWord]) == totalVs:
                    matchList=matchList+pWord+'^'
                    keyList=keyList+pWord+'^'
                else:
                    keyList=keyList+pWord+'^'
                rhyDic[keyList[:-1]] = matchList[:-1]
            keyList = str()
            matchList = str()
            
                
    print('rhyDic:', len(rhyDic))
    return rhyDic


def rhyMaker(totalVs, rSyls):
    if (rSyls <= totalVs):
        tName = str(totalVs)
        rName = str(rSyls)
        if totalVs < 10:
            tName = '0'+tName
        if rSyls < 10:
            rName = '0'+rName
        try:
            libFile = csv.reader(open('data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))
        except IOError:
            dicFile = csv.writer(open('data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", 'w', encoding='latin-1'))
            rhyDic = rhymeBuilder(totalVs, rSyls)
            for key, val in rhyDic.items():
                dicFile.writerow([key, val])
            

for totalVs in range(tVMin, tVMax):
    for rSyls in range(rSMin, rSMax):
        rhyMaker(totalVs, rSyls)

print('rhyBuild complete')


print('program complete')
