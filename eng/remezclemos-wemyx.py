

####

#   To-do list:
#   - ensure halfbeats are viable
#   - discriminate against capital words
#   - store unknown words into a file to be handled later
#   - create linemakers that don't follow meter

#  GLOSSARY

#  Three prefixes are used to distinguish the dual-layer lines. 
#  p - May be thought as the phonetic line, or the printed line. This is what will be shown as end-product
#  q - May be thought as the quantum line, because it enjoins both p and r lines in a sort of superposition to be analyzed separately and together
#  r - May be thought as the retracted or referral line, because it shows what the pLine says alternatively

#  qLine holds two lists. Most of the time, they're the same. They could split,
#  such as when contractions need to be separated, or if there's half-beats, etc.

#  qAnteLine = The line before the one currently being built, but not mutable so it could be reloaded
#  runLine = The line before the one building, but mutable so it can be cut and appended

#  qLineIndexList - Writes the index points for qLine. Starts at highest number (furthest right in sentence) and moves toward zero.
#  proxDicIndexList - Matches with qLineIndexList. Starts at 0 to find the immediate proxList for the furthest right, then the second-right gets index 1, etc.

#  superPopList = The 'list of lists' that holds words to be examined
#  superBlackList - The 'list of lists' that hold words whose paths have already been exhausted,
#      which is necessary to ensure a loop issue of trying and failing the same paths repeatedly

#  Organization of variables: empLine, qEmpLine, superPopList, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qWord, qLine, qAnteLine, redButton


##########
##  declaration of libraries
##########

from string import *
import tkinter as tk
import ___gloFunk as gF # Make sure to remove underscores later
import nltk
from nltk import wordnet as wn
import random
import datetime
import time
import csv
import inspect
import shelve
from collections import defaultdict
csv.field_size_limit(int(9999999))



##########
##  basic, essential, universal functions & lists
##########


def lineno():     ##  Returns the current line number in our program.
    return inspect.currentframe().f_back.f_lineno

unknownWords = open('data/unknownWords.txt', 'a')

quantumList = ['and', 'to', 'for', 'a', 'the', 'in', 'at', 'but']  #  List of words used for quantum emp patterns
nonEnders = ['and', 'or', 'a']

allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '"', "''", '-', '\\', '+', '=', '/', '<', '>', '(', ')']  #  Doesn't include apostrophe, because that could be part of a contraction
midPunx = [',', ';', ':', '--']
endPunx = ['.', '!', '?']  #  To gather which words immediately thereafter should start a sentence

bannedChops = ['@', '#', '&', '*', '\\', '+', '=', '/', '<', '>']


##########
##  text and library preparation
##########

def gpDataWriter(dicList, fileBit, textFile):

    ##  Writes grammar and proximity data to hard drive

    pFile = csv.writer(open('data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv', 'w+'))
    print(lineno(), 'building: data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv')
    #print(dicList)
    for key, val in dicList[0].items():
        #$ print(key)
        fullString = str()
        for each in dicList:
            dicString = str()
            for entr in each[key]:
                #4 print('gpData:', entr, )
                dicString = dicString+entr+'^'  #  Entries for each proxLib are separated by the '^'
            fullString = fullString+dicString[:-1]+'~'  #  Proxlibs are separated by '~'. proxPlusLista is saved in one file.
        for char in fullString:
            if char != '~':      # This is to screen for empty sets. If one char is not a tilde then it's non-empty.
                #$ print(lineno(), fileBit, 'writing:', key, fullString[:min(20, len(fullString))])
                pFile.writerow([key, fullString[:-1]])
                break


