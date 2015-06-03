 
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
    print('building: data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv')
    print(len(dicList))
    for key, val in dicList[0].items():
        #print(key)
        fullString = str()
        for each in dicList:
            #print(len(each))
            try:
                dicString = str()
                for entr in each[key]:
                    dicString = dicString+entr+'^'
                fullString = fullString+dicString[:-1]+'~'
                if dicList.index(each) == 19: # if we're done
                    #print('hardFinish')
                    each['thisisadeliberateKeyError']
            except KeyError:
                print(fileBit, 'writing:', key, fullString[:min(20, len(fullString))])
                if len(fullString) > 0:
                    pFile.writerow([key, fullString[:-1]])
                fullString = str()
                continue    


def flowDataRefresh(qLine): # Refreshes the prox index list
    pLNi = int(0)
    proxNumList, pLineNList = [], []
    while pLNi < len(qLine[0]):
        proxNumList.append(pLNi)
        pLineNList.insert(0, pLNi)
        pLNi+=1

    flowData = proxNumList, pLNi, pLineNList
    return flowData


def dynaMight(wordList, empKey, pLEmps, superTokens, theReverends): # Grabs possible synonyms, but only ones from the author's lexicon
    print('Entering dynaMight')
    dynamos = {}
    for each in wordList:
        dynabites = dynasaurus[each]
        for all in dynabites:
            if (all in superTokens) and (each not in dynamos) and ((pLEmps == empKey[-(len(pLEmps)):len(pLEmps)+len(emps[all])]) and (len(pLEmps)!=0)) or (empKey[0] == -1): # Might as well screen the ones that won't fit here rather than later
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
        if all in superList[-1]:
            swapList.append(all)
        else:
            superList[-1].insert(0, all)
    for all in swapList:
        superList[-1].insert(0, superList[-1].pop(superList[-1].index(all)))
    return superList



def wordWriter(empKey, qAllLines, qLine, qPopSuperList, flowData, gramSwitch, rhyList, firstWords): #  Uses the pLine data to generate a list of possible words
    print('Entering popListMaker')
    qList, keepList = [], [] # Clears the list that we will rebuild
    proxNumList, pLNi, pLineNList = flowData
    pLine, rLine = qLine
    pAllLines, rAllLines = qAllLines
    
    if len(qLine[0]) == 0:
        qPopSuperList = [], []
        for all in firstWords:
            try:
                pWord = all.lower()
                #print('testFirst:', pWord, emps[pWord], '|', empKey[:len(emps[pWord])])
                if emps[pWord] == empKey[:len(emps[pWord])]:
                    qPopSuperList[0].append(pWord)
                    qPopSuperList[1].append(pWord)
            except KeyError:
                #print('kE0 in popList maker = (firstWords):', all)
                if pWord == firstWords[-1]: # this means we've gotten to the end
                    return qPopSuperList, qLine, flowData
                else:
                    continue
        if len(qPopSuperList[0]) == 0: # If, for some reason, none of the firstWords fit our rhyme scheme
            dynaWords, theReverends = dynaMight(wordList, empKey, pLEmps, superTokens, [{}])
            for all in dynaWords:
                qPopSuperList[0].append(all)
        flowData = [0], 0, [0]
        qPopSuperList[0] = fastTracker(rhyList, qPopSuperList[0]) # preferred words to the front of the line, in this case, rhymes. non-rhyming lines will have empty lists
        qPopSuperList[1] = fastTracker(rhyList, qPopSuperList[1])
        if len(qPopSuperList[0]) == 0:
            print('tried everything, nothing started')
        return qPopSuperList, qLine, flowData

        
    else: # then we have a bit more work to do...
        # Rebuild flowData here
        while len(qLine[1]) > 0:
            try:
                flowData = flowDataRefresh(qLine[0])
                rGramLine = nltk.pos_tag(rAllLines) # Check the present line's grammar
                keepList, gKeepList = proxP1[qLine[1][-1]], gramProxP1[qLine[1][-1]]
            except KeyError:
                print(qLine[1], "=KError")
                qLine[1].pop()
                if len(qLine[1]) != 0:
                    continue
                else:
                    print('crash')
                    break            
        for all in proxNumList:
            proxList = proxLib[all][qLine[pLineNList[pLNi]]]
            keepList = proxSorter(proxList, keepList)
            if gramKill == 0: # gramKill == 0 means we are looking for grammar. gramKill == 1 means we are not.
                gProxList = gramProxLib[all][rrGramLine[pLineNList[pLNi]]]
                gKeepList = proxSorter(gProxList, gKeepList)
                killList = []
                for each in keepList:
                    testLine = []
                    for each in qLine[1]: # instead of saying testLine = qLine[1], because then they're linked. testLine should change and qLine[1] should stay immutable
                        testLine.append(each)
                    gTestLine = nltk.pos_tag(testLine)
                    if gTestLine[-1] not in gKeepList:
                        killList.append(each)
                for each in killList:
                    keepList.remove(each) # this filters against bad grammar choices in our popList
            if len(keepList) == 0: # then there are no viable choices
                if len(proxNumList) <= min(0,proxMinDial): # see if our chain has reached a minimum.
                    if gramKill == 0: # then we were looking for grammar.
                        print('gramKill on')
                        gramKill == 1 # stop looking for grammar, because it sometimes blocks progress
                    else: # then we're out of options on proximity alone
                        if allLinesLine[-1] in endPunx: # if its the end of a sentence, we make a special exception, refresh the list with firstWords
                            return qPopSuperList, qLine, flowData
                        else:    
                            qLine = qLine[0][:-1], qLine[1][:-1]
                        if len(qLine[0]) == 0: # then we've cut down to an empty line. Return failData
                            return qPopSuperList, qLine, flowData
                else:
                    flowData = proxNumList[1:], pLNi-1, pLineNList[1:]
    
            else:
                pLNi+=1
                return qPopSuperList, qLine, flowData
    # if this fails for some reason, it'll return a blank keepList and print an indicator
    print('popListMaker failed!')
    return qPopSuperList, qLine, flowData


