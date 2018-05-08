import os
import json

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
for lang in langs:
    table.append([lang])

    #users
    if os.path.exists('data/' + lang + dataString):
        users = str(len(json.load(open('data/' + lang + dataString))['gender']))
    else:
        users = '0'
    # add commas
    if len(users) == 4:
        users = users[0] + ',' + users[1:]
    else:
        users = '  ' + users
    table[-1].append(users)

    #inLang lex
    table[-1].append(getScore('runs/2.lexVScomb/' + lang + '.' + lang + '.1-2.3-6.out'))

    #inLang abs
    table[-1].append(getScore('runs/2.lexVScomb/' + lang + '.' + lang + '.comb.5.0.out'))

    #cross lexAvg
    total = 0
    for otherLang in langs:
        if lang != otherLang:
            total += float(getScore('runs/2.lexVScomb/' + otherLang + '.' + lang + '.1-2.3-6.out'))
    table[-1].append(str(round(total/(len(langs)-1), 1)))

    #cross lexAll
    table[-1].append(getScore('runs/3.4-1/' + lang + '.out'))

    #cross embeds
    table[-1].append('0')

    #cross absAvs
    total = 0
    for otherLang in langs:
        if lang != otherLang:
            total += float(getScore('runs/2.lexVScomb/' + otherLang + '.' + lang + '.comb.5.0.out'))
    table[-1].append(str(round(total/(len(langs)-1), 1)))

    #cross absAll
    table[-1].append(getScore('runs/3.4-1/' + lang + '.comb.out'))


for i in table:
    print (' & '.join(i) + ' \\\\')
