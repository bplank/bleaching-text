import os
import sys

outDir = 'runs/2.lexVScomb/'
os.system('mkdir -p ' + outDir)

for srcLang in ['EN', 'NL', 'PT', 'FR', 'ES']:
    for tgtLang in ['EN', 'NL', 'PT', 'FR', 'ES' ]:
        for feat in [('.comb', '5', '0'), ('', '1-2', '3-6')]:
            if srcLang == tgtLang:
                test = ' '
            else:
                test = ' --test data/' + tgtLang + '-data-200tweets.json.balanced' + feat[0] + ' '
            outFile = outDir + '/' + srcLang + '.' + tgtLang + '.'.join(feat) + '.out'
            trainFile = 'data/' + srcLang + '-data-200tweets.json.balanced' + feat[0] 
            cmd = 'python3 src/classifier.py ' + trainFile + ' --n-gram ' + feat[1] + ' --c-n-gram ' + feat[2] + ' ' +  test + ' > ' + outFile + ' 2> ' + outFile + '.err'
            print(cmd)


