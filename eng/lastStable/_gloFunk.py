from string import *
import random
import datetime
import time
import csv
csv.field_size_limit(int(9999999))


###################
#- Categories and lists for characters

#-!obsolete?:
rhymeDic = {}
rhymeLib = {}
defono = {}
rhyList = {}
empIndexes = []
pTotal = int(0)
pLen = int(0)
trashWords = []
bloomList = []
keyList = []
lexiLib = str()


#->pass:
emps = {}
vocs = {}
fono = {}
cons = {}

pLine = str()
pWord = str()
pWLen = int(0)

#this is the header&footer to the website

header = str('<!DOCTYPE HTML<HTML><body bgcolor=black><center><font face=courier new><font size=7><font color=#00ff66>remezclemos.net</font></center><HEAD><TITLE>remezclemos:publicaciones</TITLE><style type=text/css><!--body{text-align:left;min-width: 1080px;}#wrapper {width: 1080px;margin: 0 auto;text-align: left;}--></style></head><body><div id=wrapper><P><center><font face=courier new><font color=white><font size=3><a href=http://www.remezclemos.net/0.html>pagina principia</a> | <a href=http://www.remezclemos.net/cuentas.html>cuentas</a> | <a href=http://www.remezclemos.net/pubs.php>publicaciones</a> | <a href=http://www.remezclemos.net/bib.html>biblioteca</a> | <a href=http://www.remezclemos.net/escribir.html>escribir</a> | <a href=http://www.remezclemos.net/info.html>informacion</a> | <a href=http://www.remezclemos.net/donar.html>donar</a></center></font><font face=courier new><font size=4><font color=white>')
pubPoem = str()
footer = str('<P><center><font face=courier new><font color=white><font size=3><a href=http://www.remezclemos.net/0.html>pagina principia</a> | <a href=http://www.remezclemos.net/cuentas.html>cuentas</a> | <a href=http://www.remezclemos.net/pubs.php>publicaciones</a> | <a href=http://www.remezclemos.net/bib.html>biblioteca</a> | <a href=http://www.remezclemos.net/escribir.html>escribir</a> | <a href=http://www.remezclemos.net/info.html>informacion</a> | <a href=http://www.remezclemos.net/donar.html>donar</a></center></font><br><center><font face=courier new><font size=2><font color=grey><p>&copy2012 topher qastro<p></font><p>')

######

line = int(0)

empIndexes = []

p = ()
ip = []
pLVocs = []
pLEmps = []
lastWord = ()

catch = []
index = []
indexes = []
vowString = []
cleanList = []

empHost = []
pEmps = str()
empString = []
empsLine = []
empKey = []

iA = int(0)
iB = int(0)
iC = int(0)

escCt = int(0)
count = int(0)
couplCount = int(0)
count = int(0)
nextLCt = int(0)
xCt = int(0)
yCt = int(0)
zCt = int(0)
lineCt = int(0)
click = int(0)


vocsList = vocs = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'V', 'Y', '3', '0', '@', '&', 'L', 'M',  'N', '%', '!', '#', '$', '^', '*', '(', ')', '?', '<', '>', '.', '|', ']', '[', '=']
vow = 'y', 'a', 'e', 'i', 'o', 'u', 'ü', 'â', 'ê', 'è', 'ô', 'ö', 'õ', 'à', 'è', 'î', 'ã', 'ë', 'ä', 'ê', 'ĩ', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$', '%', '&', '!', '?', '<', '.', ':', ';', '(', ')', '[', ']', '{', '}', '1', '2'
accVow = 'á', 'é', 'ó', 'í', 'ú', 'ĕ', 'ė', 'ŏ', 'ő', 'ă', 'ą', 'Ə', 'ů', 'œ', 'þ', 'ø', 'æ'
allVow = 'y', 'a', 'e', 'i', 'o', 'u', 'ü', 'á', 'é', 'ó', 'í', 'ú', 'â', 'ê', 'è', 'ô', 'ö', 'õ', 'à', 'è', 'î', 'ã', 'ë', 'ä', 'ê', 'ĩ', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū', 'ĕ', 'ė', 'ŏ', 'ő', 'ă', 'ą', 'Ə', 'ů', 'œ', 'þ', 'ø', 'æ', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$', '%', '&', '!', '?', ',', '.', ':', ';', '(', ')', '[', ']', '{', '}', '1', '2'
empPat1 = 's', 'n', 'a', 'e', 'i', 'o', 'u', 'y', 'ë', 'ä', 'ã', 'õ', 'ö', 'ê', 'ĩ', 'î', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū'
cons = 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 'ñ'
strippers = '”', '’', "'", '…', '…', '—', '·', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '{', '}', '<', '>', '"', ',', '!', '.', ',', '‘', '’', '`', '~', '/', '+', '=', '|', '\c', '\n', '?', ';', ':', '_', '-', '¿', '»', '«', '¡', '©', '“', '”', 'º', '/', '\c'
spacers = '\n\n\n', '\n\n', '\n', '    ', '      ', '     ', '    ', '   ', '  '
caps =  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ü',
silentPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '``', '`']

palabras = []

###################
#- Lexicon preppers
##-1. For a dictionary that's formatted for data extraction

