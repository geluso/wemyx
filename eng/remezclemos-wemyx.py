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
import time
import sys
from collections import defaultdict
csv.field_size_limit(int(9999999))

# util is our own self-made file, "util.py"
from util import print_progress_bar



##########
##  basic, essential, universal functions & lists
##########

# trying to build up global configurable logging function,
# but I'm not convinced it's actually so useful
global LOGGING
LOGGING = True

# log(1)
# log(1, 2)
# log(1, "ace", ["bar", "car"], "fffaar")
def log(*args):
    if LOGGING:
        print(*args)

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
        filepath = 'data/textLibrary/textData/'+textFile+'-firstFile.txt'
        print(lineno(), 'begin fwFile load', filepath)
        firstFile = open(filepath, 'r')
        for line in firstFile:
            firstWords.append(line[:-1])
            firstPopList.append(line[:-1])
        print(lineno(), 'begin prox load')
        #  Take a look at gpDataOpener. Consider moving more code there, or bring some here
        print(lineno(), 'begin prox load proxP')
        proxPlusLista = gF.proxDataOpener(proxPlusLista, 'proxP', textFile)
        print(lineno(), 'begin prox load proxM')
        proxMinusLista = gF.proxDataOpener(proxMinusLista, 'proxM', textFile)
        print(lineno(), 'prox load complete')
            
    except FileNotFoundError:
        print(lineno(), "error reading:", textFile)
        raw_filepath = 'data/textLibrary/'+textFile+'.txt'
        output_filepath = 'data/textLibrary/textData/'+textFile+'-firstFile.txt'
        
        print(lineno(), "reading:", raw_filepath)
        print(lineno(), "creating:", output_filepath)
        
        rawText = str(open(raw_filepath, 'r', encoding='latin-1').read())
        firstFile = open(output_filepath, 'w+')
        
        def measure_time_taken_to_replace_chars(rawText, char, replacement):
            start = time.time()
            # commented out print statements because I found these replacements
            # are all actually very, very fast!
            #print("replacing", char, "with", replacement)
            #  First clean up some meta-bits that inhibit text digestion
            rawText = rawText.replace(char, replacement)
            end = time.time()
            #print("took", end - start)
            return rawText
        
        start = time.time()
        rawText = measure_time_taken_to_replace_chars(rawText, '\n', ' ')
        rawText = measure_time_taken_to_replace_chars(rawText, '_', " ")
        rawText = measure_time_taken_to_replace_chars(rawText, '``', '"')
        rawText = measure_time_taken_to_replace_chars(rawText, "''", '"')
        rawText = measure_time_taken_to_replace_chars(rawText, '`', "'")
        rawText = measure_time_taken_to_replace_chars(rawText, '&', ' and ')
        
        for all in allPunx:  #  Put a space around punctuation to tokenize later
            rawText = rawText.replace(all, ' '+all+' ')
        rawText = rawText.replace("     ", ' ')  #  Makes 5 whitespace characters shrink into 1 in text
        rawText = rawText.replace("    ", ' ')  #  Makes 4 into 1
        rawText = rawText.replace("   ", ' ')  #  Makes 3 into 1
        rawText = rawText.replace("  ", ' ')  #  Then 2 to 1 for good measure, overall 120:1. Every significant token should still have one space between the adjacent
        rawText = rawText.lower()

        end = time.time()
        print("total text processing time:", end - start)
        
        #  Tokenizes raw text, grooms into lists of words
        print("splitting text into list of words")
        splitText = rawText.split(' ')  # The reason for placing a space between all tokens to be grabbed
        splitTIndex = int(0)
        splitTLen = len(splitText)
        proxMaxDial = 19
        #$ print(lineno(), 'begin loadmakeProxLibs()')
        #  Prox and gramprox store Markov chains and build in -Liner() functions
        #  Libs declared here, made into lists of dics of lists, and called using indices on
        #  The maximum length of theseslists are truncated based on the user's initial input
        proxPlusLista = proxPlusLista[:proxMaxDial]
        proxMinusLista = proxMinusLista[:proxMaxDial]
        firstWords = []
        
        # Now that we've got an exhaustive list of real words, we'll create
        # empty lists for all of them (could this get pre-empted for common words?)
        print("creating empty lists for each word")
        for all in range(0, (len(proxPlusLista))):
            for each in splitText:
                proxPlusLista[all][each] = []
                proxMinusLista[all][each] = []
                
        # sample generated data
        # ['', 'the~old~testament~genesis~in~the~beginning~god~created~the~heavens~and~the~earth~.~now~the~earth~was']
        start = time.time()
        print("while loop processing")
        start2 = None
        
        start = time.time()
        next_words = defaultdict(lambda: defaultdict(list))
        while splitTIndex < len(splitText):
            break
            if splitTIndex % 10000 == 0:
                print(splitTIndex / len(splitText))
            word = splitText[splitTIndex]
            
            # keep track of words that begin sentences
            if word in endPunx:
                if splitTIndex + 1 < len(splitText):
                    first_word = splitText[splitTIndex + 1]
                    if first_word not in firstWords:
                        firstWords.append(first_word)
                        firstFile.write(first_word+'\n')
                
            for proximity_index in range(1, len(proxPlusLista)):
                next_word_index = splitTIndex + proximity_index
                if next_word_index < len(splitText):
                    next_word = splitText[next_word_index]
                    next_words[word][proximity_index].append(next_word)
                        
            splitTIndex += 1
        print("simple tally took:", time.time() - start)
        
        while splitTIndex < len(splitText):
            #sys.stdout.write(f"\rwhile splitTIndex < len(splitText) {splitTIndex} {len(splitText)}")
            #sys.stdout.flush()
            print_progress_bar(splitTIndex, len(splitText) - 1)
            
            # pWord: the word we're currently building up patterns for
            # proxMax: the maximum proximity to look after the current word
            pWord = splitText[splitTIndex]
            proxNumerator, proxDicCounter, proxMax = int(1), int(0), len(proxPlusLista)
            
            # detect end of sentences and add the next word
            # to a list of starting words
            if pWord in endPunx:
                firstWord = splitText[splitTIndex+1]
                if firstWord not in firstWords:
                    firstWords.append(firstWord)
                    firstFile.write(firstWord+'\n')
                    
            # while we're looking at words within the specified proximity
            # and while the words we're looking at don't extend past the end of
            # the total corpus text word list.
            while proxDicCounter < proxMax and splitTIndex+proxNumerator < splitTLen:
                # one of the words occuring after the pWord
                proxWord = splitText[splitTIndex+proxNumerator]
                #if proxWord not in proxPlusLista[proxDicCounter][pWord]:
                    #$ print(lineno(), 'plusadd = proxP:', proxWord, 'pWord:', pWord)
                proxPlusLista[proxDicCounter][pWord].append(proxWord)
                #if pWord not in proxMinusLista[proxDicCounter][proxWord]:
                    #4 print(lineno(), 'minusadd = proxM:', proxWord, 'pWord:', pWord)
                proxMinusLista[proxDicCounter][proxWord].append(pWord)
                proxDicCounter+=1
                proxNumerator+=1
            splitTIndex+=1
        end = time.time()
        # usually takes ~6 minutes to generate the file the first time
        print("while loop stuff took:", end - start)
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
    
    if len(qLine[0]) == 0 and len(runLine[0]) > 0:  #  Cut runLine
        minusWordX = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWordX = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
