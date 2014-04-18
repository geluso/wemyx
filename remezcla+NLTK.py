
  
  # Imports:
  

from string import *
import csv
import datetime
import nltk
import re
import sh
import gloFunk
import random
import rhymingDictionaryFinal
csv.field_size_limit(int(9999999))


  
  # Input for template:

  # This is where the user declares what type of poem they want.
  # The stanzas are declared by a string of letters such as "ABAB"
  # with each matching letter receiving a rhyming line.
  # The meter for each line is declared by a string of ints (formerly
  # binaries, until a tertiary option, the secondary stress, was introduced)
  # Examples are given next to each input for limmericks
  
empKey = []
textFile = str(input('Which file to remix? : ')) # superBible
rhymeMap = str(input('Declare rhymeMap : ')) # aabba
yaFound = []
for each in rhymeMap:
    if each not in yaFound:
        oneEmpLine = list(input('Declare meter for line '+each+' : ')) # a: 0100101, b: 01001
        empKey.append(oneEmpLine)
        yaFound.append(each)
proxMaxDial = int(input('Max. length of proxDics? : ')) # 20
proxMinDial = int(input('Min. length of proxDics? : ')) # 5
punxProxNum = int(input('punxProxNum? : ')) # 5
poemCt = int(input('How many poems to write? : ')) # 666
print('\ndataBuild begin...')

grammarMaps = []
grammarLexi = {}
aGrammarMap = []
 
 # Here's where I declare some useful lists and clean the text
 # for easier processing

posTags = 'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '.', ',', ';', ':', '!', '?', '"', "'"
quantumTags = 'CC', 'DT', 'WRB', 'WP', 'WP$', 'PRP', 'PRP$', 'TO', 'IN'
quantumList = []

punxTags = ['"', "'", "''", ':']
allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '``', '`', '"', "'", "''"]
midPunx = [',', ';', ',', ':', '--']
endPunx = ['.', '!', '?']
punx = [',', ';', ',', ':', '--', '"', "'", "'", '-', "''", "''", "''"]
badGrams = ['``', '"', "''", '`', '']
notFirst = ['and', 'And', 'or', 'Or']
nonEnders = ['a', 'A', 'the', 'The', 'or', 'Or', 'and', 'And', 'of', 'Of', 'an', 'An']

print('grooming text...')
texto = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())
texto = texto.replace('Mr.', 'Mister')
texto = texto.replace('Mrs.', 'Missus')
texto = texto.replace('Ms.', 'Miss')
texto = texto.replace('Dr.', 'doctor')
texto = texto.replace("Can't", 'Cannot')
texto = texto.replace("can't", 'cannot')
texto = texto.replace("Don't", 'Do not')
texto = texto.replace("don't", 'do not')
texto = texto.replace("Won't", 'Will not')
texto = texto.replace("won't", 'will not')
texto = texto.replace("Shouldn't", "Should not")
texto = texto.replace("shouldn't", "should not")
texto = texto.replace("Wouldn't", "Would not")
texto = texto.replace("wouldn't", "would not")
texto = texto.replace("Couldn't", "Could not")
texto = texto.replace("couldn't", "could not")
texto = texto.replace("Haven't", "Have not")
texto = texto.replace("haven't", "have not")
texto = texto.replace("I'm", "I am")
texto = texto.replace("I'll", "I will")
texto = texto.replace("I'd", "I would")

for all in endPunx:
    texto = texto.replace(all, ' '+all)
for all in badGrams:
    texto = texto.replace(all, '')
superTokens = nltk.word_tokenize(texto)
for all in badGrams:
    while all in superTokens:
        superTokens.remove(all)

texto = ''


  # This part loads data that allows the computer to read meter, phonetics,
  # and to differentiate between similarly-spelled words

print('loading metadatas...')

libFile = csv.reader(open('data/USen/empDic-USen-even.csv', 'r'))  # poetEmps for iambic meter
emps = {}
doubles = []
for line in libFile:
    if line != []:
        emps[line[0]] = list(line[1])
        if '(' in line[0]:
            doubWord = line[0][:-3]
            if doubWord not in doubles:
                doubles.append(doubWord)
            emps[doubWord] = list(line[1])
for all in allPunx:
    emps[all] = []

doubFile = open('data/USen/doubList.txt', 'r')
for line in doubFile:
    if line not in doubles:
        pWord = line.replace('\n', '')
        doubles.append(pWord)
        try:
            doubEmps = emps[pWord+'(0)']
            emps[pWord] = doubEmps
        except KeyError:
            continue

vocs = gloFunk.globalOpen('data/USen/vocDic-USen-MAS.csv', 'string')
cons = gloFunk.globalOpen('data/USen/conDic-USen-MAS.csv', 'string')
fono = gloFunk.globalOpen('data/USen/fonDic-USen-MAS.csv', 'string')


  # Each proxlist is a record of words that come either next, after-next,
  # third-next, etc. These are used to create data regarding the
  # proximity of the words to each other, as well as information
  # about the grammatical structure of the author

proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20]
proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20  = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20]

proxPlusLista = proxPlusLista[:proxMaxDial]
proxMinusLista = proxMinusLista[:proxMaxDial]

gramProxP1, gramProxP2, gramProxP3, gramProxP4, gramProxP5, gramProxP6, gramProxP7, gramProxP8, gramProxP9, gramProxP10, gramProxP11, gramProxP12, gramProxP13, gramProxP14, gramProxP15, gramProxP16, gramProxP17, gramProxP18, gramProxP19, gramProxP20 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
gramProxPlusLista = [gramProxP1, gramProxP2, gramProxP3, gramProxP4, gramProxP5, gramProxP6, gramProxP7, gramProxP8, gramProxP9, gramProxP10, gramProxP11, gramProxP12, gramProxP13, gramProxP14, gramProxP15, gramProxP16, gramProxP17, gramProxP18, gramProxP19, gramProxP20]
gramProxM1, gramProxM2, gramProxM3, gramProxM4, gramProxM5, gramProxM6, gramProxM7, gramProxM8, gramProxM9, gramProxM10, gramProxM11, gramProxM12, gramProxM13, gramProxM14, gramProxM15, gramProxM16, gramProxM17, gramProxM18, gramProxM19, gramProxM20  = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
gramProxMinusLista = [gramProxM1, gramProxM2, gramProxM3, gramProxM4, gramProxM5, gramProxM6, gramProxM7, gramProxM8, gramProxM9, gramProxM10, gramProxM11, gramProxM12, gramProxM13, gramProxM14, gramProxM15, gramProxM16, gramProxM17, gramProxM18, gramProxM19, gramProxM20]


