

####

#   To-do list:
#   - standardize thesaurus tags, write to file words that don't have entries
#   - ensure halfbeats are viable
#   - discriminate against capital words
#   - store unknown words into a file to be handled later
#   - create linemakers that don't follow meter

#  GLOSSARY

#  Three prefixes are used to distinguish the dual-layer lines. 
#  p - May be thought as the phonetic line, or the printed line. This is what will be shown as end-product
#  q - May be thought as the quantum line, because it enjoins both p and r lines in a sort of superposition to be analyzed separately and together
#  r - May be thought as the retracted or referral line, because it shows what the pLine says alternatively
#  qAnteData = [qAnteLine], qAnteBlackList, qAntePopList]


##########
##  declaration of libraries
##########


from string import *
from tkinter import *
import ___gloFunk as gF # Make sure to remove underscores later
import nltk
from nltk import wordnet as wn
import random
import datetime
import time
import csv
import inspect
csv.field_size_limit(int(9999999))


##########
##  basic, essential, universal functions & lists
##########


def lineno():     ##  Returns the current line number in our program.
    return inspect.currentframe().f_back.f_lineno


quantumList = ['and', 'to', 'for', 'a', 'the', 'in', 'at', 'but']  #  List of words used for quantum emp patterns
nonEnders = ['and', 'or', 'a']

allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '"', "''", '-', '\\', '+', '=', '/', '<', '>']  #  Doesn't include apostrophe, because that could be part of a contraction
midPunx = [',', ';', ':', '--']
endPunx = ['.', '!', '?']  #  To gather which words immediately thereafter should start a sentence

bannedChops = ['@', '#', '&', '*', '\\', '+', '=', '/', '<', '>']


##########
##  text and library preparation
##########


def rawToSegBank(rawText):
    
    print(lineno(), 'rawToSegBank begin\nlen(rawText) =', len(rawText))  # to show that textPrep has started
    rawText = rawText.replace('\n', ' ')  #  First clean up some meta-bits that inhibit text digestion
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


    #  Tokenizes raw text, grooms into lists of words
    splitText = rawText.split(' ')  # The reason for placing a space between all tokens to be grabbed
    segmentBank = []  #  To contain the lists of groomed "segments"
    thisSegment = []
    firstWords = []
    
    sTLen = len(splitText)  #  Save processes in while loop by measuring this now
    sTIndex = int(0)  #  Will use this to count the way along splitText, starting at zero index
    splitWord = splitText[sTIndex]  #  Starting off the word scan

    print(lineno(), 'building segments...\nlen(splitText) =', len(splitText), '|', sTIndex)
    while sTIndex < sTLen:  #  Checks over and over whether we've arrived at the end
        thisSegment.append(splitWord)  #  Keeping a running track of words for prokLibs to crunch
        try:  #  For indexError
            try:  #  For other errors
                if splitWord in endPunx:  #  Treating each in endPunx like another word, except to scan for firstWords
                    newFirstWord = splitText[sTIndex+1]  #  Looks at the next word
                    #print(lineno(), 'endPunk:', splitWord, newFirstWord)
                    if (newFirstWord not in firstWords) and (newFirstWord not in allPunx) and (newFirstWord not in bannedChops):  #  If the next word is a valid word
                        try:
                            if newFirstWord not in doubles:
                                emps[newFirstWord]
                                firstWords.append(newFirstWord)
                            else:
                                firstWords.append(newFirstWord)  #  This list gives a launching point for new, zero-length lines. Isn't triggered on an except line. Also continues segments.
                            sTIndex+=1
                            splitWord = newFirstWord
                            #print(lineno(), 'added', newFirstWord, 'to firstWords')
                        except KeyError:
                            lowWord = newFirstWord.lower()  #  Maybe it works if it's not capitalized? If
                            #print(lineno(), newFirstWord, lowWord, '| attempting lowercase version')
                            try:
                                if lowWord not in doubles:
                                    emps[lowWord]
                                    firstWords.append(lowWord)
                                    firstWords.append(newFirstWord[0].upper()+lowWord[1:])
                                else:
                                    firstWords.append(lowWord)
                                    firstWords.append(newFirstWord[0].upper()+lowWord[1:])
                                sTIndex+=1
                                splitWord = newFirstWord
                                #print(lineno(), 'lowercase made for', newFirstWord)
                            except KeyError:
                                #print(lineno(), 'kE =', newFirstWord+'/'+lowWord)
                                bannedChops.append(newFirstWord)
                                bannedChops.append(lowWord)
                                sTIndex+=1
                                splitWord = newFirstWord
                                continue
                            continue
                elif splitWord in bannedChops:  #  A set of strings which would terminate a segment
                    #print(lineno(), 'emps69')
                    emps[int(69)]  #  Trigger an error, which performs the same operations needed here
                sTIndex+=1
                splitWord = splitText[sTIndex]
            except KeyError:  #  The word wasn't recognized, either by proper name, unusual spelling, or containing unfit encoding, either ValueError, KeyError, or otherwise
                #print(lineno(), 'kE =', splitWord)
                segmentBank.append(thisSegment)
                thisSegment = []
                sTIndex+=1
                splitWord = splitText[sTIndex]
                continue
            except ValueError:
                #print(lineno(), 'vE =', splitWord)
                segmentBank.append(thisSegment)  #  Perhaps a resetSegment()
                thisSegment = []
                sTIndex+=1
                splitWord = splitText[sTIndex]
                continue  #  Advance to the next token, but I should create a log for these incidents...
        except IndexError:  #  If we're at the end of the document, we're done
            #print(lineno(), 'Index break:', sTLen, '|', sTIndex)
            break

    biggestLen = int(0)
    biggestLin = []
    for each in segmentBank:
        if len(each) > biggestLen:
            biggestLin = each
            biggestLen = len(each)
    print(lineno(), 'segments complete\nlen(firstWords):', len(firstWords), '\nlen(segmentBank):', len(segmentBank), '\nSegment samples:\n', segmentBank[10:5], '\nLargest segment:', biggestLen, biggestLin)
    #input('Press Enter to continue')
    return segmentBank, firstWords


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
  


