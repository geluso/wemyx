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

posTags = 'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '.', ',', ';', ':', '!', '?', '"', "'"
quantumTags = 'CC', 'DT', 'WRB', 'WP', 'WP$', 'PRP', 'PRP$', 'TO', 'IN'
quantumList = []

punxTags = ['"', "'", "''", ':']
allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '``', '`', '"', "''"]
midPunx = [',', ';', ',', ':', '--']
endPunx = ['.', '!', '?']
punx = [',', ';', ',', ':', '--', '"', '-', "''", "''", "''", '(', ')']
badGrams = ['``', '"', "''", '`', '']


####

#   To-do list:
#   - change emps to boolean values, ignore secondary stresses (ints, otherwise)
#   - standardize thesaurus tags, write to file words that don't have entries
#   - discover contraction handling and write function to handle it
#   - ensure halfbeats are viable
#   - redesign tkinter window to something prettier


def textPrep(texto):

    texto = texto.replace('\n', ' ')
    for all in allPunx:  #  Put a space end-punctuation to treat it like another word.
        texto = texto.replace(all, ' '+all+' ')
    texto = texto.replace("   ", ' ')  #  Makes 3 spaces after end of sentence into just one
    texto = texto.replace("  ", ' ')  #  Then more for good measure

    # print(texto)

    #  Tokenizes raw text
    #  ++ is this where I should start monitoring contractions?
    global splitText
    splitText = texto.split(' ')
    global superTokens
    superTokens = nltk.word_tokenize(texto)
    # print(splitText)
    
    return splitText, superTokens


def gpDataWriter(dicList, fileBit, textFile):

    ##  Writes grammar and proximity data to hard drive

    pFile = csv.writer(open('data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv', 'w+'))
    print('building: data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv')
    #print(dicList)
    for key, val in dicList[0].items():
        print(key)
        fullString = str()
        for each in dicList:
            dicString = str()
            for entr in each[key]:
                print('gpData:', entr, )
                dicString = dicString+entr+'^'  #  Entries for each proxLib are separated by the '^'
            fullString = fullString+dicString[:-1]+'~'  #  Proxlibs are separated by '~'. proxPlusLista is saved in one file.
        for char in fullString:
            if char != '~':      # This is to screen for empty sets. If one char is not a tilde then it's non-empty.
                print(fileBit, 'writing:', key, fullString[:min(20, len(fullString))])
                pFile.writerow([key, fullString[:-1]])
                break


def dataOpener():  # write filepath as variable to allow different types of data
    libFile = csv.reader(open('data/textLibrary/textData/'+textFile+'-'+dynaType+'.csv', 'r'))
    dynasaurus = {}
    for line in dynaFile:
        dynasaurus[line[0]] = line[1].split('^')
    return dynasaurus


def newProxLibs(proxLista, libInt, wordLista, textFile): # Subfunction in loadmakeData for brevity. Creates blank entries to add to. Uppercase versions of words too.
    for each in wordLista:
        proxLista[libInt][each.lower()] = []
        if len(each) > 1:
            proxLista[libInt][each[0].upper()+each[1:]] = []
        else:
            proxLista[libInt][each.upper()] = []
    return proxLista


def proxLibBuilder(thisLib, thisFile, specialText, textFile):  #  Another subfunction for loadmakeData. 'thisLib' is either proxLib or gramProxLib, 'specialText' is either splitText or superTokenGrams
        print('proxLib', thisFile)
        lastSpot, wordsI = len(specialText), int(0)
        while wordsI < lastSpot:   
            wordsI+=1
            try:
                pWord = specialText[wordsI]
                proxNumerator, proxDicCounter, proxMax = int(1), int(0), len(thisLib[0])
                while proxDicCounter < proxMax:
                    proxWord = specialText[wordsI+proxNumerator]
                    if proxWord not in thisLib[0][proxDicCounter][pWord]:
                        print('plusadd = proxP:', proxWord, 'pWord:', pWord)
                        thisLib[0][proxDicCounter][pWord].append(proxWord)
                    if pWord not in thisLib[1][proxDicCounter][proxWord]:
                        print('minusadd = proxM:', proxWord, 'pWord:', pWord)
                        thisLib[1][proxDicCounter][proxWord].append(pWord)
                    proxDicCounter+=1
                    proxNumerator+=1
            except IndexError:
                print("iE pLBuilder", pWord, proxWord, proxDicCounter, proxNumerator)
                print(thisLib[0][0][pWord])
                continue
            except KeyError:
                print('kE build:', pWord, proxWord, proxDicCounter, proxNumerator)
                proxDicCounter+=1  ## These are the lines you edited
                proxNumerator+=1   ## Check to see if they did anything significant
                continue
        print('writing proxLibs...')
        gpDataWriter(thisLib[0], thisFile[0], textFile)
        gpDataWriter(thisLib[1], thisFile[1], textFile)
        return thisLib