firstWords = []
lastSpot = len(superTokens)
yaFound = []
nextSentenceIndexes = []
wordsI=int(-1)
click = int(0)
proxNumerator = int(1)
proxDicCounter = int(0)
###print('04')

def dataFileOpener(proxLista, libInt, strBit, textFile):
    dataFile = csv.reader(open('data/textLibrary/textData/'+textFile+'-'+strBit+str(all+1)+'.csv', 'r'))
    for line in dataFile:
        proxLista[all][line[0]] = line[1].split('^')

def newProxLibs(proxLista, libInt, superTokens):
    for each in superTokens:
        proxLista[libInt][each.lower()] = []
        if len(each) > 1:
            proxLista[libInt][each[0].upper()+each[1:]] = []
        else:
            proxLista[libInt][each.upper()] = []
    return proxLista

try:
    firstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'r')
    for line in firstFile:
        firstWords.append(line[:-1])
    for all in range(0, (len(proxPlusLista))):
        dataFileOpener(proxPlusLista, all, 'proxP', textFile)
        dataFileOpener(proxMinusLista, all, 'proxM', textFile)
        dataFileOpener(gramProxPlusLista, all, 'gramP', textFile)
        dataFileOpener(gramProxMinusLista, all, 'gramM', textFile)
                
except FileNotFoundError:
    superTokenData = nltk.pos_tag(superTokens)
    superTokenGrams = []
    for each in superTokenData:
        superTokenGrams.append(each[1])
    superTokenData = []
    for all in range(0, (len(proxPlusLista))):
        proxPlusLista = newProxLibs(proxPlusLista, all, superTokens)
        proxMinusLista = newProxLibs(proxMinusLista, all, superTokens)
        for each in posTags:
            gramProxPlusLista[all][each] = []
            gramProxMinusLista[all][each] = []
    while (wordsI+1) < lastSpot:    
        click+=1
        wordsI+=1
        proxNumerator = int(1)
        proxDicCounter = int(0)
        try:
            while proxDicCounter < len(proxPlusLista):
                pWord = superTokens[wordsI]
                if pWord in endPunx:
                    if superTokens[wordsI+1] not in firstWords:
                        firstWords.append(superTokens[wordsI+1])
                proxWord = superTokens[wordsI+proxNumerator]
                gramPWord = superTokenGrams[wordsI]
                gramProxWord = superTokenGrams[wordsI+proxNumerator]
                if proxWord not in proxPlusLista[proxDicCounter][pWord]:
                    proxPlusLista[proxDicCounter][pWord].append(proxWord)
                if pWord not in proxMinusLista[proxDicCounter][proxWord]:
                    proxMinusLista[proxDicCounter][proxWord].append(pWord)
                if gramProxWord not in gramProxPlusLista[proxDicCounter][gramPWord]:
                    gramProxPlusLista[proxDicCounter][gramPWord].append(gramProxWord)
                if gramPWord not in gramProxMinusLista[proxDicCounter][gramProxWord]:
                    gramProxMinusLista[proxDicCounter][gramProxWord].append(gramPWord)
                proxDicCounter+=1
                proxNumerator+=1
        except IndexError:          
            continue
        except KeyError:
            ####print('kE build:', pWord, proxWord, proxDicCounter, proxNumerator)
            continue


def dataWriter(lista, libInt, strBit, textFile):
    pFile = csv.writer(open('data/textLibrary/textData/'+textFile+'-'+strBit+str(all+1)+'.csv', 'w+'))
    for key, val in lista[libInt].items():
        svVal = str()
        for each in val:
            svVal+=(each+'^')
        pFile.writerow([key, svVal[:-1]])
    
if click > 0:
    for all in range(0, (len(proxPlusLista))):
        dataWriter(proxPlusLista, all, 'proxP', textFile)
        dataWriter(proxMinusLista, all, 'proxM', textFile)
        dataWriter(gramProxPlusLista, all, 'gramP', textFile)
        dataWriter(gramProxMinusLista, all, 'gramM', textFile)

    newFirstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
    for all in firstWords:
        newFirstFile.write(all+'\n')
        ####print('writing...', all)
    newFirstFile.close()

for key, val in grammarLexi.items():
    if key in quantumTags:
        for each in val:
            quantumList.append(each)
            if each in firstWords:
                firstWords.remove(each)
    elif key in punxTags:
        for each in val:
            allPunx.append(each)


  # These are functions that build the lines and stanzas for each poem

def acceptWord(pLine, pLineNum, pLineNList, proxNum, proxNumList, nextWord, rhymeList, superBlackList, jumpProxList):
   
    pLine.append(nextWord)
    if len(proxNumList) > 0:
        proxNum = proxNumList[-1] + 1
    else:
        proxNum = 0
    proxNumList.append(proxNum)
    pLineNum = pLineNList[0] + 1
    pLineNList.insert(0, pLineNum)
    expressList = []
    for all in rhymeList:
        expressList.append(all)
    superBlackList.append([])
    burnList = []
    jumpList = proxP2[pLine[-1]]
    for all in proxNumList[:len(pLine)]:
        screenList = proxPlusLista[all+1][pLine[all]]
        if all not in jumpList:
            burnList.append(all)
    for all in burnList:
        if all in jumpList:
            jumpList.remove(all)
    jumpProxList.append(jumpList)
    return pLine, pLineNum, pLineNList, proxNum, proxNumList, expressList, superBlackList, jumpProxList


def resetLine(pLine, pLEmps, pWord, pWEmps, superPopList, anteLine, rhymeList, blackList, firstPopList, jumpProxList):
    pLine, pLEmps, pWEmps, pLineNList, proxNumList, superPopList, expressList, blackList, firstPopList, jumpProxList = [], [], [], [], [], [], [], [], [], []
    pWord = str()
    pLineNum, pLNi, proxNum = int(0), int(0), int(0)
    runLine = anteLine
    for all in rhymeList:
        expressList.append(all)
    return runLine, pLine, pLEmps, pWord, pWEmps, pLineNum, pLineNList, proxNum, proxNumList, superPopList, expressList, blackList, firstPopList, jumpProxList


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


def pStringToLineData(pString):

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