def cleanLexi():

    text = str(open('__txtBiblioteca/es-ES-opti.txt', 'r', encoding='latin-1').read())

    masterLPop = text.split('\n')
    indexList = []
    zCt =  0

    print('Building lexicon...')
    for each in masterLPop:
        each.lower()
        each.replace('\n', '')
        each.replace(' ', '')
        zCt+=1
        if zCt%1000 == 0:
            print(zCt, '@', each)
        if len(each) == 0:
            indexList.append(each)
        for all in caps:
            try:
                each.index(all)
                indexList.append(each)
                #print('swallowing=', each)
            except ValueError:
                continue
    for all in indexList:
        try:
            masterLPop.remove(all)
            #print('snag')
        except ValueError:
            #print('GONEAGE=', each)
            continue

    masterLPop.sort()
    return palabras


##-2. For prose that has formatting or non-Spanish:

def dirtyLexi(textNomer):

    #- Filepath for books: libros&escritos/' + textNomer + '/' + textNomer + '
    #textNomer = str(input('Type name and filepath open with gloFunk.dirtyLexi:  '))
    text = str(open(textNomer, 'r', encoding='latin-1').read())

    #- Format into discernable text:
    text = text.lower()
    text = ' ' + text + ' '
    for all in strippers:
        text = text.replace(all, ' ')
    for all in spacers:
        text = text.replace(all, ' ')

    #- Try to recover some characters:
    text = text.replace('à', 'á')
    text = text.replace('è', 'é')
    text = text.replace('ì', 'í')
    text = text.replace('ò', 'ó')
    text = text.replace('ù', 'ú')
    text = text.replace('ü', 'u')
    text = text.replace('ï', 'i')

    #- Transliterate string to list:
    masterList = text.split(' ')
    masterList.pop()
    masterList.pop(0)

    masterList.sort()
    return masterList


def filterLexi(palabras):

    open(negroList)

    if len(blancaLista) != 0:
        emps, vocs, fono, cons = allDBuild(blancoLista)

###################
#- These are builders. They will consume and filter new words.


def allDBuild(palabras):

    emps = empsBuild(palabras)
    print('final length =', len(emps))
    vocs = vocsBuild(palabras)
    print('final length =', len(vocs))
    fono = fonoBuild(palabras)
    print('final length =', len(fono))
    cons = consBuild(palabras)
    print('final length =', len(cons))

    return emps, vocs, fono, cons