##        minusWordX = qLine[0].pop(0)
##        minusWordX = qLine[1].pop(0)
    if len(qLine[0]) > 0:
        minusWord0 = qLine[0].pop()  #  Remove word from first part of line
        minusWord1 = qLine[1].pop()  #  Until better method introduced, cut rLine here
        #  Some sort of contractionAction function should go here
        pWEmps = gF.empsLine([minusWord0], emps, doubles)
        pLEmps = pLEmps[:-len(pWEmps)]  #  Cut emps from main line
        qLineIndexList = qLineIndexList[1:]
        proxDicIndexList = proxDicIndexList[:-1]
        superBlackList[len(qLine[0])].append(minusWord0)  #  Add to blackList
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
##    for all in frontList:
##        switchList.append(all)
##    for all in mainList:
##        if all not in frontList and all not in rearList:
##            switchList.append(all)
##    for all in allPunx:
##        if all in mainList:  #  Place all punctuation into lowest priority (for now)
##            rearList.append(all)
##    for all in rearList:
##        if all not in frontList and all not in mainList:
##            switchList.append(all)
    for all in allPunx:
        if all in mainList:
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


def superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, runLine): #  Creates a list-of-lists to pull from
    print(lineno(), 'sPLM init')
    keepList = []  #  Will return empty set upon failure
    testLine = ([],[])
    if len(runLine[0]) > 0:  #  If there's a previous line, add it into testLine
        for each in runLine[0]:
            testLine[0].append(each)
        for each in runLine[1]:
            testLine[1].append(each)
    for each in qLine[0]:
        testLine[0].append(each)
    for each in qLine[1]:
        testLine[1].append(each)
    print(lineno(), 'superPopMaker start |', len(superPopList), '|', testLine, 'proxData:', qLineIndexList, proxDicIndexList)
    # qLineIndexList: List of positions on the qLine
    # proxDicIndexList: List of positions for the qLine to find in proxDics