def proxLibBuilder(thisLib, thisFile, segmentBank, exhaustList, textFile):  #  Another subfunction for loadmakeData. 'thisLib' is either proxLib or gramProxLib, 'specialText' is either splitText or superTokenGrams
        print(lineno(), 'proxLib', thisFile)
        for all in range(0, (len(proxPlusLista))):  #  Now that we've got an exhaustive list of real words, we'll create empty lists for all of them (could this get pre-empted for common words?)
            for each in exhaustList:
                proxPlusLista[all][each] = []
                proxMinusLista[all][each] = []
        for all in segmentBank:  #  Because we divided bits by their segments
            segment = all
            segmentLen = len(segment)
            segmentIndex = int(0)
            print(lineno(), 'newSegment', segmentLen) 
            while segmentIndex < segmentLen:
                try:
                    pWord = segment[segmentIndex]
                    proxNumerator, proxDicCounter, proxMax = int(1), int(0), len(thisLib[0])
                    while proxDicCounter < proxMax:
                        proxWord = segment[segmentIndex+proxNumerator]
                        if proxWord not in thisLib[0][proxDicCounter][pWord]:
                            #$ print(lineno(), 'plusadd = proxP:', proxWord, 'pWord:', pWord)
                            thisLib[0][proxDicCounter][pWord].append(proxWord)
                        if pWord not in thisLib[1][proxDicCounter][proxWord]:
                            #4 print(lineno(), 'minusadd = proxM:', proxWord, 'pWord:', pWord)
                            thisLib[1][proxDicCounter][proxWord].append(pWord)
                        proxDicCounter+=1
                        proxNumerator+=1
                        segmentIndex+=1
                except IndexError:
                    #print(lineno(), "iE pLBuilder", pWord, proxWord, proxDicCounter, proxNumerator)
                    #print(lineno(), thisLib[0][0][pWord])
                    segmentIndex+=1
                    if segmentIndex == segmentLen:
                        break
                    continue
                except KeyError:
                    #print(lineno(), 'kE build:', pWord, proxWord, proxDicCounter, proxNumerator)
                    proxDicCounter+=1  ## These are the lines you edited
                    proxNumerator+=1   ## Check to see if they did anything significant
                    continue
        print(lineno(), 'writing proxLibs...')
        gpDataWriter(thisLib[0], thisFile[0], textFile)
        gpDataWriter(thisLib[1], thisFile[1], textFile)
        return thisLib