def empsBuild(palabras):

    emps = globalOpen('emps')
    thisCt = 0

    for all in palabras:

        try:
            emps[all]
            #print('emps ya tienen:', all)

        except KeyError:
            thisCt += 1
            if thisCt%1000 == 0:
                print(thisCt, '@', all, '#emps')

            pWord = all
            pLine = all

            #- Change vowels for processing
            pLine = pLine.replace('h', '')
            pLine = pLine.replace('que', 'qre')
            pLine = pLine.replace('qué', 'qré')
            pLine = pLine.replace('gue', 'ghe')
            pLine = pLine.replace('gué', 'ghé')
            pLine = pLine.replace('qui', 'qri')
            pLine = pLine.replace('quí', 'qrí')
            pLine = pLine.replace('gui', 'ghi')
            pLine = pLine.replace('guí', 'ghí')
            pLine = pLine.replace('y', 'i')
            pLine = pLine.replace('ü', 'u')
            #tripthongs
            pLine = pLine.replace('uai', 'a')
            pLine = pLine.replace('uoi', 'a')
            pLine = pLine.replace('uei', 'a')
            pLine = pLine.replace('iai', 'a')
            pLine = pLine.replace('iei', 'a')
            pLine = pLine.replace('ioi', 'a')
            pLine = pLine.replace('iau', 'a')
            pLine = pLine.replace('iou', 'a')
            pLine = pLine.replace('ieu', 'a')
            pLine = pLine.replace('uau', 'a')
            pLine = pLine.replace('ueu', 'a')
            pLine = pLine.replace('uou', 'a')
            pLine = pLine.replace('uáu', 'í')
            pLine = pLine.replace('uóu', 'í')
            pLine = pLine.replace('uéu', 'í')
            pLine = pLine.replace('iáu', 'í')
            pLine = pLine.replace('iéu', 'í')
            pLine = pLine.replace('ióu', 'í')
            pLine = pLine.replace('uái', 'á')
            pLine = pLine.replace('uéi', 'á')
            pLine = pLine.replace('uói', 'á')
            pLine = pLine.replace('iói', 'á')
            pLine = pLine.replace('iái', 'á')
            pLine = pLine.replace('iéi', 'á')
            #exceptions
            pLine = pLine.replace('aa', 'aba')
            pLine = pLine.replace('ee', 'efe')
            pLine = pLine.replace('oo', 'opo')
            pLine = pLine.replace('uu', 'uvu')
            pLine = pLine.replace('ii', 'iji')

            #diphthongs
            pLine = pLine.replace('ua', 'ã')
            pLine = pLine.replace('uo', 'õ')
            pLine = pLine.replace('ue', 'ê')
            pLine = pLine.replace('ia', 'ä')
            pLine = pLine.replace('ie', 'ë')
            pLine = pLine.replace('io', 'ö')
            pLine = pLine.replace('au', 'ũ')
            pLine = pLine.replace('ou', 'û')
            pLine = pLine.replace('eu', 'ü')
            pLine = pLine.replace('ai', 'ĩ')
            pLine = pLine.replace('ei', 'î')
            pLine = pLine.replace('oi', 'ï')
            pLine = pLine.replace('ui', 'ī')
            pLine = pLine.replace('iu', 'ū')
            pLine = pLine.replace('áu', 'í')
            pLine = pLine.replace('óu', 'í')
            pLine = pLine.replace('éu', 'í')
            pLine = pLine.replace('ái', 'í')
            pLine = pLine.replace('éi', 'í')
            pLine = pLine.replace('ói', 'í')
            pLine = pLine.replace('ué', 'ĕ')
            pLine = pLine.replace('ié', 'ė')
            pLine = pLine.replace('uó', 'ŏ')
            pLine = pLine.replace('ió', 'ő')
            pLine = pLine.replace('uá', 'ă')
            pLine = pLine.replace('iá', 'ą')

            pLine = pLine.replace('ý', 'í')


            pEmps = []
            empString = []
            accSnag = int(0)
            hit  = int(0)
            #print('empStart')

            #print(pWord)
            for all in accVow:
                #print(all)
                if pLine.find(all) > 0:
                    accSnag += 1
                    while pLine != str():
                        try:
                            for all in accVow:
                                if pLine[0] == all:
                                    pEmps.append('1')
                                    #print('1')
                                    pLine = pLine.lstrip(all)
                                else:
                                    for all in vow:
                                        try:
                                            if pLine[0] == all:
                                                #print('0')
                                                pEmps.append('0')
                                                pLine = pLine.lstrip(all)
                                            else:
                                                for all in cons:
                                                    con0 = str(all)
                                                    try:
                                                        pLine = pLine.lstrip(con0)
                                                    except IndexError:
                                                        continue
                                        except IndexError:
                                            continue
                        except IndexError:
                            continue

                empString.extend(pEmps)
                pEmps = []

            if accSnag == 0:
                pLine.rstrip(' ')
                for all in empPat1:
                    measure = len(pLine) - 1
                    if pLine[measure:] == all:
                        hit += 1
                while pLine != str():
                    for all in cons:
                        con0 = str(all)
                        try:
                            if pLine[0] == con0:
                                pLine = pLine.lstrip(con0)
                            else:
                                for all in allVow:
                                    try:
                                        if pLine[0] == all:
                                            #print('0')
                                            pEmps.append('0')
                                            pLine = pLine.lstrip(all)
                                        else:
                                            pLine = pLine.lstrip()
                                    except IndexError:
                                        continue
                        except IndexError:
                            continue
                eCt = int(pEmps.count('0'))
                eCt = eCt + pEmps.count('1')
                if hit >= 1:
                    if eCt > 1:
                        pEmps.pop()
                        pEmps.pop()
                        pEmps.extend('1')
                        pEmps.extend('0')
                        empString.extend(pEmps)
                    else:
                        empString.extend(pEmps)
                else:
                    if eCt > 1:
                        pEmps.pop()
                        pEmps.extend('1')
                        empString.extend(pEmps)
                    else:
                        empString.extend(pEmps)
            if thisCt%1000 == 0:
                print(empString)
            emps[pWord] = empString

            pEmps = []
            empString = []
            accSnag = int(0)
            hit  = int(0)

    globalClose(emps, 'emps')

    return emps