def loadmakeData(textFile, proxPlusLista, proxMinusLista):
    global firstWords, firstPopList
    firstWords, firstPopList = [], []
    try:
        print(lineno(), 'begin fwFile load') 
        firstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'r')
        for line in firstFile:
            firstWords.append(line[:-1])
            firstPopList.append(line[:-1])
        print(lineno(), 'begin prox load')        
        #  Take a look at gpDataOpener. Consider moving more code there, or bring some here
        proxPlusLista = gF.proxDataOpener(proxPlusLista, 'proxP', textFile)
        proxMinusLista = gF.proxDataOpener(proxMinusLista, 'proxM', textFile)
        print(lineno(), 'prox load complete')
            
    except FileNotFoundError:
        rawText = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())
        firstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
        rawText = rawText.replace('\n', ' ')  #  First clean up some meta-bits that inhibit text digestion
        rawText = rawText.replace('_', " ")
        rawText = rawText.replace('``', '"')
        rawText = rawText.replace("''", '"')
        rawText = rawText.replace('`', "'")
        rawText = rawText.replace('&', ' and ')
        for all in allPunx:  #  Put a space around punctuation to tokenize later
            rawText = rawText.replace(all, ' '+all+' ')
        rawText = rawText.replace("     ", ' ')  #  Makes 5 whitespace characters shrink into 1 in text
        rawText = rawText.replace("    ", ' ')  #  Makes 4 into 1
        rawText = rawText.replace("   ", ' ')  #  Makes 3 into 1
        rawText = rawText.replace("  ", ' ')  #  Then 2 to 1 for good measure, overall 120:1. Every significant token should still have one space between the adjacent
        rawText = rawText.lower()

        #  Tokenizes raw text, grooms into lists of words
        splitText = rawText.split(' ')  # The reason for placing a space between all tokens to be grabbed
        splitTIndex = int(0)
        splitTLen = len(splitText)
        proxMaxDial = 19
        #$ print(lineno(), 'begin loadmakeProxLibs()')
        #  Prox and gramprox store Markov chains and build in -Liner() functions
        #  Libs declared here, made into lists of dics of lists, and called using indices on     #  The maximum length of theseslists are truncated based on the user's initial input
        proxPlusLista = proxPlusLista[:proxMaxDial]
        proxMinusLista = proxMinusLista[:proxMaxDial]
        firstWords = []
        for all in range(0, (len(proxPlusLista))):  #  Now that we've got an exhaustive list of real words, we'll create empty lists for all of them (could this get pre-empted for common words?)
            for each in splitText:
                proxPlusLista[all][each] = []
                proxMinusLista[all][each] = []
        while splitTIndex < len(splitText):
            pWord = splitText[splitTIndex]
            proxNumerator, proxDicCounter, proxMax = int(1), int(0), len(proxPlusLista)
            if pWord in endPunx:
                firstWord = splitText[splitTIndex+1]
                if firstWord not in firstWords:
                    firstWords.append(firstWord)
                    firstFile.write(firstWord+'\n')
            while proxDicCounter < proxMax and splitTIndex+proxNumerator < splitTLen:
                proxWord = splitText[splitTIndex+proxNumerator]
                if proxWord not in proxPlusLista[proxDicCounter][pWord]:
                    #$ print(lineno(), 'plusadd = proxP:', proxWord, 'pWord:', pWord)
                    proxPlusLista[proxDicCounter][pWord].append(proxWord)
                if pWord not in proxMinusLista[proxDicCounter][proxWord]:
                    #4 print(lineno(), 'minusadd = proxM:', proxWord, 'pWord:', pWord)
                    proxMinusLista[proxDicCounter][proxWord].append(pWord)
                proxDicCounter+=1
                proxNumerator+=1
            splitTIndex+=1
        print(lineno(), 'writing proxLibs...')
        gpDataWriter(proxPlusLista, 'proxP', textFile)
        gpDataWriter(proxMinusLista, 'proxM', textFile)
  

def proxDataReboot(pLine):  # Recreates the proxData used in proxWords()
    pCt = int(0)
    proxNumList = []
    proxLineNumList = []
    while pCt < len(pLine):
        proxNumList.append(pCt)
        proxLineNumList.insert(0, pCt)
        pCt+=1
    pLNi = pCt
    return [proxLineNumList, pLNi, proxNumList]


def contractionAction(contraction, qLine):  #  Switches contractions between phonetic line and real/grammar line
    qLine[0]+=contraction
    qLine[1]+=contractionDic[contraction]


