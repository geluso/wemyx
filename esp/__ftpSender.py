
import ftplib
import csv
import gloFunk
csv.field_size_limit(int(9999999))

negroLista = gloFunk.dirtyLexi('__txtBiblioteca/negroList.txt')
missList = []

def ftpSender(tName, rName, cName):
    print('sending file...')
    sftp = ftplib.FTP('ftp.remezclemos.net', 'universe@remezclemos.net', '!Universe0')
    fp = open("__global/__data/__rimas/completadas/publish/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv",'rb') # file to send
    sftp.storbinary('STOR rimaLibs/rimaLib-t'+tName+"r"+rName+"c"+cName+".csv", fp) # Send the file

    fp.close() # Close file and FTP
    sftp.quit()

##tName = str()
##while tName != 'stop':
##    tName = str(input('tName to send:'))
##    rName = str(input('rName to send:'))
##    cName = str(input('cName to send:'))
##    ftpSender(tName, rName, cName)
##    tName = str(input('continue?:'))

def publishingEditor(tName, rName, cName, negroLista):
    libFile = csv.reader(open("__global/__data/__rimas/completadas/masterFiles/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv", "r"))
    dicFile = csv.writer(open("__global/__data/__rimas/completadas/publish/rimaLib-t"+tName+"r"+rName+"c"+cName+".csv", 'w', encoding='latin-1'))
    dic = {}
    print('preparing public version...')
    for line in libFile:
        if line != []:
            dic[line[0]] = str(line[1])
    for key, val in dic.items():
        keyChx = key.split('^')
        valChx = val.split('^')
        if (len(keyChx) != 1) or (len(valChx) != 1) or (keyChx != valChx):
            keyCode = str()
            valCode = str()
            for each in keyChx:
                if each not in negroLista:
                    if '…' in each: # this problem should be addressed in the masterFiles section
                        each.replace('…', '')
                    keyCode = str(keyCode)+'^'+str(each)                            
            for each in valChx:
                if each not in negroLista:
                    if '…' in each:
                        each.replace('…', '')
                    valCode = str(valCode)+'^'+str(each)
            if len(keyCode) > 0  and len(valCode) > 0:
                dicFile.writerow([keyCode[1:], valCode[1:]])

for totalVs in range(1, 11):
    for cleanR in range(1, 14):
        for rSyls in range(0, 11):
            if rSyls <= totalVs:
                tName = str(totalVs)
                rName = str(rSyls)
                cName = str(cleanR)
                if totalVs < 10:
                    tName = '0'+tName
                if rSyls < 10:
                    rName = '0'+rName
                if cleanR < 10:
                    cName = '0'+cName 
                print("opening t"+tName+'r'+rName+'c'+cName+'...')           
                try:
                    publishingEditor(tName, rName, cName, negroLista)
                    ftpSender(tName, rName, cName)
                    print('done with file')
                except IOError:
                    missList.append(tName+rName+cName)
                    continue
    for cleanR in range(0, 1):
        for rSyls in range(1, 11):
            if rSyls <= totalVs:
                tName = str(totalVs)
                rName = str(rSyls)
                cName = str(cleanR)                
                if totalVs < 10:
                    tName = '0'+tName
                if rSyls < 10:
                    rName = '0'+rName
                if cleanR < 10:
                    cName = '0'+cName 
                print("opening t"+tName+'r'+rName+'c'+cName+'...')          
                try:
                    publishingEditor(tName, rName, cName, negroLista)
                    ftpSender(tName, rName, cName)
                    print('done with file')
                except IOError:
                    missList.append(tName+rName+cName)
                    continue

print('missing:')
for all in missList:
    print(all+'\n')


print('ALL DONE!!!')