# # #               

def popListDigester(qPopSuperList, qLine, contrabandQLines, firstWords):
    while len(qPopSuperList[0]) > 0: # keep moving forward as long as we keep getting non-empty lists
        pWord = qPopSuperList[0].pop(qPopSuperList[0].index(random.choice(qPopSuperList[0])))
        if pLine+[pWord] not in contrabandLines: # This will screen against trees already explored
            pLEmps, qLine, flowData = wordAdder(pWord, qPopSuperList, qLine, pLEmps)
            pLEmps, qPopSuperList, qLine, flowData = wordWriter(empKey, qAllLines, qLine, qPopSuperList, flowData, gramSwitch, rhyList, firstWords)
    while len(qPopSuperList[0]) == 0: # keep cutting back until you have another list to pop from
        qPopSuperList, qLine, flowData,  contrabandQLines, contrabandRLines = wordSubtracter(qPopSuperList, qLine, flowData, empsLine, tagEmpsLine, contrabandQLines)
        qPopSuperList, qLine, flowData = wordWriter(empKey, qAllLines, qLine, qPopSuperList, flowData, gramSwitch, rhyList, firstWords)

    return qPopSuperList, qLine, flowData, contrabandQLines


def wordSubtracter(empsLine, tagEmpsLine, subtractThisMany):

    # by blacklisting the arrangement of words, we stop the lineBuilder from testing combinations we've already exhausted
    contrabandQLines = append(pLine)
    contrabandRLines.append(qLine[1])

    # take everything back a bit
    qPopSuperList, qLine = pPopSuperList[:-subtractThisMany], qPopSuperList[1][:-subtractThisMany], pLine[:-subtractThisMany], qLine[1][:-subtractThisMany]
    flowData = proxNumList[:-subtractThisMany], pLNi-subtractThisMany, pLineNList[subtractThisMany:] 
    
    cutCt = int(0)
    while cutCt < subtractThisMany:
        testInt, cutPoint = int(0), int(0)
        while testInt < len(tagEmpsLine):
            if tagEmpsLine[testInt] not in empsList:
                cutPoint = testInt
                print(cutPoint, empPoint)
            testInt+=1            
        empsLine = empsLine[:-(len(tagEmpsLine[cutPoint+1:]))]
        tagEmpsLine = tagEmpsLine[:cutPoint]
        cutCt+=1

    return qPopSuperList, qLine, flowData, empsLine, tagEmpsLine, contrabandQLines