def loadmakeData(textFile, thesSwitch):

    proxMaxDial = 19
    #$ print('begin loadmakeProxLibs()')
    #  Prox and gramprox store Markov chains and build in -Liner() functions
    #  Libs declared here, made into lists of dics of lists, and called using indices on 
    global proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20
    global proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20
    global gramProxP1, gramProxP2, gramProxP3, gramProxP4, gramProxP5, gramProxP6, gramProxP7, gramProxP8, gramProxP9, gramProxP10, gramProxP11, gramProxP12, gramProxP13, gramProxP14, gramProxP15, gramProxP16, gramProxP17, gramProxP18, gramProxP19, gramProxP20
    global gramProxM1, gramProxM2, gramProxM3, gramProxM4, gramProxM5, gramProxM6, gramProxM7, gramProxM8, gramProxM9, gramProxM10, gramProxM11, gramProxM12, gramProxM13, gramProxM14, gramProxM15, gramProxM16, gramProxM17, gramProxM18, gramProxM19, gramProxM20
    global proxPlusLista, proxMinusLista, gramProxPlusLista, gramProxMinusLista, proxLib, gramProxLib
    #  These dictionaries contain lists of words that come after 
    proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20 = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}] 
    proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20  = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]      
    gramProxP1, gramProxP2, gramProxP3, gramProxP4, gramProxP5, gramProxP6, gramProxP7, gramProxP8, gramProxP9, gramProxP10, gramProxP11, gramProxP12, gramProxP13, gramProxP14, gramProxP15, gramProxP16, gramProxP17, gramProxP18, gramProxP19, gramProxP20 = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    gramProxM1, gramProxM2, gramProxM3, gramProxM4, gramProxM5, gramProxM6, gramProxM7, gramProxM8, gramProxM9, gramProxM10, gramProxM11, gramProxM12, gramProxM13, gramProxM14, gramProxM15, gramProxM16, gramProxM17, gramProxM18, gramProxM19, gramProxM20  = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    #  The dictionaries are organized into lists that are accessed by index. Useful in while loops with ascending/descending numbers
    proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20]
    proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20]
    gramProxPlusLista = [gramProxP1, gramProxP2, gramProxP3, gramProxP4, gramProxP5, gramProxP6, gramProxP7, gramProxP8, gramProxP9, gramProxP10, gramProxP11, gramProxP12, gramProxP13, gramProxP14, gramProxP15, gramProxP16, gramProxP17, gramProxP18, gramProxP19, gramProxP20]
    gramProxMinusLista = [gramProxM1, gramProxM2, gramProxM3, gramProxM4, gramProxM5, gramProxM6, gramProxM7, gramProxM8, gramProxM9, gramProxM10, gramProxM11, gramProxM12, gramProxM13, gramProxM14, gramProxM15, gramProxM16, gramProxM17, gramProxM18, gramProxM19, gramProxM20]
    #  The maximum length of theseslists are truncated based on the user's initial input
    proxPlusLista = proxPlusLista[:proxMaxDial]
    proxMinusLista = proxMinusLista[:proxMaxDial]
    gramProxPlusLista = gramProxPlusLista[:proxMaxDial]
    gramProxMinusLista = gramProxMinusLista[:proxMaxDial]
    #  The two lists for each library type are combined into one variable apiece
    proxLib, gramProxLib = [proxPlusLista, proxMinusLista], [gramProxPlusLista, gramProxMinusLista]

    #  'Try' statements will attempt to load existing data. FileNotFoundErrors will build what's missing.
    #  Rather than use just one try/except section, I divided it so it can skip the ones already created. Usually, it'll just build all or none.
    firstWords = []
    try:
        print('begin fwFile load')
        firstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'r')
        for line in firstFile:
            firstWords.append(line[:-1])
    except FileNotFoundError:
        print('fwFile not found')
        sTLen = len(splitText) #  Don't put 'len(splitText)' in while loop because it'll check the len every time, which is moderately slower
        for each in ['.', '!', '?']:
            try:
                print('fw scanning: ', each)
                fwI = 0
                while fwI < sTLen:  #  Will this while loop terminate?
                    if splitText[fwI] not in firstWords:
                        splitText[fwI] = splitText[fwI].lower()
                        firstWords.append(splitText[fwI])      # Finds punctuation, then moves one step forward to get first word of new sentence.
                    fwI = splitText.index(each, fwI) + 1       # This will also start the indexing beyond the puncuation, insuring that it will keep moving
            except ValueError: #  We've gotten to the end and couldn't find any more
                continue
        newFirstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
        print('writing fwFile...')
        for all in firstWords:
            newFirstFile.write(all+'\n')
        newFirstFile.close()
        print('fw complete')

    #  
    try:
        print('begin prox/gram builds')        
        #  Take a look at gpDataOpener. Consider moving more code there, or bring some here
        proxPlusLista = gF.gpDataOpener(proxPlusLista, 'proxP', textFile)
        for each in proxPlusLista:
            print('proxP:', len(each), )
        proxMinusLista = gF.gpDataOpener(proxMinusLista, 'proxM', textFile)
        for each in proxPlusLista:
            print('proxM:', len(each), )
        gramProxPlusLista = gF.gpDataOpener(gramProxPlusLista, 'gramP', textFile)
        for each in proxPlusLista:
            print('gramP:', len(each), )
        gramProxMinusLista = gF.gpDataOpener(gramProxMinusLista, 'gramM', textFile)
        for each in proxPlusLista:
            print('gramM:', len(each), )
        print('prox/gram load complete')
            
    except FileNotFoundError:
        print('prox/gram not found')
        print('obtaining superTokens...')
        superTokenData = nltk.pos_tag(superTokens)
        superTokenWords, superTokenGrams = [], []
        for each in superTokenData:
            ##$print(each)
            ##$print('dynasaur:', len(dynasaurus))
            #superTokenWords.append(each[0])
            superTokenGrams.append(each[1])
        print('preparing proxLists')
        for all in range(0, (len(proxPlusLista))):
            proxPlusLista = newProxLibs(proxPlusLista, all, splitText, textFile)
            proxMinusLista = newProxLibs(proxMinusLista, all, splitText, textFile)
            for each in posTags:
                gramProxPlusLista[all][each] = []
                gramProxMinusLista[all][each] = []
        print('starting proxbuilds')
        proxLib = proxLibBuilder(proxLib, ['proxP', 'proxM'], splitText, textFile)
        gramProxLib = proxLibBuilder(gramProxLib, ['gramP', 'gramM'], superTokenGrams, textFile)

    if thesSwitch == True:  #  Don't bother loading if the user isn't implementing thesaurus.
        try:
            dynasaurus = gF.dynaDataOpener(textFile, dynatype)
        except FileNotFoundError:
            print('thesBuild begin')
            
    return proxLib, gramProxLib, {}, firstWords