def pLineToStringData(pLine, empKeyLet):

    pString = str()
    pLEmps = []
    pLFono = []
    pLVocs = []
    pLCons = []
    for each in pLine:
        pWord = each
        pWord = each.lower()
        if pWord in doubles:
            pWord = pWord+'(0)'
        try:
            emps[pWord]
        except KeyError:
            try:
                pWord = pWord[0].upper()+pWord[1:]
                emps[pWord]
            except KeyError:
                break
            except IndexError:
                break
            continue
        if pWord not in allPunx:
            if pWord in quantumList:
                pLEmps+=empKeyLet[len(pLEmps):(len(pLEmps)+len(emps[pWord]))]
            else:
                pLEmps+=emps[pWord]
        if '(' in pWord:
            pWord = pWord[:-3]
        if each[0].isupper():
            pWord = pWord[0].upper()+pWord[1:]

        pString = pString + pWord + ' '
    pString = pString[:-1]
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

    return pString, pLEmps, pLFono, pLVocs, pLCons    
    

def gramProxWords(proxList, pLine, runLine, proxNumList, pLNi, pLineNList, proxMinDial, proxLib, gramProxLib, superPopList, lastList, superBlackList, allLinesLine, preferredList, jumpProxList, startTimeM, startTimeH):

    stopTimeM = int(str(datetime.datetime.now())[14:16])
    stopTimeH = str(datetime.datetime.now())[11:13]
    if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and (startTimeM < (stopTimeM + 49))):
        return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
    pList = []
    proxList = []
    gramList = []
    keepList = []
    transList = []
    checkList = []
    gramLine = []
    aLLgramData = []
    aLLgramLine = []
    pGramData = []
    pGramLine = []
    firstPopList = []
    pLine = runLine + pLine
    superPopList = superPopList[:min((len(pLine)+1), len(superPopList))]
    pLNi = 0
    try:
        transList = proxP1[pLine[-1].lower()]
        for each in transList:
            pList.append(each)
    except KeyError:
        try:
            transList = proxP1[pLine[-1]]
            for each in transList:
                pList.append(each)
        except KeyError:
            pLine = pLine[len(runLine)+1:]
            return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
    if len(superBlackList) > 0:
        for all in superBlackList[-1]:
            if all in pList:
                pList.remove(all)
    else:
        superBlackList.append([])
    if (len(pLine) == 1) or (len(pLineNList) < proxMinDial):
        superPopList.append([])
        for each in pList:
            if each in preferredList:
                firstPopList.append(each)
            else:
                superPopList[-1].append(each)
        jumpProxList = [['__'], []]
        try:
            for each in proxP2[pWord]:
                jumpProxList[-1].append(each)
            pLine = pLine[len(runLine)+1:]
            return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
        except KeyError:
            return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
    else:
        try:
            if len(allLinesLine) > 0:
                aLLgramData = nltk.pos_tag(allLinesLine)                
                for each in aLLgramData:
                    aLLgramLine.append(each[1])
            if len(pLine) > 0:
                pGramData = nltk.pos_tag(pLine)
                for each in pGramData:
                    pGramLine.append(each[1])
            if len(jumpProxList) == len(pLine):
                for all in proxNumList:
                    stopTimeM = int(str(datetime.datetime.now())[14:16])
                    stopTimeH = str(datetime.datetime.now())[11:13]
                    if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and (startTimeM < (stopTimeM + 49))):
                        return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
                    gramBit = pGramLine[pLineNList[pLNi]]
                    gramList = gramProxLib[all][gramBit]
                    try:
                        proxList = proxLib[all][pLine[pLineNList[pLNi]]]
                    except KeyError:
                        proxList = proxLib[all][pLine[pLineNList[pLNi]].lower()]
                        continue
                    for each in proxList:
                        stopTimeM = int(str(datetime.datetime.now())[14:16])
                        stopTimeH = str(datetime.datetime.now())[11:13]
                        if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and (startTimeM < (stopTimeM + 49))):
                            return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
                        flashLine = []
                        if len(allLinesLine) > 0:
                            for all in allLinesLine:
                                flashLine.append(all)
                        elif len(pLine) > 0:
                            for all in pLine:
                                flashLine.append(all)
                        flashGram = nltk.pos_tag(flashLine)
                        checkGram = flashGram[-1][1]
                        if checkGram not in badGrams:
                            if (checkGram in gramList):
                                checkList.append(each)
                    else:
                        for each in pList:
                            if each in checkList:
                                keepList.append(each)
                        pList = keepList
                        keepList = []
                    pLNi+=1
                    countJumps = []
                    for each in jumpProxList:
                        thisCount = len(each)
                        countJumps.append(thisCount)
                    if len(pList) == 0:
                        break
            else:
                countJumps = []
                for each in jumpProxList:
                    thisCount = len(each)
                    countJumps.append(thisCount)
                keepList = []
                for all in pList:
                    stopTimeM = int(str(datetime.datetime.now())[14:16])
                    stopTimeH = str(datetime.datetime.now())[11:13]
                    if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and (startTimeM < (stopTimeM + 49))):
                        return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
                    if all in jumpProxList[-1]:
                        flashLine = []
                        if len(allLinesLine) > 0:
                            for all in allLinesLine:
                                flashLine.append(all)
                        elif len(pLine) > 0:
                            for all in pLine:
                                flashLine.append(all)
                        flashGram = nltk.pos_tag(flashLine)
                        checkGram = flashGram[-1][1]
                        if checkGram not in badGrams:
                            if (checkGram in gramList):
                                keepList.append(all)
            if len(pList) > 0:
                superPopList.append(pList)
                for all in superPopList[-1]:
                    if (all in preferredList) and (all not in allPunx):
                        firstPopList.append(superPopList[-1].pop(superPopList[-1].index(all)))
                pLine = pLine[len(runLine)+1:]
                return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
            elif len(pLineNList) >= proxMinDial:
                proxNumList.pop()
                pLineNList.pop()
                if len(jumpProxList) > (len(pLine) + 2):
                    jumpProxList.pop()
                superPopList.append([])
                pLine = pLine[len(runLine)+1:]
                return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
            else:
                superPopList.append([])
                pLine = pLine[len(runLine)+1:]
                return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
        except IndexError:
            superPopList.append([])
            pLine = pLine[len(runLine)+1:]
            return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
        except KeyError:
            superPopList.append([])
            pLine = pLine[len(runLine)+1:]
            return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList
        
    if len(lastList) > 0:
        while proxInt <= len(proxPlusLista):
            proxInt = int(0)
            for each in lastList:
                organizeList = []
                punxList = []
                for all in pList:
                    if all in allPunx:
                        punxList.append(all)
                    elif (each in proxPlusLista[proxInt]) or (each in proxMinusLista[proxInt]):
                        organizeList.insert(each, 0)
                    else:
                        organizeList.append(each)
                pList = organizeList
                for all in punxList:
                    pList.append(all)
    superPopList.append(pList)
    for all in preferredList:
        if (all in superPopList[-1]) and (all not in allPunx):
            firstPopList.append(superPopList[-1].pop(superPopList[-1].index(all)))

    return superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList


  # This function needs the data that the rhyming dictionary program uses.
  # The actual rhyming dictionary program works almost the same.