def wordAdder(pWord, rWord, qLine, pLEmps):

    try:
        pWEmps = emps[pWord.lower()]
    except KeyError:
        try:
            pWEmps = emps[pWord]
        except KeyError:
            pWEmps = ['3']
    pLEmps = pLEmps+pWEmps
    qLine = qLine[0]+[pWord], qLine[1]+[rWord]
    flowData = flowDataRefresh(qLine[0])
    
    return pLEmps, qLine, flowData


def plainLiner(pLine, pLineLen): # This would build lines not subject to meter and rhyme
    if len(pLine) == 0:
        pLine = [firstWords[firstWords.index(random.choice(0, len(firstWords)))]]
    else:
        pList = proxP1[pLine[-1]]
        flowData = flowDataReboot([pLine, pLine])
    keepList, gKeepList = proxP1[qLine[1][-1]], gramProxP1[qLine[1][-1]]
    print('itIs == itIs') # build this later


def poemLiner(empKey, writQLines, rhyList, metSwitch, theSwitch, gramSwitch, firstWords, proxMinDial, proxMaxDial, punxChoice, contrabandLines):

    writPLines, writRLines = writQLines
    qLine, pAllLines, qAllLines, rAllLines, pLEmps, qPopSuperList = [[],[]], [], [[],[]], [], [], [[],[]]
    flowData = flowDataRefresh(qLine)
    proxNumList, pLNi, pLineNList = flowData
    pPopSuperList, rPopSuperList = qPopSuperList
    print('poemLiner begin')
    while (pLEmps != empKey) and (len(pLEmps) != len(empKey)): # Search for a word that matches the declared meter template, line may need to rhyme (flawed logic here...) and ((len(rhyList)>0) or (pLine[-1] not in rhyList)) and metSwitch == 1 and (pLine[-1] not in quantumList)

        qAllLines = [], [] # rebuild allLines with immutable 'writ' variables and current, evolving pLine and qLine[1]
        if len(writQLines[0]) > 0:
            for all in writQLines[0]:
                pAllLines.append(all)
        if len(qLine[0]) > 0:
            for all in qLine[0]:
                pAllLines.append(all)
        if len(writQLines[1]) > 0:
            for all in writQLines[1]:
                writQLines[1].append(all)
        if len(qLine[1]) > 0:
            for all in qLine[1]:
                qLine[1].append(all)

        print('qAll:', qAllLines)

        if len(qLine[1]) == 0: # Check to see if we already have the first word:
            print('pLa', pAllLines)
            if len(pAllLines) == 0: # If there are no lines yet
                qPopSuperList = [[]], [[]]
                for all in firstWords:
                    pWord = all.lower()
                    try:
                        firstEmps = emps[pWord]  # Declare these variables to save time during their repeat use in the next conditionals
                        empLen = len(firstEmps)
                        if empLen <= len(empKey):
                            if (firstEmps == empKey[:empLen]) or (empKey[0] == -1): # Save time and screen against ones that don't fit anyway
                                qPopSuperList[0].append(pWord)
                                qPopSuperList[1].append(pWord)
                    except KeyError:
                        continue
                if len(qPopSuperList[0]) == 0:
                    dynaWords, theReverends = dynaMight(firstWords, empKey, theReverends)
                    if len(dynaWords) == 0:
                        print('not even the dynasaurus can start this.')
                        return []#to a land of pure imagination
                    else: # use the dynaWord on pLine, utilize theReverends to figure which corresponding word goes onto qLine[1]
                        qLine = qLine[0]+[qPopSuperList[0].pop(qPopSuperList[0].index(random.choice(0,len(qPopSuperList[0]))))], qLine[1]+[qPopSuperList[1].pop(qPopSuperList[1].index(theReverends[0][qLine[0][0]]))] 
                        theReverends[0].remove(qLine[0][0]) # remove that entry
                    for all in emps[qLine[0][0]]:
                        pLEmps, tagPLEmps = addWordData(qLine[0][0], pLEmps, tagPLEmps)
                else:
                    pPSLLen = len(qPopSuperList[0])
                    pWord = qPopSuperList[0].pop(qPopSuperList[0].index(random.choice(qPopSuperList[0])))
                    qLine[0].append(pWord)
                    qLine[1].append(pWord)
                print('1')                                        
                qPopSuperList, qLine, flowData = wordWriter(empKey, qAllLines, qLine, qPopSuperList, flowData, gramSwitch, rhyList, firstWords) # Start with the list of first words
            else:
                print('2')
                qPopSuperList, qLine, flowData = wordWriter(empKey, qAllLines, qLine, qPopSuperList, flowData, gramSwitch, rhyList, firstWords)
        else: # If we got at least the first word, automatically continue, looping this function:
            print('pLb')
            qPopSuperList, qLine, flowData = wordWriter(empKey, qAllLines, qLine, qPopSuperList, flowData, gramSwitch, rhyList, firstWords)
            while len(qPopSuperList[0]) > 0: # keep moving forward as long as we keep getting non-empty lists
                pWord = qPopSuperList[0].pop(qPopSuperList[0].index(random.choice(qPopSuperList[0])))
                if qLine[0]+[pWord] not in contrabandLines: # This will screen against trees already explored
                    pLEmps, qLine, flowData = wordAdder(pWord, qPopSuperList, qLine, pLEmps)
                    pLEmps, qPopSuperList, qLine, flowData = wordWriter(empKey, qAllLines, qLine, qPopSuperList, flowData, gramSwitch, rhyList, firstWords)
            while len(qPopSuperList[0]) == 0: # keep cutting back until you have another list to pop from
                qPopSuperList, qLine, flowData, contrabandQLines = wordSubtracter(qPopSuperList, qLine, flowData, empsLine, tagEmpsLine, contrabandQLines)
                qPopSuperList, qLine, flowData = wordWriter(empKey, qAllLines, qLine, qPopSuperList, flowData, gramSwitch, rhyList, firstWords)
        if len(qLine[0]) == 0:
            print('pLc')
            #if (len(proxNumList) < proxMinDial):
                #if pLine[-1] in endPunx:
            for all in firstWords:
                qPopSuperList = pPopSuperList+[all], rPopSuperList+[all] # should I keep this here? The p- and r- prefixes are being fazed out
                    #allow the program to continue using firstWords as a new starting point. Cut the empKey down to only the remainder of the line.
