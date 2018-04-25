dataString = '-data-200tweets.json.balanced'
table = []

def getScore(filePath):
    for line in open(filePath):
        if line.startswith('mean acc:'):
            return str(round(float(line.split(' ')[2]), 1))
        if line.startswith('accuracy:'):
            return str(round(float(line.split(' ')[1]), 1))
    return '0'
    
langs = ['EN', 'NL', 'FR', 'PT', 'ES']
for srcLang in langs:
    table.append([srcLang])
    for tgtLang in langs:
        if srcLang == tgtLang:
            table[-1].append('    ')
        else:
            table[-1].append(getScore('runs/2.lexVScomb/' + srcLang + '.' + tgtLang + '.1-2.3-6.out'))

for i in table:
    print (' & '.join(i) + ' \\\\')

