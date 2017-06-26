from string import *
import random
import datetime
import time
import csv
csv.field_size_limit(int(9999999))


###################
#- Categories and lists for characters

#-!obsolete?:

#->pass:
emps, vocs, fono, cons = {}, {}, {}, {}

pLine, pWord, pWLen = str(), str(), int(0)

line = int(0)

empIndexes = []

p = ()
ip = []
pLVocs = []
pLEmps = []
lastWord = ()

catch = []
index = []
indexes = []
vowString = []
cleanList = []

empHost = []
pEmps = str()
empString = []
empsLine = []
empKey = []

iA, iB, iC = int(0), int(0), int(0)

escCt, count, couplCount, count, nextLCt, xCt, yCt, zCt, lineCt, click = int(0), int(0), int(0), int(0), int(0), int(0), int(0), int(0), int(0), int(0)


vocsList = vocs = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'V', 'Y', '3', '0', '@', '&', 'L', 'M',  'N', '%', '!', '#', '$', '^', '*', '(', ')', '?', '<', '>', '.', '|', ']', '[', '=']
vow = 'y', 'a', 'e', 'i', 'o', 'u', 'ü', 'â', 'ê', 'è', 'ô', 'ö', 'õ', 'à', 'è', 'î', 'ã', 'ë', 'ä', 'ê', 'ĩ', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$', '%', '&', '!', '?', '<', '.', ':', ';', '(', ')', '[', ']', '{', '}', '1', '2'
accVow = 'á', 'é', 'ó', 'í', 'ú', 'ĕ', 'ė', 'ŏ', 'ő', 'ă', 'ą', 'Ə', 'ů', 'œ', 'þ', 'ø', 'æ'
allVow = 'y', 'a', 'e', 'i', 'o', 'u', 'ü', 'á', 'é', 'ó', 'í', 'ú', 'â', 'ê', 'è', 'ô', 'ö', 'õ', 'à', 'è', 'î', 'ã', 'ë', 'ä', 'ê', 'ĩ', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū', 'ĕ', 'ė', 'ŏ', 'ő', 'ă', 'ą', 'Ə', 'ů', 'œ', 'þ', 'ø', 'æ', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$', '%', '&', '!', '?', ',', '.', ':', ';', '(', ')', '[', ']', '{', '}', '1', '2'
empPat1 = 's', 'n', 'a', 'e', 'i', 'o', 'u', 'y', 'ë', 'ä', 'ã', 'õ', 'ö', 'ê', 'ĩ', 'î', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū'
cons = 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 'ñ'
strippers = '”', '’', "'", '…', '…', '—', '·', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '{', '}', '<', '>', '"', ',', '!', '.', ',', '‘', '’', '`', '~', '/', '+', '=', '|', '\c', '\n', '?', ';', ':', '_', '-', '¿', '»', '«', '¡', '©', '“', '”', 'º', '/', '\c'
spacers = '\n\n\n', '\n\n', '\n', '    ', '      ', '     ', '    ', '   ', '  '
caps =  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ü',
allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '``', '`', '"', "'", "''"]
silentPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '``', '`']
endPunx = ['.', '!', '?']

palabras = []


###################
#- This is wordprep. It will return lists of missing/unusable words.

def globalCheck(laLista, elNombre, palabras, textNomer):

    print('Testing incogruencies for '+elNombre)
    zCt = 0

    List = []
    negroLista = []
    for all in palabras:
##        zCt += 1
##        if zCt%1000 == 0:
##            print(zCt, '@', all)
        try:
            testLen = len(laLista[all])
            if testLen == 0:
                #print(all, 'has no ' + elNombre)
                negroLista.append(all)
                errataList.append(all)
            continue
        except KeyError:
            #print(elNombre + ' missing=', all)
            negroLista.append(all)
            errataList.append(all)
            continue

    incog = str()
    iCt = 0
    for all in errataList:
        iCt = errataList.count(all)
        while iCt > 1:
            iCt = errataList.count(all)
            errataList.remove(all)
        incog = (all+' '+incog)
    textNomer = str(input('Type name and filepath to write errata:  '))
    open(textNomer+'-'+elNombre+'.txt', 'w', encoding='latin-1').write(incog)


    return negroLista

