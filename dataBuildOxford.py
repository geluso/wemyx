import csv
import gloFunk
csv.field_size_limit(int(99999999))

doubles = gloFunk.dirtyLexi('data/UKen/altsList.txt')
dicfile = open('data/UKen/phonoLib-UKen.txt', 'r')

phonoDic = {}
print(len(doubles))
theWord = str()


for line in dicfile:
    if line != []:
        data = line.split(';')
        keyNomer = str()
        if data[0] in doubles:
            if data[0] == theWord:
                iNum+=1
                keyNomer = str(data[0]+'('+str(iNum)+')')
                phonoDic[keyNomer] = data[1]
            else:
                iNum=0
                theWord = data[0]
                keyNomer = str(data[0]+'(0)')
                phonoDic[keyNomer] = data[1]
        else:
            phonoDic[data[0]] = data[1]

def dataBuilder(phonoDic):
    cons = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Z', '|']
    cSyl = ['L', 'M', 'N']
    vocs = ['a', 'e', 'i', 'o', 'u', 'y',  'A', 'E', 'I', 'O', 'U', 'V', 'Y', '3', '0', '@', '&', 'L', 'M',  'N', '%', '!', '#', '$', '^', '*', '(', ')', '?', '<', '>', '.', '|', ']', '[', '=']
    dips = {'eI':'!', 'aI':'#', 'oI':'$', 'I@':'^', 'e@':'(', 'U@':')', '@U':'?', 'aU':'<'}
    trip = {'aI@':'>', 'aU@':'.', 'oI@':'=', '@U@':'[', 'eI@':']'}
    nums = ['1','2', '3', '4', '5', '6', '7', '8', '9', '0']
    

    condition0 = []
    condition1 = []
    condition2 = ['led', 'med', 'ned', 'les', 'mes', 'nes']

    tripAsk = str(input('Build triphthongs? (Y/N) : ')) # tripAsk = 'y'
    schwa = str(input('Schwa='))
                
    empDic = {}
    phoDic = {}
    vocDic = {}
    conDic = {}
    webDic = {}

    tripList = []
    tripFile=open('data/UKen/tripList.txt', 'w+')


    for key, val in phonoDic.items():

        catch = int(0)
        keyCut = str(key)
        valCut = str(val.replace('N', '|'))
        phoCut = valCut

        ## Optional consideration of diphthongs and triphthongs

        #  comment these two for webPhono

        ## ++ TRIPHTHONGS ==
        
        if tripAsk == ('y' or 'Y'):
            for key, val in trip.items():
                search = str(key)
                while valCut.count(search) > 0:
                    valCut = valCut[:valCut.index(search)]+val+valCut[valCut.index(search)+3:]
                    #print('hit')
                    if keyCut != tripList[:-1]:
                        tripList.append(keyCut)
                    print(len(tripList))

        ## ++ DIPHTHONGS ++

        for key, val in dips.items():
            search = str(key)
            while valCut.count(search) > 0:
                valCut = valCut[:valCut.index(search)]+val+valCut[valCut.index(search)+2:]
        #print('tripdip valCut:', valCut)



        key = keyCut
        valCut = valCut.replace(" ", '')
        valCut = valCut.replace(":", '')
        valCut = valCut.replace("\n", '')
        valCut = valCut.replace("-", '')
        valCut = valCut.replace("+", '')
        phoCut = phoCut.replace(" ", '')
        phoCut = phoCut.replace(":", '')
        phoCut = phoCut.replace("\n", '')
        phoCut = phoCut.replace("-", '')
        phoCut = phoCut.replace("+", '')
        
        empDic[key] = valCut # save the apostrophe for emp detection
        #print(key, empDic[key])
        valCut = valCut.replace("'", '')
        #print(key, valCut)
        
        
        empMap = str()

        if empDic[key].count("'") > 1:
            print('+++\nhow the hell?', key, empDic[key], '\n+++')


        ## ++ SYLLABIC CONSONANTS ++

        ## Avoid occurances of 'll', 'mm', & 'nn' in the spelling
        
        doubLMN = ['ll', 'mm', 'nn', 'rr']
        keyCut = keyCut.replace('-', '')
        for all in doubLMN:
            if len(keyCut)>=4:
                if all in keyCut[len(keyCut)-4:]:
                    keyCut = key.replace(all, all[0])
        
    ##    if 'ions' == keyCut[len(keyCut)-4:]:
    ##        print(key, valCut, keyCut[len(keyCut)-4:])

        ## Detect spellings that evoke a syllabic consonant and replace them with '%' mark
            
        try:
        
            if ((keyCut[len(keyCut)-1] == 'l') or (keyCut[len(keyCut)-1] == 'm') or (keyCut[len(keyCut)-1] == 'n')) and (valCut[len(valCut)-1] in cons) and (keyCut[len(keyCut)-2] in vocs) and (valCut[len(valCut)-2] not in vocs):
                #print('before:', valCut)
    ##            if 'ion' == keyCut[len(keyCut)-3:]:
    ##                print('before:', valCut)
                valCut = valCut[:len(valCut)-1]+valCut[len(valCut)-1].upper()
                phoCut = phoCut[:len(phoCut)-1]+phoCut[len(phoCut)-1].upper()
                #print(key, valCut)
    ##            if 'ion' == keyCut[len(keyCut)-3:]:
    ##                print(key, valCut)
                #catch+=1

            ## --& (-_s):
                            
            elif ((keyCut[len(keyCut)-2:] == 'ls') or (keyCut[len(keyCut)-2:] == 'ms') or (keyCut[len(keyCut)-2:] == 'ns')) and (valCut[len(valCut)-2] in cons) and (keyCut[len(keyCut)-3] in vocs) and (valCut[len(valCut)-3] not in vocs):
                #print('before:', valCut, '---', keyCut[len(keyCut)-3], '---', valCut[len(valCut)-3])
    ##            if 'ions' == keyCut[len(keyCut)-4:]:
    ##                print('\nbefore:', valCut)
                valCut = valCut[:len(valCut)-2]+valCut[len(valCut)-2].upper()+valCut[len(valCut)-1]
                phoCut = phoCut[:len(phoCut)-2]+phoCut[len(phoCut)-2].upper()+phoCut[len(phoCut)-1]
    ##            if 'ions' == keyCut[len(keyCut)-4:]:
    ##                print(key, valCut)
                #print(key, valCut)
                #catch+=1

            ## --& (-_e):

            elif ((keyCut[len(keyCut)-2:] == 'le') or (keyCut[len(keyCut)-2:] == 'me') or (keyCut[len(keyCut)-2:] == 'ne')) and (valCut[len(valCut)-1] in cons) and (keyCut[len(keyCut)-3] in cons) and ((valCut[len(valCut)-1] and valCut[len(valCut)-2]) not in vocs):
                valCut = valCut[:len(valCut)-1]+valCut[len(valCut)-1].upper()
                phoCut = phoCut[:len(phoCut)-1]+phoCut[len(phoCut)-1].upper()
                #catch+=1

            ## --& (-_ed or -_es)

            elif (keyCut[len(keyCut)-3:] in condition2) and ((valCut[len(valCut)-3] not in vocs) or (valCut[len(valCut)-2] in cSyl)) and ((valCut[len(valCut)-2] not in vocs) or (valCut[len(valCut)-2] in cSyl)): 
                #print('before:', valCut)
                valCut = valCut[:len(valCut)-2]+valCut[len(valCut)-2].upper()+valCut[len(valCut)-1]
                phoCut = phoCut[:len(phoCut)-2]+phoCut[len(phoCut)-2].upper()+phoCut[len(phoCut)-1]
                print(key, valCut)
                #catch+=1
                
            ##

            elif 'ional' in keyCut:
                if '@nl' in valCut:
                    if valCut.count('@nl') > 1:
                        print("PROBLEM W/", key,  valCut)
                    else:
                        valCut = valCut.replace('@nl', '@nL')