def dicWordLookup(pWord, totalVs, rSyls):
    matchBox = []
    if (rSyls <= totalVs):
        tName = str(totalVs)
        rName = str(rSyls)
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
                    matchBox.sort()
                    return matchBox
            return matchBox
        except IOError:
            return []


def getEmps(pWord):
    try:
        return emps[pWord.lower()]
    except KeyError:
        try:
            return emps[pWord]
        except KeyError:
            return []
             

def proxDataReboot(pLine):
    pCt = int(0)
    proxNumList = []
    pLineNList = []
    while pCt < len(pLine):
        proxNumList.append(pCt)
        pLineNList.insert(0, pCt)
        pCt+=1
    return pLineNList, proxNumList
    

def printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList):
    superIntLine = []
    superBIntLine = []
    jumpIntLine = []
    for all in superPopList:
        superIntLine.append(str(len(all)))
    superBIntLine = []
    for all in superBlackList:
        superBIntLine.append(str(len(all)))
    for all in jumpProxList:
        jumpIntLine.append(str(len(all)))


def startLiner(anteString, rhymeList):
    pLine, pLEmps, pWEmps, pLineNList, proxNumList, proxList, superPopList, superBlackList, expressList, subPunx, lastPunx, punxList, runList, blackList, sv1stSuperPop, sv1stSuperBlack, jumpProxList, preferredList, anteLine, runLine = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    pLLen, pLineNum, pLNi, proxNum, thisPLen = int(0), int(0), int(0), int(0), int(0)
    pWord, svPWord, result = str(), str(), str()
    superBlackList.append(metaBlackList)
    anteLine, anteLEmps, anteLFono, anteLVocs, anteLCons = pStringToLineData(anteString)
    if len(anteLine) > 2:
        anteLine = anteLine[len(anteLine)-3:]
    runString = anteString
    runLine, runLEmps, runLFono, runLVocs, runLCons = pStringToLineData(runString)
    if len(runLine) > 2:
        runLine = runLine[len(runLine)-3:]
    rhyInt = int(0)
    while rhyInt < len(rhymeList):
        rhyWord = rhymeList[rhyInt]
        for each in proxMinusLista:
            targetWords = each[rhyWord]
            for all in targetWords:
                if (all not in preferredList) and (all not in quantumList):
                    preferredList.append(all)
        rhyInt+=1
    return pLine, pLEmps, pWEmps, pLineNList, proxNumList, proxList, superPopList, superBlackList, expressList, subPunx, lastPunx, punxList, runList, blackList, sv1stSuperPop, sv1stSuperBlack, jumpProxList, preferredList, pLLen, pLineNum, pLNi, proxNum, thisPLen, pWord, svPWord, result, anteLine, anteLEmps, anteLFono, anteLVocs, anteLCons, runLine, runLEmps, runLFono, runLVocs, runLCons


  # This is where the program builds individual lines, the essence of this project.