def rhymeGrab(pWord):
    theseRhymes = []
    print(lineno(), pWord, rhymes)
    try:
        rhymeList = rhyDic[pWord]
        return rhymeList
    except KeyError: # means we haven't looked it up yet
        #print(lineno(), 'kE')
        totalSyls = 1
        while totalSyls < 10:  #  Rhyming dictionary was only built up to 10 syllables
            theseSyls = rSyls
            if totalSyls < theseSyls:
                theseSyls = totalSyls
            rhyData = totalSyls, theseSyls
            if (rSyls <= totalSyls):
                print(lineno(), 'B')
                tName, rName = str(totalSyls), str(rSyls)  #  Turn into strings so we can open the file that we need            
                if totalSyls < 10:
                    tName = '0'+tName
                if rSyls < 10:
                    rName = '0'+rName
                try:
                    dicFile = csv.reader(open('data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))
                    for line in dicFile:
                        keyChain = line[0].split('^')
                        if pWord in keyChain:
                            theseRhymes = line[1].split('^')
                            for all in theseRhymes:
                                if all not in rhyDic[pWord]:
                                    rhyDic[pWord].append(all)
                except IOError:
                    print(lineno(), 'ioE: rhyDic', rhyData, 'not found')
                    return str()
                totalSyls+=1
        return rhyDic(pWord)


def removeWordL(superPopList, qLine):  #  Remove the leftmost word from line
    return data


def removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine):  #  Remove the rightmost word from line
    print(lineno(), 'removeWordR-in', qLine)
    if len(runLine[0]) > 0:  #  Cut runLine 
        minusWordX = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWordX = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
        minusWordX = qLine[0].pop(0)
        minusWordX = qLine[1].pop(0)
    minusWord0 = qLine[0].pop()  #  Remove word from first part of line
    minusWord1 = qLine[1].pop()  #  Until better method introduced, cut rLine here
    #  Some sort of contractionAction function should go here
    pWEmps = gF.empsLine([minusWord0], emps, doubles)
    pLEmps = pLEmps[:-len(pWEmps)]  #  Cut emps from main line
    qLineIndexList = qLineIndexList[1:]
    proxDicIndexList = proxDicIndexList[:-1]
    #superBlackList[-1].append(minusWord0)  #  To avoid a loop, prevent popList from checking branch again
    if len(superPopList) > (len(qLine[0]) + 1):  #  If we've gone further than checking the list of next words
        print(lineno(), 'rMR - snipPopList')
        superPopList = superPopList[:len(qLine[0]) + 1]
    print(lineno(), 'removeWordR-out', qLine)
    return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine


def acceptWordL(qLine, nextWord, qLineIndexList, proxDicIndexList):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    print('acceptWord:', qLine, '|', nextWord)
    pLine.append(nextWord)
    if len(proxNumList) > 0:
        proxNum = proxNumList[-1] + 1
    else:
        proxNum = 0
    proxNumList.append(proxNum)
    proxLineNum = proxLineNumList[0] + 1
    proxLineNumList.insert(0, proxLineNum)
    return qLineIndexList, proxDicIndexList, qLine


def acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, nextWord):  #  Add word to right side of line
    print('acceptWordR-in:', qLine, '|', nextWord, qLineIndexList, proxDicIndexList)
    qLine[0].append(nextWord[0])
    qLine[1].append(nextWord[1])
    qLineIndexList, proxDicIndexList = proxDataBuilder(qLine, len(qLine[0]))
    if len(superBlackList) == len(qLine[0]):  #  We don't have any blackListed words that far ahead
        superBlackList.append([])
    print('acceptWordR-out:', qLine, '|', nextWord, qLineIndexList, proxDicIndexList)
    return superBlackList, qLineIndexList, proxDicIndexList, qLine


def listSorter(mainList, frontList, rearList):  # places words in the front or back of a list
    switchList = []
    for all in allPunx:
        if all in mainList:  #  Place all punctuation into lowest priority (for now)
            rearList.append(all)
    for all in rearList:
        if all in mainList:
            switchList.append(all)
            mainList.remove(all)
    for all in switchList:
        mainList.append(all)
    switchList = []
    for all in frontList:  # if word is in both front and rear lists, goes to front
        if all in mainList:
            switchList.append(all)
            mainList.remove(all)
    for all in switchList:
        mainList.insert(all, 0)
    return mainList


def proxDataBuilder(qLine, limitNum):  #  Takes the qLine and builds proxData up to a certain length
    print(lineno(), 'proxDataBuilder |', qLine, limitNum)
    qLineLen = len(qLine[0])
    proxInt = int(0)  #  Starts the proxData
    qLineIndexList, proxDicIndexList = [], []
    while proxInt < len(qLine[0]) or proxInt < limitNum:  #  Creates a list of indexes and the reverse list to index proxDics
        proxDicIndexList.append(proxInt)
        qLineIndexList.insert(0, proxInt)
        proxInt+=1
    print(lineno(), qLineIndexList, proxDicIndexList)
    return qLineIndexList, proxDicIndexList


def superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, qAnteLine): #  Creates a list-of-lists to pull from
    print(lineno(), 'sPLM init')
    keepList = []  #  Will return empty set upon failure
    if len(superPopList) != len(qLine[0]) + 1:  #  If we don't have a proper amount to pop from
        print(lineno(), 'superPopMaker start |', len(superPopList), '|', qLine, 'proxData:', qLineIndexList, proxDicIndexList)
        # qLineIndexList: List of positions on the qLine
        # proxDicIndexList: List of positions for the qLine to find in proxDics
        if len(qLineIndexList) != len(qLine[0]):  #  Determines if it needs to revamp proxData
            print(lineno(), 'sPLM -> proxDB')
            qLineIndexList, proxDicIndexList = proxDataBuilder(qLine, len(qLine[0]))
        qLineLen = len(qLine[0])
        if qLineLen == 0:  #  If we've received a totally empty line, populate it with firstWords, but not directly or corrupt global bank
            print(lineno(), 'sPM - zeroLine')
            startList = firstWordSuperPopList(superBlackList)
            return startList, [[]], qLineIndexList, proxDicIndexList, qLine, qAnteLine
                  #superPopList, superBlackList, etc

        # use rWord here, make method for dealing with doubles
        print(lineno(), 'sPM - len(qLine) >= 1', qLineIndexList, proxDicIndexList)
        try:
            while len(qLineIndexList) > 0:
                keepList = proxP1[qLine[0][-1]]  #  Practically an 'else' clause, because the 'if' above returns an answer
                if len(qLineIndexList) > 1:  #  Only keep going if we need more than 2 words analyzed
                    for each in proxDicIndexList[1:]:  #  Skip first indexNum, we already found it
                        testList = proxPlusLista[each][qLine[0][qLineIndexList[each]]]  #  Scans approximate words with indexes
                        burnList = []  #  burnList holds words that don't match with mutual proxLists
                        #print(lineno(), qLine[0][qLineIndexList[each]], qLineIndexList[each], each, '\nkeepList:', keepList, '\ntestList:', testList)
                        for all in keepList:
                            if all not in testList or all in superBlackList[each+1]:  #  Add blackList screening later
                                burnList.append(all)  #  Screen it with a burnList so we don't delete as we iterate thru list
                        #print(lineno(), 'len(keepList):', len(keepList), 'len(burnList):', len(burnList))
                        if len(keepList) > 0:
                            for all in burnList:
                                keepList.remove(all)
                        else:  #  If we run out prematurely, stop iterating over the list
                            print(lineno(), 'sPLM keepList out')
                            break
                keepList = listSorter(keepList, expressList, [])
                if len(keepList) == 0:
                    qLineIndexList = qLineIndexList[:-1]
                    proxDicIndexList = proxDicIndexList[:-1]
                    print(lineno(), 'snipping proxData', qLineIndexList, proxDicIndexList)
                else:
                    print(lineno(), 'superPopMaker grown |', len(superPopList), '|', qLine, 'proxData:', qLineIndexList, proxDicIndexList)
                    break
        except KeyError:
            print(lineno(), 'kE:', qLine, 'len(superPopList):', len(superPopList))
            unknownWords.write(qLine[0][-1])
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            qLineIndexList, proxDicIndexList = proxDataBuilder(qLine, len(qLine[0]))
            return superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine
        #print(superPopList)
        #input('waiting...')
##    if len(keepList) > 0:
    print(lineno(), 'sPM - appendKeep', len(keepList))
    superPopList.append(keepList)  #  If we didn't find anything, append an empty set
    return superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine


def plainPopDigester():  #  Digests words from list without regard to their syllables or meter
    return doo, doo


def empPopDigester():  #  Digests words based on the length of their syllables
    return doo, doo


def metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine):  #  Digests words that fit a particular meter
    print(lineno(), 'metPopDigester start')
    expressList = []  #  Haven't gotten parameters up for this yet
    pLEmps = gF.empsLine(qLine[0], emps, doubles)  #  Using 'p' prefix because measuring 'phonetic'
    print(lineno(), 'mPD pLEmps:', pLEmps, qLine)
    if len(superPopList) == len(qLine[0]):
        print(lineno(), 'mPD-if sPL=qLine')
        superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(pLEmps, superPopList, superBlackList, [], qLineIndexList, proxDicIndexList, qLine, runLine)
    elif len(superPopList) < len(qLine[0]):
        print(lineno(), 'mPD not aligned:', "len(superPopList):", len(superPopList), "| len(superPopList[-1]):", len(superPopList[-1]), qLine)
    print(lineno(), "len(superPopList):", len(superPopList), "| len(superPopList[-1]):", len(superPopList[-1]))
    while len(superPopList[-1]) > 0:
        #print(lineno(), "len(superPopList[-1]):", len(superPopList[-1]))
        pWord = superPopList[-1].pop(0)  #  Used random in past, but organized lists put preferential stuff in front / superPopList[-1].index(random.choice(superPopList[-1]))
        pWEmps = gF.empsLine([pWord], emps, doubles)
        if len(pWEmps) != 0 and pWord not in allPunx:  #  Probably a KeyError:
            testEmps = pLEmps + pWEmps
            if len(testEmps) <= len(empLine):  #  This is to screen against an error
                #print(lineno(), 'mPD testEmp0')
                if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
                    #print(lineno(), 'mPD testEmp1')
                    if pWord in contractionList:
                        print(lineno(), 'mPD - if')
                        qWord = contractionAction(qLine[0], pWord, -1)  #  Adds a contraction to the
                        superBlackList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, qWord)
                        print(lineno(), 'mPD acceptR', qLine, testEmps)
                        return testEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
                    else:
                        print(lineno(), 'mPD - else')
                        qWord = (pWord, pWord)  #  pWord is the same word unless the phonetic data doesn't match the 'real' data
                        superBlackList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, qWord)
                        print(lineno(), 'mPD acceptR', qLine, testEmps)
                        return testEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
            else:
                print(lineno(), 'fuckt')
                testEmps = testEmps[:-len(pWEmps)]  #  The word extended the line too far, so subtract it
                # removeWordR??
    print(lineno(), "len(superPopList):", len(superPopList), "| len(superPopList[-1]):", len(superPopList[-1]))
    if len(qLine[0]) > 0: #and len(qLine[0]) > proxMinDial:  #  If we have enough words, then we can remove rightmost element and metadata, then try again
        print(lineno(), 'snipLine')
        pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
        pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
    print(lineno(), 'mPD end')
    return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
          #pLEmps, superPopList, qLineIndexList, proxDicIndexList, qLine
 
        
def firstWordSuperPopList(superBlackList):  #  Creates a superPopList that reloads the global firstWords list
    print(lineno(), 'firstWordSuperPopList start')
    superPopList = [[]]
    for all in firstWords:
        if all not in superBlackList[0]:
            superPopList[0].append(all)
    print(len(superPopList))
    return superPopList


def makeList(listA):  #  Simple function that appends all from one list to other, so they are not bound together
    [] = listB
    for all in listA:
        listB.append(all)
    return listB
        
    
##############
#  line building


def vetoLine(qAnteLine, superBlackList):  #  Resets values in a line to 
    print(lineno(), 'resetLine, qAnteLine:', qAnteLine)
    runLine = ([],[])
    for each in qAnteLine[0]:  #  Re-create any qAnteLinesuperPopList, superBlackList, qLine, qLineIndexList, proxDicIndexList as a mutable variable
        runLine[0].append(each)
    for each in qAnteLine[1]:  #  Re-create any qAnteLinesuperPopList, superBlackList, qLine, qLineIndexList, proxDicIndexList as a mutable variable
        runLine[1].append(each)
    superPopList = firstWordSuperPopList(superBlackList)
    return superPopList, superBlackList, [], [], [], ([],[]), runLine, False
          #superPopList, superBlackList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton


def plainLinerLtoR(vars):
    data
    # without rhyme or meter


def plainLinerRtoL(vars):
    data