##                elif 'Sn@l' in valCut:
##                    if valCut.count('Sn@l') > 1:
##                        print("PROBLEM W/", key,  valCut)
##                    else:
##                        valCut = valCut.replace('Sn@l', 'SnL')

            ##

            #elif

            ##   for (-ally):

            #elif (keyCut[len(keyCut)-3:] == 'lly') and (keyCut[len(keyCut)-4:len(keyCut)-3] in vocs) and (valCut[len(valCut)-3:len(valCut)-2] not in vocs):

        except IndexError:
            #print('hit')
            for each in cons:
                valCut = valCut.replace(each, '')
            if len(valCut) > 1:
                print('dunno: ', key)
            else:
                empDic[key] = '1'
            continue

        if schwa == '@':
            valCut = valCut.replace('L', '@l')
            valCut = valCut.replace('M', '@m')
            valCut = valCut.replace('N', '@n')
            phoCut = phoCut.replace("L", "@l")
            phoCut = phoCut.replace("M", "@m")
            phoCut = phoCut.replace("N", "@n")
        #  for webPhono:
##        else:
##            phoCut = phoCut.replace('L', '&#809l')
##            phoCut = phoCut.replace('N', '&#809n')
            
        valCut = valCut.replace('tS', 'C')
        valCut = valCut.replace('dZ', 'G')

        #  webPhono  #

        phoCut = phoCut.replace("&", "&aelig")
        phoCut = phoCut.replace("3", "&#949")
        phoCut = phoCut.replace("E", "&#603")
        phoCut = phoCut.replace("@", "&#477")
        phoCut = phoCut.replace("0", "&#596")
        phoCut = phoCut.replace("A", "&#594")
        phoCut = phoCut.replace("U", "&#650")
        phoCut = phoCut.replace("tS", "&#679")
        phoCut = phoCut.replace("T", "&#952")
        phoCut = phoCut.replace("dZ", "&#676")
        phoCut = phoCut.replace("S", "&#643")
        phoCut = phoCut.replace("V", "&#652")
        phoCut = phoCut.replace("D", "&#240")
        phoCut = phoCut.replace("|", "&#331")
        phoCut = phoCut.replace("L", "&#7735")
        phoCut = phoCut.replace('M', '&#809m')
        phoCut = phoCut.replace("N", "&#7751")
        phoCut = phoCut.replace("Z", "&#658")

        webDic[key] = phoCut
        phoDic[key] = valCut
        empLine = empDic[key]

        valCons = valCut
        for all in vocs:
            valCons = valCons.replace(all, '')

        conDic[key] = valCons
        
        ## Strip them into a vocLine, with the difference being one with a "'" for indicating emp   
        for each in cons:
            empLine = empLine.replace(each, '')
            valCut = valCut.replace(each, '')

        vocDic[key] = valCut
        
        if "'" in empDic[key]: # Anything with 2+ emps
            empPoint = int(empLine.index("'"))
            valCut = valCut[:empPoint]+'1'+(valCut[empPoint+1:])
            for each_char in valCut:
                if each_char != '1':
                    valCut = valCut.replace(each_char, '0')
            #if catch >= 1:
                #print(key, valCut)
        else: 
            valCut = '1' # Gets a qubit

        empDic[key] = valCut

    if tripAsk == ('y' or 'Y'):
        thongNum = str('3')
        for all in tripList:
            tripFile.write(all+'\n')
    else:
        thongNum = str('2')

    return empDic, vocDic, conDic, phoDic, webDic, thongNum, schwa