def poemLiner(rhymeList, empKeyLet, anteString, startList, usedList, lastList, proxMinDial, metaBlackList, allLinesLine, startTimeM, startTimeH):
    pLine, pLEmps, pWEmps, pLineNList, proxNumList, proxList, superPopList, superBlackList, expressList, subPunx, lastPunx, punxList, runList, blackList, sv1stSuperPop, sv1stSuperBlack, jumpProxList, preferredList, pLLen, pLineNum, pLNi, proxNum, thisPLen, pWord, svPWord, result, anteLine, anteLEmps, anteLFono, anteLVocs, anteLCons, runLine, runLEmps, runLFono, runLVocs, runLCons = startLiner(anteString, rhymeList)
    while (pLEmps != empKeyLet[0:len(empKeyLet)]) and (len(pLEmps) < len(empKeyLet)):
        stopTimeM = int(str(datetime.datetime.now())[14:16])
        stopTimeH = str(datetime.datetime.now())[11:13]
        if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and (startTimeM < (stopTimeM + 49))):
            break
        pLLen = len(pLine)
        if len(runLine) > 0:
            thisPLen = len(pLine)
            pLine = runLine + pLine
            runCt = int(0)
            proxNumList = []
            pLineNList = []
            while runCt < len(pLine):
                proxNumList.append(runCt)
                pLineNList.insert(0, runCt)
                pLNi = 0
                runCt+=1
            while ((len(pLineNList) >= proxMinDial) or (thisPLen < proxMinDial)) or (len(runLine) > 0):
                if len(superPopList) == 0:
                    superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList = gramProxWords(proxList, pLine, runLine, proxNumList, pLNi, pLineNList, proxMinDial, proxPlusLista, gramProxPlusLista, superPopList, lastList, superBlackList, allLinesLine, preferredList, jumpProxList, startTimeM, startTimeH)
                    superIntLine = []
                    superBIntLine = []
                    printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                    if len(pLine) == len(runLine):
                        for all in allPunx:
                            while all in superPopList[-1]:
                                superPopList[-1].remove(all)
                            while all in firstPopList:
                                firstPopList.remove(all)

                    if (len(superPopList[-1]) > 0) or (len(firstPopList) > 0):
                        break
                    else:
                        if (len(pLineNList) > 0) and (len(runLine)==0):
                            proxNumList.pop()
                            pLineNList.pop(0)
                            if len(jumpProxList) > (len(pLine) + 2):
                                jumpProxList.pop()
                        pLine = pLine[len(runLine):]
                        runLine.pop(0)
                        thisPLen = len(pLine)
                        pLine = runLine + pLine
                else:
                    break
            pLine = pLine[len(runLine):]
            if len(pLine) == 0:
                pLEmps = ['2']
                while ((len(pLEmps) == 0) or (len(pWord) < 1) or (pWord in allPunx) or (pLEmps[:len(pLEmps)] != empKeyLet[:len(pLEmps)])) and (((len(superPopList[-1]) != 0) and (len(superPopList) != 0)) or (len(firstPopList) != 0)):
                    if len(firstPopList) > 0:
                        pWord = str(firstPopList.pop(firstPopList.index(random.choice(firstPopList))))
                    else:
                        pWord = superPopList[-1].pop(superPopList[-1].index(random.choice(superPopList[-1])))
                    if (pWord not in preferredList) and (pWord not in rhymeList) and (pWord not in superBlackList) and (pWord not in quantumList):
                        superBlackList[-1].append(pWord)
                    metaBlackList.append(pWord)
                    pLEmps = gloFunk.empsLine([pWord], emps, doubles, empKeyLet)
                    try:
                        pLineNum, pLineNList, pLNi, proxNum, proxNumList, proxList = int(0), [int(0)], int(0), int(0), [int(0)], proxP1[pWord]
                    except KeyError:
                        continue
                if (pLEmps == empKeyLet[:len(pLEmps)]) and (pWord not in allPunx):
                    pLine = [pWord]
                    if pWord in superBlackList[-1]:
                        superBlackList[-1].remove(pWord)
                if len(pLine) == 0:
                    if runLine[-1] in allPunx:
                        runnerInt = int(3)
                    else:
                        runnerInt = int(4)
                    if len(runLine) > runnerInt:
                        runLine.pop(0)
                        pLine = runLine + pLine
                        if len(superPopList) > 0:
                            superPopList.pop()
                        if len(pLineNList) > 0:
                            pLineNList.pop(0)
                            proxNumList.pop()
                            if len(jumpProxList) > (len(pLine) + 2):
                                jumpProxList.pop()
                        while runCt < len(pLine):
                            proxNumList.append(runCt)
                            pLineNList.insert(0, runCt)
                            pLNi = 0
                            runCt+=1
                        superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList = gramProxWords(proxList, pLine, runLine, proxNumList, pLNi, pLineNList, proxMinDial, proxPlusLista, gramProxPlusLista, superPopList, lastList, superBlackList, allLinesLine, preferredList, jumpProxList, startTimeM, startTimeH)
                        for all in allPunx:
                            while all in superPopList[-1]:
                                superPopList[-1].remove(all)
                        printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                        pLine = pLine[len(runLine):]
                    else:
                        break
                else:
                    pLine = runLine + pLine
                    runCt = int(0)
                    proxNumList = []
                    pLineNList = []
                    while runCt < len(pLine):
                        proxNumList.append(runCt)
                        pLineNList.insert(0, runCt)
                        pLNi = 0
                        runCt+=1
                    superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList = gramProxWords(proxList, pLine, runLine, proxNumList, pLNi, pLineNList, proxMinDial, proxPlusLista, gramProxPlusLista, superPopList, lastList, superBlackList, allLinesLine, preferredList, jumpProxList, startTimeM, startTimeH)
                    superBlackList.append([])
                    printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                    pLine = pLine[len(runLine):]

        elif (len(pLine) == 0) and (len(runLine) == 0):
            superPopList = [[]]
            for each in firstWords:
                superPopList[-1].append(each)
            superBlackList = [[]]
            pLEmps = []
            while (len(pLEmps)==0) or ((pWord in allPunx) or (pWord in notFirst) or ((pLEmps[:len(pLEmps)] != empKeyLet[:len(pLEmps)]) and len(superPopList[-1]) != 0)):
                pWord = superPopList[-1].pop(superPopList[-1].index(random.choice(superPopList[-1])))
                pLine = [pWord]
                pLEmps = gloFunk.empsLine(pLine, emps, doubles, empKeyLet)
                if (pWord not in preferredList) and (pWord not in rhymeList) and (pWord not in blackList) and (pWord not in quantumList):
                    superBlackList[-1].append(pWord)
                metaBlackList.append(pWord)
                pLineNum, pLineNList, pLNi, proxNum, proxNumList, proxList = int(0), [int(0)], int(0), int(0), [int(0)], proxP1[pWord]
            if pWord in superBlackList[-1]:
                superBlackList[-1].remove(pWord)
            superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList = gramProxWords(proxList, pLine, runLine, proxNumList, pLNi, pLineNList, proxMinDial, proxPlusLista, gramProxPlusLista, superPopList, lastList, superBlackList, allLinesLine, preferredList, jumpProxList, startTimeM, startTimeH)
            superBlackList.append([])
            printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
            if len(pLine) == 0:
                break
        if len(rhymeList) > 0 and (len(expressList) == 0):
            try:
                for all in rhymeList:
                    if all in superPopList[-1]:
                        expressList.append(superPopList[-1].pop(superPopList[-1].index(all)))
            except IndexError:
                superPopList = [[]]
                runLine, pLine, pLEmps, pWord, pWEmps, pLineNum, pLineNList, proxNum, proxNumList, superPopList, expressList, superBlackList, firstPopList, jumpProxList = resetLine(pLine, pLEmps, pWord, pWEmps, superPopList, anteLine, rhymeList, superBlackList, firstPopList, jumpProxList)
                continue
       
        for all in badGrams:
            while all in superPopList[-1]:
                superPopList[-1].remove(all)
            while all in firstPopList:
                firstPopList.remove(all)
        if len(pLine) > 0:
            if pLine[-1] in allPunx:
                for all in allPunx:
                    while all in superPopList[-1]:
                        superPopList[-1].remove(all)

        while ((len(superPopList) != 0) and (len(superPopList[-1]) > 0)) or (len(firstPopList) > 0) or (len(expressList) > 0) :
            stopTimeM = int(str(datetime.datetime.now())[14:16])
            stopTimeH = str(datetime.datetime.now())[11:13]
            if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and (startTimeM < (stopTimeM + 49))):
                break            
            pWEmps = []
            pLELen = len(pLEmps)
            while len(expressList) > 0:
                pWord = str(expressList.pop(expressList.index(random.choice(expressList))))
                if (emps[pWord] == empKeyLet[pLELen:]) and (pWord in superPopList[-1]) and (pWord not in nonEnders):
                    pLine.append(pWord)
                    pString, pLEmps, pLFono, pLVocs, pLCons = pLineToStringData(pLine, empKeyLet)
                    for all in pLine:
                        if all not in allPunx:
                            usedList.append(all)
                    if (pLine[-1] not in allPunx) and (pLine[-1] not in lastList):
                        lastList.append(pLine[-1])
                    else:
                        lastList.append(pLine[-2])
                    return pString, startList, usedList, lastList, 'pass', pLEmps
            if (len(rhymeList) > 0) and (len(expressList) == 0) and ((len(empKeyLet) - 1) == len(pLEmps)):
                sliceWord = pLine.pop()
                sliceEmps = []
                superPopList.pop()
                superBlackList.pop()
                printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                if len(superBlackList) > 0:
                    if (pWord not in rhymeList) and (pWord not in blackList) and (pWord not in quantumList):
                        superBlackList[-1].append(sliceWord)
                if len(superPopList) == 0:
                    superPopList = [[]]
                proxNumList.pop()
                pLineNList.pop(0)
                if len(jumpProxList) > (len(pLine) + 2):
                    jumpProxList.pop()
                printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                sliceEmps = gloFunk.empsLine([sliceWord], emps, doubles, empKeyLet)
                pLEmps = pLEmps[:-(len(sliceEmps))]
                break
            
            if (len(firstPopList) > 0) and (len(expressList) == 0):
                pWord = str(firstPopList.pop(firstPopList.index(random.choice(firstPopList))))
                while ((pWord in endPunx) and (len(firstPopList) > 0) and (pWord in superBlackList[-1])):
                    pWord = str(firstPopList.pop(firstPopList.index(random.choice(firstPopList))))
                    if len(firstPopList) == 0:
                        if len(superPopList[-1]) > 0:
                            pWord = str(superPopList[-1].pop(superPopList[-1].index(random.choice(superPopList[-1]))))
                        else:
                            break
            
            elif (len(superPopList[-1]) > 0) and (len(expressList) == 0):
                pWord = str(superPopList[-1].pop(superPopList[-1].index(random.choice(superPopList[-1]))))
                while ((pWord in endPunx) and (len(superPopList[-1]) > 0)):
                    pWord = str(superPopList[-1].pop(superPopList[-1].index(random.choice(superPopList[-1]))))
                    if len(superPopList[-1]) == 0:
                        break
            else:
                break

            try:
                emps[pWord.lower()]
                pWord = pWord.lower()
            except KeyError:
                continue
            try:
                if (pWord in quantumList) and (pWord not in pLine) and (len(empKeyLet) <= (len(emps[pWord])+len(pLEmps))):
                    pWEmps = emps[pWord]
                    pWEmps = empKeyLet[pLELen:(pLELen+len(pWEmps))]
                elif (pWord not in usedList) and (pWord not in badGrams) and ((pWord not in pLine) or (pWord in quantumList)):
                    pWEmps = gloFunk.empsLine([pWord], emps, doubles, empKeyLet)
                    if pWord in quantumList:
                        pWEmps = empKeyLet[pLELen:(pLELen+len(pWEmps))]
                else:
                    pWord = str()
                    
                if (len(pLine) > 0) and (len(pWord) > 0):
                    newEmps = pLEmps + pWEmps
                    if (pWord in rhymeList) and (newEmps == empKeyLet[0:len(empKeyLet)]) and ((pWord not in quantumList) or (pLine[-1] not in quantumList)):
                        pLEmps = newEmps
                        pLELen = len(pLEmps)
                        pLine, pLineNum, pLineNList, proxNum, proxNumList, expressList, superBlackList, jumpProxList = acceptWord(pLine, pLineNum, pLineNList, proxNum, proxNumList, pWord, rhymeList, superBlackList, jumpProxList)
                        break
                    elif (pWord not in rhymeList) and (pWord not in blackList) and (newEmps == empKeyLet[:(len(newEmps))]) and (len(newEmps) <= len(empKeyLet)) and ((pWord not in quantumList) or (pLine[-1] not in quantumList)):
                        punxCt = int(0)
                        for each in allPunx:
                            punxCt+=pLine[:-(min((len(pLine)), (punxProxNum)))].count(each)
                        if (punxCt == 0): ## or (pWord not in allPunx)
                            pLEmps = pLEmps + pWEmps
                            pLELen = len(pLEmps)
                            pLine, pLineNum, pLineNList, proxNum, proxNumList, expressList, superBlackList, jumpProxList = acceptWord(pLine, pLineNum, pLineNList, proxNum, proxNumList, pWord, rhymeList, superBlackList, jumpProxList)
                            superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList = gramProxWords(proxList, pLine, runLine, proxNumList, pLNi, pLineNList, proxMinDial, proxPlusLista, gramProxPlusLista, superPopList, lastList, superBlackList, allLinesLine, preferredList, jumpProxList, startTimeM, startTimeH)
                            printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                            break
                    elif (pWord not in preferredList) and (pWord not in rhymeList) and (pWord not in blackList) and (pWord not in quantumList):
                        superBlackList[-1].append(pWord)
                elif (pWEmps == empKeyLet[:len(pWEmps)]) and (pWord not in quantumList) and (pWord not in allPunx) and (len(pWord) > 0):
                    pLEmps = pWEmps
                    pLELen = len(pLEmps)
                    pLine, pLineNum, pLineNList, proxNum, proxNumList, expressList, superBlackList, jumpProxList = acceptWord([], int(0), [0], 0, [0], pWord, rhymeList, superBlackList, jumpProxList)
                    break
                else:
                    superBlackList[-1].append(pWord)                

            except KeyError:
                continue   

            if len(pLine) > pLLen:
                printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                break
            pString, qLEmps, qLFono, qLVocs, qLCons = pLineToStringData(pLine, empKeyLet)
            if (len(pLEmps) == len(empKeyLet)) and (pLine[-1] in quantumList):
                pLEmps = pLEmps[:-len(emps[pLine.pop()])]
                pLELen = len(pLEmps)

        if (len(expressList) == 0) and (len(firstPopList) == 0) and (pLLen == len(pLine) and (len(superPopList[-1]) == 0)):
            if len(runLine) > 0:
                runLine.pop(0)
                if len(pLineNList) > 0:
                    pLineNList.pop(0)
                    proxNumList.pop()
                    if len(jumpProxList) > (len(pLine) + 2):
                        jumpProxList.pop()
                pLine = runLine + pLine
                printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                pLine = pLine[len(runLine):]
            elif len(pLine) >= proxMinDial: 
                if len(pLineNList) >= proxMinDial:
                    proxNumList.pop()
                    pLineNList.pop()
                    if len(jumpProxList) > (len(pLine) + 2):
                        jumpProxList.pop()
            elif (thisPLen < len(pLineNList)) and (len(runLine) > 0):
                thisPLen = thisPLen  ## This line basically says 'do nothing'
            elif len(superPopList[0]) > 0:
                pLine, pLineNList, proxNumList = [], [], []
                superPopList = superPopList[:1]
                superBlackList = superBlackList[:1]
                runLine = anteLine
            else:
                break
        elif (len(pLEmps) == len(empKeyLet)) and (((len(rhymeList) > 0) and (pLine[:-1] not in rhymeList)) or (pLine[:-1] in nonEnders)):
            sliceWord = pLine.pop()
            sliceEmps = []
            superPopList.pop()
            superBlackList.pop()
            printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
            if len(superBlackList) > 0:
                superBlackList[-1].append(sliceWord)
            if len(superPopList) == 0:
                superPopList = [[]]
            proxNumList.pop()
            pLineNList.pop(0)
            if len(jumpProxList) > len(pLine) + 2:
                jumpProxList.pop()
            printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
            sliceEmps = gloFunk.empsLine([sliceWord], emps, doubles, empKeyLet)
            pLEmps = pLEmps[:-(len(sliceEmps))]
        if ((len(pLineNList) < proxMinDial) and (len(pLine) >= proxMinDial)) or ((len(superPopList[-1]) == 0) and (len(firstPopList) == 0)):
            superPopList[-1] = []
            while ((len(superPopList[-1]) == 0) and (len(firstPopList) == 0)) and (len(pLine) > 0):
                stopTimeM = int(str(datetime.datetime.now())[14:16])
                stopTimeH = str(datetime.datetime.now())[11:13]
                if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and (startTimeM < (stopTimeM + 49))):
                    break
                while pLine[-1] == '':
                    pLine.pop()
                    if len(pLine) == 0:
                        break
                if len(pLine) == 0:
                    break
                if (pLine[0] not in rhymeList) and (pLine[0] not in metaBlackList):
                    svPWord = pLine[0]
                if pLine[-1] not in rhymeList:
                    pLine = pLine[:-1]
                pString, pLEmps, pLFono, pLVocs, pLCons = pLineToStringData(pLine, empKeyLet)                
                pLEmps = gloFunk.empsLine(pLine, emps, doubles, empKeyLet)
                sv1stSuperPop = superPopList[0]
                sv1stSuperBlack = superBlackList[0]
                superPopList.pop()
                superBlackList.pop()
                pLineNList, proxNumList = proxDataReboot(pLine)
                printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
                if len(superPopList) == 0:
                    break
            if len(pLine) == 0:
                runLine, pLine, pLEmps, pWord, pWEmps, pLineNum, pLineNList, proxNum, proxNumList, superPopList, expressList, superBlackList, firstPopList, jumpProxList = resetLine(pLine, pLEmps, pWord, pWEmps, superPopList, anteLine, rhymeList, superBlackList, firstPopList, jumpProxList)
                superPopList.append(sv1stSuperPop)
                superBlackList.append(sv1stSuperBlack)
                if svPWord not in metaBlackList:
                    metaBlackList.append(svPWord)
    if (len(pLineNList) < proxMinDial) and (len(pLEmps) < len(empKeyLet)):
        return str(), startList, usedList, lastList, 'fail-1', pLEmps
    elif len(pLEmps) == len(empKeyLet):
        if pLine[-1] not in allPunx:
            lastWord = pLine[-1]
        else:
            lastWord = pLine[-2]
        if (len(rhymeList) > 0):
            if (lastWord in rhymeList):
                for each in midPunx:
                    if each in proxP1[lastWord]:
                        pLine.append(each)
                        break
                if pLine[-1] not in midPunx:
                    for each in endPunx:
                        if each in proxP1[lastWord]:
                            pLine.append(each)
                            break
                pString, pLEmps, pLFono, pLVocs, pLCons = pLineToStringData(pLine, empKeyLet)
                for all in pLine:
                    if all not in allPunx:
                        usedList.append(all)
                lastList.append(pLine[-1])
                return pString, startList, usedList, lastList, 'pass', pLEmps
            else:
                runLine, pLine, pLEmps, pWord, pWEmps, pLineNum, pLineNList, proxNum, proxNumList, superPopList, expressList, blackList, firstPopList, jumpProxList = resetLine(pLine, pLEmps, pWord, pWEmps, superPopList, anteLine, rhymeList, blackList, firstPopList, jumpProxList)
                return str(), startList, usedList, lastList, 'fail-0', pLEmps
        else:
            for each in midPunx:
                if each in proxP1[lastWord]:
                    pLine.append(each)
                    break
            if pLine[-1] not in midPunx:
                for each in endPunx:
                    if each in proxP1[lastWord]:
                        pLine.append(each)
                        break
            pString, pLEmps, pLFono, pLVocs, pLCons = pLineToStringData(pLine, empKeyLet)
            for all in pLine:
                if (all not in allPunx) and (all not in quantumList):
                    usedList.append(all)
            lastList.append(pLine[-1])
            
            return pString, startList, usedList, lastList, 'pass', pLEmps
    else:
        runLine, pLine, pLEmps, pWord, pWEmps, pLineNum, pLineNList, proxNum, proxNumList, superPopList, expressList, blackList, firstPopList, jumpProxList = resetLine(pLine, pLEmps, pWord, pWEmps, superPopList, anteLine, rhymeList, blackList, firstPopList, jumpProxList)
        return str(), startList, usedList, lastList, 'fail-1', pLEmps
       

  # This function manages lines within a stanza

