import sys
import csv
import json

if len(sys.argv) < 2:
    print('please give csv file(s)')
    exit(1)

data = {}

for i in range(1,len(sys.argv)):
     with open(sys.argv[i])as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row[0] == '_unit_id':
                continue
            if len(row) != 31 and len(row) != 33:
                print('Error!', len(row))
                continue
            guess = row[10]
            gold = row[11]
            sentId = row[0]
            userId = row[7]
            tweets = ' NEWLINE '.join(row[15:35])
            if tweets not in data:
                data[tweets] = {}
            data[tweets]['gold'] = gold
            data[tweets]['text'] = tweets
            if 'human' not in data[tweets]:
                data[tweets]['human'] = {}
            data[tweets]['human'][userId] = guess

finalData = {'gold':[], 'tweets':[], 'human':[]}
for sentId in data:
    finalData['gold'].append(data[sentId]['gold'])
    finalData['tweets'].append(data[sentId]['text'])
    judgements = data[sentId]['human']
    finalData['human'].append(data[sentId]['human'])

print(len(finalData['gold']), ' items')
path = sys.argv[1][:sys.argv[1].rfind('/') + 1] + 'all.json'
print('writing to ', path)
json.dump(finalData, open(path, 'w'))

