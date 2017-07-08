
nameBank = open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/census-derived-all-first.txt', 'r+')
nameList = []
wordNameList0 = open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/nameWhiteList0.txt', 'r+')
wordNameList1 = open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/nameWhiteList1.txt', 'r+')
wordNames = []
pureNames = open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/pureNames.txt', 'w+')
nameWords = open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/nameWords.txt', 'w+')

for line in wordNameList0:
    lineBreak = line.split(' ')
    wordNames.append(lineBreak[0].lower())

for line in wordNameList1:
    try:
        breakSpot = line.index('was')
        thisWord = line[4:breakSpot].lower()
        #print(thisWord)
        if thisWord not in wordNames:
            wordNames.append(thisWord)
    except ValueError:
        continue

for line in nameBank:
    lineBreak = line.split(' ')
    if lineBreak[0].lower() not in wordNames:
        nameList.append(lineBreak[0].lower())

print(len(wordNames))
print(len(nameList))

for all in nameList:
    pureNames.write(all+'\n')
for all in wordNames:
    nameWords.write(all+'\n')