def loadmakeData(textFile):

    proxMaxDial = 19
    #$ print(lineno(), 'begin loadmakeProxLibs()')
    #  Prox and gramprox store Markov chains and build in -Liner() functions
    #  Libs declared here, made into lists of dics of lists, and called using indices on 
    global proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20
    global proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20
    global proxPlusLista, proxMinusLista, proxLib # gramProxLib, gramProxPlusLista, gramProxMinusLista
    #  These dictionaries contain lists of words that come after 
    proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20 = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}] 
    proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20 = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]      
    #  The dictionaries are organized into lists that are accessed by index. Useful in while loops with ascending/descending numbers
    proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20]
    proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20]
    #  The maximum length of theseslists are truncated based on the user's initial input
    proxPlusLista = proxPlusLista[:proxMaxDial]
    proxMinusLista = proxMinusLista[:proxMaxDial]
    #  The two lists for each library type are combined into one variable apiece
    proxLib = proxPlusLista, proxMinusLista #[gramProxPlusLista, gramProxMinusLista]

    #  'Try' statements will attempt to load existing data. FileNotFoundErrors will build what's missing.
    #  Rather than use just one try/except section, I divided it so it can skip the ones already created. Usually, it'll just build all or none.
    firstWords = []
    try:
        print(lineno(), 'begin fwFile load') 
        firstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'r')
        global firstPopList
        firstPopList = []
        for line in firstFile:
            firstWords.append(line[:-1])
            firstPopList.append(line[:-1])
            
    except FileNotFoundError:
        print(lineno(), 'fwFile not found')
        rawText = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())
        segmentBank, firstWords = rawToSegBank(rawText)
        newFirstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
        print(lineno(), 'writing fwFile...')
        for all in firstWords:
            newFirstFile.write(all+'\n')
        newFirstFile.close()
        print(lineno(), 'fw complete')

    try:
        print(lineno(), 'begin prox load')        
        #  Take a look at gpDataOpener. Consider moving more code there, or bring some here
        proxPlusLista = gF.proxDataOpener(proxPlusLista, 'proxP', textFile)
        proxMinusLista = gF.proxDataOpener(proxMinusLista, 'proxM', textFile)
        print(lineno(), 'prox load complete')
            
    except FileNotFoundError:
        print(lineno(), 'initial files for', textFile, 'not found')
        try:
            len(segmentBank)
        except UnboundLocalError:
            rawText = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())
            segmentBank, firstWords = rawToSegBank(rawText)
        exhaustList = []  #  Creating an exhaustive list of words to enter into data files
        for all in segmentBank:
            for each in all:
                if each not in exhaustList:
                   exhaustList.append(each)
        print(lineno(), 'starting proxbuilds')
        proxLib = proxLibBuilder(proxLib, ['proxP', 'proxM'], segmentBank, exhaustList, textFile)
            
    return proxLib, {}, firstWords


def proxDataReboot(pLine):  # Recreates the proxData used in proxWords()
    pCt = int(0)
    proxNumList = []
    pLineNList = []
    while pCt < len(pLine):
        proxNumList.append(pCt)
        pLineNList.insert(0, pCt)
        pCt+=1
    pLNi = pCt
    return [pLineNList, pLNi, proxNumList]


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


def removeWordL(superPopList, superBlackList, qLine):  #  Remove the leftmost word from line
    return data


def removeWordR(superPopList, superBlackList, qLine):  #  Remove the rightmost word from line
    proxNumList.append(proxNum)
    pLineNum = pLineNList[0] + 1
    pLineNList.insert(0, pLineNum)


def acceptWordL(pLine, proxData, nextWord, rhymeList, superPopList, superBlackList):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    print('acceptWord:', pLine, '|', nextWord, len(superPopList))
    pLine.append(nextWord)
    if len(proxNumList) > 0:
        proxNum = proxNumList[-1] + 1
    else:
        proxNum = 0
    proxNumList.append(proxNum)
    pLineNum = pLineNList[0] + 1
    pLineNList.insert(0, pLineNum)
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
    print('len(superPopList):', len(superPopList))