def meterLiner(empLine, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine):  #  
    print(lineno(), 'meterLiner start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    pLEmps, superPopList, runLine = [], [[]], ([],[])
    for each in qAnteLine[0]:  #  qAnteLine gets appended to runLine because this function will be cutting from it when it doesn't yield results
        runLine[0].append(each)
    for each in qAnteLine[1]:
        runLine[1].append(each)
    while pLEmps != empLine:  #  Keep going until the line is finished or returns blank answer
        print(lineno(), 'empLine:', empLine, 'pLEmps:', len(pLEmps), pLEmps)
        if (len(runLine[0]) == 0) and (len(qLine[0]) == 0):  #  Check if we're starting with a completely empty line, load firstWords to superPopList if so
            print(lineno(), 'met if0')
            superPopList = firstWordSuperPopList(superBlackList) 
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            if len(superPopList[0]) == 0 and len(qLine[0]) == 0:
                print(lineno(), 'redButton == True')
                return superPopList, superBlackList, usedList, qLine, qAnteLine, True #  redButton event
        elif len(runLine[0]) > 0:  #  Checks before trying to manipulate qAnteLine just below, also loops it so it subtracts from anteLine first
            print(lineno(), 'met if1')
            for all in runLine[0]:  #  Add runLine to qLine to analyze continuing lines
                qLine[0].append(all)
            for all in runLine[1]:
                qLine[1].append(all)
            while len(superBlackList) <= len(qLine[0]):  #  Make sure superBlackList is long enough to add to w/ runLine
                superBlackList.append([])
            print(lineno(), 'runLine + qLine:', qLine)
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            qLine = (qLine[0][len(runLine[0]):], qLine[1][len(runLine[1]):])  #  Cut runLine out of qLine
##            qLine[1] = qLine[1][len(runLine[1]):]
            superBlackList = superBlackList[len(runLine[0]):]  #  Cut runLine back. The previous line doesn't need a blackList, we already found that a valid line
            print(lineno(), 'qLine - runLine:', qLine)
        elif len(qLine[0]) > 0:
            print(lineno(), 'met if2 qLine:', qLine, 'len(superBlackList):', len(superBlackList))
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            if len(superPopList[0]) == 0 and len(qLine[0]) == 0:  #  Nothing seems to work
                print(lineno(), 'met if2-if') 
                return superPopList, superBlackList, usedList, qLine, qAnteLine, True  #  redButton event, as nothing in the list worked
        else:  #  No runLine, no qLine, and superPopList[0] is out of firstWords
            print(lineno(), 'met if3')
            superPopList, superBlackList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton = vetoLine(qAnteLine, superBlackList)
            return [[]], superBlackList, usedList, qLine, qAnteLine, True
        pLEmps = gF.empsLine(qLine[0], emps, doubles)
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
    print(lineno(), 'meterLiner out:', qLine)
    return superPopList, superBlackList, usedList, qLine, qAnteLine, False
          #superPopList, qAnteLine, qLine, usedList, redButton
            

def rhymeLiner(empLine, qLineIndexList, proxDicIndexList, qAnteLine, ):
    print(lineno(), 'rhymeLiner start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    for all in rhymeList:
        expressList.append(all)
    superPopList, superBlackList, usedList, qLine, qAnteLine, redButton = meterLiner(empLine, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)  #  First, let it build a line, then if it doesn't happen to rhyme, send it back 
    while qLine[0][-1] not in rhymeList:  #  Unless we find a rhyme to escape this loop, it'll subtract the word every time it gets to the beginning of the loop
        for each in superPopList[-1]:  #  Let's see if there was a rhyme in our popList to add. If we don't return anything, it leaves this section like an moves on, like an implied "else"
            if each in rhymeList:  #  If there's a rhyme, then we can switch out the last word for that instead
                qLine = subtractWordR(qLine)
                qLine.append(each)
                return qLine  #  We've found a rhyming line, and we're done building
        if len(expressList) > 0:  # 
            while (len(qAnteLine[0]) > 0) and (len(qLine[0]) > 0):  #  Make sure there are both rhymes and non-empty lines, otherwise it's failed
                qLine = subtractWordL(qAnteLine)  #  Take away a word from the previous line's beginning, because this line didn't yield anything
                qLine = subtractWordR(qLine)  #  And take away the word that didn't work
            if len(expressList) > 0:  #  Use the expressList with rhyming words created at the beginning of this function
                superPopList, superBlackList, usedList, qLine, qAnteLine, redButton = meterLiner(empLine, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
        elif len(qLine[0]) > 0:  #  Subtract from 
            qLine = subtractWordR(qLine)
            superPopList, superBlackList, usedList, qLine, qAnteLine, redButton = meterLiner(empLine, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)  #  Here and below, meterLiner now has an expressList with the rhyming words, to increase their preference
        else:
            return qLine, usedList, True
    return qLine, usedList, False


def lineGovernor(qAnteLine, usedList, expressList, rhymeThisLine, rhymeList, empLine):
    print(lineno(), 'lineGovernor start', rhymeThisLine)
    superBlackList = [[]]  #  Even if the line is vetoed, record words that didn't work moving forward
    superPopList, superBlackList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton = vetoLine(qAnteLine, superBlackList)  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
    if rhymeThisLine == True:
        print(lineno(), rhymeThisLine)
        if (len(rhymeList) > 0):  #  This dictates whether stanzaGovernor sent a rhyming line. An empty line indicates metered-only, or else it would've been a nonzero population
            usedList, qLine, redButton = rhymeLiner(qAnteLine, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, empLine)
        else:
            print(lineno(), 'no rhymes')
            return [], ([],[]), True  #  usedList, qLine, redButton
    elif metSwitch == True:  #  If metSwitch is off, then we wouldn't have either rhyme or meter
        print(lineno(), 'lineGov - meterLiner activate')
        superPopList, superBlackList, usedList, qLine, qAnteLine, redButton = meterLiner(empLine, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
    else:
        print(lineno(), 'lineGov - plainLiner activate')
        usedList, qLine, redButton = plainLinerLtoR(qAnteLine, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, empLine)
    if redButton == True:
        print(lineno(), 'lineGov - redButton')
        superPopList, superBlackList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton = vetoLine(qAnteLine, superBlackList)
        return [], [], True
    else:
        return usedList, qLine, False  #  usedList, qLine, redButton
            


################
#  poem building


def vetoStanza(usedList):
    return [], ([],[]), [], int(0), False, False
          #stanza, qAnteLine, usedList, lineCt, redButton


def stanzaGovernor(usedList):
    print(lineno(), 'stanzaGovernor begin len(rhyMap):', len(rhyMap), 'len(empMap):', len(empMap))
    expressList = []  #  A list of words that go to the front of the line. Declared and left empty, for now
    stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
    while lineCt < len(rhyMap):
        if rhySwitch == True:
            anteRhyme = rhyMap.index(rhyMap[lineCt])  #  Use the length of the stanza with rhyMap to determine if a previous line should be rhymed with the current
            print(lineno(), 'stanzaGov -', anteRhyme, lineCt)
            if anteRhyme < lineCt:  #  If you hit a matching letter that comes before current line, grab rhys from that line. Otherwise, go straight to forming a metered line
                rhymeLine = stanza[anteRhyme]
                lastWordIndex = int(0)
                while rhymeLine[lastWordIndex] in punx:  #  Start from the end and bypass all punctuation
                    try:
                        lastWordIndex-=1
                        rhymeWord = rhymeLine[lastWordIndex]
                    except IndexError:
                        print(lineno(), "iE:", rhymeLine, lastWordIndex)
                        return  [], [], True  #  redButton event
                rhymeList = rhymeGrab(rhymeWord)
                rhymeThisLine = True
                if len(rhymeList) > 0:  #  Ensure that this produced some rhymes
                    print(lineno(), 'stanzaGov - rhymer')
                    usedList, newLine, redButton = lineGovernor(qAnteLine, usedList, expressList, rhymeThisLine, rhymeList, empMap[lineCt])  #  If so, we try to create rhyming lines
                else:  #  Our lines created nothing, so we hit a redbutton event
                    return [], [], True
            else:  #  Then you don't need rhymes
                rhymeList = []
                print(lineno(), 'stanzaGov -', qAnteLine, usedList, expressList, False, rhymeList, empMap[lineCt])
                usedList, newLine, redButton = lineGovernor(qAnteLine, usedList, expressList, False, rhymeList, empMap[lineCt])  #                
        elif metSwitch == False:
            usedList, newLine, redButton = plainLinerLtoR(qAnteLine, usedList, expressList, rhymeList, empMap[lineCt])
        else:
            print(lineno(), 'stanzaGov - lineGov')
            usedList, newLine, redButton = lineGovernor(qAnteLine, usedList, expressList, rhymeThisLine, [], empMap[lineCt])
        if redButton == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            print(lineno(), 'stanzaGov - redButton')
            stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])
        elif len(newLine) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the stanza with empty list
            print(lineno(), 'stanzaGov - newLine:', newLine) 
            stanza.append(newLine)
            qAnteLine = ([],[])  #  Rebuild qAnteLine, meant to direct the proceeding line(s)
            if len(stanza) > 0:
                for each in stanza[-1][0]:
                    qAnteLine[0].append(each)
                for each in stanza[-1][1]:
                    qAnteLine[1].append(each)
        elif len(stanza) > 0:  #  Check if the stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            stanza = stanza[:-1]
        else:  #  Redundant, as the stanza should logically be vetoed already, but just to clean house
            print(lineno(), 'stanzaGov - vetoStanza')
            stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])
        lineCt = len(stanza)  #  Count the length of the stanza, provided no redButton events occurred...

    return stanza, usedList, redButton