##            else:
##                print('pLd')
##                return [], [] # no results, go back a line
    if (pLEmps != empKey) and (len(pLEmps) != len(empKey)) and ((len(pRhymeList)==0) or (qLine[0][-1] in rhyList)):
        print('pLe')
        return qLine
    elif (pLEmps != empKey) and (len(pLEmps) != len(empKey)) and (qLine[0][-1] not in rhyList) and (len(pRhymeList) > 0): #
        pLEmps = pLEmps[:-(len(emps[qLine[1].pop()]))] # One line removes the word from the qLine[1] and the emps of pLine
        print('shouldnt happen')
        if len(popList) > 0:
            result = lineAdvancer(popList, empKey)
            return qLine
        else:
            print('breakpointA')
            return [], []
    else:
        print('failboat')
        return [], []

# # #                   


def testPoemLine(newPLine, writQLines, writIndex):
    print('testPoemLine')
    if len(newPLine) > 0: # anything that results in failure from poemLiner will return a line with len==0, the implicit else is that nothing is added. Start over.
        writQLines = writPLines+[newPLine], writRLines+[newRLine]
    elif len(writQLines[0]) > 0:
        writQLines = writPLines[:-1], writRLines[:-1]
    writIndex = len(writQLines[0])
    print(writQLines, writIndex)
    return writQLines, writIndex