def vocsBuild(palabras):

    vocs = globalOpen("vocs")
    thisCt = 0

    for all in palabras:
        #print('vocs=', all)
        zCt = palabras.count(all)

        try:
            vocs[all]
            #print('vocs ya tienen:', all)

        except KeyError:
            pLine = all
            pWord = all
            thisCt += 1
            if thisCt%1000 == 0:
                print(thisCt, '@', all, ' #vocs')
            index = []
            iA = 0
            hitNum = 0
            pLen = (len(pLine))
            iB = []
            catch = []
            vowString = []
            pLine = pLine.replace('h', '')
            pLine = pLine.replace('que', 'qre')
            pLine = pLine.replace('qué', 'qre')
            pLine = pLine.replace('gue', 'ghe')
            pLine = pLine.replace('gué', 'ghe')
            pLine = pLine.replace('qui', 'qri')
            pLine = pLine.replace('quí', 'qri')
            pLine = pLine.replace('gui', 'ghi')
            pLine = pLine.replace('guí', 'ghi')
            pLine = pLine.replace('ü', 'u')
            pLine = pLine.replace('y', 'i')
            pLine = pLine.replace('uai', '4')
            pLine = pLine.replace('uoi', '5')
            pLine = pLine.replace('uei', '6')
            pLine = pLine.replace('iai', '7')
            pLine = pLine.replace('iei', '8')
            pLine = pLine.replace('ioi', '9')
            pLine = pLine.replace('iau', '0')
            pLine = pLine.replace('iou', '@')
            pLine = pLine.replace('ieu', '#')
            pLine = pLine.replace('uau', '$')
            pLine = pLine.replace('ueu', '%')
            pLine = pLine.replace('uou', '&')
            pLine = pLine.replace('uáu', '$')
            pLine = pLine.replace('uóu', '&')
            pLine = pLine.replace('uéu', '%')
            pLine = pLine.replace('iáu', '0')
            pLine = pLine.replace('iéu', '#')
            pLine = pLine.replace('ióu', '@')
            pLine = pLine.replace('uái', '4')
            pLine = pLine.replace('uéi', '6')
            pLine = pLine.replace('uói', '5')
            pLine = pLine.replace('iói', '9')
            pLine = pLine.replace('iái', '7')
            pLine = pLine.replace('iéi', '8')

            pLine = pLine.replace('ua', ':')
            pLine = pLine.replace('uo', ';')
            pLine = pLine.replace('ue', '?')
            pLine = pLine.replace('ia', '!')
            pLine = pLine.replace('ie', '(')
            pLine = pLine.replace('io', ')')
            pLine = pLine.replace('au', '[')
            pLine = pLine.replace('ou', ']')
            pLine = pLine.replace('eu', '{')
            pLine = pLine.replace('ai', '}')
            pLine = pLine.replace('ei', '<')
            pLine = pLine.replace('oi', '.')
            pLine = pLine.replace('áu', '[')
            pLine = pLine.replace('óu', ']')
            pLine = pLine.replace('éu', '{')
            pLine = pLine.replace('ái', '}')
            pLine = pLine.replace('éi', '<')
            pLine = pLine.replace('ói', '.')
            pLine = pLine.replace('ui', '1')
            pLine = pLine.replace('iu', '2')
            pLine = pLine.replace('ué', '?')
            pLine = pLine.replace('ié', '(')
            pLine = pLine.replace('uó', ';')
            pLine = pLine.replace('ió', ')')
            pLine = pLine.replace('uá', ':')
            pLine = pLine.replace('iá', '!')
            pLine = pLine.replace('á', 'a')
            pLine = pLine.replace('é', 'e')
            pLine = pLine.replace('í', 'i')
            pLine = pLine.replace('ó', 'o')
            pLine = pLine.replace('ú', 'u')

            pLine = pLine.replace('è', 'e')

            for each in vow:
                iA = 0
                baseNum = 0
                vowCt = pLine.count(each)
                #print('vCt=', vowCt)
                while vowCt > 0:
                    hitNum = pLine[iA:].index(each)
                    baseNum = hitNum + iA
                    index.append(baseNum)
                    iA = baseNum + 1
                    vowCt -= 1
                    if thisCt%1000 == 0:
                        print('iA:', iA, ' | :', catch, ' | index:', index)
            index.sort()

            for int in index:
                vowString.append(pLine[int])
            index = []
            if thisCt%100 == 0:
                print(vowString)
            vocs[pWord] = vowString

    globalClose(vocs, "vocs")

    return vocs


