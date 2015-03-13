import random
import gloFunk

def proxWords(proxList, pLine, proxNumList, pLNi, pLineNList):
    # start from latest word and keep building until you run out of words, then return that list
    while len(pLineNList) > 0:
        #print('\n'+str(proxNumList)+'\n'+str(pLineNList)+'\n'+str(pLNi)+'\n')
        proxList = proxP1[pLine[pLineNList[0]]]
        if len(pLineNList) == 1:
            break
        else:
            pLNi = 0
            for all in proxNumList:
                keepList = []
                #print('data:', all, pLineNList[pLNi], pLNi)
                checkList = proxPlusLista[all][pLine[pLineNList[pLNi]]]
                #print('checkList for :', pLine[pLineNList[pLNi]], proxPlusLista[all][pLine[pLineNList[pLNi]]])
                for each in checkList:
                    if each in proxList:
                        keepList.append(each)
                pLNi+=1
                if len(keepList) > 0:
                    proxList = keepList
                    #print('spot1')
                else:
                    break
                #print('proxList:', proxList)
            if len(proxList) > 0:
                #print('gotIt')
                break
            elif len(pLineNList) > 0:
                proxNumList.pop()
                pLineNList.pop()
            else:
                pLine = []
                pLEmps = []
                pWord = str()
                pWEmps = ['2']
                proxList = []
                #print('spot2')
                break


                
    return proxList, proxNumList, pLNi, pLineNList


## clauses

texto = str(open('__txtBiblioteca/libros&escritos/ali8.txt', 'r', encoding='latin-1').read())
texto = texto.lower()

breakPunx = ['.', ',', '!', '?', '(', ')', ':', ';', '\n', '-', '«'] 
dropPunx = ['+', '-', '*', '=', '/', '@', '#', '$', '%', '^', '&', '|', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

for all in dropPunx:
    if all in texto:
        texto.replace(all, '')

click = int(0)
elTexto = [texto]

for each in breakPunx:
    #print(each)
    strikeList = []
    qLines = []
    for all in elTexto:
        if each in all:
            qLines = all.split(each)
            strikeList.append(all)
    if len(strikeList) > 0:
        for all in strikeList:
            elTexto.remove(all)
        for all in qLines:
            if len(all) > 0:
                clause = str(all[1:])
                clause.lower()
                if (clause[:2] == 'y ') or (clause[:2] == 'o '):
                    elTexto.append(clause[2:])
                else:
                    elTexto.append(clause)


## proxSys

print('building proxDics')

proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10]
proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10]


for all in elTexto:
    ## give all words an entry, even if it is empty.
    ## remove/break empty nugs
    chopThis = str(all)
    sentence = chopThis.split(' ') # split into words
    for each in sentence:
        for all in range(0, (len(proxPlusLista))):
            proxPlusLista[all][each] = []
        for all in range(0, (len(proxMinusLista))):
            proxMinusLista[all][each] = []
    if (sentence[0] == '') or (sentence[len(sentence)-1] == ''):
        sentence.remove('')
    if '' in sentence:
        print(sentence)
        elTexto.insert(len(elTexto), sentence[(sentence.index('')+1):])        
        while len(sentence) > (sentence.index('')+1):
            sentence.pop()
        sentence.pop()

for all in elTexto:
    chopThis = str(all)
    sentence = chopThis.split(' ') # split into words
    proxNumerator = int(1)
    proxDicCounter = int(0)
    while proxDicCounter < len(proxPlusLista):
        for each in sentence:
            if (sentence.index(each) + proxNumerator) < len(sentence):
                if sentence[sentence.index(each) + proxNumerator] not in proxPlusLista[proxDicCounter][each]:
                    proxPlusLista[proxDicCounter][each].append(sentence[sentence.index(each) + proxNumerator]) # adds to dics if exists
                if each not in proxMinusLista[proxDicCounter][sentence[sentence.index(each) + proxNumerator]]:
                    proxMinusLista[proxDicCounter][sentence[sentence.index(each) + proxNumerator]].append(each)
        if len(proxPlusLista[proxDicCounter]) > 0:
            proxDicCounter+=1
            proxNumerator+=1
        else:
            while len(proxPlusLista) > proxDicCounter:
                proxPlusLista.remove(proxPlusLista[proxDicCounter])
                proxMinusLista.remove(proxMinusLista[proxDicCounter])
            break

print('proxDics complete\nstarting remix')


emps = gloFunk.globalOpen('emps', 'lista')

def newLine():
    empKey = ['0', '1', '0', '0', '1', '0', '0', '1', '0']
    pWEmps = ['2']
    pLEmps = ['2']
    while pLEmps != empKey:
        try:
            while (pWEmps != empKey[:len(pWEmps)]) and (len(pWEmps) > 0):
                xLine = str(random.choice(elTexto))
                pWord = random.choice(xLine.split(' '))
                try:
                    pWEmps = emps[pWord]
                except KeyError:
                    print('kError:', pWord)
                    continue
            #print('lineStart w/ pWord:', pWord)
            pLine = [pWord]
            pLEmps = emps[pWord]
            pLineNum = int(0)
            pLineNList = [pLineNum]
            pLNi = int(0)
            proxNum = int(0)
            proxNumList = [proxNum]
            proxList = proxP1[pWord]
            while (pLEmps != empKey[0:len(empKey)]) and (len(pLEmps) < len(empKey) + 10) and (len(pLineNList) > 0):
                if len(pLine) == 1:
                    proxList = proxP1[pWord]
                    if len(proxList) == 0:
                        pLine = []
                        pLEmps = []
                        pWord = str()
                        pWEmps = ['2']  
                        break
                else:
                    proxList, proxNumList, pLNi, pLineNList = proxWords(proxList, pLine, proxNumList, pLNi, pLineNList)
                if len(proxList) == 0:
                    pLineNList = []
                while len(pLineNList) > 0:
                    #print('proxList here:', proxList)
                    nextWord = proxList.pop(proxList.index(random.choice(proxList)))
                    pLEmps = pLEmps + emps[nextWord]
                    if pLEmps != empKey[:len(pLEmps)]:
                        pLEmps = pLEmps[:len(pLEmps) - len(emps[nextWord])]
                    else:
                        pLine.append(nextWord)
                        #print('pLine growth:', pLine)
                        proxNum = len(proxNumList)
                        proxNumList.append(proxNum)
                        pLineNum = len(pLine) - 1
                        pLineNList.insert(0, pLineNum)
                        break
                    if len(proxList) == 0:
                        #print('spot4')
                        proxNumList.pop()
                        pLineNList.pop()
                        break
            if (len(pLEmps) > len(empKey) + 10) or (len(pLineNList) == 0):
                #print('out')
                pLine = []
                pLEmps = []
                pWord = str()
                pWEmps = ['2']
        except KeyError:
            pLine = []
            pLEmps = []
            pWord = str()
            pWEmps = ['2']
            #print('\nkeyError!:', pWord, pLine, '\n')
            continue
    pString = str()
    for all in pLine:
        pString = pString+' '+all
    pString = pString[1:]
    return pString

pCt = 0
while pCt < 12:
    oneLine = str()
    oneLine = newLine()
    if pCt%4==0:
        print('\n')
    print(oneLine)
    pCt+=1
                
                


                
