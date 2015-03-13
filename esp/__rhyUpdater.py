#!/usr/local/bin/python3.2

from string import *
import csv
csv.field_size_limit(int(9999999))
import re
import gloFunk       


masterLexi = gloFunk.dirtyLexi('__txtBiblioteca/es-ES-opti.txt')
negroLista = gloFunk.dirtyLexi('__txtBiblioteca/negroList.txt')
blackList = 'mbits', 'vme', 'kant', 'fetch', 'fddi', 'theuth', 'helmholtz', 'trap', 'phi', 'cpu', 'judit', 'ieee', 'cm', 'mhz', 'km', 'mm', 'khz', 'oh', 'i', 'bcd', 'eh', 'hao', 'ghz', 'hz', 'bits', 'kbits', 'khces', 'mflops', 'mhces', 'gflops', 'ghces', 'marx', 'scsi', 'dma', 'gflop', 'mflop', 'traps', 'tick', 'checkpoints', 'ccitt', 'chist', 'kbit', 'mbit', 'sangley', 'mmu', 'risc', 'cisc'
for all in blackList:
    negroLista.append(all)
superDic = gloFunk.globalOpen('superDic', 'string')
fCons = 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'w', 'z'


def fLiner(pWord, emps, fono, superDic, totalVs, rSyls, cleanR):
    superData = superDic[pWord].split('+')
    theseEmps = list(superData[0])
    theseFono = list(superData[2])

    vocsCt = int(0)
    consCt = int(0)
    fLine = str()
    pCt = len(theseFono)-1

    while ((consCt < cleanR) or (vocsCt < rSyls)) and (pCt>=0):
        if (theseFono[pCt] in fCons) and (consCt < cleanR):
            fLine = theseFono[pCt]+fLine
            consCt+=1
        elif (theseFono[pCt] not in fCons) and (vocsCt < rSyls):
            fLine = theseFono[pCt]+fLine
            vocsCt+=1
        else:
            fLine = ' '+fLine
        pCt-=1
    fLine = fLine.rstrip()
    
    return theseEmps, fLine

def chStrike(totalVs, rSyls, cleanR):
    try:
        if (rSyls <= totalVs):       
            print('opening file...')
            libFile = csv.reader(open("__global/__data/__rimas/completadas/corrupt/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv", "r", encoding='latin-1'))
            dicFile = csv.writer(open("__global/__data/__rimas/completadas/cleand/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv", "w", encoding='latin-1'))
            print('starting: rimaLib-t'+tName+"r"+rName+"c"+cName+".csv")
            lib = {}
            for line in libFile:
                if line != []:
                    lib[line[0]] = str(line[1])
            for key, val in lib.items():
                killList = []
                keyCleaner = key.split('^')
                for all in keyCleaner:
                    if (re.search('ch', all)) or (all in negroLista):
                        killList.append(all)
                for all in killList:
                    keyCleaner.remove(all)
                killList = []
                valCleaner = val.split('^')
                for all in valCleaner:
                    if (re.search('ch', all)) or (all in negroLista):
                        killList.append(all)
                for all in killList:
                    valCleaner.remove(all)
                if (len(keyCleaner) > 0) and (len(valCleaner) > 0):
                    scWords = str()
                    for each in keyCleaner:
                        scWords = scWords + each + '^'
                    svWords = str()
                    for each in valCleaner:
                        svWords = svWords + each + '^'
                    dicFile.writerow([scWords[0:-1], svWords[0:-1]])
        return str("true")
    except IOError:
        print('\nskipping rimaLib-t'+tName+"r"+rName+"c"+cName+".csv\n")
        return 'FALSE'

        
def chLexiPrep(masterLexi, negroLista, totalVs, rSyls, cleanR, tName, rName, cName):

    chList = []

    cons = gloFunk.globalOpen('cons', 'lista')
    emps = gloFunk.globalOpen('emps', 'lista')
    fono = gloFunk.globalOpen('fono', 'lista')

    for all in negroLista:
        try:
            masterLexi.remove(all)
        except ValueError:
            continue

    for all in masterLexi:
        if re.search('ch', all) and (len(emps[all]) >= rSyls) and (len(cons[all]) >= cleanR):            
            chList.append(all)

    print('chList = ', len(chList))
    rhyFile = csv.reader(open("__global/__data/__rimas/completadas/cleand/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv", "r", encoding='latin-1'))
    rhyDic = {}
    for line in rhyFile:
        if len(line) != 0:
            rhyDic[line[0]] = str(line[1])

    return chList, rhyDic, fono, cons, emps

                