def fonoBuild(palabras):

    fono = globalOpen('fono')
    xCt = 0
    grabList = []
    lexiLib = str()

    for all in palabras:
        try:
            fono[all]
        except KeyError:
            grabList.append(all)

    print('fonoStart')
    thisCt = int(0)

    for all in grabList:
        thisCt += 1
        #print('wordCount2:', len(masterLPop), all)

        pLine = str()
        pLine = all

        if (pLine[0] == 'ps'):
            pLine.lstrip('p')

        pLine = pLine.replace('ch', '3')
        pLine = pLine.replace('ll', '2')
        pLine = pLine.replace('rr', '1')
        pLine = pLine.replace('ü', 'u')
        pLine = pLine.replace('y', 'i')
        pLine = pLine.replace('h', '')

        pLine = pLine.replace('ge', 'je')
        pLine = pLine.replace('gi', 'ji')
        pLine = pLine.replace('gé', 'jé')
        pLine = pLine.replace('gí', 'jí')

        pLine = pLine.replace('gue', 'ge')
        pLine = pLine.replace('gui', 'gi')
        pLine = pLine.replace('gué', 'gé')
        pLine = pLine.replace('guí', 'gí')

        pLine = pLine.replace('que', 'ke')
        pLine = pLine.replace('qui', 'ki')
        pLine = pLine.replace('qué', 'ké')
        pLine = pLine.replace('quí', 'kí')

        pLine = pLine.replace('ca', 'ka')
        pLine = pLine.replace('ce', 'se')
        pLine = pLine.replace('ci', 'si')
        pLine = pLine.replace('co', 'ko')
        pLine = pLine.replace('cu', 'ku')
        pLine = pLine.replace('cá', 'ká')
        pLine = pLine.replace('cé', 'sé')
        pLine = pLine.replace('cí', 'sí')
        pLine = pLine.replace('có', 'kó')
        pLine = pLine.replace('cú', 'kú')

        pLine = pLine.replace('c', 'k')
        pLine = pLine.replace('q', 'k')
        pLine = pLine.replace('x', 'ks')
        pLine = pLine.replace('nn', 'n')
        pLine = pLine.replace('mm', 'm')
        pLine = pLine.replace('pp', 'p')
        pLine = pLine.replace('tt', 't')
        pLine = pLine.replace('bb', 'b')
        pLine = pLine.replace('dd', 'd')
        pLine = pLine.replace('kk', 'k')
        pLine = pLine.replace('vv', 'b')
        pLine = pLine.replace('v', 'b')
        pLine = pLine.replace('bb', 'b')
        pLine = pLine.replace('zz', 'z')
        pLine = pLine.replace('ss', 's')
        pLine = pLine.replace('ff', 'f')

        pLine = pLine.replace('3', 'c')
        pLine = pLine.replace('2', 'h')
        pLine = pLine.replace('1', 'q')

        pLine = pLine.replace('uai', '4')
        pLine = pLine.replace('uoi', '5')
        pLine = pLine.replace('uei', '6')
        pLine = pLine.replace('iai', '7')
        pLine = pLine.replace('iei', '8')
        pLine = pLine.replace('ioi', '9')
        pLine = pLine.replace('iau', '0')
        pLine = pLine.replace('iou', '1')
        pLine = pLine.replace('ieu', '2')
        pLine = pLine.replace('uau', '3')
        pLine = pLine.replace('ueu', '%')
        pLine = pLine.replace('uou', '&')

        pLine = pLine.replace('uáu', '+')
        pLine = pLine.replace('uóu', '-')
        pLine = pLine.replace('uéu', '|')
        pLine = pLine.replace('iáu', 'A')
        pLine = pLine.replace('iéu', 'E')
        pLine = pLine.replace('ióu', 'I')
        pLine = pLine.replace('uái', 'O')
        pLine = pLine.replace('uéi', 'U')
        pLine = pLine.replace('uói', 'Q')
        pLine = pLine.replace('iói', 'W')
        pLine = pLine.replace('iái', 'E')
        pLine = pLine.replace('iéi', 'R')

        pLine = pLine.replace('ua', 'T')
        pLine = pLine.replace('uo', 'Y')
        pLine = pLine.replace('ue', 'P')
        pLine = pLine.replace('ia', 'S')
        pLine = pLine.replace('ie', 'D')
        pLine = pLine.replace('io', 'F')
        pLine = pLine.replace('au', 'G')
        pLine = pLine.replace('ou', 'H')
        pLine = pLine.replace('eu', 'J')
        pLine = pLine.replace('ai', 'K')
        pLine = pLine.replace('ei', 'L')
        pLine = pLine.replace('oi', 'Z')

        pLine = pLine.replace('áu', 'X')
        pLine = pLine.replace('óu', 'C')
        pLine = pLine.replace('éu', 'V')
        pLine = pLine.replace('ái', 'B')
        pLine = pLine.replace('éi', 'N')
        pLine = pLine.replace('ói', 'M')
        pLine = pLine.replace('ui', '`')
        pLine = pLine.replace('iu', '=')
        pLine = pLine.replace('ué', '_')
        pLine = pLine.replace('ié', '-')
        pLine = pLine.replace('uó', 'x')
        pLine = pLine.replace('ió', 'v')
        pLine = pLine.replace('uá', 'y')
        pLine = pLine.replace('iá', 'ü')

        lexiLib = lexiLib + ' ' + all
        xCt += 1

        fono[all] = pLine

    globalClose(fono, 'fono')

    return fono

def consBuild(palabras):

    cons = globalOpen('cons')
    thisCt = 0

    for all in palabras:
        try:
            cons[all]

        except KeyError:
            pLine = all
            if thisCt%1000 == 0:
                print(thisCt, '@', all, ' #cons')

            if pLine[0] == 'r':
                pLine = '1'+pLine[1:]

            pLine = pLine.replace('ch', '3')
            pLine = pLine.replace('ll', '2')
            pLine = pLine.replace('rr', '1')
            pLine = pLine.replace('h', '')

            pLine = pLine.replace('ge', 'je')
            pLine = pLine.replace('gi', 'ji')
            pLine = pLine.replace('gé', 'jé')
            pLine = pLine.replace('gí', 'jí')

            pLine = pLine.replace('gue', 'ge')
            pLine = pLine.replace('gui', 'gi')
            pLine = pLine.replace('gué', 'gé')
            pLine = pLine.replace('guí', 'gí')

            pLine = pLine.replace('que', 'ke')
            pLine = pLine.replace('qui', 'ki')
            pLine = pLine.replace('qué', 'ké')
            pLine = pLine.replace('quí', 'kí')

            pLine = pLine.replace('ca', 'ka')
            pLine = pLine.replace('ce', 'se')
            pLine = pLine.replace('ci', 'si')
            pLine = pLine.replace('co', 'ko')
            pLine = pLine.replace('cu', 'ku')
            pLine = pLine.replace('cá', 'ká')
            pLine = pLine.replace('cé', 'sé')
            pLine = pLine.replace('cí', 'sí')
            pLine = pLine.replace('có', 'kó')
            pLine = pLine.replace('cú', 'kú')

            pLine = pLine.replace('c', 'k')
            pLine = pLine.replace('q', 'k')
            pLine = pLine.replace('x', 'ks')
            pLine = pLine.replace('nn', 'n')
            pLine = pLine.replace('mm', 'm')
            pLine = pLine.replace('pp', 'p')
            pLine = pLine.replace('tt', 't')
            pLine = pLine.replace('bb', 'b')
            pLine = pLine.replace('dd', 'd')
            pLine = pLine.replace('kk', 'k')
            pLine = pLine.replace('vv', 'b')
            pLine = pLine.replace('v', 'b')
            pLine = pLine.replace('bb', 'b')
            pLine = pLine.replace('zz', 'z')
            pLine = pLine.replace('ss', 's')
            pLine = pLine.replace('ff', 'f')

            pLine = pLine.replace('á', '')
            pLine = pLine.replace('é', '')
            pLine = pLine.replace('í', '')
            pLine = pLine.replace('ó', '')
            pLine = pLine.replace('ú', '')
            pLine = pLine.replace('a', '')
            pLine = pLine.replace('e', '')
            pLine = pLine.replace('i', '')
            pLine = pLine.replace('o', '')
            pLine = pLine.replace('u', '')
            pLine = pLine.replace('y', '')
            pLine = pLine.replace('ý', '')

            if thisCt%1000 == 0:
                print(pLine)
            cons[all] = pLine
            thisCt+=1
            continue

    ## REMOVE <IF VAL != 0 CONDITION IN GLOBALCLOSE()> ##
    globalClose(cons, 'cons')