#- Use these functions to open global data

def dataFileOpener(proxLista, libInt, strBit, textFile):
    dataFile = csv.reader(open('data/textLibrary/textData/'+textFile+'-'+strBit+str(all+1)+'.csv', 'r'))
    for line in dataFile:
        proxLista[all][line[0]] = line[1].split('^')
    return proxLista


def dynaDataWriter(dynaList, textFile, dynaType):
    dynaFile = csv.writer(open('data/textLibrary/textData/dynasaurus/'+textFile+'-'+dynaType+'.csv', 'w+'))
    dynaSaurus = {}
    for key, val in dynaList.items():
        svVal = str()
        for each in val:
            svVal = svVal+'^'
        dynaFile.writerow([pWord, svVal]) 
    #dynaFile.close()
    return dynaSaurus


def dynaDataOpener(textFile, dynaType):
    dynaFile = csv.reader(open('data/textLibrary/textData/dynasaurus/'+textFile+'-'+dynaType+'.csv', 'r'))
    dynaSaurus = {}
    for line in dynaFile:
        dynaSaurus[line[0]] = line[1].split('^')
    return dynaSaurus


def proxDataOpener(allDics, strBit, textFile):
    dataFile = csv.reader(open('data/textLibrary/textData/'+textFile+'-'+strBit+'.csv', 'r'))
    gpDic = {}
    for line in dataFile:
        dicInt = int(0)
        dicEntries = line[1].split('~')
        for all in allDics:
            try:
                all[line[0]] = dicEntries[dicInt].split('^')
                dicInt+=1
            except IndexError:
                continue
    #dataFile.close()
    return allDics


def gpDataWriter(allDics, strBit, textFile):
    pFile = csv.writer(open('data/textLibrary/textData/'+textFile+'-'+strBit+'.csv', 'w+'))
    print('building: data/textLibrary/textData/'+textFile+'-'+strBit+'.csv')
    gpDic = {}
    gpEntr = str()
    print(len(allDics))
    #print(allDics[0])
    for dicIndex in range(0, 19):
        if dicIndex == 0:
            for key, val in allDics[0].items():
                for each in val:
                    gpEntr=gpEntr+each+'^'
                gpDic[key] = gpEntr[:-1]+'~'
                print(gpEntr)
        else:
            try:
                for each in allDics[dicIndex]:
                    for key, val in each.items():
                        gpEntr = str()
                        for each in val:
                            gpEntr=gpEntr+each+'^'
                            print("gpEntr:", len(gpEntr))
                        gpDic[key] = gpDic[key]+gpEntr[:-1]+'~'
            except KeyError:
                print('kE datawriter:', pWord)
                continue
    for key, val in gpDic:
        pFile.writerow([pWord, gpEntr])

   
def dataWriter(lista, libInt, strBit, textFile):
    print(lista, libInt, strBit, textFile)
    pFile = csv.writer(open('data/textLibrary/textData/'+textFile+'-'+strBit+str(libInt+1)+'.csv', 'w+'))
    yaWrote = []
    for key, val in lista[libInt].items():
        svVal = str()
        for each in val:
            totChk = val.count(each)
            if (totChk >= 2) and (each not in yaWrote):
                svVal+=(each+'^')
                yaWrote.append(each)
        pFile.writerow([key, svVal[:-1]])


def globalOpen(name, mode):

    lib = {}

    libFile = csv.reader(open(name, 'r+', encoding='utf-8'))
    
    for line in libFile:
        if line != []:
            if mode == 'lista':
                lib[line[0]] = list(line[1])
            elif mode == 'string':
                lib[line[0]] = str(line[1])

    return lib

def globalClose(lib, name):

    libFile = csv.writer(open("__global/__data/" + name + "File.csv", "w+", encoding='latin-1'))

    for key, val in lib.items():
        ## REMOVE NEXT LINE'S CONDITION FOR CONSBUILD ##
        if val != []:
            svData = str()
            for each in lib[key]:
                svData = svData + each
            val = svData
            libFile.writerow([key, val])

