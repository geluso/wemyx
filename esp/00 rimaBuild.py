#!/usr/local/bin/python3.2

import ftplib
from string import *
import csv
csv.field_size_limit(int(9999999))
import gloFunk

masterLexi = gloFunk.dirtyLexi('__txtBiblioteca/es-ES-opti.txt')
negroLista = gloFunk.dirtyLexi('__txtBiblioteca/negroList.txt')
fCons = 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'w', 'z'
listDefs = {}
superDic = gloFunk.globalOpen('superDic', 'string')

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


def wordPrep(totalVs, rSyls, cleanR, negroLista):
    blackList = 'mbits', 'vme', 'kant', 'fetch', 'fddi', 'theuth', 'helmholtz', 'trap', 'phi', 'cpu', 'judit', 'ieee', 'cm', 'mhz', 'km', 'mm', 'khz', 'oh', 'i', 'bcd', 'eh', 'hao', 'ghz', 'hz', 'bits', 'kbits', 'khces', 'mflops', 'mhces', 'gflops', 'ghces', 'marx', 'scsi', 'dma', 'gflop', 'mflop', 'traps', 'tick', 'checkpoints', 'ccitt', 'chist', 'kbit', 'mbit', 'sangley', 'mmu', 'risc', 'cisc'
    for all in blackList:
        negroLista.append(all)

    yaNoFound = []
    testLexi = []

    cons = gloFunk.globalOpen('cons', 'lista')
    emps = gloFunk.globalOpen('emps', 'lista')
    fono = gloFunk.globalOpen('fono', 'lista')
    testEDic = {}
    testFDic = {}

    for all in negroLista:
        try:
            masterLexi.remove(all)
        except ValueError:
            continue

    for all in masterLexi:
        if (len(emps[all]) >= rSyls) and (len(cons[all]) >= cleanR):            
            if (len(emps[all]) == totalVs):
                yaNoFound.insert(0, all)
                testLexi.append(all)
                testEDic[all] = emps[all]
                testFDic[all] = fono[all]
            else:
                yaNoFound.append(all)

    print('Lexicon=', len(yaNoFound), '\nTestLexi=', len(testLexi))

    return emps, fono, testEDic, testFDic, testLexi, yaNoFound


def rimaFinder(testLexi, yaNoFound, emps, fono, testEDic, testFDic, dicFile, tName, rName, cName):
    matchKeys = str()
    listDefs.clear()
    rhyList = {}
    rhyStrike = []
    while (len(yaNoFound) > 0) and (len(testLexi) > 0):
        pWord = yaNoFound[0]
        yaNoFound.remove(pWord)
        rhyList[pWord] = []
        takeOut = []
        rhyStrike = []
        if len(testLexi)%100 == 0:
            print(str(len(testLexi)), 'potential rhymes left\nlen of listDefs:', len(listDefs), '\npWord:', pWord)
        keyEmps, fKeyLine = fLiner(pWord, emps, fono, superDic, totalVs, rSyls, cleanR)
        for each in testLexi:
            testWord = each
            testEmps, fTestLine = fLiner(testWord, emps, fono, superDic, totalVs, rSyls, cleanR)
            if (fTestLine == fKeyLine) and (testEmps[(len(testEmps) - rSyls):len(testEmps)] == keyEmps[(len(keyEmps) - rSyls):len(keyEmps)]):
                rhyList[pWord].append(testWord)
                rhyStrike.append(testWord)
        if len(rhyList[pWord]) > 0:
            matchKeys = pWord
            rWord = rhyList[pWord][0]
            testEmps, fTestLine = fLiner(rWord, emps, fono, superDic, totalVs, rSyls, cleanR)
            for each in yaNoFound:
                qWord = each
                keyEmps, fKeyLine = fLiner(qWord, emps, fono, superDic, totalVs, rSyls, cleanR)
                if (fTestLine == fKeyLine) and (testEmps[(len(testEmps) - rSyls):len(testEmps)] == keyEmps[(len(keyEmps) - rSyls):len(keyEmps)]):
                    matchKeys = matchKeys+'^'+qWord
                    takeOut.append(qWord)
            listDefs[matchKeys] = rhyList[pWord]
        for each in takeOut:
            yaNoFound.remove(each)
        for each in rhyStrike:
            testLexi.remove(each)
        rhyList.clear()

    print('writing file...')
    for key, val in listDefs.items():
        svWords = str()
        for each in listDefs[key]:
            if len(each) != 0:
                svWords = svWords + each + '^'
        val = svWords
        dicFile.writerow([key, val[0:-1]])

    print('sending file...')
    sftp = ftplib.FTP('ftp.remezclemos.net', 'universe@remezclemos.net', '!Universe0')
    fp = open("__global/__data/__rimas/completadas/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv",'rb') # file to send
    sftp.storbinary('STOR rimaLibs/rimaLib-t'+tName+"r"+rName+"c"+cName+".csv", fp) # Send the file
    fp.close() # Close file and FTP
    sftp.quit()

    print('done with t'+tName+"r"+rName+"c"+cName)

def rhyMaker(totalVs, rSyls, cleanR):
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
            libFile = csv.reader(open("__global/__data/__rimas/completadas/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv", "r"))
        except IOError:
            dicFile = csv.writer(open("__global/__data/__rimas/completadas/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv", 'w', encoding='latin-1'))
            print("starting t"+tName+'r'+rName+'c'+cName)
            emps, fono, testEDic, testFDic, testLexi, yaNoFound = wordPrep(totalVs, rSyls, cleanR, negroLista)
            rimaFinder(testLexi, yaNoFound, emps, fono, testEDic, testFDic, dicFile, tName, rName, cName)

for totalVs in range(1, 11):
    for cleanR in range(1, 14):
        for rSyls in range(0, 11):
            rhyMaker(totalVs, rSyls, cleanR)
    for cleanR in range(0, 1):
        for rSyls in range(1, 11):
            rhyMaker(totalVs, rSyls, cleanR)
                                      
print('PROGRAM FINISH')
