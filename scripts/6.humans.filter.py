import json
import sys

if len(sys.argv) < 4:
    print('please give human file, train file and outPath for new train')
    exit(1)

human = json.load(open(sys.argv[1]))
train = json.load(open(sys.argv[2]))

idxs = []
for humanIdx in range(len(human['tweets'])):
    splittedTweets = human['tweets'][humanIdx].split('NEWLINE')
    comp1 = splittedTweets[0]
    comp2 = splittedTweets[1]
    for trainIdx in range(len(train['tweets'])):
        if train['tweets'][trainIdx].find(comp1) >= 0 and train['tweets'][trainIdx].find(comp2) >= 0:
            idxs.append(trainIdx)

print(len(idxs), len(human['tweets']))
newTrain = {'tweets':[], 'gender':[]}
newTest = {'tweets':[], 'gender':[]}
for i in range(len(train['tweets'])):
    if i in idxs: #RM NOT TO GET TEST.200
        newTest['tweets'].append(train['tweets'][i])
        newTest['gender'].append(train['gender'][i])
    else:
        newTrain['tweets'].append(train['tweets'][i])
        newTrain['gender'].append(train['gender'][i])
        
print(len(newTrain['tweets']))
print(len(newTest['tweets']))
json.dump(newTrain, open(sys.argv[3] + '.train', 'w'))
json.dump(newTrain, open(sys.argv[3] + '.test', 'w'))