def allDicsOpen(palabras, textNomer):

    lib, emps, vocs, fono, cons = {}, {}, {}, {}, {}
    negroLista = []
    dicSets = emps, vocs, fono, cons
    dicNames = 'emps', 'vocs', 'fono', 'cons'
    iCt = int(0)
    print('Opening dics...')
    negroLista = str()
    for each in dicSets:
        each = {}
        print('Opening '+dicNames[iCt]+'...')
        each = globalOpen(dicNames[iCt])
        print(len(each))
        #negroLista.append(globalCheck(each, dicNames[iCt], palabras, textNomer))
        #globalClose(each, dicNames[iCt])
        print(dicNames[iCt] + ' loaded')
        iCt+=1
    return  emps, vocs, fono, cons, negroLista


###################
#- Use these functions to pull phonetic data


def dataString(pString, dic): # Get vocal data from string object
    pData = dataLine(pString.split(' '), dic)
    return pData
    
def dataLine(pLine, dic):
    pData = []
    for each in pLine:
        if each in doubList:
            print('figure out')
        if (each not in silentPunx) and (len(each) > 0):
            pData.extend(dic[each])
    return pData
        
        

def empsLine(pLine, emps, doubles):

    empsLine = []
    #empHost = pLine.split(' ')
##    for all in silentPunx:
##        while all in pLine:
##            pLine.remove(all)
    for all in pLine:
        if (all not in silentPunx) and (len(all) > 0):
            eWord = all.lower()
            try:
                emps[eWord]
            except KeyError:
                try:
                    eWord = eWord[0].upper()+eWord[1:]
                    emps[eWord]
                except KeyError:
                    empsLine = []
                    #print('kE empsLine:', all)
                    break
                except IndexError:
                    print('wut?', eWord)
                    continue
            if all != '':
                eWord = all.lower()
                for each in silentPunx:
                    if each in eWord:
                        eWord = eWord.replace(each, '')
                if len(eWord) > 0:
                    if eWord in doubles:
                        doubInt = int(0)
                        eWord = eWord+'('+str(doubInt)+')'
                        testEmps = empsLine+emps[eWord]
                        while testEmps != empKeyLet[:len(testEmps)]:
                            try:
                                #print('testEmps:', testEmps)
                                testEmps = testEmps[:-len(emps[eWord])]
                                doubInt+=1
                                eWord = eWord[:-3]+'('+str(doubInt)+')'
                                testEmps = empsLine+emps[eWord]
                            except KeyError:
                                eWord = eWord[:-3]+'(0)'
                                continue
                    for each in emps[eWord]:
                        empsLine.append(each)
    return empsLine


def getLineData(pLine, vocs, emps, cons, phos): # pulls all the phonetic info at once

    pLVocs, pLEmps, pLFono, pLCons = [], [], [], []
    pLVocs = dataLine(pLine, vocs)
    pLEmps = dataLine(pLine, emps)
    pLFono = dataLine(pLine, phos)
    pLCons = dataLine(pLine, cons)

    return pLVocs, pLEmps, pLFono, pLCons


def getStringData(pString, vocs, emps, cons, phos): # Uses above function for string object

    pLine = pString.split(' ')
    pLVocs, pLEmps, pLFono, pLCons = getLineData(pLine, vocs, emps, cons, phos)
    
    return pLVocs, pLEmps, pLFono, pLCons, lastWord


def dataFileOpener(proxLista, libInt, strBit, textFile):
    dataFile = csv.reader(open('data/textLibrary/textData/'+textFile+'-'+strBit+str(all+1)+'.csv', 'r'))
    for line in dataFile:
        proxLista[all][line[0]] = line[1].split('^')
        

def lineToString(pLine):
    pString = str()
    for each in pLine:
        pString+=str(each)+' '
    for each in silentPunx:
        if each in pString:
            pString.replace(' '+each, each)
   #$ print('line2Str:', pString)
    return pString
    
def stringToLine(pString):
    for all in silentPunx:
        if all in pString:
            pString = pString.replace(all, ' '+all)
    pLine = pString.split(' ')
    while '' in pLine:
        pLine.remove('')
   #$ print('str2Line:', pLine)
    return pLine


