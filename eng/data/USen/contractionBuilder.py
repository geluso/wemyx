import csv

emps = csv.reader(open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/USen/empDic-USen-unik.csv', 'r+'))

letList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
firstCharList = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

contractions = []
contractionFile = open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/USen/contractionList.txt', 'w+')
surnameList = open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/USen/surnameList.txt', 'w+')
contractionSwitch = csv.writer(open('/home/tqastro/projects/skrypts/GitLib/wemyx/eng/data/USen/contractionSwitches.csv', 'w+'))
stillOut = []

for all in emps:
    if '(' in all[0]:  #  This takes care of words with more than one pronunciation
        pWord = all[0][:-3]
    else:  #  These are single-pronunciation words
        pWord = all[0]
    if pWord[0] in letList:
        letIndex = letList.index(pWord[0])
        firstCharList[letIndex].append(pWord)
        try:
            apostropheIndex = pWord.index("'")
            #print('found contrackt:', pWord)
            contractions.append(pWord)
        except ValueError:
            continue

print(len(contractions))
for all in contractions:
    firstCharChk = letList.index(all[0])
    contractionFile.write(all+'\n')
    #print(letList[firstCharChk], all)
    if all[-2:] == "'s" and all[:-2] in firstCharList[firstCharChk]:
        contractionSwitch.writerow([all, all[:-2]+' '+'is'])
    elif all[-3:] == "n't":
        if all[:-2] in firstCharList[firstCharChk]:
            contractionSwitch.writerow([all, all[:-2]+' '+'not'])
        elif all[:-3] in firstCharList[firstCharChk]:
            contractionSwitch.writerow([all, all[:-3]+' '+'not'])
        else:
            stillOut.append(all)
    elif all[-3:] == "'ll":
        if all[:-3] in firstCharList[firstCharChk]:
            contractionSwitch.writerow([all, all[:-3]+' '+'will'])
        else:
            stillOut.append(all)
    elif all[-2:] == "'d":
        if all[:-2] in firstCharList[firstCharChk]:
            contractionSwitch.writerow([all, all[:-2]+' '+'would'])
        else:
            stillOut.append(all)
    elif all[-3:] == "'re":
        if all[:-3] in firstCharList[firstCharChk]:
            contractionSwitch.writerow([all, all[:-3]+' '+'are'])
        else:
            stillOut.append(all)
    elif all[-3:] == "'ve":
        if all[:-3] in firstCharList[firstCharChk]:
            contractionSwitch.writerow([all, all[:-3]+' '+'have'])
        else:
            stillOut.append(all)
    elif all[:2] == ("o'"):
        surnameList.write(all+'\n')
    elif all == "i'm":
        contractionSwitch.writerow(["i'm", 'i am'])  # This one is common, but unique!
    elif all == "y'all":
        contractionSwitch.writerow(["y'all", 'you all'])  # This one is common, but unique!
    elif all[-1] != "'":
        stillOut.append(all)

print(stillOut)
