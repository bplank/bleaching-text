import os

for langPath in ['NL.filtered.train', 'NL.filtered.test', 'NL.filtered.train.20', 'NL.filtered.test.20', 'data/FR-data-20tweets.json.balanced']:
    if langPath[0] != 'd':
        langPath = 'data_humans/' + langPath
    allFeats = []
    for feat in ['punctCons', 'punctAgr', 'vowels', 'length', 'frequency', 'shape']:
        allFeats.append(langPath + '.' + feat)
        cmd = 'python3 scripts/0.genFeatures.py ' + langPath + ' ' + feat
        print(cmd)

    cmd = 'python3 scripts/0.combineJson.py ' + langPath + '.comb ' + ' ' + ' '.join(allFeats)
    print(cmd)
    
    cmd = 'python3 scripts/0.combineJson.py ' + langPath + '.combOrig ' + ' '.join([langPath] * len(allFeats))
    print(cmd)

    #cmd = 'python3 scripts/0.combineJson.py ' + langPath + '.combPlusLex ' + langPath + ' ' + ' '.join(allFeats) + ' '
    #print(cmd)