def contractionAction(contraction, qLine):  #  Switches contractions between phonetic line and real/grammar line
    qLine[0]+=contraction
    qLine[1]+=contractionDic[contraction]


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


def popListMaker(qLine, qPopList, qAllLines, empKey, tagEmpsLine, thesBools):
    if len(qLine[0]) == 0:
        return firstWords, firstWords, flowData # as qPopList
    else:
        pLNi = int(0)
        proxNumList, pLineNList = [], []
        while pLNi < len(zLine[1]):
            proxNumList.append(pLNi)
            pLineNList.insert(0, pLNi)
            pLNi+=1
        pLNi-=1
        print(proxNumList, pLNi, pLineNList)
        flowData = proxNumList[:proxMaxDial], min(pLNi, proxMaxDial), pLineNList[:proxMaxDial]


def popListDigester(qLine, qPopList, qAllLines, empKey, thesBools):
    svList = []
    while len(qPopList[0]) > 0:
        pWord = qPopList[0].pop(0)
        if pWEmps == empKey[:-len(pWEmps)]:
            addWord(pWord)
            break
        elif halfBeats:
            tagEmpsLine+=['']  # test that you can use += operator to add list element to metalist
            svList.append(pWord)
    if len(qPopList[0][-1]) == 0 and pWEmps != empKey[:-len(pWEmps)] and thesClick[-1] == 0:
        qPopList = dynamight(getWords)
        


