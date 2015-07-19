 
##  It starts with a word. Then it scans a list of possible following words based on
##  their postion to other words and grammar of the author.
##  If one of these words is accepted, it places that word in a line. It builds thereon.
##  If it exhausts the list, then it moves back. If nothing works, it restarts.
##  To allow more fluidity, the program reads the line in two ways: by meaning, and by
##  poesy. It utilizes a thesaurus to change a word with the same meaning to one that
##  fits with the phonetics of the poem.

##  The variables p, q, and r are common for logic. In this program, the 'variable line'
##  utilizes these characters as prefixes, and their application within the function is:
##  p: The "phonetics" variable, also our end product
##  q: The "quantum" variable, a paired list of matching 'p' and 'r' variables (eg qWord = pWord, rWord)
##  r: The "real" variable, used to anchor grammar and meaning, perhaps "relationship" to 'p'
##  They manifest as pWord, qList, rAnteString, and so on.



from string import *
from tkinter import *
import ___gloFunk as gF # Make sure to remove underscores later
import nltk
from nltk import wordnet as wn
import random
import datetime
import time
import csv
csv.field_size_limit(int(9999999))


 # Here's where I declare some useful lists and clean the text
 # for easier processing

alphabet = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
empsList = -1, 0, 1, 2

posTags = 'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '.', ',', ';', ':', '!', '?', '"', "'"
dynaPOS = 'N', 'V', 'W', 'R'
quantumTags = 'CC', 'DT', 'WRB', 'WP', 'WP$', 'PRP', 'PRP$', 'TO', 'IN'
quantumList = []

punxTags = ['"', "'", "''", ':']
allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '``', '`', '"', "''"]
midPunx = [',', ';', ',', ':', '--']
endPunx = ['.', '!', '?']
punx = [',', ';', ',', ':', '--', '"', '-', "''", "''", "''"]
badGrams = ['``', '"', "''", '`', '']
notFirst = ['and', 'And', 'or', 'Or']
nonEnders = ['a', 'A', 'the', 'The', 'or', 'Or', 'and', 'And', 'of', 'Of', 'an', 'An']
quantumWords = ['of', 'or', 'and', 'the', 'but', 'for', 'a', 'an', 'with']



##   Here's where I make some global declarations, just to ensure all functions have access

##  Each proxlist is a record of words that come either next, after-next,
##  third-next, etc. These are used to create data regarding the
##  proximity of the words to each other, as well as information
##  about the grammatical structure of the author

##  Essentially, this is a list of dictionaries, and they are accessed by
##  indexing, which corresponds to how the main function strings together
##  the lines.


##  This program will steadily incorporate the concept of dials, which allows
##  the user to create different types of poetry through manipulation of
##  certain factors.

##  The dial as an index restricts how long the connected chain of words can
##  become. The maximum chain length is currently 20, but that can easily be
##  enlarged.

##  Here's where one input from the user are utilized. I recommend leaving
##  the max on 20 for now, because it doesn't hurt. Minimums do.


# This part is only provisional. I need a better method for heteronyms


dynasaurus= {}

def gpDataWriter(dicList, fileBit, textFile):
    pFile = csv.writer(open('data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv', 'w+'))
    #$print('building: data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv')
    #$print(len(dicList))
    for key, val in dicList[0].items():
        ##$print(key)
        fullString = str()
        for each in dicList:
            ##$print(len(each))
            try:
                dicString = str()
                for entr in each[key]:
                    dicString = dicString+entr+'^'
                fullString = fullString+dicString[:-1]+'~'
                if dicList.index(each) == 19: # if we're done
                    ##$print('hardFinish')
                    each['thisisadeliberateKeyError']
            except KeyError:
                ##$print(fileBit, 'writing:', key, fullString[:min(20, len(fullString))])
                if len(fullString) > 0:
                    pFile.writerow([key, fullString[:-1]])
                fullString = str()
                continue    


def dynaMight(wordList, empKey, empStr, pLEmps, superTokens, theReverends): # Grabs possible synonyms, but only ones from the author's lexicon
    #$print('Entering dynaMight')
    dynamos = {}
    for each in wordList:
        dynabites = dynasaurus[each]
        for all in dynabites:
            if (all in superTokens) and (each not in dynamos) and ((pLEmps == empKey[-(len(pLEmps)):len(pLEmps)+len(emps[all])]) and (len(pLEmps)!=0)) or (empKey[0] == -1):
                # Might as well screen the ones that won't fit here rather than later
                dynamos[each].append(all)
                theReverends[-1][each][all]
                
    return dynamos, theReverends # rWord is the key to pWords in this dictionary


def contractionAction(qLine):
    # contractions are going to be a pain in the ass to handle.
    # use this function to equate pLine and qLine[1]
    print('contractionAction, you have not generated attraction')


def proxSorter(testList, keepList):
    killList = []
    for each in keepList:
        if each not in testList:
            killList.append(each)
    for each in killList:
        keepList.remove(each)

    return keepList


def fastTracker(expressList, superList):
    swapList = []
    for all in expressList:
        if all in superList:
            swapList.append(all)
    #$if len(swapList) > 0:
        #$print('fasttrakt:', len(swapList))
    for all in swapList:
        superList.insert(0, superList.pop(superList.index(all))) # This line pops the word and moves it to the front
    return superList


def gramLineMaker(xLine, flowData):
    gramLine = []
    xString = gF.lineToString(xLine)
    gramTuples = nltk.pos_tag(xLine) 
    for pair in gramTuples:
        gramLine.append(pair[1])
        ##$print(pair[1])
    return gramLine[-len(flowData[0]):]


def resetEverything():
    qLine = [[], []]
    qPopSuperList = [[[]], [[]]]
    pLEmps, tagEmpsLine = [], [[]]
    return qLine, qPopSuperList, pLEmps, tagEmpsLine