def runLiner(rhymeMap, empKey, usedList, emps, firstWords, startTimeM, startTimeH):
    lineNum, currentLine, eKCt, iCt = int(0), int(0), int(0), int(0)
    writtenLines, lineFound, metaBlackList, allLinesLine = [], [], [], []
    rhymeMapData, empKeyBits = {}, {}
    status = str()
    startList = firstWords
    while lineNum < len(rhymeMap):
        lCt = int(0)
        while str(str(rhymeMap[lineNum])+str(lCt)) in lineFound:
            lCt+=1
        rhymeMapData[lineNum] = str(str(rhymeMap[lineNum])+str(lCt))
        lineFound.append(str(rhymeMap[lineNum])+str(lCt))
        try:
            empKeyBits[rhymeMap[lineNum]]
            lineNum+=1
        except KeyError:
            empKeyBits[rhymeMap[lineNum]] = eKCt
            eKCt+=1
            lineNum+=1
            continue
    while len(writtenLines) < len(rhymeMap):
        stopTimeM = int(str(datetime.datetime.now())[14:16])
        stopTimeH = str(datetime.datetime.now())[11:13]
        if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and (startTimeM < (stopTimeM + 49))):
            startTimeM = int(str(datetime.datetime.now())[14:16])
            startTimeH = str(datetime.datetime.now())[11:13]
            usedList = []
            usedList = runLiner(rhymeMap, empKey, usedList, emps, firstWords, startTimeM, startTimeH)
            writtenLines = writtenLines[:len(rhymeMap)]
            status = 'done'
            break
        cLineData = rhymeMapData[currentLine]
        if len(writtenLines) > 0:
            anteLine = str(writtenLines[-1])
        else:
            anteLine = str()
        if cLineData[1] == '0':
            lastList = []
            oneString, startList, usedList, lastList, result, pLEmps = poemLiner([], empKey[int(empKeyBits[cLineData[0]])], anteLine, startList, usedList, lastList, proxMinDial, metaBlackList, allLinesLine, startTimeM, startTimeH)
        else:
            iCt = int(0)
            rhyPairLet = rhymeMapData[currentLine][0]
            rhymeList = []
            while iCt < len(writtenLines):
                if rhymeMapData[iCt][0] == rhyPairLet:
                    rhyString = writtenLines[iCt]
                    rhyLine, rhyEmps, rhyFono, rhyVocs, rhyCons = pStringToLineData(rhyString)
                    lastWordNum = int(-1)
                    while rhyLine[-1] in allPunx:
                        rhyLine.pop()
                    while lastWordNum > (-1000):
                        if str(rhyLine[lastWordNum]) in allPunx:
                            lastWordNum-=1
                        else:
                            rhyWord = str(rhyLine[lastWordNum])
                            break
                    lastList.append(rhyWord)
                    rhyWord = rhyWord.lower()
                    doubInt = int(0)
                    while rhyWord in doubles:
                        try:
                            rhyWord+='('+str(doubInt)+')'
                            emps[rhyWord]
                            for all in range(1, 11):
                                matchBox = dicWordLookup(rhyWord, all, min(all, len(emps[rhyWord])))
                                for each in matchBox:
                                    if each not in rhymeList:
                                        rhymeList.append(each)
                            doubInt+=1
                            rhyWord = rhyWord[:-3]
                        except KeyError:
                            rhyWord = rhyWord[:-3]
                            if len(rhymeList) == 0:
                                for all in range(1, 11):
                                    matchBox = dicWordLookup(rhyWord, all, min(all, len(emps[rhyWord])))
                                    for each in matchBox:
                                        rhymeList.append(each)                                 
                            break
                        
                    if rhyWord not in doubles:
                        for all in range(1, 11):
                            matchBox = dicWordLookup(rhyWord, all, min(all, len(emps[rhyWord])))
                            for each in matchBox:
                                rhymeList.append(each)
                            
                    for all in lastList:
                        if len(rhymeList) > 0:
                            if all in rhymeList:
                                rhymeList.remove(all)
                    rhyLinesInt = int(0)
                    for key, val in rhymeMapData.items():
                        if val[0] == cLineData[0]:
                            rhyLinesInt+=1
                    if len(rhymeList) >= (rhyLinesInt-1):
                        oneString, startList, usedList, lastList, result, pLEmps = poemLiner(rhymeList, empKey[int(empKeyBits[cLineData[0]])], anteLine, startList, usedList, lastList, proxMinDial, metaBlackList, allLinesLine, startTimeM, startTimeH)
                    else:
                        result = 'fail-1'
                iCt+=1
        if len(pLEmps) > 0:
            if pLEmps[0] == '2':
                result = 'fail-1'
        if len(oneString) == 0:
            result = 'fail-1'
        if result == 'pass':
            metaBlackList = []
            if (len(writtenLines)+1) == len(rhymeMap):
                if oneString[-1] in midPunx:
                    oneString = oneString[:-1]
                elif oneString[-1] not in endPunx:
                    oneString+='.'
            oneLine, oneEmps, oneThis, oneThat, oneVar = pStringToLineData(oneString)
            for each in oneLine:
                allLinesLine.append(each)
            writtenLines.append(oneString)
            currentLine+=1
        elif result == 'fail-0':
            currentLine = currentLine
        elif (result == 'fail-1') or (cLineData[1] == 0) or (len(rhymeList) <= rhyLinesInt):
            if len(writtenLines) > 0:
                minusLine, fuckThis, cuntLickers, thisVarIrrelevant, toothFairy = pStringToLineData(writtenLines.pop())
                for all in minusLine:
                    allLinesLine.pop()
                currentLine = len(writtenLines)
            else:
                currentLine = 0
                writtenLines = []
            metaBlackList = []
        elif cLineData[1] != 0:
            backInt = int(0)
            svCLInt = currentLine
            for key, val in rhymeMapData.items():
                if (str(cLineData[0]) == val[0]) and (cLineData[1] == ((int(val[1]))-1)):
                    metaBlackList = []
                    backInt = key
            allPopInt = int(0)
            lastPopInt = len(writtenLines) - (backInt+1)
            while allPopInt != lastPopInt:
                minusLine, mothersPie, tRex, neverLand, jackHammer = pStringToLineData(writtenLines.pop())
                for all in minusLine:
                    allLinesLine.pop()
                allPopInt+=1
            currentLine = backInt
            if backInt < (svCLInt-1):
                metaBlackList = []
            break

    writtenInt = int(0)
    if status != 'done':
        while writtenInt < len(rhymeMap):
            print(writtenLines[writtenInt])
            writtenInt+=1

    return usedList

# Here it goes. I have it set up to ignore all errors.

print('\nstarting remix')

usedList, lastList, metaBlackList = [], [], []
while rCt<poemCt:
    rCt+=1
    print('\n\nPoem #'+str(rCt)+'\n')##+str(datetime.datetime.now())+'\n')
    try:
        startTimeM = int(str(datetime.datetime.now())[14:16])
        startTimeH = str(datetime.datetime.now())[11:13]
        usedList = []
        usedList = runLiner(rhymeMap, empKey, usedList, emps, firstWords, startTimeM, startTimeH)
        usedList = ['']
        lastList, metaBlackList = [], []
    except:
        startTimeM = int(str(datetime.datetime.now())[14:16])
        startTimeH = str(datetime.datetime.now())[11:13]
        usedList = []
        usedList = runLiner(rhymeMap, empKey, usedList, emps, firstWords, startTimeM, startTimeH)
        usedList = ['']
        lastList, metaBlackList = [], []
        continue
    
print('\nremix complete')


## Copyright 2014, Christopher Shumaker aka Topher Qastro, All rights reserved.