##
    
    return pLine, pLineNum, pLineNList, proxNum, proxNumList, superPopList, expressList, superBlackList, jumpProxList


def acceptWordR(pLine, proxData, nextWord, rhymeList, superPopList, superBlackList):  #  Add word to right side of line
    print('acceptWord:', pLine, '|', nextWord, len(superPopList))
    pLine.append(nextWord)
    if len(proxNumList) > 0:
        proxNum = proxNumList[-1] + 1
    else:
        proxNum = 0
    proxNumList.append(proxNum)
    pLineNum = pLineNList[0] + 1
    pLineNList.insert(0, pLineNum)
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
    print('len(superPopList):', len(superPopList))
    return pLine, pLineNum, pLineNList, proxNum, proxNumList, superPopList, expressList, superBlackList, jumpProxList


def listSorter(mainList, frontList, rearList):  # places words in the front or back of a list
    switchList = []
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
    return organizedList


def superPopListMaker(superPopList, superBlackList, xLine, proxLineData, expressList): # 
    print(lineno(), 'superPopMaker begin')
    xLineLen = len(xLine)
    if xLineLen == 0:  #  If we've received a totally empty line, populate it with firstWords, but not directly or corrupt global bank
        startList = firstWordSuperPopList()
        return [startList]
    keepList = proxP1[xLine[-1]]
    for each in pLineNumList:
        testList = proxLibStuff[indexes]  #  The use of proxData comes into play by scanning the proxLibs and returning lists of words
        for all in keepList:
            if all not in testList or all in superBlackList[someIndex]:
                burnList.append(all)
        if len(keepList) > 0:
            for all in burnList:
                keepList.remove(all)
        else:  #  If we run out prematurely, stop iterating over the list
            break
    keepList = listSorter(keepList, expressList, [])
    superPopList.append(keepList) #  Even if the last entry is empty, we return it
    return superPopList


def plainDigester():
    return doo, doo


def metPopDigester(empLine, superPopList, qAnteLine, qLine, proxData):
    pLEmps = gF.empsLine(qLine[0], emps, doubles)
    while len(superPopList[-1]) > 0:
        pWord = superPopList[-1].pop(superPopList[-1].index(random.choice(superPopList[-1])))
        pWEmps = gF.empsLine([pWord], emps, doubles)
        testEmps = pLEmps + pWEmps
        if len(testEmps) <= len(empLine):  #  This is to screen against an error
            if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
                if pWord in contractionList:
                   qWord = contractionAction(qLine[0], pWord, -1)  #  Adds a contraction to the 
                   return superPopList, qWord
                else:
                    acceptWordR(qWord)
                    pLine, pLineNum, pLineNList, proxNum, proxNumList, superPopList, expressList, superBlackList, jumpProxList = acceptWordR(qLine)
                    return superPopList, qLine, proxData  #
        else:
            testEmps = testEmps[:-len(pWEmps)]  #  The word extended the line too far, so subtract it
    return superPopList, '', proxData  #  If we've run out of words, empty newWord

        
def firstWordSuperPopList():  #  Creates a superPopList that reloads the global firstWords list
    superPopList = [[]]
    for all in firstWords:
        superPopList[0].append(all)
    return superPopList


def makeList(listA):  #  Simple function that appends all from one list to other, so they are not bound together
    [] = listB
    for all in listA:
        listB.append(all)
    return listB
        
    
##############
#  line building


def vetoLine(qAnteLine):  #  Resets values in a line to 
    print(lineno(), 'resetLine')
    runLine = []
    for each in qAnteLine:  #  Re-create any qAnteLine as a mutable variable
        runLine.append(all)
    superPopList = firstWordSuperPopList()
    return runLine, superPopList, [int(0), int(0), int(0), []], [], False
          #runLine, qLine, proxData, rhymeList, redButton


def plainLinerLtoR(vars):
    data
    # without rhyme or meter


def plainLinerRtoL(vars):
    data