def chopZLine(zLine, qAllLines):
    qLine = zLine[0][len(qAllLines[0]):], zLine[1][len(qAllLines[1]):]    
    return qLine


def printData(time, qLine, qAllLines, pLEmps, tagEmpsLine):
    # no return statement, just printing data
    print(time, '\n', qLine, '\n', qAllLines, '\n', pLEmps, '\n', tagEmpsLine)


def acceptKeepers(zLine, qAllLines, qPopSuperList, keepList, rhyList):
    qPopSuperList[0].append(keepList)
    qPopSuperList[1].append(keepList)
    qPopSuperList[0][-1] = fastTracker(rhyList, qPopSuperList[0][-1])
    qPopSuperList[1][-1] = fastTracker(rhyList, qPopSuperList[1][-1])
    qLine = chopZLine(zLine, qAllLines)
    #$printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
    return qLine, qPopSuperList


def popListMaker(empKey, empStr, qAllLines, qLine, qPopSuperList, rhyList, pLEmps, tagEmpsLine, contrabandQLines): #  Uses the pLine data to generate a list of possible words
    print('Entering popListMaker')
    printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
    qList, keepList = [], [] # Clears the list that we will rebuild
    pLine, rLine = qLine
    zLine = [], [] # zLine is a temporary variable for adding the present line to the previous
    pAllLines, rAllLines = qAllLines
    # if we have an anteLine, then we'll just plug it in as if it were the whole line
    print('A')
    printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
    quickList0, quickList1 = [], []
    for each in qAllLines[0]:
        quickList0.append(each)
    for each in qLine[0]:
        quickList0.append(each)
    for each in qAllLines[1]:
        quickList1.append(each)
    for each in qLine[1]:
        quickList1.append(each)
    zLine = quickList0, quickList1
    if len(zLine[0]) == 0:
        print('B')
        qPopSuperList = [[[]], [[]]]
        for all in firstWords:
            if [all] not in supContraLines[empStr]:
                #$print('B0')
                try:
                    pWEmps = emps[all.lower()]
                    if pWEmps != empKey[:len(pWEmps)]:
                        #$print('B00')
                        supContraLines[empStr].append([all])
                    elif len(pWord) > 0:
                        #$print('B01')
                        qPopSuperList[0][0].append(all.lower())
                        qPopSuperList[1][0].append(all.lower())
                except KeyError:
                    #$print('kefucka82', all)
                    supContraLines[empStr].append([all])
                    continue
            #$else:
               #$print('B01')
               #$print('other contra screen')
        
        if len(qPopSuperList[0][-1]) == 0: # If, for some reason, none of the firstWords fit our rhyme scheme
            print('B1')
            dynaWords, theReverends = dynaMight(wordList, empKey, empStr, pLEmps, superTokens, [{}])
            for all in dynaWords:                
                qPopSuperList[0][-1].append(all)
        qWord = qPopSuperList[0][-1].pop(qPopSuperList[0][-1].index(random.choice(qPopSuperList[0][-1])))
        zLine = [qWord], [qWord]
        pWEmps = emps[qWord]
        pLEmps, tagEmpsLine = pWEmps, [pWEmps]
        keepList = []
        for all in proxP1[qWord]:
            keepList.append(all)
        qLine, qPopSuperList = acceptKeepers(zLine, qAllLines, qPopSuperList, keepList, rhyList)
        printData(datetime.datetime.now(), zLine, qAllLines, pLEmps, tagEmpsLine)        
        #$if len(qPopSuperList[0]) == 0:
            #$print('tried everything, nothing started')
        print('exit0')
        return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
       
    else: # then we have a bit more work to do...
        print('C')
        pLNi = int(0)
        proxNumList, pLineNList = [], []
        while pLNi < len(zLine[1]):
            proxNumList.append(pLNi)
            pLineNList.insert(0, pLNi)
            pLNi+=1
        pLNi-=1
        print(proxNumList, pLNi, pLineNList)
        printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
        flowData = proxNumList[:proxMaxDial], min(pLNi, proxMaxDial), pLineNList[:proxMaxDial]
        keepList = []
        while len(zLine[1]) > 0:
            print('C0')
            #$print(zLine[1])
            try:
                keepList = []
                for each in proxP1[zLine[1][-1]]:
                    keepList.append(each)
                if gramSwitch == 0:
                    rGramLine = gramLineMaker(zLine[1], flowData) # Check the present line's grammar
                    gKeepList = []
                    for each in gramProxP1[rGramLine[-1]]:
                        gKeepList.append(each)
                print('rebuild:', zLine[0], pLEmps, tagEmpsLine, flowData)
                break
            except KeyError:
                print(zLine[1], "=KError")
                zLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine = wordSubtracter(zLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, 1)
                if len(zLine[0]) != 0:
                    continue
                else:
                    print('crash')
                    #flowData = flowDataRefresh(zLine[0])
                    break            
        for all in proxNumList: # starts at 0, indexes from the end of line, organized as pLineNList
            print('proxCycle:', flowData)
            proxList = []
            try:
                for each in proxPlusLista[all][zLine[1][pLineNList[all]]]:
                    if zLine[0]+[each] not in contrabandQLines and zLine[0]+[each] not in supContraLines[empStr]:
                        proxList.append(each)
                    if all == 0:
                        keepList.append(each)
                if len(proxList) == 0:
                    print('exit1')
                    qLine, qPopSuperList = acceptKeepers(zLine, qAllLines, qPopSuperList, keepList, rhyList)
                    return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
                killList = []
                keepList = proxSorter(proxList, keepList)
                #$print('len(proxList)', len(proxList))
                if gramSwitch == 0: # gramSwitch == 0 means we are looking for grammar. gramSwitch == 1 means we are not.
                    gProxList = []
                    for each in gramProxPlusLista[all][rGramLine[pLineNList[pLNi]]]:
                        gProxList.append(each)
                    gKeepList = proxSorter(gProxList, gKeepList)
                    #$print('gKeepList:', gKeepList)
                    for each in keepList:
                        testLine = []
                        for word in zLine[1]: # instead of saying testLine = zLine[1], because then they're linked. testLine should change and zLine[1] should stay immutable
                            testLine.append(word)
                        testLine.append(each)
                        rGramLine = gramLineMaker(testLine, flowData)
                        ##$print(all, '/', len(proxNumList), '|  testLine:', testLine)
                        ##$print(rGramLine)
                        if rGramLine[-1] not in gKeepList or len(each) == 0:  # Send to a separate list to remove. If you remove during this 'for' section, it will index incorrectly
                            killList.append(each)
                    #$print('killList@:', len(killList))             
                if len(killList) == len(keepList):
                    qLine, qPopSuperList = acceptKeepers(zLine, qAllLines, qPopSuperList, keepList, rhyList)
                    print('exit2')
                    return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
                else:
                    for each in killList:
                        keepList.remove(each) # this filters against bad grammar choices in our popList
            #$print('keepList@:', len(keepList))
            except IndexError:
                print('wtf shouldnt happen...') # proxNumList is built alongside and in coordination with pLineNList. Index shouldn't be out of range.
                printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
                everything = resetEverything()
                printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
                return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
        if len(keepList) == 0: # then there are no viable choices
            qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine = wordSubtracter(qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, 1)
            while (len(qPopSuperList[0][-1]) == 0) and (len(qPopSuperList[0]) > 0):
                qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine = wordSubtracter(qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, 1)
                if len(qPopSuperList[0][-1]) == 0 and len(qPopSuperList[0]) == 1:
                    print('derp')
                    break
                qLine = chopZLine(zLine, qAllLines)
                print('exit3')
                printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
                return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
            qLine = chopZLine(zLine, qAllLines)
            print('exit4')
            printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
            return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
        elif (len(proxNumList) > proxMinDial or len(qLine) <= proxMinDial):
            qLine, qPopSuperList = acceptKeepers(zLine, qAllLines, qPopSuperList, keepList, rhyList)
            print('exit5')
            return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
    # if this fails for some reason, it'll return a blank keepList and print an indicator
    qLine, qPopSuperList, pLEmps, tagEmpsLine = resetEverything()
    print('exit6')
    printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
    return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines

#halfBeatNum = tagEmpsLine.count('')
#if ((halfSwitch == 1) and (halfBeatNum == 0) and (qLine[-1] in quantumWords)):

# # #               

def popListDigester(qPopSuperList, qLine, qAllLines, pLEmps, tagEmpsLine, empKey, empStr, rhyList, contrabandQLines):
    print('entering popListDigester', datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
    firstLineLen = len(qLine[0])
    while (len(qPopSuperList[0][-1]) > 0): # and ((len(proxNumList) > proxMinDial) or (len(qLine[0]) <= proxMinDial)): # keep moving forward as long as we keep getting non-empty lists, proxDial restrictions
        pWord = qPopSuperList[0][-1].pop(qPopSuperList[0][-1].index(random.choice(qPopSuperList[0][-1])))
        #$print('digest:', pWord, '/', len(qPopSuperList[0][-1]))
        ##$print(qLine[0]+[pWord], '|', qLine[0], pWord)
        if qLine[0]+[pWord] not in supContraLines[empStr] and qLine[0]+[pWord] not in contrabandQLines[0]: # This will screen against trees already explored
            pLEmps, qLine, tagEmpsLine = wordAdder(pWord, qPopSuperList, qAllLines, qLine, pLEmps, tagEmpsLine)
            halfBeatNum = tagEmpsLine.count('')
            if pWord in allPunx:
                pnxCt = 0
                for all in allPunx:
                    if all in qLine[0][max(0,(len(qLine[0])-punxDial)):]:
                        #$print('punkt')
                        pnxCt+=1
                if pnxCt > 0:
                    qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine = wordSubtracter(qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, 1)
                    #$print('punktured')
                else:
                    #$print('punkRock')
                    return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
            elif pLEmps == empKey[:len(pLEmps)] or ((halfSwitch == 1) and (halfBeatNum == 0) and (qLine[-2] in quantumWords) and (qLine in quantumWords)):
                if rhySwitch == 0 and len(pLEmps) == len(empKey) and len(rhyList) > 0 and qLine[0][-1] not in rhyList:
                    #$print('notaRhyme')
                    qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine = wordSubtracter(qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, 1)
                else:
                    if qLine[-2] in quantumWords and qLine[-1] in quantumWords:
                        print('quantumShift')
                        tagEmpsLine = tagEmpsLine[:-1]
                        tagEmpsLine.append('')
                        pLEmps = pLEmps[:-1]
                    print('hit0!', qLine, pLEmps)
                    qPopSuperList[0].append([])
                    qPopSuperList[1].append([])
##                    if len(qAllLines[0] > 0:
##                        qLine = qLine[0][len(qAllLines[0])-1:], qLine[1][len(qAllLines[1])-1:]
                    print('exitY')
                    return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines
            else:
                supContraLines[empStr].append(qLine[0]+[pWord])
                #$print('contra1:', qLine[0], len(supContraLines[empStr]), '\n', pLEmps, '|', empKey)
                qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine = wordSubtracter(qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, 1)
                #$print('A: pxNumList:', len(proxNumList), '>', proxMinDial, '|or| qLineLen:', len(qLine[0]), '<', proxMinDial)
                #$print('qPoppa0:', len(qPopSuperList[0]), len(qPopSuperList[0][-1]))
        #$else:
            #$print('contraScreen:', qLine, '|', pWord)
        if len(qPopSuperList[0][-1]) == 0 and pLEmps != empKey[:len(pLEmps)]:
            qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine = wordSubtracter(qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, 1)
            #$print('B: pxNumList:', len(proxNumList), '>', proxMinDial, '|or| qLineLen:', len(qLine[0]), '<', proxMinDial)
            #$print('qPoppa0:', len(qPopSuperList[0]), len(qPopSuperList[0][-1]))
    #$print(len(qPopSuperList[0][-1]), len(proxNumList), proxMinDial, qLine[0])
    #$print('firstLine2:', firstLineLen)
    if (pLEmps == empKey[:len(pLEmps)]) and (len(qLine[0]) > firstLineLen) and len(qLine[0]) > 0 and (len(proxNumList) < proxMinDial or len(qLine[0]) < proxMinDial):
        if ((qLine[0][-1] in rhyList) or (len(rhyList) == 0)):
            #$print('hit1!', qLine, pLEmps)
            qPopSuperList[0].append([])
            qPopSuperList[1].append([])
    else:
        contrabandQLines[0].append(qLine[0])
        contrabandQLines[1].append(qLine[1])
        qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine = wordSubtracter(qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, 1)
        #$print('pxNumList:', len(proxNumList), '>', proxMinDial, '|or| qLineLen:', len(qLine[0]), '<', proxMinDial)
        #$print('qPoppa1:', len(qPopSuperList[0]), len(qPopSuperList[0][-1]))
    #qLine = qLine[0][len(qAllLines[0]):], qLine[1][len(qAllLines[1]):]
    print('exitZ')
    return qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines


def wordSubtracter(qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine, minusThis):

    #$print('subtract:')
    # by blacklisting the arrangement of words, we stop the lineBuilder from testing combinations we've already exhausted
    # take everything back a bit
    #$printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
    qLine = qLine[0][:-minusThis], qLine[1][:-minusThis] 
    if len(qPopSuperList[0][-1]) == 0:
        if len(qAllLines[0]) > 0:
            qAllLines[0].pop(0) 
            qAllLines[1].pop(0)
    tagEmpsLine = tagEmpsLine[:-minusThis]
    qPopSuperList = qPopSuperList[0][:(len(qLine[0])+1)], qPopSuperList[1][:(len(qLine[1])+1)]
    pLEmps = []
    for all in tagEmpsLine:
        ##$print('tEL0:', all)
        for each in all:
            ##$print('tEL1:', each)
            pLEmps.append(each)
    #$print('subtractDone:')
    #$printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
    return qLine, qPopSuperList, qAllLines, pLEmps, tagEmpsLine


def wordAdder(pWord, qPopSuperList, qAllLines, qLine, pLEmps, tagEmpsLine):

    #$print('add:', pWord)
    if pWord not in allPunx:
        try:
            pWEmps = emps[pWord.lower()]
        except KeyError:
            try:
                #$print('kefucka0:', pWord)
                pWEmps = emps[pWord]
            except KeyError:
                #$print('kefucka1:', pWord)
                pWEmps = ['3']
        pLEmps = pLEmps+pWEmps
        tagEmpsLine.append(pWEmps)
    else:
        tagEmpsLine.append([])
    if len(qAllLines[0]) > 0:
        qLine = qLine[0][len(qAllLines[0]):]+[pWord], qLine[1][len(qAllLines[1]):]+[pWord]
    elif len(qLine[0]) == 0:
        qLine = [pWord], [pWord]
    else:
        qLine = qLine[0]+[pWord], qLine[1]+[pWord]
    #$print(pWord, pLEmps, tagEmpsLine)
    
    return pLEmps, qLine, tagEmpsLine


def plainLiner(pLine, pLineLen): # This would build lines not subject to meter and rhyme
    if len(pLine) == 0:
        pLine = [firstWords[firstWords.index(random.choice(0, len(firstWords)))]]
    else:
        pList = []
        for all in proxP1[pLine[-1]]:
            pList.append(all)
        flowData = flowDataReboot(pLine)
        proxNumList, pLNi, pLineNList = flowData
    keepList, gKeepList = [], []
    for all in proxP1[qLine[1][-1]]:
        keepList.append(all)
    for all in gramProxP1[qLine[1][-1]]:
        gKeepList.append(all)
    #$print('itIs == itIs') # build this later


def poemLiner(empKey, writQLines, rhyList):

    writPLines, writRLines = writQLines
    qLine, pAllLines, qAllLines, rAllLines, pLEmps, tagEmpsLine, qPopSuperList = [[],[]], [], [[],[]], [], [], [], [[[]], [[]]]
    pPopSuperList, rPopSuperList = qPopSuperList
    pLEmps, tagEmpsLine = [], []
    empStr = gF.lineToString(empKey) # we have to convert empKey to str() to be used as a key in supContraLines
    qAllLines = [], [] # rebuild allLines with immutable 'writ' variables and current, evolving pLine and qLine[1]
    contrabandQLines = [], []
    print('entering poemLiner')
    printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
    try:
        supContraLines[empStr]
    except KeyError:
        supContraLines[empStr] = [] # contrabandLines will now be global dic, based on empKey
    if len(writQLines[0]) > 0:
        for each in writQLines[0]:
            for word in each:
                qAllLines[0].append(word)
    if len(writQLines[1]) > 0:
        for each in writQLines[1]:
            for word in each:
                qAllLines[1].append(word)
    while (pLEmps != empKey) and (len(pLEmps) != len(empKey)): # Search for a word that matches the declared meter template, line may need to rhyme (flawed logic here...) and ((len(rhyList)>0) or (pLine[-1] not in rhyList)) and metSwitch == 1 and (pLine[-1] not in quantumList)
        #$printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
        if len(qPopSuperList[0][-1]) == 0:
            qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines = popListMaker(empKey, empStr, qAllLines, qLine, qPopSuperList, rhyList, pLEmps, tagEmpsLine, contrabandQLines)
            qPopSuperList[0][-1] = fastTracker(rhyList, qPopSuperList[0][-1])
        qPopSuperList, qLine, pLEmps, tagEmpsLine, qAllLines, contrabandQLines  = popListDigester(qPopSuperList, qLine, qAllLines, pLEmps, tagEmpsLine, empKey, empStr, rhyList, contrabandQLines)
        #$print('\n\nend of main while:')
        #$printData(datetime.datetime.now(), qLine, qAllLines, pLEmps, tagEmpsLine)
        nowM = int(str(datetime.datetime.now())[14:16]) # checks the minute hand
        if str(datetime.datetime.now())[11:13] != startTimeH: # adds 60mins if we've changed the hour
            nowM+=60
        if (nowM - int(startTimeM)) > 10:
            #$print('\n--RESET--\n')
            return [], []
    if ((pLEmps != empKey) or (len(pLEmps) != len(empKey))) and ((len(rhyList)==0) or (qLine[0][-1] in rhyList)):
        #$print('breakpointA')
        return qLine
    elif (pLEmps != empKey) and (len(pLEmps) != len(empKey)) and (qLine[0][-1] not in rhyList) and (len(rhyList) > 0): #
        pLEmps = pLEmps[:-(len(emps[qLine[1].pop()]))] # One line removes the word from the qLine[1] and the emps of pLine
        #$print('shouldnt happen')
        if len(popList) > 0:
            result = lineAdvancer(popList, empKey)
            return qLine
        else:
            #$print('breakpointB')
            return qLine
    else:
        #$print('\n\nsuccess!\n', qLine[0], pLEmps)
        return qLine

# # #                   


def testPoemLine(newQLine, writQLines, writIndex, rhymeMap):
    #$print('testPoemLine', writQLines, writIndex, rhymeMap)
    if len(newQLine[0]) > 0 and len(writQLines) > 0: # anything that results in failure from poemLiner will return a line with len==0, the implicit else is that nothing is added. Start over.
        #$print('tPL1')
        writQLines[0].append(newQLine[0])
        writQLines[1].append(newQLine[1])
    elif len(writQLines[0]) > 0:
        #$print('tPL2')
        writQLines = writQLines[0][:-1], writQLines[1][:-1]
    writIndex = len(writQLines[0])
    if writIndex == len(rhymeMap):       # then we're done, and we'd get an indexError otherwise 
        return writQLines, writIndex
    elif writIndex > 0:
        rhyNum = rhymeMap.count(rhymeMap[writIndex-1])
        if rhyNum > 1 and len(newQLine[0]) > 0:
            checkPunx, checkRhy = -1, '.'
            while checkRhy in endPunx:
                #$print('chkrhy:', checkRhy, newQLine[rhymeMap.index(rhymeMap[writIndex])])
                checkRhy = newQLine[rhymeMap.index(rhymeMap[writIndex])][checkPunx]
                checkPunx-=1
            rhyWords = gF.rhyDictator(superTokens, checkRhy, 10, 10) # Submit these as lists, it'll enable ranges of values!
            #$print('tPL rhys', len(rhyWords))
            if len(rhyWords) == 0:
                #$print('tPLnorhys')
                newQLine = [],[]
                writQLines[0].pop()
                writQLines[1].pop()
        writIndex = len(writQLines[0])
    #$print(writQLines, writIndex)
    return writQLines, writIndex


def stanzaWriter(stanza, rhymeMap, meterMap, usedList):
    writQLines = [], []
    writIndex = int(0)
    pLine, rLine = [], []
    qLine = [pLine, rLine]
    writPLines, writRLines = [], []
    writQLines = [writPLines, writRLines]
    pAllLines, rAllLines = [], []
    qAllLines = pAllLines, rAllLines
    if rhySwitch == 0 and metSwitch == 0: # then we have rhyme and meter in the template
        while len(writQLines[0]) < min(len(meterMap), len(rhymeMap)):
            #$print('stanzaWriter1')
            global startTimeM, startTimeH
            startTimeM = int(str(datetime.datetime.now())[14:16])
            startTimeH = str(datetime.datetime.now())[11:13]
            #$print('readyset', startTimeM, startTimeH)
            if len(writQLines[0]) == 0:
                #$print('sWa')
                newQLine = poemLiner(meterMap[writIndex], [[],[]], [])
            elif writIndex != rhymeMap.index(rhymeMap[writIndex]): # then the present rhyme token isn't the first in rhymeMap; we need a rhymelist.
                #$print('sWb')
                checkPunx, checkRhy = -1, '.'
                while checkRhy in endPunx:
                    #$print('chkrhy:', checkRhy, writQLines[0][rhymeMap.index(rhymeMap[writIndex])])
                    checkRhy = writQLines[0][rhymeMap.index(rhymeMap[writIndex])][checkPunx]
                    checkPunx-=1
                rhyWords = gF.rhyDictator(superTokens, checkRhy, 10, 10) # Submit these as lists, it'll enable ranges of values!
                if len(rhyWords) == 0: # then we didn't find any rhymes for that line. We cut all the way back.
                    #$print('noRhys', writIndex, rhymeMap)
                    rhyBit = rhymeMap[writIndex]
                    writQLines = writQLines[0][:rhymeMap.index(rhyBit)], writQLines[1][:rhymeMap.index(rhyBit)]
                else:
                    #$print('swb gogo')
                    #$print(rhyWords)
                    newQLine = poemLiner(meterMap[writIndex], writQLines, rhyWords) # feed the rhyList and the anteLines into poemLiner, depending on the writIndex count
            else: # then we have an unrhyming line that is after another. No rhymes, but anteLines
                #$print('sWc')
                newQLine = poemLiner(meterMap[writIndex], writQLines, [])
            writQLines, writIndex = testPoemLine(newQLine, writQLines, writIndex, rhymeMap)
            time.sleep(5)
    elif rhySwitch == 1 and metSwitch == 0: # then we have meter but not rhyme
        while len(writQLines[0]) < len(meterMap):
            #$print('stanzaWriter2')
            newQLine = poemLiner(empKey, writQLines, [])
            writQLines, writIndex = testPoemLine(newQLine, writQLines, writIndex, rhymeMap)
    elif rhySwitch == 0 and metSwitch == 1: # then we have rhyme but not meter
        while len(writQLines[0]) < len(rhymeMap): # do poemLiner with rhymeMap, not empKey. Warning: if emps are different in matched lines, no rhymes will yield.
            #$print('stanzaWriter3')
            for each in meterMap: # The value of -1 will tell poemLiner to ignore it
                for all in each:
                    all = -1
            rhyWords = gF.rhyDictator(writQLines[0][rhymeMap.index(rhymeMap[writIndex])], 10, 10)
            newQLine = poemLiner(empKey, writQLines, rhyWords)
            writQLines, writIndex = testPoemLine(newQLine, writQLines, writIndex, rhymeMap)
    else:
        plainLiner() 
    stanza = []
    for each in writQLines[0]:
        thisLine = gF.lineToString(each)
        stanza.append(thisLine)
    #$print('finished stanza function')
    return stanza, usedList

##    else:
##        #$print("we don't have enough lines")
##        return stanza, []
            
        
# # #

def newProxLibs(proxLista, libInt, wordLista, textFile):
    for each in wordLista:
        proxLista[libInt][each.lower()] = []
        if len(each) > 1:
            proxLista[libInt][each[0].upper()+each[1:]] = []
        else:
            proxLista[libInt][each.upper()] = []
    return proxLista


    newFirstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
    for all in firstWords:
        newFirstFile.write(all+'\n')
        #$print('writing...', all)
    newFirstFile.close()


def startWemyx():
    #$print('\nstarting remix')
    textFile = textChoice.get() # superBible
    texto = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())
    rhymeMap=str()
    meterMap, usedList, lastList, metaBlackList = [], [], [], []
    global metSwitch, rhySwitch, theSwitch, gramSwitch, halfSwitch, usedSwitch
    metSwitch, rhySwitch, theSwitch, gramSwitch, halfSwitch, usedSwitch = meterVar.get(), rhymeVar.get(), thesaVar.get(), grammVar.get(), halfVar.get(), usedVar.get()
    global proxMinDial, proxMaxDial, punxDial
    proxMinDial, proxMaxDial, punxDial = int(proxMinChoice.get()), int(proxMaxChoice.get()), int(punxChoice.get())
    #$print('starting proxBuilds', gramSwitch)
    global proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20
    global proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20
    global gramProxP1, gramProxP2, gramProxP3, gramProxP4, gramProxP5, gramProxP6, gramProxP7, gramProxP8, gramProxP9, gramProxP10, gramProxP11, gramProxP12, gramProxP13, gramProxP14, gramProxP15, gramProxP16, gramProxP17, gramProxP18, gramProxP19, gramProxP20
    global gramProxM1, gramProxM2, gramProxM3, gramProxM4, gramProxM5, gramProxM6, gramProxM7, gramProxM8, gramProxM9, gramProxM10, gramProxM11, gramProxM12, gramProxM13, gramProxM14, gramProxM15, gramProxM16, gramProxM17, gramProxM18, gramProxM19, gramProxM20
    global proxPlusLista, proxMinusLista, gramProxPlusLista, gramProxMinusLista, proxLib, gramProxLib
    proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20 = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}] 
    proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20  = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]      
    gramProxP1, gramProxP2, gramProxP3, gramProxP4, gramProxP5, gramProxP6, gramProxP7, gramProxP8, gramProxP9, gramProxP10, gramProxP11, gramProxP12, gramProxP13, gramProxP14, gramProxP15, gramProxP16, gramProxP17, gramProxP18, gramProxP19, gramProxP20 = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    gramProxM1, gramProxM2, gramProxM3, gramProxM4, gramProxM5, gramProxM6, gramProxM7, gramProxM8, gramProxM9, gramProxM10, gramProxM11, gramProxM12, gramProxM13, gramProxM14, gramProxM15, gramProxM16, gramProxM17, gramProxM18, gramProxM19, gramProxM20  = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]  
    proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20]
    proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20]
    gramProxPlusLista = [gramProxP1, gramProxP2, gramProxP3, gramProxP4, gramProxP5, gramProxP6, gramProxP7, gramProxP8, gramProxP9, gramProxP10, gramProxP11, gramProxP12, gramProxP13, gramProxP14, gramProxP15, gramProxP16, gramProxP17, gramProxP18, gramProxP19, gramProxP20]
    gramProxMinusLista = [gramProxM1, gramProxM2, gramProxM3, gramProxM4, gramProxM5, gramProxM6, gramProxM7, gramProxM8, gramProxM9, gramProxM10, gramProxM11, gramProxM12, gramProxM13, gramProxM14, gramProxM15, gramProxM16, gramProxM17, gramProxM18, gramProxM19, gramProxM20]
    proxPlusLista = proxPlusLista[:proxMaxDial]
    proxMinusLista = proxMinusLista[:proxMaxDial]
    gramProxPlusLista = gramProxPlusLista[:proxMaxDial]
    gramProxMinusLista = gramProxMinusLista[:proxMaxDial]
    proxLib, gramProxLib = [proxPlusLista, proxMinusLista], [gramProxPlusLista, gramProxMinusLista]
    global supContraLines
    supContraLines = {}
    for each in rhyEntries:
        if rhySwitch == 0:
            rhyMore = str(each.get())
            rhymeMap+=rhyMore
        else:
            rhymeMap+=alphabet[rhyEntries.index(each)]
    for each in metEntries:
        metMore = list(each.get())
        if len(metMore) > 0:
            meterMap.append(metMore)
    
    #$print(metSwitch, rhySwitch, gramSwitch, rhymeMap, meterMap, proxMinDial, punxDial)

    texto = texto.replace('Mr.', 'Mister')
    texto = texto.replace('Mrs.', 'Missus')
    texto = texto.replace('Ms.', 'Miss')
    texto = texto.replace('Dr.', 'doctor')

    for all in endPunx:
        texto = texto.replace(all, ' '+all)
    for all in badGrams:
        texto = texto.replace(all, '')
    global superTokens
    superTokens = nltk.word_tokenize(texto)

    ##  This part loads data that allows the computer to read meter, phonetics,
    ##  and to differentiate between similarly-spelled words

    # Now Wemyx fills the empty dictionaries it created

    global firstWords
    firstWords, yaFound, nextSentenceIndexes, theReverends = [], [], [], []
    lastSpot, wordsI, click, proxNumerator, proxDicCounter = len(superTokens), int(-1), int(0), int(1), int(0)

    try:
        compFile = open('data/textLibrary/textData/'+textFile+'-compFile.txt', 'r')
        firstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'r')
        for line in firstFile:
            firstWords.append(line[:-1])
        proxPlusLista = gF.gpDataOpener(proxPlusLista, 'proxP', textFile)
        #$for each in proxPlusLista:
            #$print(len(each))
        proxMinusLista = gF.gpDataOpener(proxMinusLista, 'proxM', textFile)
        #$for each in proxPlusLista:
            #$print(len(each))
        gramProxPlusLista = gF.gpDataOpener(gramProxPlusLista, 'gramP', textFile)
        #$for each in proxPlusLista:
            #$print(len(each))
        gramProxMinusLista = gF.gpDataOpener(gramProxMinusLista, 'gramM', textFile)
        #$for each in proxPlusLista:
            #$print(len(each))
        dynaSaurus = gF.dynaDataOpener(textFile, 'thes')
        #$print('done with builds')
                    
    except FileNotFoundError:
        superTokenData = nltk.pos_tag(superTokens)
        superTokenWords, superTokenGrams = [], []
        for each in superTokenData:
            ##$print(each)
            superTokenWords.append(each[0])
            superTokenGrams.append(each[1])
            dynasaurus[str(each[0])+'.'+str(each[1][0])] = []
        for each in superTokenData:
            try:
                pWord = str(each[0])
                quickToke = str(each[1][0])
                if quickToke in dynaPOS:
                    if quickToke == 'N':
                        for syns in supersaurus[pWord]:
                            if syns in superTokenWords:
                                dynasaurus[pWord+'.'+quickToke].append(syns)        
                    if quickToke == 'V':
                        for syns in supersaurus[pWord]:
                            if syns in superTokenWords:
                                dynasaurus[pWord+'.'+quickToke].append(syns) 
                    if quickToke == 'R':
                        for syns in supersaurus[pWord]:
                            if syns in superTokenWords:
                                dynasaurus[pWord+'.'+quickToke].append(syns) 
                    if quickToke == 'J':
                        for syns in supersaurus[pWord]:
                            if syns in superTokenWords:
                                dynasaurus[pWord+'.'+quickToke].append(syns)
            except KeyError:
                continue
        killList = []
        for key, val in dynasaurus.items():
            if len(val) == 0:
                killList.append(key)
        for all in killList:
            del dynasaurus[all]
        
        gF.dynaDataWriter(dynasaurus, textFile, 'thes')

        
        #$print('len(superTokenData):', len(superTokenData), '\nlen(superTokenGrams):', len(superTokenGrams), '\n', superTokenData[1000:1200], superTokenGrams[1000:1200], '\ncontinue?')
        for all in range(0, (len(proxPlusLista))):
            proxPlusLista = newProxLibs(proxPlusLista, all, superTokenWords, textFile)
            proxMinusLista = newProxLibs(proxMinusLista, all, superTokenWords, textFile)
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
                        #$print('plusadd = gramProx:', gramProxWord, 'gramPWord:', gramPWord)
                        gramProxPlusLista[proxDicCounter][gramPWord].append(gramProxWord)
                    if gramPWord not in gramProxMinusLista[proxDicCounter][gramProxWord]:
                        #$print('minusadd = gramProx:', gramProxWord, 'gramPWord:', gramPWord)
                        gramProxMinusLista[proxDicCounter][gramProxWord].append(gramPWord)
                    proxDicCounter+=1
                    proxNumerator+=1
            except IndexError:          
                continue
            except KeyError:
                #$print('kE build:', pWord, proxWord, proxDicCounter, proxNumerator)
                proxDicCounter+=1  ## These are the lines you edited
                proxNumerator+=1   ## Check to see if they did anything significant
                continue
    if click > 0:
        newFirstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
        for all in firstWords:
            newFirstFile.write(all+'\n')
        #$print('writing...', all)
        newFirstFile.close()
        gpDataWriter(proxPlusLista, 'proxP', textFile)
        gpDataWriter(proxMinusLista, 'proxM', textFile)
        gpDataWriter(gramProxPlusLista, 'gramP', textFile)
        gpDataWriter(gramProxMinusLista, 'gramM', textFile)
        #gF.dynaDataWriter(dynasaurus, textFile, 'thes')

            

    compFile = open('data/textLibrary/textData/'+textFile+'-compFile.txt', 'w+')

    # This group of numbers will control how the Markov chains are made.
    # The 'list of lists' strategy allows for a variable length of connectivity
    # among the words that the user can govern. It's programmed to attempt the
    # longest chains possible within the user's bounds.

    rCt = int(0)
    poemCt = int(poemNum.get())
    printIndex = int(0)
    print('sourcetext: ', textFile+'.txt\n\nformat:')
    while printIndex < len(rhymeMap):
        print(rhymeMap[printIndex], meterMap[printIndex])
        printIndex+=1
    print("\n")
    if gramSwitch == 1:
        print('grammar    | off')
    else:
        print('grammar    | on')
    if rhySwitch == 1:
        print('rhyme      | off')
    else:
        print('rhyme      | on')
    if metSwitch == 1:
        print('meter      | off')
    else:
        print('meter      | on')
    print('half-beats | N/A')
    print('thesaurus  | N/A')
    while rCt<poemCt:
        rCt+=1
        print('\n\nPoem #'+str(rCt)+'\n'+str(datetime.datetime.now())+'\n')
        #try:
            ## A timer is used to restart the process if it stalls on a long loop. It feeds into the stanzaWriter function.
        stanza, usedList = [], [] # to prevent repeat words
        while len(stanza) != len(rhymeMap):
            stanza, usedList = stanzaWriter(stanza, rhymeMap, meterMap, usedList)
        for each in stanza:
             print(each)
        time.sleep(20)
        if usedSwitch == 1: 
            usedList = ['']