###################
#- This is wordprep. It will return lists of missing/unusable words.

def globalCheck(laLista, elNombre, palabras, textNomer):

    print('Testing incogruencies for '+elNombre)
    zCt = 0

    List = []
    negroLista = []
    for all in palabras:
##        zCt += 1
##        if zCt%1000 == 0:
##            print(zCt, '@', all)
        try:
            testLen = len(laLista[all])
            if testLen == 0:
                #print(all, 'has no ' + elNombre)
                negroLista.append(all)
                errataList.append(all)
            continue
        except KeyError:
            #print(elNombre + ' missing=', all)
            negroLista.append(all)
            errataList.append(all)
            continue

    incog = str()
    iCt = 0
    for all in errataList:
        iCt = errataList.count(all)
        while iCt > 1:
            iCt = errataList.count(all)
            errataList.remove(all)
        incog = (all+' '+incog)
    textNomer = str(input('Type name and filepath to write errata:  '))
    open(textNomer+'-'+elNombre+'.txt', 'w', encoding='latin-1').write(incog)


    return negroLista

#- Use these functions to open global data

def globalOpen(name, mode):

    lib = {}

    libFile = csv.reader(open(name, 'r+', encoding='utf-8'))
    
    for line in libFile:
        if line != []:
            if mode == 'lista':
                lib[line[0]] = list(line[1])
            elif mode == 'string':
                lib[line[0]] = str(line[1])

    return lib

def globalClose(lib, name):

    libFile = csv.writer(open("__global/__data/" + name + "File.csv", "w+", encoding='latin-1'))

    for key, val in lib.items():
        ## REMOVE NEXT LINE'S CONDITION FOR CONSBUILD ##
        if val != []:
            svData = str()
            for each in lib[key]:
                svData = svData + each
            val = svData
            libFile.writerow([key, val])

def allDicsOpen(palabras, textNomer):

    lib = {}
    emps = {}
    vocs = {}
    fono = {}
    cons = {}
    negroLista = []
    dicSets = emps, vocs, fono, cons
    dicNames = 'emps', 'vocs', 'fono', 'cons'
    iCt = int(0)
    print('Opening dics...')
    negroLista = str()
    for each in dicSets:
        each = {}
        print('Opening '+dicNames[iCt]+'...')
        each = globalOpen(dicNames[iCt])
        print(len(each))
        #negroLista.append(globalCheck(each, dicNames[iCt], palabras, textNomer))
        #globalClose(each, dicNames[iCt])
        print(dicNames[iCt] + ' loaded')
        iCt+=1
    return  emps, vocs, fono, cons, negroLista


###################
#- Use these functions to find data from a string


def vocsLine(pLine, vocs):

    vocsLine = []
    vocHost = pLine.split(' ')
    for all in vocHost:
        vocsLine.extend(vocs[all])
    return vocsLine


def empsLine(pLine, emps, doubles, empKeyLet):

    empsLine = []
    #empHost = pLine.split(' ')
##    for all in silentPunx:
##        while all in pLine:
##            pLine.remove(all)
    for all in pLine:
        if (all not in silentPunx) and (len(all) > 0):
            eWord = all.lower()
            try:
                emps[eWord]
            except KeyError:
                try:
                    eWord = eWord[0].upper()+eWord[1:]
                    emps[eWord]
                except KeyError:
                    empsLine = []
                    #print('kE empsLine:', all)
                    break
                except IndexError:
                    print('wut?', eWord)
                    continue
            if all != '':
                eWord = all.lower()
                for each in silentPunx:
                    if each in eWord:
                        eWord = eWord.replace(each, '')
                if len(eWord) > 0:
                    if eWord in doubles:
                        doubInt = int(0)
                        eWord = eWord+'('+str(doubInt)+')'
                        testEmps = empsLine+emps[eWord]
                        while testEmps != empKeyLet[:len(testEmps)]:
                            try:
                                #print('testEmps:', testEmps)
                                testEmps = testEmps[:-len(emps[eWord])]
                                doubInt+=1
                                eWord = eWord[:-3]+'('+str(doubInt)+')'
                                testEmps = empsLine+emps[eWord]
                            except KeyError:
                                eWord = eWord[:-3]+'(0)'
                                continue
                    for each in emps[eWord]:
                        empsLine.append(each)
    return empsLine