empDic, vocDic, conDic, phoDic, webDic, thongNum, schwa = dataBuilder(phonoDic)

print(len(empDic), len(vocDic), len(conDic), len(phoDic), len(thongNum), len(schwa))

empPhile = csv.writer(open('data/UKen/empDic-UKen('+thongNum+')'+schwa+'.csv', 'w+', encoding='utf8'))
for key, val in empDic.items():
    empPhile.writerow([key, val])
    
phonoPhile = csv.writer(open('data/UKen/phoDic-UKen('+thongNum+')'+schwa+'.csv', 'w+', encoding='utf8'))
for key, val in phoDic.items():
    phonoPhile.writerow([key, val])
    
consoPhile = csv.writer(open('data/UKen/conDic-UKen('+thongNum+')'+schwa+'.csv', 'w+', encoding='utf8'))
for key, val in conDic.items():
    consoPhile.writerow([key, val])
    
vocsaPhile = csv.writer(open('data/UKen/vocDic-UKen('+thongNum+')'+schwa+'.csv', 'w+', encoding='utf8'))
for key, val in vocDic.items():
    vocsaPhile.writerow([key, val])
    
##webPhoPhile = csv.writer(open('data/UKen/webPhonoDic-UKen('+thongNum+')'+schwa+'.csv', 'w+', encoding='utf8'))
##for key, val in webDic.items():
##    webPhoPhile.writerow([key, val])
    
superPhile = csv.writer(open('data/UKen/superDic-UKen('+thongNum+')'+schwa+'.csv', 'w+', encoding='utf8'))
for key, val in vocDic.items():
    try:
        superData = str(empDic[key]+'+'+vocDic[key]+'+'+phoDic[key]+'+'+conDic[key])
        superPhile.writerow([key, superData])
    except KeyError:
        print(key)
        continue