##        except:
##            startTimeM = int(str(datetime.datetime.now())[14:16])
##            startTimeH = str(datetime.datetime.now())[11:13]
##            usedList = []
##            usedList = stanzaWriter(rhymeMap, meterMap, usedList, emps, firstWords, startTimeM, startTimeH)
##            if usedSwitch == 1:
##                usedList = ['']
##            continue
        
    #$print('\nremix complete')


##  This is where the user declares what type of poem they want.
##  It uses a GUI built with TKinter to tweak variables.
##  The stanzas are declared by a column of letters such as "ABAB"
##  with each matching letter receiving a rhyming line.thesa
##  The meter for each line is declared by a string of ints (formerly
##  binaries, until a tertiary option, the secondary stress, was introduced)


master = Tk()
master.title("Wemyx")

meterVar = IntVar() # choose to have rhythm, will follow map
Checkbutton(master, text="not metered", variable=meterVar).grid(row=0, column=0, sticky=W)
rhymeVar = IntVar() # choose to rhyme or not, will follow map
Checkbutton(master, text="not rhyming", variable=rhymeVar).grid(row=1, column=0, sticky=W)
grammVar = IntVar() # regulates whether the program utilizes thesaurus tools
Checkbutton(master, text="grammar deactivate", variable=grammVar).grid(row=2, column=0, sticky=W)
thesaVar = IntVar() # regulates whether the program utilizes thesaurus tools
Checkbutton(master, text="ignore thesaurus", variable=thesaVar).grid(row=3, column=0, sticky=W)
halfVar = IntVar() # regulates whether to allow additional half-beats during non-emphasis syllables
Checkbutton(master, text="half-beats", variable=halfVar).grid(row=4, column=0, sticky=W)
usedVar = IntVar() # regulates whether the program omits words that repeat within stanzas
Checkbutton(master, text="filter used", variable=usedVar).grid(row=5, column=0, sticky=W)

