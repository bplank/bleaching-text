import os

for lang in ['EN', 'ES', 'FR', 'NL', 'PT']:
    langPath = 'data/' + lang + '-data-200tweets.json.balanced'
    allFeats = []
    for feat in ['punctCons', 'punctAgr', 'vowels', 'length', 'frequency', 'shape']:
        allFeats.append(langPath + '.' + feat)
        cmd = 'python3 scripts/0.genFeatures.py ' + langPath + ' ' + feat
        print(cmd)

    cmd = 'python3 scripts/0.combineJson.py ' + langPath + '.comb ' + ' ' + ' '.join(allFeats)
    print(cmd)
    
    #cmd = 'python3 scripts/0.combineJson.py ' + langPath + '.combOrig ' + ' '.join([langPath] * len(allFeats))
    #print(cmd)

    #cmd = 'python3 scripts/0.combineJson.py ' + langPath + '.combPlusLex ' + langPath + ' ' + ' '.join(allFeats) + ' '
    #print(cmd)