############0####
#  poem building


def vetoPoem():
    return [], [], 0, False
          #poem, usedList, stanzaCt, redButton


def poemGovernor(usedList):  #  Outlines the parameters of the poem
    print(lineno(), 'poemGovernor initialized\n'+str(datetime.datetime.now())+'\n')
    print(rhyMap, '+', empMap, '+', usedList)
    poem, usedList, stanzaCt, redButton = vetoPoem()
    while len(poem) < stanzaQuota:
        stanza, usedList, redButton = stanzaGovernor(usedList)
        if usedSwitch == 1: 
            usedList = ['']
        if redButton == True:
            usedList, lastList, stanzaCt = vetoPoem()
        elif len(stanza) == 0 and len(poem) > 0:
            poem = poem[:-1]
        else:        
            poem.append(stanza)
        if len(poem) == stanzaQuota:
            return poem, usedList
        


################
#  MAIN SECTION


def main__init():

    print(lineno(), 'initializing program')

    #########################
    #  Static data, will change with GUI and testVals progs

##    values = guiInterface()
    global rhyDic
    rhyDic = {}

    global poemQuota, stanzaQuota    
    poemQuota = 20
    stanzaQuota = 4
     
    textFile = 'shkspr'
    rawText = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())

    global proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20
    global proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20
    global proxPlusLista, proxMinusLista, proxLib # gramProxLib, gramProxPlusLista, gramProxMinusLista
    #  These dictionaries contain lists of words that come after 
    proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} 
    proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
    #  The dictionaries are organized into lists that are accessed by index. Useful in while loops with ascending/descending numbers
    proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20]
    proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20]

    global proxMinDial, proxMaxDial, punxProxNum
    proxMinDial = int(3)
    proxMaxDial = int(20)
    punxProxNum = int(3)

    stanza, usedList = [], []

    global rhyMap, empMap
    rhyMap = 'abcd'
    empMap = [[bool(1), bool(0), bool(1), bool(0), bool(1), bool(0), bool(1), bool(0), bool(1), bool(0)],
              [bool(1), bool(0), bool(1), bool(0), bool(1), bool(0), bool(1), bool(0), bool(1), bool(0)],
              [bool(1), bool(0), bool(0), bool(1), bool(0), bool(0), bool(1), bool(0)],
              [bool(1), bool(0), bool(0), bool(1), bool(0), bool(0), bool(1), bool(0)]]

    empMode = 0

    contractionFile = open('data/USen/contractionList.txt', 'r')
    contractionSwitch = csv.reader(open('data/USen/contractionSwitches.csv', 'r+'))
    global contractionDic, contractionList  #  These are immutable and should be accessed wherever
    contractionDic = {}  #  Use a dictionary to look up contraction switches
    contractionList = []  #  Use a list to check if the contraction exists (circumvents excepting KeyErrors)
    for line in contractionFile:  #  Makes a dictionary of contractions
        contractionList.append(line)
    for line in contractionSwitch:
        contractionDic[line[0]] = line[1] 
        
        

    rSyls = 2

    global usedSwitch, rhySwitch, metSwitch, thesSwitch
    usedSwitch = False
    rhySwitch = True
    metSwitch = True
    thesSwitch = False
    
    #
    ##########################


    print('opening fonoFiles')  #  These are global values, so they need to be opened regardless
    global emps
    emps = gF.globalOpen('data/USen/empDic-USen-unik.csv', 'lista')
    for key, val in emps.items():  #  Stored as ints because could be numbers up to 2. Change to bools
        boolSwitch = []
        for each in val:
            if each == '1':
                boolSwitch.append(bool(True))
            else:
                boolSwitch.append(bool(False))
        emps[key] = boolSwitch
    vocs = gF.globalOpen('data/USen/vocDic-USen-MAS.csv', 'lista')
    cons = gF.globalOpen('data/USen/conDic-USen-MAS.csv', 'lista')
    fono = gF.globalOpen('data/USen/fonDic-USen-MAS.csv', 'lista')
    
    # if rhySwitch == on, load rhyming dictionary here
    # write it in __gloFunk
    
    print(lineno(), 'len(emps):', len(emps))
    print(lineno(), 'opening doubles')
    global doubles
    doubles = []
    for key, val in emps.items():
        if '(' in key:
            doubles.append(key[:-3])
    print(lineno(), "rhySwitch =", rhySwitch)
    loadmakeData(textFile, proxPlusLista, proxMinusLista)  #  Loads the data needed or makes it
    poemCt = int(0)
    while poemCt < poemQuota:
        poem, usedList = poemGovernor(stanzaQuota)
        poemCt+=1
        print('Poem #'+str(poemCt))
        for each in poem:
            print(each+'\n')

    input(lineno(), 'PROGRAM FINISHED')

main__init() #  and now that everything's in place, set it off!

##  END