def stanzaWriter(rhymeMap, meterMap, rhySwitch, metSwitch, theSwitch, gramSwitch, firstWords, usedList, startTimeM, startTimeH, proxMinDial, proxMaxDial, punxChoice, contrabandLines):
    writQLines = [], []
    writIndex = int(0)
    pPopSuperList, rPopSuperList, contrabandLines = [[]], [[]], [[]]
    qPopSuperList = [pPopSuperList, rPopSuperList]
    pLine, rLine = [], []
    qLine = [pLine, rLine]
    writPLines, writRLines = [], []
    writQLines = [writPLines, writRLines]
    pAllLines, rAllLines = [], []
    qAllLines = pAllLines, rAllLines
    if rhySwitch == 0 and metSwitch == 0: # then we have rhyme and meter in the template
        while len(writQLines[0]) < min(len(meterMap), len(rhymeMap)):
            print('stanzaWriter1')
            if len(writQLines[0]) == 0:
                print('sWa')
                newPLine, newRLine = poemLiner(meterMap[0], [[],[]], [], metSwitch, theSwitch, gramSwitch, firstWords, proxMinDial, proxMaxDial, punxChoice, contrabandLines)
            elif writIndex != rhymeMap.index(rhymeMap[writIndex]): # then the present rhyme token isn't the first in rhymeMap; we need a rhymelist.
                print('sWb')
                checkPunx, checkRhy = -1, '.'
                while checkRhy in endPunx:
                    checkRhy = writQLines[0][rhymeMap.index(rhymeMap[writIndex])][checkPunx]
                    checkPunx-=1
                rhyWords = gF.rhyDictator(checkRhy, 10, 10) # Submit these as lists, it'll enable ranges of values!
                if len(rhyWords) == 0: # then we didn't find any rhymes for that line. We cut all the way back.
                    writQLines = writQLines[0][:rhymeMap.index(rhymeMap[writIndex])], writQLines[1][:rhymeMap.index(rhymeMap[writIndex])]
                    if len(writQLines[0]) > 0: # then we're going to give the last lines as our pLine and qLine[1], so testPoemLiner doesn't cut one off by accident. If there are no lines, no bother.
                        newPLine = writQLines[0].pop()
                        newRLine = writQLines[1].pop()
                else:
                    newPLine, newRLine = poemLiner(meterMap[writIndex], writQLines, rhyWords, metSwtich, theSwitch, gramSwitch, firstWords, proxMinDial, proxMaxDial, punxChoice, contrabandLines) # feed the rhyList and the anteLines into poemLiner, depending on the writIndex count
            else: # then we have an unrhyming line that is after another. No rhymes, but anteLines
                print('sWc')
                newPLine, newRLine = poemLiner(meterMap[writIndex], writQLines, [], metSwtich, theSwitch, gramSwitch, firstWords, proxMinDial, proxMaxDial, punxChoice, contrabandLines)
            writQLines, writIndex = testPoemLine(newPLine, writQLines, writIndex)
    elif rhySwitch == 1 and metSwitch == 0: # then we have meter but not rhyme
        while len(writQLines[0]) < len(meterMap):
            print('stanzaWriter2')
            newPLine, newRLine = poemLiner(empKey, writQLines, [], metSwtich, theSwitch, gramSwitch, firstWords, proxMinDial, proxMaxDial, punxChoice, contrabandLines)
            writQLines, writIndex = testPoemLine(newPLine, writQLines, writIndex)
    elif rhySwitch == 0 and metSwitch == 1: # then we have rhyme but not meter
        while len(writQLines[0]) < len(rhymeMap): # do poemLiner with rhymeMap, not empKey. Warning: if emps are different in matched lines, no rhymes will yield.
            print('stanzaWriter3')
            for each in meterMap: # The value of -1 will tell poemLiner to ignore it
                for all in each:
                    all = -1
            rhyWords = gF.rhyDictator(writQLines[0][rhymeMap.index(rhymeMap[writIndex])], 10, 10)
            newPLine, newRLine = poemLiner(empKey, writQLines, rhyWords, metSwtich, theSwitch, gramSwitch, firstWords, proxMinDial, proxMaxDial, punxChoice, contrabandLines)
            writQLines, writIndex = testPoemLine(newPLine, writQLines, writIndex)
    else:
        plainLiner() 
    if len(writQLines[0]) == len(rhymeMap): # success, hopefully!
        for each in writQLines[0]:
            print(each)
    else:
        print("we don't have enough lines")
            
        
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
        print('writing...', all)
    newFirstFile.close()


