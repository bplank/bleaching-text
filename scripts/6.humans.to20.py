import json
import sys


data = json.load(open(sys.argv[1]))

newData = {'tweets':[], 'gender':[]}
for i in range(len(data['tweets'])):
    newData['gender'].append(data['gender'][i])
    newTweets = ' NEWLINE '.join(data['tweets'][i].split(' NEWLINE ')[:20])
    newData['tweets'].append(newTweets)

json.dump(newData, open(sys.argv[2], 'w'))

