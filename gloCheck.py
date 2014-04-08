import gloFunk

vocs = gloFunk.globalOpen('data/UKen/vocDic-UKen(2)@.csv', 'lista')
emps = gloFunk.globalOpen('data/UKen/empDic-UKen(2)@.csv', 'lista')
cons = gloFunk.globalOpen('data/UKen/conDic-UKen(2)@.csv', 'lista')
phos = gloFunk.globalOpen('data/UKen/phoDic-UKen(2)@.csv', 'lista')

pLVocs, pLEmps, pLFono, pLCons, lastWord = gloFunk.getLineData('is my line', vocs, emps, cons, phos)
print('is my line\n', '\n', pLVocs,  '\n', pLEmps, '\n', pLFono, '\n', pLCons)