def startWemyx():
    print('\nstarting remix')
    textFile = textChoice.get() # superBible
    texto = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())
    rhymeMap=str()
    meterMap, usedList, lastList, metaBlackList = [], [], [], []
    metSwitch, rhySwitch, theSwitch, gramSwitch = meterVar.get(), rhymeVar.get(), thesaVar.get(), grammVar.get()
    proxMinDial, proxMaxDial, punxDial = int(proxMinChoice.get()), int(proxMaxChoice.get()), int(punxChoice.get())
    print('starting proxBuilds')
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
    
    print(metSwitch, rhySwitch, rhymeMap, meterMap, proxMinDial, punxDial)

    texto = texto.replace('Mr.', 'Mister')
    texto = texto.replace('Mrs.', 'Missus')
    texto = texto.replace('Ms.', 'Miss')
    texto = texto.replace('Dr.', 'doctor')

    for all in endPunx:
        texto = texto.replace(all, ' '+all)
    for all in badGrams:
        texto = texto.replace(all, '')
    superTokens = nltk.word_tokenize(texto)

    ##  This part loads data that allows the computer to read meter, phonetics,
    ##  and to differentiate between similarly-spelled words

    # Now Wemyx fills the empty dictionaries it created

    firstWords, yaFound, nextSentenceIndexes, theReverends = [], [], [], []
    lastSpot, wordsI, click, proxNumerator, proxDicCounter = len(superTokens), int(-1), int(0), int(1), int(0)

    try:
        compFile = open('data/textLibrary/textData/'+textFile+'-compFile.txt', 'r')
        firstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'r')
        for line in firstFile:
            firstWords.append(line[:-1])
        proxPlusLista = gF.gpDataOpener(proxPlusLista, 'proxP', textFile)
        for each in proxPlusLista:
            print(len(each))
        proxMinusLista = gF.gpDataOpener(proxMinusLista, 'proxM', textFile)
        for each in proxPlusLista:
            print(len(each))
        gramProxPlusLista = gF.gpDataOpener(gramProxPlusLista, 'gramP', textFile)
        for each in proxPlusLista:
            print(len(each))
        gramProxMinusLista = gF.gpDataOpener(gramProxMinusLista, 'gramM', textFile)
        for each in proxPlusLista:
            print(len(each))
        dynaSaurus = gF.dynaDataOpener(textFile, 'thes')
        print('done with builds')
                    
    except FileNotFoundError:
        superTokenData = nltk.pos_tag(superTokens)
        superTokenWords, superTokenGrams = [], []
        for each in superTokenData:
            #print(each)
            superTokenWords.append(each[0])
            superTokenGrams.append(each[1])
        for key, val in supersaurus.items():
            dynasaurus[str(key)] = val
            quickToke = each[1][0]
            if quickToke in dynaPOS:
                if quickToke == 'N':
                    dynasaurus[str(each+'.'+each[1][0])] = supersaurus[pWord]
                if quickToke == 'V':
                    dynasaurus[str(each+'.'+each[1][0])] = supersaurus[pWord]
                if quickToke == 'R':
                    dynasaurus[str(each+'.'+each[1][0])] = supersaurus[pWord]
                if quickToke == 'J':
                    dynasaurus[str(each+'.'+each[1][0])] = supersaurus[pWord]
        
        gF.dynaDataWriter(dynasaurus, textFile, 'thes')

        
        print('len(superTokenData):', len(superTokenData), '\nlen(superTokenGrams):', len(superTokenGrams), '\n', superTokenData[1000:1200], superTokenGrams[1000:1200], '\ncontinue?')
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
                        print('plusadd = gramProx:', gramProxWord, 'gramPWord:', gramPWord)
                        gramProxPlusLista[proxDicCounter][gramPWord].append(gramProxWord)
                    if gramPWord not in gramProxMinusLista[proxDicCounter][gramProxWord]:
                        print('minusadd = gramProx:', gramProxWord, 'gramPWord:', gramPWord)
                        gramProxMinusLista[proxDicCounter][gramProxWord].append(gramPWord)
                    proxDicCounter+=1
                    proxNumerator+=1
            except IndexError:          
                continue
            except KeyError:
                print('kE build:', pWord, proxWord, proxDicCounter, proxNumerator)
                proxDicCounter+=1  ## These are the lines you edited
                proxNumerator+=1   ## Check to see if they did anything significant
                continue
    if click > 0:
        newFirstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
        for all in firstWords:
            newFirstFile.write(all+'\n')
        print('writing...', all)
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

    proxNumList, pLNi, pLineNList = [], int(0), []
    flowData = proxNumList, pLNi, pLineNList

    rCt = int(0)
    poemCt = int(poemNum.get())
    while rCt<poemCt:
        rCt+=1
        print('\n\nPoem #'+str(rCt)+'\n'+str(datetime.datetime.now())+'\n')
        #try:
            ## A timer is used to restart the process if it stalls on a long loop. It feeds into the stanzaWriter function.
        startTimeM = int(str(datetime.datetime.now())[14:16])
        startTimeH = str(datetime.datetime.now())[11:13]
        usedList, contrabandLines = [], [[]] # to prevent repeat words
        usedList = stanzaWriter(rhymeMap, meterMap, rhySwitch, metSwitch, theSwitch, gramSwitch, firstWords, usedList, startTimeM, startTimeH, proxMinDial, proxMaxDial, punxChoice, contrabandLines)
        if usedListSwitch == 1:
            usedList = ['']