def fonoLine(pLine, fono):

    fonoLine = []
    fonoHost = pLine.split(' ')
    for all in fonoHost:
        fonoLine.append(fono[all])
    return fonoLine


def consLine(pLine, cons):

    consLine = []
    consHost = pLine.split(' ')
    for all in empHost:
        consLine.append(cons[all])
    return consLine


def getLineData(pLine, vocs, emps, cons, phos):

    pLVocs = []
    pLEmps = []
    pLFono = []
    pLCons = []
    splitText = []

    pLVocs = vocsLine(pLine, vocs)
    pLEmps = empsLine(pLine, emps)
    pLFono = fonoLine(pLine, phos)
    pLCons = consLine(pLine, cons)

    splitText = pLine.split(' ')
    lastWord = splitText.pop()
    pLen = len(pLine)

    return pLVocs, pLEmps, pLFono, pLCons, lastWord


def testWords(pLine, pWList):

    pWLCt = len(pWList)
    pWord = 'nada'
    pLEmps = gloFunk.empsLine(pLine)
    pLELen = len(pLEmps)
    click = 1

    while (pWLCt > 0) and (click != 0):

        cntStr = str(pWLCt)

        pWord = pWList.pop(random.choice(range(0, pWLCt)))
        pWLCt = len(pWList)

        pWEmps = []

        for all in emps[pWord]:
            pWEmps.append(all)
        pWELen = len(pWEmps)

        for all in pWEmps:
            pLEmps.append(all)
        pLELen = len(pLEmps)

        #print('tst:: pLine: ', pLine, ' | pWord: ', pWord, ' | left: ', cntStr)

        if ((pLEmps != empKey[0:pLELen]) or (pLEmps > empKey[:empKLen])) and (pWLCt > 0):
            yCt = 0
            while yCt < pWELen:
                pLEmps.pop()
                yCt += 1
        else:
            click = 0

    if pWLCt == 0:
        click = 1

    #print('testWordData = ', pLine, pLEmps, 'pLELen=', pLELen, 'cl:', click)

    return pLine, pWord, pLEmps, pLELen, pWList, click


def testWordsRV(pLine, pWList):

    pWLCt = len(pWList)
    pWord = 'nada'
    pLEmps = gloFunk.empsLine(pLine)
    pLELen = len(pLEmps)
    click = 1

    while (pWLCt > 0) and (click != 0):

        cntStr = str(pWLCt)

        pWord = pWList.pop(random.choice(range(0, pWLCt)))
        pWLCt = len(pWList)

        pWEmps = []

        for all in emps[pWord]:
            pWEmps.append(all)
        pWELen = len(pWEmps)

        pLEmps = pWEmps + pLEmps

        print('tst:: pLine: ', pLine, ' | pWord: ', pWord, ' | left: ', cntStr)

        if ((pLEmps != empKey[(empKLen - pLELen):empKLen]) or (pLEmps > empKey[:empKLen])) and (pWLCt > 0):
            yCt = 0
            while yCt < pWELen:
                pLEmps.pop(0)
                yCt += 1
            spentList.append(pWord)
        else:
            click = 0

    if pWLCt == 0:
        click = 1

    #print('testWordData = ', pLine, pLEmps, 'pLELen=', pLELen, 'cl:', click)

    return pLine, pWord, pLEmps, pLELen, pWList, spentList, click


def lastWData(lastWord):

    lastWEmps = []
    for all in emps[lastWord]:
        lastWEmps.append(all)
    for all in vocs[lastWord]:
        lastWVocs.append(all)
    lastWELen = len(lastWEmps)
    lastLECt = empKLen - lastWELen
    return lastWVocs, lastWEmps, lastWELen, lastLECt


##masterLexi = dirtyLexi('__txtBiblioteca/es-ES-opti.txt')
##negroLista = dirtyLexi('__txtBiblioteca/negroList.txt')
##scndNegro = 'mbits', 'vme', 'kant', 'fetch', 'fddi', 'theuth', 'helmholtz', 'trap', 'phi', 'cpu', 'judit', 'ieee', 'cm', 'mhz', 'km', 'mm', 'khz', 'oh', 'i', 'bcd', 'eh', 'hao', 'ghz', 'hz', 'bits', 'kbits', 'khces', 'mflops', 'mhces', 'gflops', 'ghces', 'marx', 'scsi', 'dma', 'gflop', 'mflop', 'traps', 'tick', 'checkpoints', 'ccitt', 'chist', 'kbit', 'mbit', 'sangley', 'mmu', 'risc', 'cisc'
##for all in scndNegro:
##    negroLista.append(all)
##for all in negroLista:
##    try:
##        masterLexi.remove(all)
##    except ValueError:
##        continue
##emps=globalOpen('emps')
##vocs=globalOpen('vocs')
##fono=globalOpen('fono')
##cons=globalOpen('cons')
##superDic = {}
##for each in masterLexi:
##    thisEmps = str()
##    for all in emps[each]:
##        thisEmps = thisEmps+all
##    thisVocs = str()
##    for all in vocs[each]:
##        thisVocs = thisVocs+all
##    thisFono = str()
##    for all in fono[each]:
##        thisFono = thisFono+all
##    thisCons = str()
##    for all in cons[each]:
##        thisCons = thisCons+all
##    superDic[each] = str(thisEmps+'+'+thisVocs+'+'+thisFono+'+'+thisCons)
##globalClose(superDic, 'superDic')