rhy1, rhy2, rhy3, rhy4, rhy5, rhy6 = Entry(master), Entry(master), Entry(master), Entry(master), Entry(master), Entry(master)
met1, met2, met3, met4, met5, met6 = Entry(master), Entry(master), Entry(master), Entry(master), Entry(master), Entry(master)

rhyEntries = rhy1, rhy2, rhy3, rhy4, rhy5, rhy6
metEntries = met1, met2, met3, met4, met5, met6

rhy1.grid(row=0, column=1), met1.grid(row=0, column=2)
rhy2.grid(row=1, column=1), met2.grid(row=1, column=2)
rhy3.grid(row=2, column=1), met3.grid(row=2, column=2)
rhy4.grid(row=3, column=1), met4.grid(row=3, column=2)
rhy5.grid(row=4, column=1), met5.grid(row=4, column=2)
rhy6.grid(row=5, column=1), met6.grid(row=5, column=2)

Label(master, text="----", justify=CENTER).grid(row=6, column=0)

proxMinChoice = Entry(master)
proxMinChoice.grid(row=7, column=1)
Label(master, text="proxMinDial").grid(row=7, column=0)

proxMaxChoice = Entry(master)
proxMaxChoice.grid(row=8, column=1)
Label(master, text="proxMaxDial").grid(row=8, column=0)