def plainLinerLtoR(vars):

    data
    # without rhyme or meter

def meterLiner(empKey, qAllLines):
    data
    

def rhymeLiner(vars):

    # starts with rhymewords, looks at anteline, and proxLibs, then builds backwards
    # can function with or without meter

    
    for all in rhyList:
        if metSwitch == True:
            if emps[all] == empLine[:-len(emps[all])]:
                lastWords.append(all)
        else:
            if len(emps[all]) <= len(empLine):
                lastWords.append(all)


def resetEverything():
    data
    # wipes away all values, starts a fresh stanza


def stanzaWriter(stanza, rhyMap, metMap, usedList):

    # manages how a set of lines progresses
    
    print('stanzaWriter begin len(rhyMap):', len(rhyMap), 'len(metMap):', len(metMap))
    if rhySwitch == 0 and metSwitch == 0: # then we have rhyme and meter in the template
        print('make rhyming lines')
    elif rhySwitch == 1 and metSwitch == 0: # then we have meter but not rhyme
        print('make plainlines with rhymes')
    elif rhySwitch == 0 and metSwitch == 1: # then we have rhyme but not meter
        print('metered but unrhymed')
    #else: #  we have freeverse
        

def startWemyx():  #  Main function that begins entire program

    global rhySwitch, metSwitch
    rhySwitch, metSwitch = False, False

    rhyMap = 'aa'
    metMap = [[1001], [1001]]
    
    print('\nstarting remix')
    textFile = 'test0' # textChoice.get() # name will access text and data about it
    texto = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())

    splitText, superTokens = textPrep(texto)  #  A function to prepare the text for analysis
    proxLib, gramProxLib, dynasaurus, firstwords = loadmakeData(textFile, False) #  Either generates or loads proxLibs

    rCt = int(0)
    poemCt = int(10) #int(poemNum.get())
    printIndex = int(0)
    print('sourcetext: ', textFile+'.txt\n\nformat:')
    while printIndex < len(rhyMap):
        print(rhyMap[printIndex], metMap[printIndex])
        printIndex+=1
    print("\n")
    # if gramSwitch == 1:
    print('grammar    | off')
    #else:
        #print('grammar    | on')
    #if rhySwitch == 1:
    print('rhyme      | off')
    #else:
        #print('rhyme      | on')
    #if metSwitch == 0:
    print('meter      | off')
    #else:
        #print('meter      | on')
    #if halfSwitch == 1:
        #print('half-beats | on')
    #if theSwitch == 1:
    print('thesaurus  | off')
    while rCt<poemCt:
        rCt+=1
        print('\n\nPoem #'+str(rCt)+'\n'+str(datetime.datetime.now())+'\n')
        #try:
            ## A timer is used to restart the process if it stalls on a long loop. It feeds into the stanzaWriter function.
        stanza, usedList = [], [] # to prevent repeat words
        while len(stanza) != len(rhyMap):
            stanza, usedList = stanzaWriter(stanza, rhyMap, metMap, usedList)
        for each in stanza:
             print(each)
        time.sleep(20)
        if usedSwitch == 1: 
            usedList = ['']


print('loading metadatas...')  #  seems like these could be combined into one function

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

contractionFile = open('data/USen/contractionList.txt', 'r')

print('opening fonoFiles')
vocs = gF.globalOpen('data/USen/vocDic-USen-MAS.csv', 'string')
cons = gF.globalOpen('data/USen/conDic-USen-MAS.csv', 'string')
fono = gF.globalOpen('data/USen/fonDic-USen-MAS.csv', 'string')

#  and.... GO!
startWemyx()    