##    if len(qLineIndexList) != len(testLine[0]):  #  Determines if it needs to revamp proxData
##        print(lineno(), 'sPLM -> proxDB')
    qLineIndexList, proxDicIndexList = proxDataBuilder(testLine, len(testLine[0]))  #  Refresh proxData
    testLineLen = len(testLine[0])
    if testLineLen == 0:  #  If we've received a totally empty line, populate it with firstWords, but not directly or corrupt global bank
        print(lineno(), 'sPM - zeroLine')
        startList = firstWordSuperPopList(superBlackList)
        return startList, [[]], qLineIndexList, proxDicIndexList, qLine, runLine
              #superPopList, superBlackList, etc

    # use rWord here, make method for dealing with doubles
    print(lineno(), 'sPM - len(testLine) >= 1', qLineIndexList, proxDicIndexList)
    try:
        while len(qLineIndexList) > 0:
            for all in proxP1[testLine[0][-1]]:
                keepList.append(all)  #  Practically an 'else' clause, because the 'if' above returns an answer
            if len(qLineIndexList) > 1:  #  Only keep going if we need more than 2 words analyzed
                for each in proxDicIndexList[1:]:  #  Skip first indexNum, we already found it
                    testList = proxPlusLista[each][testLine[0][qLineIndexList[each]]]  #  Scans approximate words with indexes
                    burnList = []  #  burnList holds words that don't match with mutual proxLists
                    testString = str()  #  Look for that same string in the rawText
                    #print(lineno(), each, len(superBlackList))
                    #print(lineno(), superBlackList[qLineIndexList[0]-len(runLine[0])])
                    #qLineIndexLen = len(qLineIndexList)  #  Use this to rebuild testString without words that have failed
                    for all in qLineIndexList:  #  Build a line with words already used
                        testString = testLine[0][all]+' '+testString  #  Build backwards because we trim failed lines from the front
                    for all in allPunx:
                        testString = testString.replace(' '+all, all)  #  Get rid of whitespace characters in front of puncuation
                    for all in keepList:
                        if all not in allPunx:
                            testString+=all+' '  #  Add the new word to the string, plus a space so we don't see a false positive with a partial word ('you' mistaken for 'your')
                        else:
                            testString = testString[:-1]+all+' '  #  Shave off a whitespace character because puncuation is attached
                        #print(lineno(),  testString)
                        if (all not in testList) or (testString not in rawText) or (all in superBlackList[len(qLine[0])]):  #  Add blackList screening later
                            burnList.append(all)  #  Screen it with a burnList so we don't delete as we iterate thru list
                        if all in allPunx:  #  Add whitespace character if not puncuation, because we subtracted one earlier
                            testString = testString[:-2]+' '
                        else:
                            testString = testString[:-(len(all)+1)]  #  Remove the word to prepare for another testString addition
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
                print(lineno(), 'superPopMaker grown |', len(superPopList), '|', testLine, 'proxData:', qLineIndexList, proxDicIndexList)
                break
    except KeyError:
        print(lineno(), 'kE:', testLine, 'len(superPopList):', len(superPopList))
        unknownWords.write(testLine[0][-1])
        pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
        #qLineIndexList, proxDicIndexList = proxDataBuilder(qLine, len(qLine[0]))
        return superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
    #print(superPopList)
    #input('waiting...')