def chBuildr(chList, rhyDic, fono, cons, emps, superDic, totalVs, rSyls, cleanR, tName, rName, cName):
    fixedDefs = {}
    yaFound = []
    while len(chList) > 0:
        chClick = int(0)
        chWord = chList[0]
        print('nowIs=', len(chList), '\nchWord=', chWord)
        chEmps, fChLine = fLiner(chWord, emps, fono, superDic, totalVs, rSyls, cleanR)
        for key, val in rhyDic.items():
            strikeList = []
            valChecker = val.split('^')
            vIndex = int(0)
            testWord = valChecker[vIndex]
            while testWord in negroLista:
                testWord = valChecker[vIndex]
                vIndex+=1
            testEmps, fTestLine = fLiner(testWord, emps, fono, superDic, totalVs, rSyls, cleanR)
            if (fTestLine == fChLine) and (testEmps[(len(testEmps) - rSyls):len(testEmps)] == chEmps[(len(chEmps) - rSyls):len(chEmps)]):
                yaFound.append(key)
                scWords = str(key+'^'+chWord)
                for all in chList:
                    qWord = all
                    qEmps, fQLine = fLiner(qWord, emps, fono, superDic, totalVs, rSyls, cleanR)
                    if (fQLine == fTestLine) and (qEmps[(len(qEmps) - rSyls):len(qEmps)] == testEmps[(len(testEmps) - rSyls):len(testEmps)]):
                        scWords = scWords+'^'+qWord
                        if len(emps[qWord]) == totalVs:
                            valChecker.append(qWord)
                        strikeList.append(qWord)
                if (len(emps[chWord]) == totalVs) and (chWord not in valChecker):
                    valChecker.append(chWord)
                svWords = str()
                for each in valChecker:
                    if len(each) != 0:
                        svWords = svWords + each + '^'
                fixedDefs[scWords] = svWords[0:-1]
                chClick = 1
                for all in strikeList:
                    chList.remove(all)
        if chClick == 0:
            strikeList = []
            matchKeys = chWord
            matchVals = str()
            for each in chList:
                pWord = each
                pEmps, fPLine = fLiner(pWord, emps, fono, superDic, totalVs, rSyls, cleanR)
                if (fPLine == fChLine) and (pEmps[(len(pEmps) - rSyls):len(pEmps)] == chEmps[(len(chEmps) - rSyls):len(chEmps)]):
                    matchKeys = matchKeys+'^'+pWord
                    if len(emps[pWord]) == totalVs:
                        matchVals = matchVals+'^'+pWord
                    strikeList.append(pWord)
            fixedDefs[matchKeys] = matchVals
            for each in strikeList:
                chList.remove(each)             
        if chWord in chList:
            chList.remove(chWord)
    for key, val in rhyDic.items():
        if key not in yaFound:
            fixedDefs[key] = val
    cleanFile = csv.writer(open("__global/__data/__rimas/completadas/fixt/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv", 'w', encoding='latin-1'))
    for key, val in fixedDefs.items():
        if (len(key) > 0) and (len(val) > 0):
            cleanFile.writerow([key, val])


for totalVs in range(3, 4):
    for cleanR in range(0, 1):
        for rSyls in range(1, 4):
            if (rSyls <= totalVs):
                tName = str(totalVs)
                rName = str(rSyls)
                cName = str(cleanR)
                if totalVs < 10:
                    tName = '0'+tName
                if rSyls < 10:
                    rName = '0'+rName
                if cleanR < 10:
                    cName = '0'+cName
                try:
                    print("starting t"+tName+'r'+rName+'c'+cName)
                    ans = chStrike(totalVs, rSyls, cleanR)
                    if ans == 'true':
                        chList, rhyDic, fono, cons, emps = chLexiPrep(masterLexi, negroLista, totalVs, rSyls, cleanR, tName, rName, cName)
                        chBuildr(chList, rhyDic, fono, cons, emps, superDic, totalVs, rSyls, cleanR, tName, rName, cName)
                except FileNotFoundError:
                    continue

print('PROGRAM FINISH')
