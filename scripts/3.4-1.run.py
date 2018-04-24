import os
import sys

outDir = 'runs/3.4-1/'
os.system('mkdir -p ' + outDir)

for tgtLang in ['EN', 'NL', 'PT', 'FR', 'ES']:
    for feat in [('.comb', '5', '0'), ('', '1-2', '3-6')]:    
        outFile = outDir + '/' + tgtLang + feat[0] + '.out'
        trainFile = 'data_4-1/4lang-data-200tweets.json.balanced.' + tgtLang + feat[0]
        testFile = 'data/' + tgtLang + '-data-200tweets.json.balanced' + feat[0]
        cmd = 'python3 src/classifier.py ' + trainFile + ' --n-gram ' + feat[1] + ' --c-n-gram ' + feat[2] + ' --test ' + testFile + ' > ' + outFile + ' 2> ' + outFile + '.err'
        print(cmd)

