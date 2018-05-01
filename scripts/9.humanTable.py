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

def getHumanScore(filePath):
    data = json.load(open(filePath))
    scores = {}
    for i in range(len(data['human'])):
        for humanId in data['human'][i]:
            if humanId not in scores:
                scores[humanId] = [0,0]
            if data['human'][i][humanId] == data['gold'][i]:
                scores[humanId][0] = scores[humanId][0] + 1
            scores[humanId][1] = scores[humanId][1] + 1
    totalScores = 0
    for humanId in scores:
        totalScores += (scores[humanId][0] / scores[humanId][1])
    return str(round(100 * totalScores / len(scores), 1))
    
    
for lang in [('NL','NL'), ('NL', 'PT'), ('FR', 'NL')]:
    table.append([lang[0] + '$\mapsto$' + lang[1]])

    #human
    table[-1].append(getHumanScore('data_humans/' + lang[0] + '.' + lang[1] + '.json'))

    #lex 20
    table[-1].append(getScore('runs/6.humans/lex.' + lang[0] + '.' + lang[1] + '.20.out'))
    #lex 200
    table[-1].append(getScore('runs/6.humans/lex.' + lang[0] + '.' + lang[1] + '.200.out'))
    
    #comb 20
    table[-1].append(getScore('runs/6.humans/comb.' + lang[0] + '.' + lang[1] + '.20.out'))
    #comb 200
    table[-1].append(getScore('runs/6.humans/comb.' + lang[0] + '.' + lang[1] + '.200.out'))


for i in table:
    print (' & '.join(i) + ' \\\\')