def pStringToLineData(pString, doubles):

    pLine = []
    pLEmps = []
    pLFono = []
    pLVocs = []
    pLCons = []
    for all in allPunx:
        if all in pString:
            pString = pString.replace(all, ' '+all)
    pLine = pString.split(' ')
    while '' in pLine:
        pLine.remove('')
    for each in pLine:
        pWord = each.lower()
        if each in doubles:
            pWord = pWord+'(0)'
        try:
            emps[pWord]
        except KeyError:
            pWord = pWord[0].upper()+pWord[1:]
            try:
                emps[pWord]
            except KeyError:
                break
            continue
        except IndexError:
            continue
        if pWord == ("i'm" or 'i' or "I'll" or "i'd"):
            pWord = pWord.replace('i', 'I')
        if pWord not in allPunx:
            pLEmps+=emps[pWord]

    return pLine, pLEmps, pLFono, pLVocs, pLCons


def pLineToStringData(pLine, empKeyLet, doubles):

    pString = str()
##    pLEmps = []
##    pLFono = []
##    pLVocs = []
##    pLCons = []
##    for each in pLine:
##        pWord = each
##        pWord = each.lower()
##        if pWord in doubles:
##            pWord = pWord+'(0)'
##        try:
##            emps[pWord]
##        except KeyError:
##            try:
##                pWord = pWord[0].upper()+pWord[1:]
##                emps[pWord]
##            except KeyError:
##                break
##            except IndexError:
##                break
##            continue
##        if pWord not in allPunx:
##            if pWord in quantumList:
##                pLEmps+=empKeyLet[len(pLEmps):(len(pLEmps)+len(emps[pWord]))]
##            else:
##                pLEmps+=emps[pWord]
##        if '(' in pWord:
##            pWord = pWord[:-3]
##        if each[0].isupper():
##            pWord = pWord[0].upper()+pWord[1:]
    for each in pLine:
        pString = pString + each + ' '
    pString = pString[:-1]
    #print('pString check:', pString)
    for each in allPunx:
        if each in pString:
            pString = pString.replace(' '+each, each)
    for each in endPunx:
        iSpot = int(0)
        if each in pString:
            punxSpot = pString.index(each)
            if punxSpot <= (len(pString)-3):
                bigLetter = pString[punxSpot+2].capitalize()
                pString = pString[:punxSpot+2]+bigLetter+pString[punxSpot+3:]
    if len(pString) >= 2:
        pString = pString[0].upper() + pString[1:]

    return pString



#####
#  rhymes&rimas

## Can this be used to find a range of totalVs and rSyls?


def rhyDictator(superTokens, pWord, maxTotalVs, maxRSyls): # Find rhymes of a particular word
    matchBox, finalRhys = [], []
    totalVs, rSyls = int(1), int(1)
    while totalVs < maxTotalVs:
        while (rSyls <= totalVs):
            tName, rName = str(totalVs), str(rSyls)
           #$ print('gF.rhy:', pWord, str(totalVs), str(rSyls))
            if totalVs < 10:
                tName = '0'+tName
            if rSyls < 10:
                rName = '0'+rName
            try:
                dicFile = csv.reader(open('data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))
                for line in dicFile:
                    strikeList = []
                    keyChain = line[0].split('^')
                    if pWord in keyChain:
                        matchBox = line[1].split('^')
                        if pWord in matchBox:
                            matchBox.remove(pWord)
                        for all in matchBox:
                            if '(' in all:
                                newWord = all[:-3]
                                matchBox.append(newWord)
                                strikeList.append(all)
                            if all not in superTokens:
                                strikeList.append(all)
                        for all in strikeList:
                            if all in matchBox:
                                matchBox.remove(all)
                        strikeList = []                        
                        for all in matchBox:
                            if all not in finalRhys:
                                finalRhys.append(all)
                for all in matchBox:
                    if all not in finalRhys:
                        finalRhys.append(all)
            except IOError:
                return []
            rSyls+=1
        totalVs+=1
        rSyls = int(1)
    finalRhys.sort()
   #$ print('gF.rhys:', len(finalRhys))
    return finalRhys


def testAlts(pWord, altNum):
    altEmps = []
    altLet = str(altNum)
    altWord = pWord+'('+altLet+')'
    altNum+=1
    try:
        altEmps = emps[altWord]
    except KeyError:
        altNum = 2000

    return altEmps, altNum