##    if len(keepList) > 0:
    print(lineno(), 'sPM - appendKeep', len(keepList))
    if len(superPopList) != len(testLine[0]) + 1:  #  If we don't have a proper amount to pop from
        superPopList.append([])
    for all in keepList:
        superPopList[len(qLine[0])].append(all)  #  If we didn't find anything, append an empty set
    return superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine


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
        print(lineno(), 'mPD not aligned:', "len(superPopList):", len(superPopList), "| len(superPopList[len(qLine[0])]):", len(superPopList[len(qLine[0])]), qLine)
    print(lineno(), "len(superPopList):", len(superPopList), "| len(superPopList[len(qLine[0])]):", len(superPopList[len(qLine[0])]), 'qLine:', qLine)
    while len(superPopList[len(qLine[0])]) > 0:
        print(lineno(), "len(superPopList[len(qLine[0])]):", len(superPopList[len(qLine[0])]))
        pWord = superPopList[len(qLine[0])].pop(0)  #  Used random in past, but organized lists put preferential stuff in front / superPopList[-1].index(random.choice(superPopList[-1]))
        pWEmps = gF.empsLine([pWord], emps, doubles)
        if len(pWEmps) != 0 and pWord not in allPunx:  #  Probably a KeyError:
            testEmps = pLEmps + pWEmps
            if len(testEmps) <= len(empLine):  #  This is to screen against an error
                print(lineno(), 'mPD testEmp0 |', pWord)
                if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
                    print(lineno(), 'mPD testEmp1')
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
                pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
        elif (pWord in allPunx) and (len(qLine[0]) > 0):
            for all in allPunx:
                print(lineno(), all, qLine[0][-(min(punxProxNum, len(qLine[0]))):])
                if pWord in allPunx and all not in qLine[0][-(min(punxProxNum, len(qLine[0]))):]:  #  Will discriminate any puncuation within the designated length away
                    superBlackList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, (pWord, pWord))
                    print(lineno(), 'mPD acceptR', qLine, pLEmps)
                    return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
    print(lineno(), "len(superPopList):", len(superPopList), "| len(superPopList[-1]):", len(superPopList[-1]), 'qLine:', qLine)
    if len(qLine[0]) > 0 or len(runLine[0]) > 0: #and len(qLine[0]) > proxMinDial:  #  If we have enough words, then we can remove rightmost element and metadata, then try again
        try:
            print(lineno(), 'snipLine', qLine, '|', runLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(pLEmps, superPopList, superBlackList, [], qLineIndexList, proxDicIndexList, qLine, runLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
        except RuntimeError:
            return [], [[]], [[]], [], [], ([],[]), ([],[])  #  redButton situation
    else:
        print(lineno(), 'no qLine or runLine')
        return [], [[]], [[]], [], [], ([],[]), ([],[])  #  redButton situation
    print(lineno(), 'mPD end')
    return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
          #pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine
 
        
def firstWordSuperPopList(superBlackList):  #  Creates a superPopList that reloads the global firstWords list
    print(lineno(), 'firstWordSuperPopList start')
    superPopList = [[]]
    for all in firstWords:
        if all not in superBlackList[0]:
            superPopList[0].append(all)
    print(lineno(), len(superPopList))
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
##            for all in runLine[0]:  #  Add runLine to qLine to analyze continuing lines
##                qLine[0].append(all)
##            for all in runLine[1]:
##                qLine[1].append(all)
            while len(superBlackList) <= len(qLine[0]):  #  Make sure superBlackList is long enough to add to w/ runLine
                superBlackList.append([])
            print(lineno(), 'runLine + qLine:', qLine, ', superBlackList:', len(superBlackList))
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, runLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
##            qLine = (qLine[0][len(runLine[0]):], qLine[1][len(runLine[1]):])  #  Cut runLine out of qLine
##            qLine[1] = qLine[1][len(runLine[1]):]
##            superBlackList = superBlackList[len(runLine[0]):]  #  Cut runLine back. The previous line doesn't need a blackList, we already found that a valid line
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
        print(lineno(), 'end of meterLiner while')
        if len(qLine[0]) > 0:  #  Make sure there's a line to analyze
            print(lineno(), 'metLiner if out')
            pLEmps = gF.empsLine(qLine[0], emps, doubles)
        elif len(runLine[0]) == 0:  #  If runLine is also out, redButton
            print(lineno(), 'metLiner elif out')
            return [[]], superBlackList, usedList, qLine, qAnteLine, False
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            (lineno(), 'meterLiner over emps')
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


def lineGovernor(superBlackList, qAnteLine, usedList, expressList, rhymeThisLine, rhymeList, empLine):
    print(lineno(), 'lineGovernor start', rhymeThisLine)
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


def removeLine(stanza, superBlackList):
    print(lineno(), 'removeLine in | len(stanza):', len(stanza))
    stanzaSnip = stanza.pop()  #  Remove the last line of the stanza
    superBlackList[0].append(stanzaSnip[0][0])  #  Add the first word of the line to blacklist to ensure the repeat doesn't happen
    print(lineno(), 'removeLine', stanzaSnip, len(superBlackList))
    qAnteLine = ([],[])  #  Rebuild qAnteLine, meant to direct the proceeding line(s). Returns empty if stanza empty
    if len(stanza) > 1:
        for each in stanza[-1][0]:
            qAnteLine[0].append(each)
        for each in stanza[-1][1]:
            qAnteLine[1].append(each)
    print(lineno(), 'removeLine out | len(stanza):', len(stanza))
    return stanza, superBlackList, qAnteLine


def acceptLine(stanza, newLine):
    print(lineno(), 'acceptLine in | len(stanza):', len(stanza))
    stanza.append(newLine)
    print(lineno(), 'acceptLine in | len(stanza):', len(stanza))
    return stanza, newLine
          #stanza, qAnteLine


def stanzaGovernor(usedList):
    print(lineno(), 'stanzaGovernor begin len(rhyMap):', len(rhyMap), 'len(empMap):', len(empMap))
    expressList = []  #  A list of words that go to the front of the line. Declared and left empty, for now
    superBlackList = [[]]  #  Must be declared separate from vetoStanza because it starts empty but may hold screened words
    stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
    while lineCt < len(rhyMap):
        if rhySwitch == True:
            anteRhyme = rhyMap.index(rhyMap[lineCt])  #  Use the length of the stanza with rhyMap to determine if a previous line should be rhymed with the current
            print(lineno(), 'stanzaGov -', anteRhyme, lineCt)
            for each in stanza:
                print(each)
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
                    usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, expressList, rhymeThisLine, rhymeList, empMap[lineCt])  #  If so, we try to create rhyming lines
                else:  #  Our lines created nothing, so we hit a redbutton event
                    return [], [], True
            else:  #  Then you don't need rhymes
                rhymeList = []
                print(lineno(), 'stanzaGov -', qAnteLine, usedList, expressList, False, rhymeList, empMap[lineCt])
                usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, expressList, False, rhymeList, empMap[lineCt])  #
        elif metSwitch == False:
            usedList, newLine, redButton = plainLinerLtoR(qAnteLine, usedList, expressList, rhymeList, empMap[lineCt])
        else:
            print(lineno(), 'stanzaGov - lineGov')
            superBlackList, usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, expressList, rhymeThisLine, [], empMap[lineCt])
        if redButton == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            print(lineno(), 'stanzaGov - redButton')
            stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
        elif len(newLine[0]) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the stanza with empty list
            print(lineno(), 'stanzaGov - newLine:', newLine)
            stanza, qAnteLine = acceptLine(stanza, newLine)
        elif len(stanza) > 0:  #  Check if the stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            stanza, superBlackList, qAnteLine = removeLine(stanza, superBlackList)
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
        print(lineno(), 'gotStanza\n')
        for each in stanza:
            thisString = str()
            for all in each[0]:
                thisString= thisString+' '+all
            for all in allPunx:
                if ' '+all in thisString:
                    thisString.replace(' '+all, all)
            print(thisString)
        input('press enter to continue')
        print('\n')
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
    rhyDic = defaultdict(list)

    global poemQuota, stanzaQuota
    poemQuota = 20
    stanzaQuota = 4
     
    textFile = 'bibleZ'
    global rawText
    rawText = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())

    global proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20
    global proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20
    global proxPlusLista, proxMinusLista, proxLib # gramProxLib, gramProxPlusLista, gramProxMinusLista
    #  These dictionaries contain lists of words that come after
    proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
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
    contractionDic = defaultdict(list)  #  Use a dictionary to look up contraction switches
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
            print(each, '\n')

    input(lineno(), 'PROGRAM FINISHED')

main__init() #  and now that everything's in place, set it off!

##  END