punxChoice = Entry(master)
punxChoice.grid(row=9, column=1)
Label(master, text="punxDial").grid(row=9, column=0)

poemNum = Entry(master)
poemNum.grid(row=10 , column=1)
Label(master, text="how many poems?").grid(row=10, column=0)

empChoice = StringVar(master)
empChoice.set("Multi-binary") # default value

empMenu = OptionMenu(master, empChoice, "Single-binary", "Multi-binary", "Trinary", "MasterFile")
empMenu.grid(row=11)

Label(master, text="----").grid(row=12, column=0)

textChoice = Entry(master)
textChoice.grid(row=13 , column=1)
Label(master, text="which file to remix?").grid(row=13, column=0)

startButton = Button(master, text='Start', command=startWemyx, compound=CENTER).grid(row=14, column=0, sticky=W, pady=4)
stopButton = Button(master, text='Quit', command=master.quit, compound=CENTER).grid(row=14, column=1, sticky=W, pady=4)


#$print('loading metadatas...')

libFile = csv.reader(open('data/USen/empDic-USen-unik.csv', 'r'))
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


#$print('opening fonoFiles')
vocs = gF.globalOpen('data/USen/vocDic-USen-MAS.csv', 'string')
cons = gF.globalOpen('data/USen/conDic-USen-MAS.csv', 'string')
fono = gF.globalOpen('data/USen/fonDic-USen-MAS.csv', 'string')

#$print('opening dynasaurus')
supersaurus = {}
for each in 'ADJ', 'ADV', 'NOUN', 'VERB':
    thesFile = open('data/USen/dynasaurus/thes-'+each+'.csv')
    for line in thesFile:
        supersaurus[line[0]] = line[1].split('^')