#####
#  rhymes&rimas

def rhyFileOpen(lang, pWord, emps, fono, vocs, cons, empKeyLet, doubles):
    #print('vocs:', len(vocs))
    rhyWords = []
    vocSpots = []
    #vCt = int(0)
    vIndex = int(0)
    vSpot = int(0)
    try:
        rhyWord = fono[pWord.lower()]
    except KeyError:
        try:
            rhyWord = fono[pWord[0].upper()+pWord[1:]]
        except KeyError:
            #print('RHY no data for ', rhyWord)
            return
    #print('len(emps):', len(emps))
    #print('vocSpots1 :', vocSpots)
    #print('pWord = '+pWord, '| rhyWord = ', rhyWord)
    for each in vocsList:
        elVoc = each
        #print('vSpot Data:', rhyWord, '| searching:', elVoc, '\nmeta |', vSpot, vIndex, elVoc)
        vIndex = 0
        while elVoc in rhyWord:
            try:
                vSpot = rhyWord.index(elVoc, vIndex)
                vocSpots.append(vSpot)
                vIndex = vSpot+1
                #print('vocSpots', vocSpots, '\nmeta |', vSpot, vIndex, elVoc)
            except ValueError:
                #print('vE')
                vIndex = 0
                vSpot = 0
                break
    vocSpots.sort()
    rSyls = 1
    vCt=int(1)
    if len(vocSpots) > 0:
        lastClean = int(len(rhyWord) - vocSpots[0] - len(vocSpots))
        lastRSyls = len(vocSpots)
    else:
        lastClean = int(1)
        lastRSyls = int(1)
    for tVocs in range(2, 10):
        rhymeList = []
        #print('vocSpots2 :', vocSpots)
        if lastClean < 0:
            lastClean == 0
        if 4 == tVocs:
            rSyls+=0
        elif len(vocSpots) > 0:
            clenR = len(rhyWord) - vocSpots.pop() - vCt + 1
            rSyls+=1
            vCt+=1
        else:
            rSyls = lastRSyls
            clenR = lastClean
            #print('alpha')
            
            
        if lang == 'eng':
            datapath = 'data/UKen/rhymes/publish/2@/rhymeLib-t'
        elif lang == 'esp':
            datapath = 'there'
        tName = str(tVocs)
        rName = str(rSyls)
        cName = str(clenR)
        if tVocs < 10:
            tName = '0'+tName
        if rSyls < 10:
            rName = '0'+rName
        if clenR < 10:
            cName = '0'+cName
        #print('rhydata: '+tName+'r'+rName+'c'+cName)
        rhyFile = csv.reader(open(datapath+tName+'r'+rName+'c'+cName +'.csv', 'r+'))
        for line in rhyFile:
            if line!=[]:
                testLine = line[0].split('^')
                if pWord in testLine:
                    #print('hit')
                    rhymeList = line[1].split('^')
        strikeList = []
        for all in rhymeList:
            try:
                pWEmps = emps[pWord]
                if all in doubles:
                    doubInt = int(0)
                    while 1 > 0:
                        try:
                            doubWord = all + '('+str(doubInt)+')'
                            if vocs[doubWord][-1] != vocs[pWord]:
                                strikeList.append(all)
                            else:
                                qWord = doubWord
                            doubInt+=1
                        except KeyError:
                            qWord = all
                            break
                else:
                    qWord = all
##                try:                   
##                    vocs[qWord][-1]
##                except KeyError:
##                    print('kEvocs', qWord)
##                    continue
##                try:
##                    vocs[pWord][-1]
##                except KeyError:
##                    print('kEvocs', pWord)
##                try:
##                    #print(cons[pWord][-1])
##                    cons[qWord][-1]
##                except KeyError:
##                    print('kEcons', pWord, '&', qWord)
##                try:
##                    #print(fono[pWord][-1])
##                    fono[qWord][-1]
##                except KeyError:
##                    print('kEfono', pWord, '&', qWord)
                try:
                    if (qWord not in strikeList) and (qWord != pWord) and (qWord not in rhyWords) and (vocs[pWord][-1] == vocs[qWord][-1]) and (cons[pWord][-1] == cons[qWord][-1]) and (fono[pWord][-1] == fono[qWord][-1]):
                        rhyWords.append(qWord)
                except IndexError:
                    continue
            except KeyError:
                #print('kE', pWord, '&', qWord)
                continue
        #print('glo+rhyWords:', len(rhyWords))
                    
    return rhyWords