def meterLiner(qAnteLine, usedList, expressList, rhymeList, proxData, empLine):
    print(lineno(), 'meterLiner start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    qLine, runLine, pLEmps = [[],[]], [], []
    for all in qAnteLine[0]:  #  qAnteLine  
        runLine.append(all)
    while pLEmps != empLine:  #  Keep going until the line is finished or returns blank answer
        if (len(runLine) == 0) and (len(qLine[0]) == 0):  #  Check if we're starting with a completely empty line, load firstWords to superPopList if so
            print(lineno(), 'met if0')
            superPopList = firstWordSuperPopList() 
            superPopList, qLine, proxData = metPopDigester(empLine, superPopList, qAnteLine, qLine, proxData)
            if len(superPopList[0]) == 0 and len(qWord[0]) == 0:
                return superPopList, qAnteLine, qLine, usedList, True #  redButton event
            else:
                return superPopList, qAnteLine, qLine, usedList, False
        elif len(runLine) > 0:  #  Checks before trying to manipulate qAnteLine just below, also loops it so it subtracts from anteLine first
            print(lineno(), 'met if1')
            runLine = runLine + qLine[0]  #  Maybe qLine[0] is still nothing, but the whole stanza is one continuous line, in a sense of thinking
            superPopList = superPopListMaker(runLine)
            superPopList, qWord = superPopListDigester(superPopList, run)
            runLine = wordTester(empKey, runLine, qWord)
            if len(qWord[0]) == 0:  #  No word was found
                runLine, superPopList, proxData = subtractWordL(superPopList, runLine, etc)
            else:
                print('fill-in line')
        elif len(qLine[0]) > 0:
            print(lineno(), 'met if2')
            superPopList = superPopListMaker(qLine[0], etc)
            superPopList, qWord = superPopListDigester(superPopList, etc)
            runLine = wordTester(empKey, runLine, qWord)
            if len(qWord[0]) == 0:
                if len(qLine[0]) == 0:
                    return superPopList, qAnteLine, qLine, usedList, True  #  redButton event, as nothing in the list worked
                else:
                    runLine, superPopList, proxData = subTractWordR(data, data)
                    superPopList = superPopListMaker(runLine)
        else:  #  No runLine, no qLine, and superPopList[0] is out of firstWords
            print(lineno(), 'met if3')
            runLine, qLine, proxData, rhymeList, redButton = vetoLine(qAnteLine)
            return [[]], qAnteLine, qLine, usedList, True
        while len(pLEmps) > empKey:  #  If somehow the line went over the numbered lists
            runLine, superPopList, proxData = subtractWordR(data, data)
    return superPopList, qAnteLine, qLine, usedList, False
          #superPopList, qAnteLine, qLine, usedList, redButton
            

def rhymeLiner(qAnteLine, usedList, expressList, rhymeList, proxData, empLine):
    for all in rhymeList:
        expressList.append(all)
    superPopList, qAnteLine, qLine, usedList, redButton = meterLiner(qAnteLine, usedList, expressList, proxData, empLine)  #  First, let it build a line, then if it doesn't happen to rhyme, send it back 
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
                superPopList, qAnteLine, qLine, usedList, redButton = meterLiner(qAnteLine, usedList, expressList, proxData, empLine)
        elif len(qLine[0]) > 0:  #  Subtract from 
            qLine = subtractWordR(qLine)
            superPopList, qAnteLine, qLine, usedList, redButton = meterLiner(qAnteLine, usedList, expressList, proxData, empLine)  #  Here and below, meterLiner now has an expressList with the rhyming words, to increase their preference
        else:
            return qLine, usedList, True
    return qLine, usedList, False


def lineGovernor(qAnteLine, usedList, expressList, rhymeThisLine, rhymeList, empLine):
    print(lineno(), 'lineGovernor start', rhymeThisLine)
    runLine, qLine, proxData, rhymeList, redButton = vetoLine(qAnteLine)  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
    if rhymeThisLine == True:
        print(lineno(), rhymeThisLine)
        if (len(rhymeList) > 0):  #  This dictates whether stanzaGovernor sent a rhyming line. An empty line indicates metered-only, or else it would've been a nonzero population
            qLine, usedList, redButton = rhymeLiner(qAnteLine, usedList, expressList, rhymeList, proxData, empLine)
        else:
            print(lineno(), 'no rhymes')
            return [], [], True  #  newLine, usedList, redButton
    elif metSwitch == True:  #  If metSwitch is off, then we wouldn't have either rhyme or meter
        superPopList, qAnteLine, qLine, usedList, redButton = meterLiner(qAnteLine, usedList, expressList, rhymeList, proxData, empLine)
    else:
        qLine, usedList, redButton = plainLinerLtoR(qAnteLine, usedList, expressList, rhymeList, proxData, empLine)
    if redButton == True:
        runLine, qLine, proxData, rhymeList, redButton = vetoLine(qAnteLine)
        return [], [], True
    else:
        return newLine, usedList, True  #  newLine, usedList, redButton
            


################
#  poem building


def vetoStanza(usedList):
    return [], [[],[]], [], int(0), False, False
          #stanza, qAnteLine, usedList, lineCt, redButton


def stanzaGovernor(usedList):
    print(lineno(), 'stanzaGovernor begin len(rhyMap):', len(rhyMap), 'len(empMap):', len(empMap))
    expressList = []  #  A list of words that go to the front of the line. Declared and left empty, for now
    stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
    while lineCt < len(rhyMap):
        if rhySwitch == True:
            anteRhyme = rhyMap.index(rhyMap[lineCt])  #  Use the length of the stanza with rhyMap to determine if a previous line should be rhymed with the current
            print(anteRhyme, lineCt)
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
                    newLine, usedList, redButton = lineGovernor(qAnteLine, usedList, expressList, rhymeThisLine, rhymeList, empMap[lineCt])  #  If so, we try to create rhyming lines
                else:  #  Our lines created nothing, so we hit a redbutton event
                    return [], [], True
            else:  #  Then you don't need rhymes
                rhymeList = []
                print(lineno(), qAnteLine, usedList, expressList, False, rhymeList, empMap[lineCt])
                newLine, usedList, redButton = lineGovernor(qAnteLine, usedList, expressList, False, rhymeList, empMap[lineCt])  #                
        elif metSwitch == False:
            newLine, usedList, redButton = plainLinerLtoR(qAnteLine, usedList, expressList, rhymeList, empMap[lineCt])
        else:
            newLine, usedList, redButton = lineGovernor(qAnteLine, usedList, expressList, rhymeThisLine, [], empMap[lineCt])
        if redButton == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])
        elif len(newLine) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the stanza with empty list
            stanza.append(newLine)
            qAnteLine = []  #  Rebuild qAnteLine, meant to direct the proceeding line(s)
            for each in stanza:
                for all in each:
                    qAnteLine.append(all)
            newLine = []
        elif len(stanza) > 0:  #  Check if the stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            stanza = stanza[:-1]
        else:  #  Redundant, as the stanza should logically be vetoed already, but just to clean house
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
     
    textFile = 'ulysses'
    rawText = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())

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
    emps = gF.globalOpen('data/USen/empDic-USen-unik.csv', 'string')
    vocs = gF.globalOpen('data/USen/vocDic-USen-MAS.csv', 'string')
    cons = gF.globalOpen('data/USen/conDic-USen-MAS.csv', 'string')
    fono = gF.globalOpen('data/USen/fonDic-USen-MAS.csv', 'string')
    
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
    global firstWords
    proxLib, xThing, firstWords = loadmakeData(textFile)  #  Loads the data needed or makes it
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



##                    while runCt < len(pLine):
##                        proxNumList.append(runCt)
##                        pLineNList.insert(0, runCt)
##                        pLNi = 0
##                        runCt+=1
##                    superPopList, firstPopList, proxNumList, pLNi, pLineNList, jumpProxList, runLine = proxWords(proxList, pLine, runLine, proxNumList, pLNi, pLineNList, proxMinDial, proxPlusLista, superPopList, lastList, superBlackList, allLinesLine, preferredList, jumpProxList) # gramProxPlusLista
##                    superBlackList.append([])
##                    printSuperLines(pLine, superPopList, superBlackList, firstPopList, jumpProxList)
##                    pLine = pLine[len(runLine):]