##        except:
##            startTimeM = int(str(datetime.datetime.now())[14:16])
##            startTimeH = str(datetime.datetime.now())[11:13]
##            usedList = []
##            usedList = stanzaWriter(rhymeMap, meterMap, usedList, emps, firstWords, startTimeM, startTimeH)
##            if usedListSwitch == 1:
##                usedList = ['']
##            continue
        
    print('\nremix complete')


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
halfBeatVar = IntVar() # regulates whether to allow additional half-beats during non-emphasis syllables
Checkbutton(master, text="half-beats", variable=halfBeatVar).grid(row=4, column=0, sticky=W)
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


print('loading metadatas...')

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


print('opening fonoFiles')
vocs = gF.globalOpen('data/USen/vocDic-USen-MAS.csv', 'string')
cons = gF.globalOpen('data/USen/conDic-USen-MAS.csv', 'string')
fono = gF.globalOpen('data/USen/fonDic-USen-MAS.csv', 'string')

print('opening dynasaurus')
supersaurus = {}
for each in 'ADJ', 'ADV', 'NOUN', 'VERB':
    thesFile = open('data/USen/dynasaurus/thes-'+each+'.csv')
    for line in thesFile:
        supersaurus[line[0]] = line[1].split('^')





























##################
## Errata                   

##    elif len(qLine) == 1: # a special condition, since a single word out of context doesn't lend much to guide it
##        try:
##            for all in proxP1[qLine[0]]
##                if (emps[all] == empKey[:len(emps[all])]):
##                    gram1 = nltk.pos_tag(qLine)
##                    gram2 = nltk.pos_tag(all)
##                    if gram2 in gramProxP1[gram1]:
##                        goList[1].append(all)
##            if len(goList[1]) == 0:
##                for all in proxP1[qLine[0]]
##                    if (emps[all] == empKey[len(emps[all])]):
##                        goList[1].append(all)
##            flowData = [0], 0, [0], proxMinDial, proxMaxDial
##            return qPopSuperList, qLine, flowData
##        except KeyError:
##            print('kE1 in popList maker = (firstWords):', all)
##            return qPopSuperList, qLine, flowData

       

##def lineAdvancer(pList, pEmpKey, rhymeList, theSwitch): # "theSwitch"==thesaurus switch, used to check if the thesaurus has been activated, prevents infinite loop
##    #print('Entering lineAdvancer')
##    pLEmps = []
##    pLELen = int(0)
##    while ((pLEmps != empKey[:len(pLEmps)]) or (pLELen == 0)) and (len(popList) > 0):
##        #print('A, len(popList) =', len(popList))  #  Shows that we've entered this loop, prints length of our shrinking list
##        pLEmps = pLEmps[:(-pLELen)]
##        qLine[1].append(pList.pop(random.choice()))
##        pLEmps = gF.getEmps(str(qLine[1][-1]))
##        pLELen = len(pLEmps)
##        if pLEmps != empKey[:-(len(pLEmps))]: # Check to see if the word matches the prescribed meter
##            pLEmps = pLEmps[:-(len(emps[qLine[1].pop()]))] # One line removes the word from the qLine[1] and the emps of pLine
##        else: # If we found the right word, we go here
##            #  These next few lines amend the governing lists that control the Markov chains
##            if len(proxNumList) > 0:
##                proxNum = proxNumList[-1] + 1
##            else:
##                proxNum = 0
##            proxNumList.append(proxNum)
##            pLineNum = pLineNList[0] + 1
##            pLineNList.insert(0, pLineNum)
##            expressList = []
##            if len(proxNumList) > 0:
##                proxNum = proxNumList[-1] + 1
##            else:
##                proxNum = 0
##            for all in rhymeList:
##                expressList.append(all)
##            return stuffs
##    if ((pLEmps != empKey[-(len(pLEmps)):]) or (pLELen == 0)) and (len(popList) > 0): # If we exit the loop, it means we exhausted our have no word
##        #print('B')
##        if theSwitch == true:
##            theSwitch = false # this way, we only try it once. Next pass, we won't enter this section
##            dynaList = dynaMight(pList, empKey)
##            data data = lineAdvancer(dynaList, pEmpKey, theSwitch) # lineAdvancer calls itself by plugging in synonyms from the initial pList, 
##        else: # 
##        
##        
##    return stuffs

